import os
import uuid
import docx
import re
from typing import List, Dict, Any
from ..models.document_ast import CanonicalAST, ASTBlock
from ..models.semantic_block import SemanticType

def parse_docx_file(docx_path: str) -> CanonicalAST:
    ast = CanonicalAST(metadata={"filename": os.path.basename(docx_path), "format": "docx"})
    if not os.path.exists(docx_path):
        return ast

    doc = docx.Document(docx_path)
    raw_lines = []
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    for item in doc.element.body:
        tag = item.tag.split('}')[-1]

        if tag == 'p':
            p = docx.text.paragraph.Paragraph(item, doc)
            text = p.text.strip()
            raw_lines.append(p.text)

            style_name = p.style.name if p.style else "Normal"
            style_name_lower = style_name.lower()

            # Check OpenXML <w:numPr> tag for Word Bullet/Numbered lists
            pPr = p._p.get_or_add_pPr()
            numPr = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr')
            pbPr = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pageBreakBefore')

            detection_method = "explicit_style"
            confidence = 0.99
            sem_type = SemanticType.PARAGRAPH.value
            level = None
            extra = {}

            if pbPr is not None:
                extra["page_break_before"] = True

            if numPr is not None:
                sem_type = SemanticType.BULLET_LIST.value
                detection_method = "docx_numpr"
                confidence = 0.99
            elif 'title' in style_name_lower:
                sem_type = SemanticType.TITLE.value
            elif 'subtitle' in style_name_lower:
                sem_type = SemanticType.SUBTITLE.value
            elif 'heading 1' in style_name_lower:
                sem_type = SemanticType.HEADING_1.value
                level = 1
            elif 'heading 2' in style_name_lower:
                sem_type = SemanticType.HEADING_2.value
                level = 2
            elif 'heading 3' in style_name_lower:
                sem_type = SemanticType.HEADING_3.value
                level = 3
            elif 'list' in style_name_lower or 'bullet' in style_name_lower:
                sem_type = SemanticType.BULLET_LIST.value
            else:
                detection_method = "unclassified"
                confidence = 0.50

            # Inspect run formatting
            font_size = None
            is_bold = False
            for r in p.runs:
                if r.font and r.font.size:
                    font_size = r.font.size.pt
                if r.bold:
                    is_bold = True

            block = ASTBlock(
                id=f"block_{uuid.uuid4().hex[:8]}",
                type=sem_type,
                text=text,
                level=level,
                confidence=confidence,
                detection_method=detection_method,
                source={
                    "format": "docx",
                    "style": style_name,
                    "font_size": font_size,
                    "bold": is_bold
                },
                extra=extra
            )
            ast.blocks.append(block)

        elif tag == 'tbl':
            tbl = docx.table.Table(item, doc)
            table_headers = []
            table_rows = []

            for r_idx, row in enumerate(tbl.rows):
                row_vals = [cell.text.strip() for cell in row.cells]
                raw_lines.append(" | ".join(row_vals))

                if r_idx == 0:
                    table_headers = row_vals
                else:
                    table_rows.append(row_vals)

            block = ASTBlock(
                id=f"block_{uuid.uuid4().hex[:8]}",
                type=SemanticType.TABLE.value,
                text=f"Table: {len(table_rows)} rows x {len(table_headers)} columns",
                confidence=1.0,
                detection_method="explicit_table",
                source={"format": "docx", "style": "Table"},
                extra={"headers": table_headers, "rows": table_rows}
            )
            ast.blocks.append(block)

    ast.metadata["raw_lines"] = raw_lines
    ast.metadata["total_raw_lines"] = len(raw_lines)
    return ast
