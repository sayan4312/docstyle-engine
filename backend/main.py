"""
DocStyle Engine - Main CLI Entry Point
Automated document restyling, template merging, inspection, and PDF generation.

Usage:
  # Generate styled output:
  python main.py --template "Document A.docx" --content "Document B.docx" --output "Output Document.docx"

  # Inspect any document's parsed structure & lists:
  python main.py --inspect "Document C.docx"
"""
import os
import sys
import argparse

from style_extractor import extract_style_tokens_from_docx
from content_parser import parse_content_document
from doc_builder import build_styled_document
from pdf_exporter import export_to_pdf
from verifier import verify_content_integrity


def inspect_document(doc_path: str):
    """Cleanly prints the complete parsed structure, blocks, and lists of any document."""
    if not os.path.exists(doc_path):
        print(f"Error: File '{doc_path}' not found.")
        sys.exit(1)

    print("=" * 70)
    print(f"             DOCUMENT INSPECTION: {os.path.basename(doc_path)}")
    print("=" * 70)
    
    parsed = parse_content_document(doc_path)
    print(f"Total Semantic Blocks : {len(parsed.blocks)}")
    print(f"Total Raw Lines       : {len(parsed.raw_lines)}\n")
    print(f"{'#':<4} | {'TYPE':<12} | {'PREFIX':<8} | {'PREVIEW'}")
    print("-" * 70)

    for i, b in enumerate(parsed.blocks):
        if b.block_type == 'table':
            headers = b.extra.get('headers', [])
            rows = b.extra.get('rows', [])
            print(f"{i:<4} | {'TABLE':<12} | {'':<8} | {len(rows)} rows x {len(headers)} columns")
        else:
            prefix = b.extra.get('num', '') or b.extra.get('alpha', '') or b.extra.get('co_id', '') or ''
            preview = b.text.replace('\n', ' ')[:50]
            print(f"{i:<4} | {b.block_type:<12} | {prefix:<8} | {preview}")

    print("=" * 70)


def run_pipeline(template_path: str, content_path: str, output_path: str):
    """Executes the full automated DocStyle pipeline."""
    print("=" * 70)
    print("               DOCSTYLE ENGINE - AUTOMATED PIPELINE")
    print("=" * 70)
    
    # 1. Extract Styles
    print(f"\n[1/4] Extracting design tokens from Template: {os.path.basename(template_path)}...")
    styles = extract_style_tokens_from_docx(template_path)
    print(f"      • Primary Accent Color : {styles.primary_color}")
    print(f"      • Font Family          : {styles.font_family}")
    print(f"      • Table Header Fill    : {styles.table_header_fill}")
    print(f"      • Margins (dxa)        : L:{styles.margin_left}, R:{styles.margin_right}, T:{styles.margin_top}")

    # 2. Parse Content
    print(f"\n[2/4] Parsing verbatim content from: {os.path.basename(content_path)}...")
    parsed = parse_content_document(content_path)
    print(f"      • Extracted Blocks     : {len(parsed.blocks)} semantic elements")
    print(f"      • Raw Text Lines       : {len(parsed.raw_lines)} lines")

    # 3. Build Styled Document
    print(f"\n[3/4] Building styled Word document: {os.path.basename(output_path)}...")
    saved_docx = build_styled_document(template_path, parsed, styles, output_path)
    print(f"      • Saved DOCX to        : {saved_docx}")

    # 4. Verify Integrity
    print(f"\n[+] Running Verbatim Integrity Verification...")
    report = verify_content_integrity(parsed.raw_lines, output_path)
    print(f"      • Integrity Score      : {report.similarity_score * 100:.1f}%")
    print(f"      • Matched Lines        : {report.matched_lines} / {report.total_source_lines}")

    # 5. Export PDF
    pdf_path = os.path.splitext(output_path)[0] + '.pdf'
    print(f"\n[4/4] Exporting to vector PDF: {os.path.basename(pdf_path)}...")
    saved_pdf = export_to_pdf(output_path, pdf_path)
    if saved_pdf:
        print(f"      • Successfully saved PDF to: {saved_pdf}")
    else:
        print(f"      • PDF export skipped or failed.")

    print("\n" + "=" * 70)
    print("                     PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="DocStyle Engine - Document Template Restyler")
    parser.add_argument("--template", "-t", default=os.path.join("samples", "Document A.docx"), help="Path to Template Document A (.docx)")
    parser.add_argument("--content", "-c", default=os.path.join("samples", "Document B.docx"), help="Path to Content Document B/C (.docx)")
    parser.add_argument("--output", "-o", default=os.path.join("outputs", "Output Document.docx"), help="Path for generated output (.docx)")
    parser.add_argument("--inspect", "-i", default=None, help="Inspect any document's structure and lists directly")

    args = parser.parse_args()

    if args.inspect:
        inspect_document(args.inspect)
    else:
        run_pipeline(args.template, args.content, args.output)


if __name__ == "__main__":
    main()
