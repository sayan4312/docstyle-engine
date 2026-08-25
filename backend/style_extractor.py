"""
Style Extractor Module
Extracts design tokens, color palette, typography hierarchy, table styling, 
and page geometry dynamically from any Document A (Word .docx or .pdf) using PyMuPDF and OpenXML.
"""
import os
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class StyleTokens:
    # Page layout (in dxa: 1 inch = 1440 dxa, 1 pt = 20 dxa)
    margin_top: int = 1080       # dxa (0.75 in)
    margin_bottom: int = 720     # dxa (0.5 in)
    margin_left: int = 992       # dxa (0.69 in)
    margin_right: int = 992      # dxa (0.69 in)
    page_width: int = 11920      # dxa (A4)
    page_height: int = 16840     # dxa (A4)
    
    # Colors (Hex without #)
    primary_color: str = "1F3764"       # Primary Accent Color
    secondary_color: str = "2E74B5"     # Secondary Color
    table_header_fill: str = "1F3764"   # Table Header Fill
    table_header_text_color: str = "FFFFFF"
    table_border_color: str = "999999"
    body_text_color: str = "111111"
    
    # Typography
    font_family: str = "Calibri"
    title_size: float = 16.0
    subtitle_size: float = 12.0
    heading3_size: float = 11.0
    subheading_size: float = 10.5
    body_size: float = 10.5
    table_text_size: float = 9.0
    table_head_size: float = 9.5
    
    # Spacing tokens (in pt)
    title_space_before: float = 14.0
    title_space_after: float = 4.0
    heading_space_before: float = 11.0
    heading_space_after: float = 4.0
    subheading_space_before: float = 7.0
    subheading_space_after: float = 3.0
    body_space_before: float = 4.0
    body_space_after: float = 3.0
    bullet_space_before: float = 3.0
    bullet_space_after: float = 2.0
    line_spacing: float = 1.15

    raw_metadata: Dict[str, Any] = field(default_factory=dict)


def clean_font_name(font_raw: str) -> str:
    """Cleans internal font names like TimesNewRomanPSMT to readable names like Times New Roman."""
    if not font_raw:
        return "Calibri"
    
    clean = font_raw.replace("-Bold", "").replace("-Italic", "").replace("PSMT", "").replace("MT", "").replace("PS", "")
    
    font_map = {
        "TimesNewRoman": "Times New Roman",
        "Arial": "Arial",
        "Calibri": "Calibri",
        "Georgia": "Georgia",
        "Helvetica": "Helvetica",
        "Aptos": "Aptos",
        "SegoeUI": "Segoe UI",
        "Verdana": "Verdana",
        "TrebuchetMS": "Trebuchet MS",
        "ComicSansMS": "Comic Sans MS",
        "CourierNew": "Courier New",
        "Garamond": "Garamond",
        "Cambria": "Cambria"
    }
    
    for key, val in font_map.items():
        if key.lower() in clean.lower():
            return val
            
    return clean.strip() or "Calibri"


