"""
DocStyle Engine API Server
Flask REST API server backed by the modular Canonical AST Transformation Pipeline.
"""
import os
import sys
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from engine.analyzers.template_analyzer import analyze_template
from engine.parsers.docx_parser import parse_docx_file
from engine.parsers.pdf_parser import parse_pdf_file
from engine.parsers.txt_parser import parse_txt_file
from engine.classifiers.rule_classifier import classify_ast_blocks
from engine.pipeline.transformation_pipeline import run_docstyle_pipeline
from pdf_exporter import export_to_pdf

import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(BASE_DIR, 'samples')

# Check if running in Vercel Serverless environment or read-only filesystem
is_vercel = os.environ.get('VERCEL') == '1' or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') is not None

if is_vercel or not os.access(BASE_DIR, os.W_OK):
    OUTPUTS_DIR = os.path.join(tempfile.gettempdir(), 'docstyle_outputs')
    TEMP_DIR = os.path.join(tempfile.gettempdir(), 'docstyle_temp')
else:
    OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')
    TEMP_DIR = os.path.join(BASE_DIR, 'temp')

for d in [OUTPUTS_DIR, TEMP_DIR]:
    try:
        os.makedirs(d, exist_ok=True)
    except Exception:
        pass

def clean_all_temp_files():
    """Wipes all temporary processing and preview files."""
    for folder in [OUTPUTS_DIR, TEMP_DIR]:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                except Exception:
                    pass

clean_all_temp_files()

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health():
    samples_count = len(os.listdir(SAMPLES_DIR)) if os.path.exists(SAMPLES_DIR) else 0
    outputs_count = len(os.listdir(OUTPUTS_DIR)) if os.path.exists(OUTPUTS_DIR) else 0
    return jsonify({
        "status": "healthy",
        "engine": "DocStyle AST Engine v2.0",
        "samples_count": samples_count,
        "outputs_count": outputs_count
    })

@app.route('/api/presets', methods=['GET'])
def get_presets():
    presets = []
    if os.path.exists(SAMPLES_DIR):
        for f in os.listdir(SAMPLES_DIR):
            if f.endswith(('.docx', '.pdf', '.txt')):
                presets.append({
                    "name": f,
                    "path": f"/api/preset-file/{f}",
                    "size_kb": round(os.path.getsize(os.path.join(SAMPLES_DIR, f)) / 1024, 1)
                })
    return jsonify({"presets": presets})

@app.route('/api/extract-styles', methods=['POST'])
def extract_styles_endpoint():
    file_path = None
    temp_filename = None
    is_uploaded = False
    req_data = request.get_json(silent=True) or request.form or {}

    if 'file' in request.files and request.files['file'].filename:
        uploaded = request.files['file']
        temp_filename = f"t_{uuid.uuid4().hex[:8]}_{uploaded.filename}"
        file_path = os.path.join(TEMP_DIR, temp_filename)
        uploaded.save(file_path)
        is_uploaded = True
    elif 'preset' in req_data:
        preset_name = req_data['preset']
        file_path = os.path.join(SAMPLES_DIR, preset_name)
        temp_filename = preset_name
    else:
        file_path = os.path.join(SAMPLES_DIR, 'Document A.docx')
        temp_filename = 'Document A.docx'

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": f"File not found: {file_path}"}), 404

    try:
        model = analyze_template(file_path)
        
        # Generate PDF preview if input is docx
        import base64
        preview_filename = None
        preview_data_url = None
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf' and os.path.exists(file_path):
            preview_filename = temp_filename
            try:
                with open(file_path, "rb") as f:
                    preview_data_url = f"data:application/pdf;base64,{base64.b64encode(f.read()).decode('utf-8')}"
            except Exception:
                pass
        elif ext == '.docx':
            preview_name = f"prev_{os.path.splitext(temp_filename)[0]}.pdf"
            preview_path = os.path.join(OUTPUTS_DIR, preview_name)
            if export_to_pdf(file_path, preview_path) and os.path.exists(preview_path):
                preview_filename = preview_name
                try:
                    with open(preview_path, "rb") as f:
                        preview_data_url = f"data:application/pdf;base64,{base64.b64encode(f.read()).decode('utf-8')}"
                except Exception:
                    pass

        primary_font = model.styles.get("PARAGRAPH", {}).font_family if hasattr(model.styles.get("PARAGRAPH"), "font_family") else "Calibri"

        return jsonify({
            "success": True,
            "filename": temp_filename,
            "styles": {
                "primary_color": model.primary_color,
                "secondary_color": model.secondary_color,
                "table_header_fill": model.table_header_fill,
                "table_header_text_color": model.table_header_text_color,
                "table_border_color": model.table_border_color,
                "font_family": primary_font,
                "title_size": model.styles.get("TITLE", {}).font_size if hasattr(model.styles.get("TITLE"), "font_size") else 20.0,
                "subtitle_size": model.styles.get("SUBTITLE", {}).font_size if hasattr(model.styles.get("SUBTITLE"), "font_size") else 12.0,
                "heading3_size": model.styles.get("HEADING_3", {}).font_size if hasattr(model.styles.get("HEADING_3"), "font_size") else 11.5,
                "subheading_size": model.styles.get("HEADING_2", {}).font_size if hasattr(model.styles.get("HEADING_2"), "font_size") else 13.0,
                "body_size": model.styles.get("PARAGRAPH", {}).font_size if hasattr(model.styles.get("PARAGRAPH"), "font_size") else 10.5,
                "table_text_size": 9.0,
                "table_head_size": 9.5,
                "margin_top": model.margin_top,
                "margin_bottom": model.margin_bottom,
                "margin_left": model.margin_left,
                "margin_right": model.margin_right,
                "line_spacing": 1.15
            },
            "preview_pdf_filename": preview_filename,
            "preview_pdf_data_url": preview_data_url
        })
    except Exception as e:
        return jsonify({"error": f"Style extraction failed: {str(e)}"}), 500
    finally:
        if is_uploaded and file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

