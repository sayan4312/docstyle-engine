"""
Convenience CLI runner when executing from inside docstyle_engine directory.
"""
import os
import sys

# Add parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from main import run_pipeline

if __name__ == "__main__":
    t_path = os.path.join(parent_dir, "Document A.docx")
    c_path = os.path.join(parent_dir, "Document B.docx")
    o_path = os.path.join(parent_dir, "Output Document.docx")
    run_pipeline(t_path, c_path, o_path)
