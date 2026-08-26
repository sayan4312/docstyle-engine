import re
from typing import List
from ..models.document_ast import CanonicalAST, ASTBlock
from ..models.semantic_block import SemanticType

def classify_ast_blocks(ast: CanonicalAST) -> CanonicalAST:
    blocks = ast.blocks
    total = len(blocks)

    # First pass: Identify ONLY genuine Course Subtitles e.g. "( Theory course for B.Tech I-I)", "(B.Tech III year All Branches)"
    for i in range(total):
        text = blocks[i].text.strip()
        if not text:
            continue

        # Strict Subtitle Matching: Must match (B.Tech ...), (M.Tech ...), (Theory course for ...), (Lab course for ...)
        if re.search(r'\(.*(b\.?\s*tech|m\.?\s*tech|theory\s+course|lab\s+course).*\)', text, re.IGNORECASE):
            blocks[i].type = SemanticType.SUBTITLE.value
            blocks[i].confidence = 0.99
            blocks[i].detection_method = "strict_regex_subtitle"

            # Mark preceding non-empty block as TITLE
            for prev_j in range(i - 1, -1, -1):
                prev_text = blocks[prev_j].text.strip()
                if prev_text:
                    blocks[prev_j].type = SemanticType.TITLE.value
                    blocks[prev_j].confidence = 0.99
                    blocks[prev_j].detection_method = "title_before_subtitle"
                    break

    for i, b in enumerate(blocks):
        text = b.text.strip()
        if not text:
            b.type = SemanticType.PARAGRAPH.value
            b.confidence = 0.50
            b.detection_method = "empty_line"
            continue

        # Preserve First Pass Classifications (Subtitle, Title, OpenXML numPr, Tables)
        if b.detection_method in ("strict_regex_subtitle", "title_before_subtitle", "docx_numpr", "explicit_table"):
            continue

        if b.detection_method == "explicit_style" and b.confidence >= 0.95 and b.type != SemanticType.PARAGRAPH.value:
            continue

        # Document Header Title (Fallback for First Short Line)
        if i == 0 and len(text) < 90 and not text.endswith('.'):
            b.type = SemanticType.TITLE.value
            b.confidence = 0.95
            b.detection_method = "header_title"
            continue

        # Major Section Headings ending in colon e.g. "Course outline:", "Objectives:", "Course Outcomes:", "Contents:", "Textbooks:"
        if re.match(r'^(Course\s+outline|Objectives|Course\s+Outcomes|Contents|Textbooks|References|Syllabus|Prerequisites|Evaluation\s+Scheme|Summary|Introduction|Background|Methodology|Results|Conclusion):?$', text, re.IGNORECASE):
            b.type = SemanticType.HEADING_1.value
            b.level = 1
            b.confidence = 0.95
            b.detection_method = "major_section_heading"
            continue

        # Unit / Module Sub-Headings e.g. "Unit-I: Environment", "Unit 1: ...", "Module 2: ..."
        if re.match(r'^(Unit|Module|Chapter|Section)\s*[\-\:\s]*[I|V|X|\d]+', text, re.IGNORECASE):
            b.type = SemanticType.HEADING_2.value
            b.level = 2
            b.confidence = 0.95
            b.detection_method = "unit_module_subheading"
            continue

        # Course Outcome Code Blocks e.g. "CO1 (Understand): ..."
        if re.match(r'^(CO\d+|Course\s+Outcome\s*\d*)', text, re.IGNORECASE) and len(text) < 30:
            b.type = SemanticType.HEADING_3.value
            b.level = 3
            b.confidence = 0.92
            b.detection_method = "course_outcome"
            continue

        # Sub-topic short titles (e.g. "Narrating Events", "Describing Objects", "Data Collection")
        if not text.endswith('.') and len(text) < 55 and not text.startswith('•') and not re.match(r'^\d+', text):
            # Check if line looks like a sub-topic heading
            if re.match(r'^[A-Z][A-Za-z0-9\s\-\,\(\)]+$', text):
                b.type = SemanticType.HEADING_2.value
                b.level = 2
                b.confidence = 0.88
                b.detection_method = "subtopic_heading"
                continue

        # Heading 3 (e.g. 1.1.1 Data Collection)
        if re.match(r'^\d+\.\d+\.\d+\s+', text):
            b.type = SemanticType.HEADING_3.value
            b.level = 3
            b.confidence = 0.95
            b.detection_method = "regex_numbering"
            continue

        # Heading 2 (e.g. 1.1 Background)
        if re.match(r'^\d+\.\d+\s+', text):
            b.type = SemanticType.HEADING_2.value
            b.level = 2
            b.confidence = 0.95
            b.detection_method = "regex_numbering"
            continue

        # Heading 1 (e.g. 1. Introduction or I. Overview)
        if re.match(r'^(\d+|[I|V|X]+)\.\s+[A-Z]', text):
            b.type = SemanticType.HEADING_1.value
            b.level = 1
            b.confidence = 0.92
            b.detection_method = "regex_numbering"
            continue

        # Bullet List Item
        if re.match(r'^[•\-\*]\s+', text) or text.startswith("•"):
            b.type = SemanticType.BULLET_LIST.value
            b.confidence = 0.95
            b.detection_method = "regex_bullet"
            b.text = re.sub(r'^[•\-\*]\s*', '', text)
            continue

        # Flexible Numbered List Item
        m_num = re.match(r'^(\d+)[\.\)]?\s+(.*)', text)
        if m_num:
            num_val = m_num.group(1)
            rest_text = m_num.group(2)
            b.type = SemanticType.NUMBERED_LIST.value
            b.confidence = 0.95
            b.detection_method = "regex_numbered"
            b.extra["num"] = num_val + "."
            b.text = rest_text
            continue

        # Alpha List Item
        m_alpha = re.match(r'^([a-z])[\.\)]\s+(.*)', text, re.IGNORECASE)
        if m_alpha:
            b.type = SemanticType.NUMBERED_LIST.value
            b.confidence = 0.95
            b.detection_method = "regex_alpha"
            b.extra["alpha"] = m_alpha.group(1) + "."
            b.text = m_alpha.group(2)
            continue

        # Layer 4: Typography & Formatting Analysis
        src = b.source or {}
        font_size = src.get("font_size")
        is_bold = src.get("bold", False)

        if font_size:
            if font_size >= 18.0:
                b.type = SemanticType.TITLE.value
                b.confidence = 0.92
                b.detection_method = "typography_size"
                continue
            elif font_size >= 14.0:
                b.type = SemanticType.HEADING_1.value
                b.level = 1
                b.confidence = 0.90
                b.detection_method = "typography_size"
                continue
            elif font_size >= 12.0 and is_bold:
                b.type = SemanticType.HEADING_2.value
                b.level = 2
                b.confidence = 0.88
                b.detection_method = "typography_size"
                continue

        # Short line ending in colon
        if text.endswith(':') and len(text) < 60:
            b.type = SemanticType.HEADING_2.value
            b.level = 2
            b.confidence = 0.85
            b.detection_method = "context_colon"
            continue

        # Default fallback to PARAGRAPH
        b.type = SemanticType.PARAGRAPH.value
        b.confidence = 0.80
        b.detection_method = "default_body"

    return ast
