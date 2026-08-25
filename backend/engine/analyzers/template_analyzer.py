import os
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, Any
from ..models.template_model import TemplateModel, ElementStyle

def clean_font_name(font_raw: str) -> str:
    if not font_raw:
        return "Calibri"
    clean = font_raw.replace("-Bold", "").replace("-Italic", "").replace("PSMT", "").replace("MT", "").replace("PS", "")
    font_map = {
        "TimesNewRoman": "Times New Roman", "Arial": "Arial", "Calibri": "Calibri",
        "Georgia": "Georgia", "Helvetica": "Helvetica", "Aptos": "Aptos",
        "SegoeUI": "Segoe UI", "Verdana": "Verdana", "TrebuchetMS": "Trebuchet MS"
    }
    for k, v in font_map.items():
        if k.lower() in clean.lower():
            return v
    return clean.strip() or "Calibri"


def analyze_template_docx(docx_path: str) -> TemplateModel:
    model = TemplateModel()
    if not os.path.exists(docx_path):
        return model

    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            if 'word/document.xml' in z.namelist():
                doc_xml = z.read('word/document.xml')
                root = ET.fromstring(doc_xml)

                colors_found = []
                for color_elem in root.findall('.//w:color', ns):
                    val = color_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                    if val and val not in ('auto', '000000', 'FFFFFF', '1A1A1A'):
                        colors_found.append(val)

                for shd_elem in root.findall('.//w:shd', ns):
                    fill = shd_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill')
                    if fill and fill not in ('auto', 'clear', 'FFFFFF', '000000'):
                        model.table_header_fill = fill
                        model.primary_color = fill
                        break

                if colors_found:
                    model.primary_color = colors_found[0]
                    if len(colors_found) > 1:
                        model.secondary_color = colors_found[1]

                sectPr = root.find('.//w:sectPr', ns)
                if sectPr is not None:
                    pgMar = sectPr.find('w:pgMar', ns)
                    if pgMar is not None:
                        model.margin_top = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}top', model.margin_top))
                        model.margin_bottom = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bottom', model.margin_bottom))
                        model.margin_left = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left', model.margin_left))
                        model.margin_right = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}right', model.margin_right))

            if 'word/fontTable.xml' in z.namelist():
                font_xml = z.read('word/fontTable.xml')
                froot = ET.fromstring(font_xml)
                fonts = [clean_font_name(f.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name')) for f in froot.findall('w:font', ns)]
                if fonts:
                    primary_font = fonts[0]
                else:
                    primary_font = "Calibri"
            else:
                primary_font = "Calibri"

            # Populate Element Styles
            model.styles["TITLE"] = ElementStyle(font_family=primary_font, font_size=20.0, bold=True, color_rgb=model.primary_color, space_before=16.0, space_after=6.0, alignment="CENTER")
            model.styles["SUBTITLE"] = ElementStyle(font_family=primary_font, font_size=12.0, italic=True, color_rgb=model.secondary_color, space_before=4.0, space_after=12.0, alignment="CENTER")
            model.styles["HEADING_1"] = ElementStyle(font_family=primary_font, font_size=15.0, bold=True, color_rgb=model.primary_color, space_before=14.0, space_after=4.0, alignment="LEFT")
            model.styles["HEADING_2"] = ElementStyle(font_family=primary_font, font_size=13.0, bold=True, color_rgb=model.secondary_color, space_before=10.0, space_after=3.0, alignment="LEFT")
            model.styles["HEADING_3"] = ElementStyle(font_family=primary_font, font_size=11.5, bold=True, color_rgb="333333", space_before=8.0, space_after=2.0, alignment="LEFT")
            model.styles["PARAGRAPH"] = ElementStyle(font_family=primary_font, font_size=10.5, bold=False, color_rgb=model.body_text_color, space_before=4.0, space_after=3.0, line_spacing=1.15, alignment="LEFT")
            model.styles["BULLET_LIST"] = ElementStyle(font_family=primary_font, font_size=10.5, color_rgb=model.body_text_color, space_before=3.0, space_after=2.0, line_spacing=1.15, alignment="LEFT")
            model.styles["NUMBERED_LIST"] = ElementStyle(font_family=primary_font, font_size=10.5, color_rgb=model.body_text_color, space_before=3.0, space_after=2.0, line_spacing=1.15, alignment="LEFT")

    except Exception as e:
        print(f"Warning analyzing DOCX template: {e}")

    return model


def analyze_template_pdf(pdf_path: str) -> TemplateModel:
    model = TemplateModel()
    if not os.path.exists(pdf_path):
        return model

    try:
        import fitz
        doc = fitz.open(pdf_path)
        if not doc or len(doc) == 0:
            return model

        page = doc[0]
        model.page_width = int(page.rect.width * 20)
        model.page_height = int(page.rect.height * 20)

        # Drawings for table fill / shape color
        drawings = page.get_drawings()
        shape_colors = []
        for d in drawings:
            fill = d.get("fill")
            if fill and isinstance(fill, (list, tuple)) and len(fill) == 3:
                r, g, b = [int(c * 255) if isinstance(c, float) and c <= 1.0 else int(c) for c in fill]
                hex_c = f"{r:02X}{g:02X}{b:02X}"
                if hex_c not in ("FFFFFF", "000000", "F4EFEA"):
                    shape_colors.append(hex_c)

        if shape_colors:
            model.primary_color = shape_colors[0]
            model.table_header_fill = shape_colors[0]
            if len(shape_colors) > 1:
                model.secondary_color = shape_colors[1]

        text_dict = page.get_text("dict")
        fonts_found = []
        colors_found = []
        min_x, min_y = page.rect.width, page.rect.height

        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span.get("text", "").strip()
                        if text:
                            bbox = span.get("bbox", (0, 0, 0, 0))
                            min_x = min(min_x, bbox[0])
                            min_y = min(min_y, bbox[1])

                            fn = clean_font_name(span.get("font", ""))
                            if fn:
                                fonts_found.append(fn)

                            c = span.get("color", 0)
                            r = (c >> 16) & 255
                            g = (c >> 8) & 255
                            b = c & 255
                            hex_c = f"{r:02X}{g:02X}{b:02X}"
                            if hex_c not in ("000000", "FFFFFF", "1A1A1A"):
                                colors_found.append(hex_c)

        primary_font = max(set(fonts_found), key=fonts_found.count) if fonts_found else "Calibri"

        if min_y < page.rect.height:
            model.margin_top = max(360, int(min_y * 20))
        if min_x < page.rect.width:
            model.margin_left = max(360, int(min_x * 20))
            model.margin_right = max(360, int(min_x * 20))

        model.styles["TITLE"] = ElementStyle(font_family=primary_font, font_size=20.0, bold=True, color_rgb=model.primary_color, alignment="CENTER")
        model.styles["HEADING_1"] = ElementStyle(font_family=primary_font, font_size=15.0, bold=True, color_rgb=model.primary_color, alignment="LEFT")
        model.styles["PARAGRAPH"] = ElementStyle(font_family=primary_font, font_size=10.5, color_rgb=model.body_text_color, alignment="LEFT")

    except Exception as e:
        print(f"Warning analyzing PDF template: {e}")

    return model


def analyze_template(file_path: str) -> TemplateModel:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return analyze_template_docx(file_path)
    elif ext == '.pdf':
        return analyze_template_pdf(file_path)
    else:
        return TemplateModel()
