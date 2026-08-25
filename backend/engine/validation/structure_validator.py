from typing import Dict, Any
from ..models.document_ast import CanonicalAST

def validate_ast_structure(ast: CanonicalAST) -> Dict[str, Any]:
    """Validates structural count statistics of the CanonicalAST."""
    counts = {
        "titles": sum(1 for b in ast.blocks if b.type == "TITLE"),
        "subtitles": sum(1 for b in ast.blocks if b.type == "SUBTITLE"),
        "headings": sum(1 for b in ast.blocks if b.type.startswith("HEADING_")),
        "paragraphs": sum(1 for b in ast.blocks if b.type == "PARAGRAPH"),
        "bullet_lists": sum(1 for b in ast.blocks if b.type == "BULLET_LIST"),
        "numbered_lists": sum(1 for b in ast.blocks if b.type == "NUMBERED_LIST"),
        "tables": sum(1 for b in ast.blocks if b.type == "TABLE"),
        "total_blocks": len(ast.blocks)
    }
    return counts
