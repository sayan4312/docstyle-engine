import sys
import os
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from verifier import verify_content_integrity, VerificationResult

def validate_verbatim_integrity(raw_lines: List[str], generated_docx_path: str) -> VerificationResult:
    """Verifies that 100% of text content is preserved without alteration."""
    return verify_content_integrity(raw_lines, generated_docx_path)
