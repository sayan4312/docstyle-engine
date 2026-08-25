from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class ElementStyle:
    font_family: str = "Calibri"
    font_size: float = 11.0
    bold: bool = False
    italic: bool = False
    color_rgb: str = "111111"
    space_before: float = 4.0
    space_after: float = 3.0
    line_spacing: float = 1.15
    alignment: str = "LEFT"

@dataclass
class TemplateModel:
    # Page layout
    margin_top: int = 1080       # dxa
    margin_bottom: int = 720     # dxa
    margin_left: int = 992       # dxa
    margin_right: int = 992      # dxa
    page_width: int = 11920      # dxa
    page_height: int = 16840     # dxa

    # Color Palette
    primary_color: str = "1F3764"
    secondary_color: str = "2E74B5"
    table_header_fill: str = "1F3764"
    table_header_text_color: str = "FFFFFF"
    table_border_color: str = "999999"
    body_text_color: str = "111111"

    # Element Styles Map
    styles: Dict[str, ElementStyle] = field(default_factory=dict)
    raw_metadata: Dict[str, Any] = field(default_factory=dict)

    def get_style_for(self, semantic_type: str) -> ElementStyle:
        st = str(semantic_type).upper()
        if st in self.styles:
            return self.styles[st]
        elif st.startswith("HEADING_"):
            return self.styles.get("HEADING_1", ElementStyle(font_family=self.styles.get("PARAGRAPH", ElementStyle()).font_family, font_size=14.0, bold=True, color_rgb=self.primary_color))
        else:
            return self.styles.get("PARAGRAPH", ElementStyle(font_family="Calibri", font_size=11.0, color_rgb=self.body_text_color))
