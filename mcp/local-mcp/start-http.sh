#!/usr/bin/env sh
set -eu
PORT="${1:-8788}"
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
echo "Starting Delphi Behavior Contracts Local MCP Server (Streamable HTTP) on http://127.0.0.1:${PORT}/mcp ..."
exec python3 "${DIR}/server.py" --http --host 127.0.0.1 --port "${PORT}"
