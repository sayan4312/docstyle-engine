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

    if os.path.exists(abs_pdf):
        return True

    # 3. Guaranteed Pure Python ReportLab Fallback
    try:
        return docx_to_reportlab_pdf(abs_docx, abs_pdf)
    except Exception as e:
        print(f"[-] ReportLab Fallback error: {e}")

    return os.path.exists(abs_pdf)


def docx_to_reportlab_pdf(abs_docx: str, abs_pdf: str) -> bool:
    """Converts DOCX to PDF natively in Python using ReportLab."""
    try:
        import docx
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

        doc = docx.Document(abs_docx)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#1F3764'),
            spaceAfter=12
        )
        h1_style = ParagraphStyle(
            'DocH1',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=17,
            textColor=colors.HexColor('#1F3764'),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'DocBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#222222'),
            spaceAfter=6
        )
        bullet_style = ParagraphStyle(
            'DocBullet',
            parent=body_style,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=4
        )

        story = []
        for p in doc.paragraphs:
            txt = p.text.strip()
            if not txt:
                continue
            p_style = (p.style.name or '').lower()
            if 'title' in p_style or 'heading 1' in p_style:
                story.append(Paragraph(txt, title_style))
            elif 'heading' in p_style:
                story.append(Paragraph(txt, h1_style))
            elif 'bullet' in p_style or 'list' in p_style:
                story.append(Paragraph(f"• {txt}", bullet_style))
            else:
                story.append(Paragraph(txt, body_style))

        if not story:
            story.append(Paragraph("Restyled Document Content", body_style))

        pdf_doc = SimpleDocTemplate(abs_pdf, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
        pdf_doc.build(story)
        return os.path.exists(abs_pdf)
    except Exception as e:
        print(f"[-] ReportLab PDF conversion failed: {e}")
        return False

