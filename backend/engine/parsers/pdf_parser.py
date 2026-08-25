import os
import uuid
try:
    from ..models.document_ast import CanonicalAST, ASTBlock
    from ..models.semantic_block import SemanticType
except (ImportError, ValueError):
    import sys
    from pathlib import Path
    backend_dir = str(Path(__file__).resolve().parent.parent.parent)
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    from engine.models.document_ast import CanonicalAST, ASTBlock
    from engine.models.semantic_block import SemanticType

def parse_pdf_file(pdf_path: str) -> CanonicalAST:
    ast = CanonicalAST(metadata={"filename": os.path.basename(pdf_path), "format": "pdf"})
    if not os.path.exists(pdf_path):
        return ast

    try:
        import fitz
        doc = fitz.open(pdf_path)
        raw_lines = []

        for p_idx, page in enumerate(doc):
            text_dict = page.get_text("dict")
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    block_text_spans = []
                    for line in block["lines"]:
                        line_str = "".join([span.get("text", "") for span in line.get("spans", [])]).strip()
                        if line_str:
                            raw_lines.append(line_str)
                            block_text_spans.append(line_str)

                    full_text = " ".join(block_text_spans).strip()
                    if full_text:
                        ast_block = ASTBlock(
                            id=f"block_{uuid.uuid4().hex[:8]}",
                            type=SemanticType.PARAGRAPH.value,
                            text=full_text,
                            confidence=0.50,
                            detection_method="unclassified",
                            source={"format": "pdf", "page": p_idx + 1}
                        )
                        ast.blocks.append(ast_block)

        ast.metadata["raw_lines"] = raw_lines
        ast.metadata["total_raw_lines"] = len(raw_lines)
    except Exception as e:
        print(f"Warning parsing PDF: {e}")

    return ast