@app.route('/api/inspect', methods=['POST'])
def inspect_endpoint():
    file_path = None
    temp_filename = None
    is_uploaded = False
    req_data = request.get_json(silent=True) or request.form or {}

    if 'file' in request.files and request.files['file'].filename:
        uploaded = request.files['file']
        temp_filename = f"c_{uuid.uuid4().hex[:8]}_{uploaded.filename}"
        file_path = os.path.join(TEMP_DIR, temp_filename)
        uploaded.save(file_path)
        is_uploaded = True
    elif 'preset' in req_data:
        preset_name = req_data['preset']
        file_path = os.path.join(SAMPLES_DIR, preset_name)
        temp_filename = preset_name
    else:
        file_path = os.path.join(SAMPLES_DIR, 'Document B.docx')
        temp_filename = 'Document B.docx'

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": f"File not found: {file_path}"}), 404

    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.docx':
            ast = parse_docx_file(file_path)
        elif ext == '.pdf':
            ast = parse_pdf_file(file_path)
        else:
            ast = parse_txt_file(file_path)

        ast = classify_ast_blocks(ast)

        # Generate PDF preview for DOCX
        import base64
        preview_filename = None
        preview_data_url = None
        if ext == '.pdf' and os.path.exists(file_path):
            preview_filename = temp_filename
            try:
                with open(file_path, "rb") as f:
                    preview_data_url = f"data:application/pdf;base64,{base64.b64encode(f.read()).decode('utf-8')}"
            except Exception:
                pass
        elif ext == '.docx':
            preview_name = f"prev_{os.path.splitext(temp_filename)[0]}.pdf"
            preview_path = os.path.join(OUTPUTS_DIR, preview_name)
            if export_to_pdf(file_path, preview_path) and os.path.exists(preview_path):
                preview_filename = preview_name
                try:
                    with open(preview_path, "rb") as f:
                        preview_data_url = f"data:application/pdf;base64,{base64.b64encode(f.read()).decode('utf-8')}"
                except Exception:
                    pass

        blocks = [b.to_dict() for b in ast.blocks]

        return jsonify({
            "total_blocks": len(ast.blocks),
            "blocks_count": len(ast.blocks),
            "blocks": blocks,
            "sample_blocks": blocks[:10],
            "temp_filename": temp_filename,
            "preview_pdf_filename": preview_filename,
            "preview_pdf_data_url": preview_data_url
        })
    except Exception as e:
        return jsonify({"error": f"Inspection failed: {str(e)}"}), 500
    finally:
        if is_uploaded and file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

@app.route('/api/process', methods=['POST'])
@app.route('/api/restyle', methods=['POST'])
def process_pipeline():
    template_path = None
    content_path = None
    req_data = request.get_json(silent=True) or request.form or {}

    t_is_uploaded = False
    c_is_uploaded = False

    tf = request.files.get('template') or request.files.get('template_file') or request.files.get('doc_a')
    if tf and tf.filename:
        template_path = os.path.join(TEMP_DIR, f"t_{uuid.uuid4().hex[:8]}_{tf.filename}")
        tf.save(template_path)
        t_is_uploaded = True
    else:
        t_preset = req_data.get('template_preset') or 'Document A.docx'
        template_path = os.path.join(SAMPLES_DIR, t_preset)

    cf = request.files.get('content') or request.files.get('content_file') or request.files.get('doc_b')
    if cf and cf.filename:
        content_path = os.path.join(TEMP_DIR, f"c_{uuid.uuid4().hex[:8]}_{cf.filename}")
        cf.save(content_path)
        c_is_uploaded = True
    else:
        c_preset = req_data.get('content_preset') or 'Document B.docx'
        content_path = os.path.join(SAMPLES_DIR, c_preset)

    if not os.path.exists(template_path):
        return jsonify({"error": f"Template file missing: {template_path}"}), 404
    if not os.path.exists(content_path):
        return jsonify({"error": f"Content file missing: {content_path}"}), 404

    output_name = req_data.get('output_name') or "Output Document.docx"
    if not output_name.endswith('.docx'):
        output_name += '.docx'

    output_docx_path = os.path.join(OUTPUTS_DIR, output_name)

    try:
        res = run_docstyle_pipeline(template_path, content_path, output_docx_path)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": f"Pipeline execution failed: {str(e)}"}), 500
    finally:
        if t_is_uploaded and template_path and os.path.exists(template_path):
            try:
                os.remove(template_path)
            except Exception:
                pass
        if c_is_uploaded and content_path and os.path.exists(content_path):
            try:
                os.remove(content_path)
            except Exception:
                pass

@app.route('/api/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(OUTPUTS_DIR, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": f"File not found: {filename}"}), 404
    return send_file(file_path, as_attachment=True)

@app.route('/api/preview/<path:filename>', methods=['GET'])
def preview_file(filename):
    file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(OUTPUTS_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": f"Preview file not found: {filename}"}), 404
    return send_file(file_path, mimetype='application/pdf')

if __name__ == '__main__':
    print("DocStyle AST Engine Server starting at http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
