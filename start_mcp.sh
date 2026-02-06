#!/bin/sh
set -eu

# Start MCP servers if present. Logs are written to /workspace/logs.
mkdir -p /workspace/logs

echo "Starting git-mcp (if present)" >&2
if [ -f /workspace/tools/git_mcp/app.py ]; then
  nohup python3 /workspace/tools/git_mcp/app.py > /workspace/logs/git_mcp.log 2>&1 &
  echo "git-mcp started, logging to /workspace/logs/git_mcp.log" >&2
else
  echo "git-mcp not found, skipping" >&2
fi

echo "Starting filesystem-mcp (if present)" >&2
if [ -f /workspace/tools/filesystem_mcp/app.py ]; then
  nohup python3 /workspace/tools/filesystem_mcp/app.py > /workspace/logs/filesystem_mcp.log 2>&1 &
  echo "filesystem-mcp started, logging to /workspace/logs/filesystem_mcp.log" >&2
else
  echo "filesystem-mcp not found, skipping" >&2
fi

echo "Tailing logs (press Ctrl-C to exit)" >&2
tail -F /workspace/logs/*.log
