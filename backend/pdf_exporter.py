"""
PDF Exporter Module
Converts generated .docx documents into print-ready vector PDF files 
using direct COM Automation with explicit timeout.
"""
import os
import sys
import subprocess

def export_to_pdf(docx_path: str, pdf_path: str) -> bool:
    """Exports a Word .docx document to PDF reliably."""
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    
    if not os.path.exists(abs_docx):
        print(f"[-] Error: {abs_docx} does not exist.")
        return False

    # 1. Try LibreOffice conversion on Linux / Render
    try:
        out_dir = os.path.dirname(abs_pdf)
        res = subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", abs_docx, "--outdir", out_dir],
            capture_output=True,
            text=True,
            timeout=30
        )
        expected_pdf = os.path.join(out_dir, os.path.splitext(os.path.basename(abs_docx))[0] + ".pdf")
        if os.path.exists(expected_pdf):
            if expected_pdf != abs_pdf:
                try:
                    if os.path.exists(abs_pdf):
                        os.remove(abs_pdf)
                    os.replace(expected_pdf, abs_pdf)
                except Exception:
                    pass
            return True
    except Exception as e:
        pass

    # 2. Try Windows MS Word COM Automation
    export_py = f"""
import sys
import os
import win32com.client
import pythoncom

pythoncom.CoInitialize()
try:
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(r"{abs_docx}", False, True)
    doc.SaveAs(r"{abs_pdf}", 17) # wdFormatPDF = 17
    doc.Close(0)
    word.Quit(0)
    print("PDF_OK")
except Exception as e:
    print(f"ERROR: {{e}}")
finally:
    pythoncom.CoUninitialize()
"""
    try:
        res = subprocess.run(
            [sys.executable, "-c", export_py],
            capture_output=True,
            text=True,
            timeout=15
        )
        if "PDF_OK" in res.stdout and os.path.exists(abs_pdf):
            return True
    except Exception as e:
        print(f"Notice: PDF export attempt: {e}")
    return os.path.exists(abs_pdf)