def extract_style_tokens_from_pdf(pdf_path: str) -> StyleTokens:
    """Extracts dynamic design tokens from a PDF document using PyMuPDF (fitz)."""
    tokens = StyleTokens()
    if not os.path.exists(pdf_path):
        return tokens
        
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        if not doc or len(doc) == 0:
            return tokens
            
        page = doc[0]
        tokens.page_width = int(page.rect.width * 20)
        tokens.page_height = int(page.rect.height * 20)
        
        # 1. Inspect drawings/shapes for fill colors
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
            tokens.primary_color = shape_colors[0]
            tokens.table_header_fill = shape_colors[0]
            if len(shape_colors) > 1:
                tokens.secondary_color = shape_colors[1]

        # 2. Inspect text blocks for fonts, colors, and font sizes
        text_dict = page.get_text("dict")
        fonts_found: List[str] = []
        colors_found: List[str] = []
        sizes_found: List[float] = []
        min_x, min_y = page.rect.width, page.rect.height

        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span.get("text", "").strip()
                        if text:
                            # Margins
                            bbox = span.get("bbox", (0, 0, 0, 0))
                            min_x = min(min_x, bbox[0])
                            min_y = min(min_y, bbox[1])
                            
                            # Font
                            font_name = clean_font_name(span.get("font", ""))
                            if font_name:
                                fonts_found.append(font_name)
                                
                            # Size
                            size = round(span.get("size", 10.5), 1)
                            sizes_found.append(size)
                            
                            # Color
                            c = span.get("color", 0)
                            r = (c >> 16) & 255
                            g = (c >> 8) & 255
                            b = c & 255
                            hex_c = f"{r:02X}{g:02X}{b:02X}"
                            if hex_c not in ("000000", "FFFFFF", "1A1A1A"):
                                colors_found.append(hex_c)

        # Set dynamic font family
        if fonts_found:
            tokens.font_family = max(set(fonts_found), key=fonts_found.count)

        # Set dynamic font sizes
        if sizes_found:
            sorted_sizes = sorted(list(set(sizes_found)), reverse=True)
            tokens.title_size = sorted_sizes[0]
            if len(sorted_sizes) > 1:
                tokens.subtitle_size = sorted_sizes[1]
            if len(sorted_sizes) > 2:
                tokens.body_size = sorted_sizes[-1]

        # Set dynamic colors if found in text
        if colors_found:
            if not shape_colors:
                tokens.primary_color = colors_found[0]
                tokens.table_header_fill = colors_found[0]
            if len(colors_found) > 1 and tokens.secondary_color == "2E74B5":
                tokens.secondary_color = colors_found[1]

        # Set dynamic page margins
        if min_y < page.rect.height:
            tokens.margin_top = max(360, int(min_y * 20))
        if min_x < page.rect.width:
            tokens.margin_left = max(360, int(min_x * 20))
            tokens.margin_right = max(360, int(min_x * 20))

    except Exception as e:
        print(f"Warning during PDF style extraction: {e}")

    return tokens


