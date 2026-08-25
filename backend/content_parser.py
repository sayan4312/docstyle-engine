"""
Content Parser Module
Parses any Content Document (Word .docx, Markdown, or Text) into a structured 
sequence of semantic content blocks while preserving 100% verbatim text AND intentional blank spaces.
Automatically cleans trailing/redundant blank lines before page breaks to eliminate blank pages.
"""
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ContentBlock:
    block_type: str  # 'title', 'subtitle', 'heading', 'subheading', 'body', 'bullet', 'numbered', 'alpha', 'outcome', 'table', 'empty_space', 'page_break'
    text: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ParsedDocument:
    blocks: List[ContentBlock] = field(default_factory=list)
    raw_lines: List[str] = field(default_factory=list)


def extract_elements_in_order(element, ns):
    """Recursively yields (tag, element) for 'p' and 'tbl' in exact document flow order."""
    for child in element:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'p':
            yield ('p', child)
        elif tag == 'tbl':
            yield ('tbl', child)
        elif tag == 'sdt':
            sdt_content = child.find('w:sdtContent', ns)
            if sdt_content is not None:
                yield from extract_elements_in_order(sdt_content, ns)
            else:
                yield from extract_elements_in_order(child, ns)


def int_to_alpha(n: int, upper: bool = False) -> str:
    """Converts 1 -> 'a', 2 -> 'b', etc."""
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder if upper else 97 + remainder) + result
    return result


def int_to_roman(n: int, upper: bool = False) -> str:
    """Converts 1 -> 'i', 2 -> 'ii', 4 -> 'iv', etc."""
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num if upper else roman_num.lower()


def load_numbering_definitions(docx_zip, ns) -> Dict[str, Dict[str, Any]]:
    """Loads numId -> {format: 'decimal'|'lowerLetter'|'bullet', pattern: '%1.'} mapping."""
    num_map = {}
    if 'word/numbering.xml' not in docx_zip.namelist():
        return num_map
        
    try:
        nroot = ET.parse(docx_zip.open('word/numbering.xml')).getroot()
        abstract_map = {}
        for ab in nroot.findall('w:abstractNum', ns):
            ab_id = ab.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}abstractNumId')
            lvl = ab.find('w:lvl', ns)
            if lvl is not None:
                numFmt = lvl.find('w:numFmt', ns)
                fmt_val = numFmt.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if numFmt is not None else 'bullet'
                lvlText = lvl.find('w:lvlText', ns)
                txt_val = lvlText.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if lvlText is not None else '%1.'
                start_elem = lvl.find('w:start', ns)
                start_val = int(start_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '1')) if start_elem is not None else 1
                abstract_map[ab_id] = {'format': fmt_val, 'pattern': txt_val, 'start': start_val}

        for num in nroot.findall('w:num', ns):
            nid = num.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numId')
            ab_ref = num.find('w:abstractNumId', ns)
            if ab_ref is not None:
                ab_id = ab_ref.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                if ab_id in abstract_map:
                    num_map[nid] = dict(abstract_map[ab_id])
    except Exception as e:
        print(f"Notice during numbering extraction: {e}")
    return num_map


def sanitize_blocks(blocks: List[ContentBlock]) -> List[ContentBlock]:
    """Removes redundant empty spaces before page breaks and collapses multiple blank lines."""
    clean_blocks = []
    
    for i, b in enumerate(blocks):
        # 1. Collapse multiple consecutive empty spaces into max 1
        if b.block_type == 'empty_space':
            if len(clean_blocks) > 0 and clean_blocks[-1].block_type in ('empty_space', 'page_break'):
                continue
            
            # 2. Look ahead: if followed by a page_break or title, strip this empty space
            next_meaningful = None
            for j in range(i + 1, min(i + 5, len(blocks))):
                if blocks[j].block_type != 'empty_space':
                    next_meaningful = blocks[j].block_type
                    break
            if next_meaningful in ('page_break', 'title'):
                continue

        clean_blocks.append(b)

    # Remove any trailing empty space at very end of document
    while clean_blocks and clean_blocks[-1].block_type == 'empty_space':
        clean_blocks.pop()

    return clean_blocks


