# pyrefly: ignore [missing-import]
from ..models.document_ast import CanonicalAST
# pyrefly: ignore [missing-import]
from ..models.semantic_block import SemanticType

def normalize_heading_hierarchy(ast: CanonicalAST) -> CanonicalAST:
    """Ensures heading levels (HEADING_1, HEADING_2, HEADING_3) maintain clean visual hierarchy."""
    current_level = 1
    for b in ast.blocks:
        if b.type == SemanticType.TITLE.value:
            b.level = None
        elif b.type == SemanticType.HEADING_1.value:
            b.level = 1
            current_level = 1
        elif b.type == SemanticType.HEADING_2.value:
            b.level = 2
            current_level = 2
        elif b.type == SemanticType.HEADING_3.value:
            b.level = 3
            current_level = 3
    return ast
