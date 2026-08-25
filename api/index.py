import sys
import os

# Add parent and backend directories to python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

try:
    from backend.server import app
except ImportError as orig_err:
    try:
        from server import app  # type: ignore # pyright: ignore[reportMissingImports]
    except ImportError:
        raise orig_err

# Export WSGI application for Vercel Serverless
app = app
