# filesystem-mcp (minimal HTTP MCP server)

This is a minimal HTTP MCP-compatible server called `filesystem-mcp` that exposes basic filesystem operations scoped to the project directory.

Endpoints:
- `GET /` - health
- `GET /list?subpath=<relative/path>` - list files/directories under `subpath` (relative to project root). If omitted, lists project root.
- `GET /read?path=<relative/path>` - read a file (returns its text content)
- `POST /write` - write a file. JSON body: `{ "path": "relative/path", "content": "...", "mode": "w" }` where `mode` is `w` or `a` (optional, default `w`).

Run (recommended in a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r tools\filesystem_mcp\requirements.txt
python tools\filesystem_mcp\app.py
```

Server listens on `http://127.0.0.1:9000` by default.

Example requests (PowerShell):

```powershell
# list project root
Invoke-RestMethod -Uri 'http://127.0.0.1:9000/list'

# list a subfolder
Invoke-RestMethod -Uri 'http://127.0.0.1:9000/list?subpath=specs'

# read file
Invoke-RestMethod -Uri 'http://127.0.0.1:9000/read?path=README.md'

# write file
$body = @{ path = 'notes/hello.txt'; content = 'hello from mcp'; mode = 'w' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://127.0.0.1:9000/write' -Method POST -Body $body -ContentType 'application/json'
```

Security:
- This server performs filesystem operations under the repository root only. It prevents path traversal outside the project root.
- Do not expose this server to untrusted networks.

MCP entry (add to `.vscode/mcp.json`):

```jsonc
"filesystem-mcp": {
  "url": "http://127.0.0.1:9000",
  "type": "http"
}
```
