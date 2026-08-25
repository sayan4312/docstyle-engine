import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from pdf_exporter import export_to_pdf

def render_docx_to_pdf(docx_path: str, pdf_path: str) -> bool:
    """Converts a rendered Word .docx file into a high-resolution vector PDF."""
    return export_to_pdf(docx_path, pdf_path)
