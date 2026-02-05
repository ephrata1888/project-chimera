# git-mcp (minimal HTTP MCP server)

This is a minimal HTTP MCP-compatible server called `git-mcp` that exposes basic git operations as JSON over HTTP.

Endpoints:
- `GET /` - health
- `GET /status?path=<repo_path>` - runs `git status --porcelain --branch` in the given path (or server cwd)
- `GET /diff?path=<repo_path>&files=file1,file2` - runs `git diff [files]`
- `POST /commit` - JSON body: `{ "path": "<repo_path>", "message": "commit msg", "files": ["f1","f2"] }`.

Run (recommended in a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r tools\git_mcp\requirements.txt
python tools\git_mcp\app.py
```

The server listens on `http://127.0.0.1:8000` by default.

Example requests (PowerShell):

```powershell
# status for repo in current folder
Invoke-WebRequest -Uri 'http://127.0.0.1:8000/status' -UseBasicParsing | Select-Object -Expand Content

# diff for specific files
Invoke-WebRequest -Uri 'http://127.0.0.1:8000/diff?files=README.md,main.py' -UseBasicParsing | Select-Object -Expand Content

# commit
$body = @{ path = '.'; message = 'mcp: quick test'; files = @() } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/commit' -Method POST -Body $body -ContentType 'application/json'
```

MCP entry (add to `.vscode/mcp.json` or your MCP config):

```jsonc
"git-mcp": {
  "url": "http://127.0.0.1:8000",
  "type": "http"
}
```

Notes and security:
- This server executes `git` CLI commands on the host. Do not expose it to untrusted networks.
- It validates that the target path contains a `.git` directory before running commands.