def extract_style_tokens_from_docx(docx_path: str) -> StyleTokens:
    """
    Inspects OpenXML theme1.xml, styles.xml, fontTable.xml, and document.xml
    to extract design tokens, theme colors, typography, and page geometry.
    """
    tokens = StyleTokens()
    if not os.path.exists(docx_path):
        return tokens
        
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            ns_w = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            ns_a = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            
            theme_colors = {}
            
            # 1. Parse Theme XML (word/theme/theme1.xml) for Theme Accent Colors & Fonts
            if 'word/theme/theme1.xml' in z.namelist():
                theme_xml = z.read('word/theme/theme1.xml')
                troot = ET.fromstring(theme_xml)
                
                clr_scheme = troot.find('.//a:clrScheme', ns_a)
                if clr_scheme is not None:
                    for color_tag in ['accent1', 'accent2', 'accent3', 'accent4', 'accent5', 'accent6', 'dk1', 'dk2', 'lt1', 'lt2']:
                        elem = clr_scheme.find(f'a:{color_tag}', ns_a)
                        if elem is not None:
                            srgb = elem.find('a:srgbClr', ns_a)
                            if srgb is not None:
                                val = srgb.get('val')
                                if val:
                                    theme_colors[color_tag] = val
                            else:
                                sys_clr = elem.find('a:sysClr', ns_a)
                                if sys_clr is not None and sys_clr.get('lastClr'):
                                    theme_colors[color_tag] = sys_clr.get('lastClr')

                if 'accent1' in theme_colors:
                    tokens.primary_color = theme_colors['accent1']
                    tokens.table_header_fill = theme_colors['accent1']
                if 'accent2' in theme_colors:
                    tokens.secondary_color = theme_colors['accent2']

                # Extract theme major & minor fonts
                font_scheme = troot.find('.//a:fontScheme', ns_a)
                if font_scheme is not None:
                    major = font_scheme.find('.//a:majorFont/a:latin', ns_a)
                    minor = font_scheme.find('.//a:minorFont/a:latin', ns_a)
                    if minor is not None and minor.get('typeface'):
                        tokens.font_family = clean_font_name(minor.get('typeface'))
                    elif major is not None and major.get('typeface'):
                        tokens.font_family = clean_font_name(major.get('typeface'))

            # 2. Inspect styles.xml for heading fonts, colors, and font sizes
            if 'word/styles.xml' in z.namelist():
                styles_xml = z.read('word/styles.xml')
                sroot = ET.fromstring(styles_xml)
                
                for style_elem in sroot.findall('.//w:style', ns_w):
                    style_id = style_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}styleId', '')
                    rPr = style_elem.find('w:rPr', ns_w)
                    if rPr is not None:
                        # Color
                        color_elem = rPr.find('w:color', ns_w)
                        if color_elem is not None:
                            val = color_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                            theme_clr = color_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}themeColor')
                            if val and val not in ('auto', '000000', 'FFFFFF', '1A1A1A'):
                                tokens.primary_color = val
                                tokens.table_header_fill = val
                            elif theme_clr and theme_clr in theme_colors:
                                tokens.primary_color = theme_colors[theme_clr]
                                tokens.table_header_fill = theme_colors[theme_clr]

                        # Font size (sz is in half-points)
                        sz_elem = rPr.find('w:sz', ns_w)
                        if sz_elem is not None:
                            sz_val = sz_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                            if sz_val and sz_val.isdigit():
                                size_pt = int(sz_val) / 2.0
                                if 'Heading1' in style_id or 'Title' in style_id:
                                    tokens.title_size = size_pt
                                elif 'Heading2' in style_id:
                                    tokens.subtitle_size = size_pt
                                elif 'Normal' in style_id:
                                    tokens.body_size = size_pt

                        # Font family
                        rFonts = rPr.find('w:rFonts', ns_w)
                        if rFonts is not None:
                            ascii_font = rFonts.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii')
                            if ascii_font:
                                tokens.font_family = clean_font_name(ascii_font)

            # 3. Inspect document.xml for explicit colors, table header fills, and page margins
            if 'word/document.xml' in z.namelist():
                doc_xml = z.read('word/document.xml')
                root = ET.fromstring(doc_xml)
                
                colors_found = []
                for color_elem in root.findall('.//w:color', ns_w):
                    val = color_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                    theme_clr = color_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}themeColor')
                    if val and val not in ('auto', '000000', 'FFFFFF', '1A1A1A'):
                        colors_found.append(val)
                    elif theme_clr and theme_clr in theme_colors:
                        colors_found.append(theme_colors[theme_clr])
                
                # Check for table header shading fill
                for shd_elem in root.findall('.//w:shd', ns_w):
                    fill = shd_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill')
                    theme_fill = shd_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}themeFill')
                    if fill and fill not in ('auto', 'clear', 'FFFFFF', '000000'):
                        tokens.table_header_fill = fill
                        tokens.primary_color = fill
                        break
                    elif theme_fill and theme_fill in theme_colors:
                        tokens.table_header_fill = theme_colors[theme_fill]
                        tokens.primary_color = theme_colors[theme_fill]
                        break
                        
                if colors_found:
                    tokens.primary_color = colors_found[0]
                    if len(colors_found) > 1:
                        tokens.secondary_color = colors_found[1]

                # Check page margins in sectPr
                sectPr = root.find('.//w:sectPr', ns_w)
                if sectPr is not None:
                    pgMar = sectPr.find('w:pgMar', ns_w)
                    if pgMar is not None:
                        tokens.margin_top = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}top', tokens.margin_top))
                        tokens.margin_bottom = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bottom', tokens.margin_bottom))
                        tokens.margin_left = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left', tokens.margin_left))
                        tokens.margin_right = int(pgMar.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}right', tokens.margin_right))

            # 4. Fallback font table check if font_family is still default
            if 'word/fontTable.xml' in z.namelist() and tokens.font_family == "Calibri":
                font_xml = z.read('word/fontTable.xml')
                froot = ET.fromstring(font_xml)
                fonts = [clean_font_name(f.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name')) for f in froot.findall('w:font', ns_w)]
                if fonts:
                    tokens.font_family = fonts[0]

    except Exception as e:
        print(f"Warning during DOCX style extraction: {e}")

    return tokens


def extract_style_tokens(file_path: str) -> StyleTokens:
    """Universal dispatcher for style extraction from .docx or .pdf templates."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return extract_style_tokens_from_docx(file_path)
    elif ext == '.pdf':
        return extract_style_tokens_from_pdf(file_path)
    else:
        return StyleTokens()
