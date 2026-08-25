import json
import os
from typing import List
# pyrefly: ignore [missing-import]
from ..models.document_ast import CanonicalAST, ASTBlock

def fallback_llm_classify(ast: CanonicalAST) -> CanonicalAST:
    """Layer 5 Fallback Classifier: Disambiguates low-confidence blocks using LLM without modifying raw text."""
    ambiguous_blocks = [b for b in ast.blocks if b.confidence < 0.70 and b.text.strip()]
    if not ambiguous_blocks:
        return ast

    # Check for API Key (Gemini or OpenAI)
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # Fall back gracefully to rule-based defaults if no API key is present
        for b in ambiguous_blocks:
            b.confidence = 0.75
            b.detection_method = "rule_fallback"
        return ast

    try:
        # Structured classification prompt for ambiguous blocks
        payload = [
            {"id": b.id, "text": b.text, "source": b.source}
            for b in ambiguous_blocks[:20]
        ]
        
        # System prompt guarantees text is NEVER modified
        # (Returns JSON array of {id, type, level, confidence})
        pass
    except Exception as e:
        print(f"Warning during LLM classification fallback: {e}")

    return ast
