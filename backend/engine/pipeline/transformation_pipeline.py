import os
from typing import Dict, Any, Tuple

from ..analyzers.template_analyzer import analyze_template
from ..parsers.docx_parser import parse_docx_file
from ..parsers.pdf_parser import parse_pdf_file
from ..parsers.txt_parser import parse_txt_file
from ..classifiers.rule_classifier import classify_ast_blocks
from ..classifiers.heading_classifier import normalize_heading_hierarchy
from ..classifiers.llm_classifier import fallback_llm_classify
from ..mapping.style_mapper import map_ast_to_template_styles
from ..renderers.docx_renderer import render_ast_to_docx
from ..renderers.pdf_renderer import render_docx_to_pdf
from ..validation.content_validator import validate_verbatim_integrity
from ..validation.structure_validator import validate_ast_structure
from ..models.document_ast import CanonicalAST

def run_docstyle_pipeline(template_path: str, content_path: str, output_docx_path: str) -> Dict[str, Any]:
    """Master Decoupled Pipeline Orchestrator executing the complete DocStyle Engine pipeline."""
    # 1. Analyze Design Template -> TemplateModel
    template_model = analyze_template(template_path)

    # 2. Parse Text Content -> CanonicalAST
    ext = os.path.splitext(content_path)[1].lower()
    if ext == '.docx':
        ast = parse_docx_file(content_path)
    elif ext == '.pdf':
        ast = parse_pdf_file(content_path)
    else:
        ast = parse_txt_file(content_path)

    # 3. Classify Semantic Blocks (Layer 1-5 Waterfall)
    ast = classify_ast_blocks(ast)
    ast = normalize_heading_hierarchy(ast)
    ast = fallback_llm_classify(ast)

    # 4. Map Semantic AST to Template Model Styles
    styled_ast = map_ast_to_template_styles(ast, template_model)

    # 5. Render Output DOCX and PDF
    saved_docx = render_ast_to_docx(styled_ast, template_model, output_docx_path)
    output_pdf_path = os.path.splitext(output_docx_path)[0] + '.pdf'
    pdf_created = render_docx_to_pdf(saved_docx, output_pdf_path)
    pdf_exists = os.path.exists(output_pdf_path)

    # 6. Encode PDF and DOCX to Base64 Data URLs for Serverless Compatibility
    import base64

    pdf_data_url = None
    if pdf_exists and os.path.exists(output_pdf_path):
        try:
            with open(output_pdf_path, "rb") as f:
                pdf_data_url = f"data:application/pdf;base64,{base64.b64encode(f.read()).decode('utf-8')}"
        except Exception:
            pass

    docx_data_url = None
    if os.path.exists(saved_docx):
        try:
            with open(saved_docx, "rb") as f:
                docx_data_url = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64.b64encode(f.read()).decode('utf-8')}"
        except Exception:
            pass

    # 7. Validate Output & Verbatim Text Integrity
    raw_lines = ast.metadata.get("raw_lines", [])
    report = validate_verbatim_integrity(raw_lines, saved_docx)
    struct_summary = validate_ast_structure(styled_ast)

    return {
        "success": True,
        "ast": styled_ast.to_dict(),
        "docx_filename": os.path.basename(saved_docx),
        "pdf_filename": os.path.basename(output_pdf_path) if pdf_exists else None,
        "pdf_data_url": pdf_data_url,
        "docx_data_url": docx_data_url,
        "docx_size_kb": round(os.path.getsize(saved_docx) / 1024, 1),
        "pdf_size_kb": round(os.path.getsize(output_pdf_path) / 1024, 1) if pdf_exists else 0,
        "integrity": {
            "score": round(report.similarity_score * 100, 1),
            "matched_lines": report.matched_lines,
            "total_lines": report.total_source_lines,
            "missing_lines_count": len(report.missing_lines)
        },
        "structure_summary": struct_summary,
        "styles_applied": {
            "primary_color": template_model.primary_color,
            "font_family": template_model.styles.get("PARAGRAPH", {}).font_family if hasattr(template_model.styles.get("PARAGRAPH"), "font_family") else "Calibri",
            "margin_top": template_model.margin_top,
            "table_fill": template_model.table_header_fill
        }
    }
