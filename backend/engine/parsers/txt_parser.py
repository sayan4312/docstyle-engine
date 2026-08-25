import os
import uuid
try:
    from ..models.document_ast import CanonicalAST, ASTBlock
    from ..models.semantic_block import SemanticType
except (ImportError, ValueError):
    import sys
    from pathlib import Path
    backend_dir = str(Path(__file__).resolve().parent.parent.parent)
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    from engine.models.document_ast import CanonicalAST, ASTBlock
    from engine.models.semantic_block import SemanticType

def parse_txt_file(txt_path: str) -> CanonicalAST:
    ast = CanonicalAST(metadata={"filename": os.path.basename(txt_path), "format": "txt"})
    if not os.path.exists(txt_path):
        return ast

    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    raw_lines = [l.rstrip('\r\n') for l in lines]
    ast.metadata["raw_lines"] = raw_lines
    ast.metadata["total_raw_lines"] = len(raw_lines)

    for line in lines:
        text = line.strip()
        block = ASTBlock(
            id=f"block_{uuid.uuid4().hex[:8]}",
            type=SemanticType.PARAGRAPH.value if text else SemanticType.PAGE_BREAK.value,
            text=text,
            confidence=0.50,
            detection_method="unclassified",
            source={"format": "txt"}
        )
        ast.blocks.append(block)

    return ast
