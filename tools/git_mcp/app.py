from flask import Flask, request, jsonify
import subprocess
import os
from pathlib import Path

app = Flask(__name__)


def run_git(args, repo_path=None):
    repo = Path(repo_path or os.getcwd()).resolve()
    if not (repo / '.git').exists():
        return {
            'ok': False,
            'error': f"Not a git repository: {repo}"
        }
    try:
        res = subprocess.run(['git'] + args, cwd=str(repo), capture_output=True, text=True, check=False)
        return {
            'ok': res.returncode == 0,
            'returncode': res.returncode,
            'stdout': res.stdout,
            'stderr': res.stderr
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@app.route('/')
def index():
    return jsonify({'service': 'git-mcp', 'status': 'ready'})


@app.route('/status', methods=['GET'])
def status():
    repo = request.args.get('path')
    res = run_git(['status', '--porcelain', '--branch'], repo_path=repo)
    return jsonify(res)


@app.route('/diff', methods=['GET'])
def diff():
    repo = request.args.get('path')
    # Optional: accept ?stat=1 to return --stat instead of full diff
    files = request.args.get('files')
    args = ['diff']
    if files:
        # comma-separated list
        args += files.split(',')
    res = run_git(args, repo_path=repo)
    return jsonify(res)


@app.route('/commit', methods=['POST'])
def commit():
    payload = request.get_json() or {}
    repo = payload.get('path')
    message = payload.get('message')
    files = payload.get('files')  # optional list
    if not message:
        return jsonify({'ok': False, 'error': 'commit message required'}), 400

    # git add files or all
    if files and isinstance(files, list) and len(files) > 0:
        add_args = ['add'] + files
    else:
        add_args = ['add', '--all']

    add_res = run_git(add_args, repo_path=repo)
    if not add_res.get('ok'):
        return jsonify({'ok': False, 'phase': 'add', 'result': add_res}), 500

    commit_res = run_git(['commit', '-m', message], repo_path=repo)
    if not commit_res.get('ok'):
        # return commit stderr (e.g., nothing to commit)
        return jsonify({'ok': False, 'phase': 'commit', 'result': commit_res}), 500

    rev = run_git(['rev-parse', 'HEAD'], repo_path=repo)
    return jsonify({'ok': True, 'commit': rev.get('stdout', '').strip(), 'add': add_res, 'commit_out': commit_res})


if __name__ == '__main__':
    # default: serve on localhost:8000
    app.run(host='127.0.0.1', port=8000)
