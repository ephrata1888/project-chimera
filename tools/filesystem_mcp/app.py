from flask import Flask, request, jsonify
from pathlib import Path
import os
import json

app = Flask(__name__)

# Project root (two levels up from this file: tools/filesystem_mcp -> tools -> project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resolve_safe(rel_path: str) -> Path:
    """Resolve a user-supplied relative path safely within PROJECT_ROOT.

    Raises ValueError if the resolved path is outside the project root.
    """
    if rel_path is None or rel_path == '':
        return PROJECT_ROOT
    # normalize and join
    candidate = (PROJECT_ROOT / rel_path).resolve()
    try:
        candidate.relative_to(PROJECT_ROOT)
    except Exception:
        raise ValueError('path outside project root')
    return candidate


@app.route('/')
def index():
    return jsonify({'service': 'filesystem-mcp', 'project_root': str(PROJECT_ROOT)})


@app.route('/list', methods=['GET'])
def list_files():
    sub = request.args.get('subpath', '')
    try:
        base = resolve_safe(sub)
    except ValueError:
        return jsonify({'ok': False, 'error': 'path outside project root'}), 400

    entries = []
    for p in sorted(base.iterdir()):
        rel = p.relative_to(PROJECT_ROOT).as_posix()
        entries.append({'path': rel, 'is_dir': p.is_dir(), 'size': p.stat().st_size if p.is_file() else None})

    return jsonify({'ok': True, 'base': str(base), 'entries': entries})


@app.route('/read', methods=['GET'])
def read_file():
    rel = request.args.get('path')
    if not rel:
        return jsonify({'ok': False, 'error': 'path parameter required'}), 400
    try:
        target = resolve_safe(rel)
    except ValueError:
        return jsonify({'ok': False, 'error': 'path outside project root'}), 400

    if not target.exists() or not target.is_file():
        return jsonify({'ok': False, 'error': 'file not found'}), 404

    # read as text (utf-8)
    try:
        text = target.read_text(encoding='utf-8')
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

    return jsonify({'ok': True, 'path': str(target.relative_to(PROJECT_ROOT)), 'content': text})


@app.route('/write', methods=['POST'])
def write_file():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({'ok': False, 'error': 'invalid json'}), 400

    rel = payload.get('path')
    content = payload.get('content')
    mode = payload.get('mode', 'w')  # 'w' (overwrite) or 'a' (append)

    if not rel or content is None:
        return jsonify({'ok': False, 'error': 'path and content required'}), 400

    if mode not in ('w', 'a'):
        return jsonify({'ok': False, 'error': 'invalid mode'}), 400

    try:
        target = resolve_safe(rel)
    except ValueError:
        return jsonify({'ok': False, 'error': 'path outside project root'}), 400

    # ensure parent dirs
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        written = 0
        # write
        if mode == 'w':
            target.write_text(content, encoding='utf-8')
            written = len(content)
        else:
            with target.open('a', encoding='utf-8') as fh:
                fh.write(content)
                written = len(content)
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

    return jsonify({'ok': True, 'path': str(target.relative_to(PROJECT_ROOT)), 'written_bytes': written})


if __name__ == '__main__':
    # default listen on 127.0.0.1:9000
    app.run(host='127.0.0.1', port=9000)
