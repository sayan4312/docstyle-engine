from typing import Dict, Any
from ..models.document_ast import CanonicalAST, ASTBlock
from ..models.template_model import TemplateModel, ElementStyle

def map_ast_to_template_styles(ast: CanonicalAST, template: TemplateModel) -> CanonicalAST:
    """Decoupled Style Mapper: Applies TemplateModel design tokens onto CanonicalAST blocks."""
    for block in ast.blocks:
        elem_style = template.get_style_for(block.type)
        
        # Build style override dictionary
        block.style_override = {
            "font_family": elem_style.font_family,
            "font_size": elem_style.font_size,
            "bold": elem_style.bold,
            "italic": elem_style.italic,
            "color_rgb": elem_style.color_rgb,
            "space_before": elem_style.space_before,
            "space_after": elem_style.space_after,
            "line_spacing": elem_style.line_spacing,
            "alignment": elem_style.alignment,
            "table_header_fill": template.table_header_fill,
            "table_border_color": template.table_border_color,
            "margin_top": template.margin_top,
            "margin_bottom": template.margin_bottom,
            "margin_left": template.margin_left,
            "margin_right": template.margin_right
        }

    return ast
