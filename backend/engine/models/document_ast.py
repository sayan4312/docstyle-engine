import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from .semantic_block import SemanticType

@dataclass
class ASTSource:
    format: str = "docx"
    style: Optional[str] = None
    page: int = 1
    line_number: Optional[int] = None

@dataclass
class ASTBlock:
    id: str
    type: str  # SemanticType string value
    text: str
    level: Optional[int] = None
    confidence: float = 1.0
    detection_method: str = "explicit_style"
    source: Dict[str, Any] = field(default_factory=lambda: {"format": "docx", "style": "Normal"})
    extra: Dict[str, Any] = field(default_factory=dict)
    style_override: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "text": self.text,
            "level": self.level,
            "confidence": round(self.confidence, 2),
            "detection_method": self.detection_method,
            "source": self.source,
            "extra": self.extra,
            "style_override": self.style_override
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ASTBlock':
        return cls(
            id=data.get("id", f"block_{uuid.uuid4().hex[:8]}"),
            type=data.get("type", SemanticType.PARAGRAPH.value),
            text=data.get("text", ""),
            level=data.get("level"),
            confidence=data.get("confidence", 1.0),
            detection_method=data.get("detection_method", "rule_based"),
            source=data.get("source", {"format": "docx"}),
            extra=data.get("extra", {}),
            style_override=data.get("style_override")
        )

@dataclass
class CanonicalAST:
    metadata: Dict[str, Any] = field(default_factory=dict)
    blocks: List[ASTBlock] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document": {
                "metadata": self.metadata,
                "blocks": [b.to_dict() for b in self.blocks]
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CanonicalAST':
        doc_data = data.get("document", data)
        metadata = doc_data.get("metadata", {})
        raw_blocks = doc_data.get("blocks", [])
        blocks = [ASTBlock.from_dict(b) for b in raw_blocks]
        return cls(metadata=metadata, blocks=blocks)