def parse_docx_content(docx_path: str) -> ParsedDocument:
    """Extracts semantic blocks, exact numbering, blank spaces, and tables from Word .docx file."""
    parsed = ParsedDocument()
    if not os.path.exists(docx_path):
        return parsed

    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            num_defs = load_numbering_definitions(z, ns)
            list_counters = {} # numId -> current_count

            doc_xml = z.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            body = root.find('w:body', ns)
            if body is None:
                return parsed

            raw_elements = list(extract_elements_in_order(body, ns))
            raw_blocks = []
            
            for idx, (tag, elem) in enumerate(raw_elements):
                if tag == 'p':
                    texts = [t.text for t in elem.findall('.//w:t', ns) if t.text]
                    full_text = ''.join(texts).strip()
                    
                    # Capture exact intentional blank line / empty paragraph
                    if not full_text:
                        raw_blocks.append(ContentBlock(block_type='empty_space', text=''))
                        continue
                    
                    parsed.raw_lines.append(full_text)
                    
                    # Lookahead: get next non-empty paragraph text
                    next_text = ""
                    for j in range(idx + 1, min(idx + 5, len(raw_elements))):
                        n_tag, n_elem = raw_elements[j]
                        if n_tag == 'p':
                            n_texts = [t.text for t in n_elem.findall('.//w:t', ns) if t.text]
                            nt = ''.join(n_texts).strip()
                            if nt:
                                next_text = nt
                                break

                    # Inspect OpenXML numPr (Native Word Bullet / Numbering)
                    numPr = elem.find('.//w:numPr', ns)
                    has_numPr = (numPr is not None)
                    numId = None
                    if has_numPr:
                        numId_elem = numPr.find('w:numId', ns)
                        if numId_elem is not None:
                            numId = numId_elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')

                    # 1. Course Outcomes: CO1, CO2, CO3...
                    co_match = re.match(r'^(CO\d+)[\s:]*(.*)', full_text, re.IGNORECASE)
                    if co_match:
                        co_id = co_match.group(1).upper()
                        co_text = co_match.group(2).strip()
                        raw_blocks.append(ContentBlock(
                            block_type='outcome',
                            text=co_text,
                            extra={'co_id': co_id}
                        ))
                        continue

                    # 2. Check if paragraph has native Word numbering (decimal, letter, roman, or bullet)
                    if has_numPr and numId and numId in num_defs:
                        defn = num_defs[numId]
                        fmt = defn.get('format', 'bullet')
                        pattern = defn.get('pattern', '%1.')
                        
                        if numId not in list_counters:
                            list_counters[numId] = defn.get('start', 1)
                        else:
                            list_counters[numId] += 1
                        
                        current_idx = list_counters[numId]

                        if fmt == 'decimal':
                            label = pattern.replace('%1', str(current_idx))
                            if not label.endswith(('.', ')', ':')):
                                label = f"{label}."
                            raw_blocks.append(ContentBlock(
                                block_type='numbered',
                                text=full_text,
                                extra={'num': label}
                            ))
                            continue
                        elif fmt == 'lowerLetter':
                            label = pattern.replace('%1', int_to_alpha(current_idx, upper=False))
                            if not label.endswith(('.', ')', ':')):
                                label = f"{label}."
                            raw_blocks.append(ContentBlock(
                                block_type='alpha',
                                text=full_text,
                                extra={'alpha': label}
                            ))
                            continue
                        elif fmt == 'upperLetter':
                            label = pattern.replace('%1', int_to_alpha(current_idx, upper=True))
                            if not label.endswith(('.', ')', ':')):
                                label = f"{label}."
                            raw_blocks.append(ContentBlock(
                                block_type='alpha',
                                text=full_text,
                                extra={'alpha': label}
                            ))
                            continue
                        elif fmt in ('lowerRoman', 'upperRoman'):
                            label = pattern.replace('%1', int_to_roman(current_idx, upper=(fmt=='upperRoman')))
                            if not label.endswith(('.', ')', ':')):
                                label = f"{label}."
                            raw_blocks.append(ContentBlock(
                                block_type='alpha',
                                text=full_text,
                                extra={'alpha': label}
                            ))
                            continue
                        elif fmt == 'bullet':
                            raw_blocks.append(ContentBlock(
                                block_type='bullet',
                                text=full_text
                            ))
                            continue

                    # 3. Explicit typed numbers in text e.g. "1. www.esl-lab.com"
                    num_match = re.match(r'^(\(?\d+[\.\)\s]+)\s*(.*)', full_text)
                    if num_match and (len(full_text.split()) < 15 or 'www.' in full_text or 'http' in full_text):
                        num_prefix = num_match.group(1).strip()
                        item_text = num_match.group(2).strip()
                        raw_blocks.append(ContentBlock(
                            block_type='numbered',
                            text=item_text,
                            extra={'num': num_prefix}
                        ))
                        continue

                    # 4. Explicit typed alphabets e.g. "a.", "a)", "(a)"
                    alpha_match = re.match(r'^(\(?[a-zA-Z][\.\)]\s+)(.*)', full_text)
                    if alpha_match and len(full_text.split()) < 15:
                        alpha_prefix = alpha_match.group(1).strip()
                        item_text = alpha_match.group(2).strip()
                        raw_blocks.append(ContentBlock(
                            block_type='alpha',
                            text=item_text,
                            extra={'alpha': alpha_prefix}
                        ))
                        continue

                    # 5. Explicit bullet symbols (•, -, *)
                    if full_text.startswith(('•', '-', '*')):
                        cleaned = re.sub(r'^[•\-\*]\s*', '', full_text)
                        raw_blocks.append(ContentBlock(
                            block_type='bullet',
                            text=cleaned
                        ))
                        continue

                    # 6. Dynamic Main Course Title:
                    is_first_block = (len([b for b in raw_blocks if b.block_type != 'empty_space']) == 0)
                    is_followed_by_subtitle = (next_text.startswith('(') and next_text.endswith(')'))
                    is_course_header = (len(full_text.split()) <= 10 and not full_text.endswith(('.', ':', ';', ',')) and not has_numPr)

                    if (is_first_block and not full_text.startswith('(')) or (is_course_header and is_followed_by_subtitle) or ('- lab' in full_text.lower() and len(full_text.split()) <= 8):
                        if len(raw_blocks) > 0 and not is_first_block:
                            raw_blocks.append(ContentBlock(block_type='page_break'))
                        raw_blocks.append(ContentBlock(block_type='title', text=full_text))
                        continue

                    # 7. Subtitle pattern e.g. "( Theory course for B.Tech I-I)"
                    if full_text.startswith('(') and full_text.endswith(')'):
                        raw_blocks.append(ContentBlock(block_type='subtitle', text=full_text))
                        continue

                    # 8. Section Headings (ending with colon, or specific section keywords)
                    heading_keywords = [
                        'Course outline:', 'Objectives:', 'Course outcomes:', 'Course Outcomes:',
                        'Contents:', 'Topics:', 'Textbooks:', 'Reference Books:', 'Web Resources:',
                        'Assessment Pattern', 'Suggested Software:'
                    ]
                    if any(full_text.lower().startswith(kw.lower()) for kw in heading_keywords) or (len(full_text.split()) <= 4 and full_text.endswith(':')):
                        raw_blocks.append(ContentBlock(block_type='heading', text=full_text))
                        continue

                    # 9. Sub-headings e.g. "Each unit should have:", "Internal: 40%", "External assessment: 60%"
                    if full_text.startswith(('Each unit should have:', 'Internal:', 'Internal Assessment:', 'External assessment:')):
                        raw_blocks.append(ContentBlock(block_type='subheading', text=full_text))
                        continue

                    # 10. Default: Regular Body Paragraph (NO BULLET ADDED)
                    raw_blocks.append(ContentBlock(block_type='body', text=full_text))

                elif tag == 'tbl':
                    # Table element
                    rows_data = []
                    for tr in elem.findall('.//w:tr', ns):
                        row_cells = []
                        for tc in tr.findall('.//w:tc', ns):
                            cell_texts = []
                            for p in tc.findall('.//w:p', ns):
                                p_texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
                                if p_texts:
                                    cell_texts.append(''.join(p_texts).strip())
                            row_cells.append('\n'.join(cell_texts))
                        if any(c.strip() for c in row_cells):
                            rows_data.append(row_cells)

                    if rows_data:
                        headers = rows_data[0]
                        data_rows = rows_data[1:]
                        raw_blocks.append(ContentBlock(
                            block_type='table',
                            text='',
                            extra={'headers': headers, 'rows': data_rows}
                        ))

            # Sanitize blocks to remove redundant spaces before page breaks
            parsed.blocks = sanitize_blocks(raw_blocks)

    except Exception as e:
        print(f"Error parsing docx: {e}")

    return parsed


def parse_content_document(file_path: str) -> ParsedDocument:
    """Universal dispatcher to parse any content document."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        return parse_docx_content(file_path)
    else:
        parsed = ParsedDocument()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [l.strip() for l in f.readlines()]
            parsed.raw_lines = [l for l in lines if l]
            for l in lines:
                if not l:
                    parsed.blocks.append(ContentBlock(block_type='empty_space', text=''))
                elif l.startswith('# '):
                    parsed.blocks.append(ContentBlock(block_type='title', text=l[2:].strip()))
                elif l.startswith('## '):
                    parsed.blocks.append(ContentBlock(block_type='heading', text=l[3:].strip()))
                elif l.startswith(('- ', '* ', '• ')):
                    parsed.blocks.append(ContentBlock(block_type='bullet', text=l[2:].strip()))
                else:
                    parsed.blocks.append(ContentBlock(block_type='body', text=l))
            parsed.blocks = sanitize_blocks(parsed.blocks)
        return parsed
