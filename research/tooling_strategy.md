# Tooling & MCP Server Strategy

Source: [.vscode/mcp.json](.vscode/mcp.json)

This document lists the MCP servers configured for this workspace, their types, current reachability, and any authentication requirements. It is intended for submission to reviewers and for onboarding team members.

## git-mcp (local HTTP)

- **Type:** http (local)
- **Endpoint:** http://127.0.0.1:8000
- **Reachability:** Reachable — local check returned a ready status ({"service":"git-mcp","status":"ready"}).
- **Authentication required:** None by default (local loopback). Ensure access control if exposing externally.
- **Notes:** This service wraps local `git` CLI operations (status, diff, commit). Do not expose to untrusted networks.
- **Quick verification:**

  ```powershell
  Invoke-RestMethod -Uri 'http://127.0.0.1:8000/'
  Invoke-RestMethod -Uri 'http://127.0.0.1:8000/status'
  ```

## filesystem-mcp (local HTTP)

- **Type:** http (local)
- **Endpoint:** http://127.0.0.1:9000
- **Reachability:** Reachable — local check returned service info including the project root.
- **Authentication required:** None by default. The service enforces filesystem scoping to the repository root to prevent traversal outside the project.
- **Notes:** Supports `list`, `read`, and `write` operations scoped to the project directory. Do not expose to untrusted networks.
- **Quick verification:**

  ```powershell
  Invoke-RestMethod -Uri 'http://127.0.0.1:9000/'
  Invoke-RestMethod -Uri 'http://127.0.0.1:9000/list'
  Invoke-RestMethod -Uri 'http://127.0.0.1:9000/read?path=README.md'
  ```

## tenxfeedbackanalytics (remote HTTP)

- **Type:** http (remote)
- **Endpoint:** https://mcppulse.10academy.org/proxy
- **Reachability:** Reachable — endpoint responded but returned HTTP 401 with an authentication error when probed.
- **Authentication required:** Yes. The configured `mcp.json` includes custom headers, but the endpoint requires valid authentication (token/OAuth). See the `headers` block in [.vscode/mcp.json](.vscode/mcp.json) for the configured headers (e.g., `X-Device`, `X-Coding-Tool`). A valid access token or credential must be provided to obtain a 2xx response.
- **Notes:** Use the same headers plus any required auth token. Example response from an unauthenticated probe: `{"error":"invalid_token","error_description":"Authentication required"}`.
- **Suggested verification (with token):**

  ```powershell
  $headers = @{ 'X-Device'='windows'; 'X-Coding-Tool'='vscode'; 'Authorization'='Bearer <TOKEN>' }
  Invoke-WebRequest -Uri 'https://mcppulse.10academy.org/proxy' -Headers $headers -UseBasicParsing
  ```

## Summary & Recommendations

- Local test servers (`git-mcp`, `filesystem-mcp`) are reachable on loopback and ready for development use. Keep them bound to `127.0.0.1` unless you implement proper authentication and network controls.
- The remote `tenxfeedbackanalytics` server is reachable but requires authentication. Add the required token or follow the service's OAuth flow to obtain access; incorporate credentials securely (environment variables, secret store) rather than checking them into source control.
- For CI / automation, ensure the MCP client supplies the required headers and credentials when contacting `tenxfeedbackanalytics`.
