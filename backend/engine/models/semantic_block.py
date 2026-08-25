from enum import Enum

class SemanticType(str, Enum):
    TITLE = "TITLE"
    SUBTITLE = "SUBTITLE"
    AUTHOR = "AUTHOR"
    DATE = "DATE"
    
    HEADING_1 = "HEADING_1"
    HEADING_2 = "HEADING_2"
    HEADING_3 = "HEADING_3"
    HEADING_4 = "HEADING_4"
    
    PARAGRAPH = "PARAGRAPH"
    
    BULLET_LIST = "BULLET_LIST"
    NUMBERED_LIST = "NUMBERED_LIST"
    
    TABLE = "TABLE"
    TABLE_HEADER = "TABLE_HEADER"
    TABLE_CELL = "TABLE_CELL"
    
    IMAGE = "IMAGE"
    CAPTION = "CAPTION"
    
    QUOTE = "QUOTE"
    CODE_BLOCK = "CODE_BLOCK"
    
    HEADER = "HEADER"
    FOOTER = "FOOTER"
    FOOTNOTE = "FOOTNOTE"
    ENDNOTE = "ENDNOTE"
    
    PAGE_BREAK = "PAGE_BREAK"
    HORIZONTAL_RULE = "HORIZONTAL_RULE"

    @classmethod
    def from_legacy_type(cls, legacy_type: str, level: int = 1) -> 'SemanticType':
        mapping = {
            'title': cls.TITLE,
            'subtitle': cls.SUBTITLE,
            'heading': cls.HEADING_1 if level == 1 else (cls.HEADING_2 if level == 2 else cls.HEADING_3),
            'subheading': cls.HEADING_2,
            'heading3': cls.HEADING_3,
            'body': cls.PARAGRAPH,
            'paragraph': cls.PARAGRAPH,
            'bullet': cls.BULLET_LIST,
            'numbered': cls.NUMBERED_LIST,
            'alpha': cls.NUMBERED_LIST,
            'outcome': cls.PARAGRAPH,
            'table': cls.TABLE,
            'page_break': cls.PAGE_BREAK,
        }
        return mapping.get(str(legacy_type).lower(), cls.PARAGRAPH)
