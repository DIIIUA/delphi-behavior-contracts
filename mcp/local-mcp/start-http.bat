@echo off
setlocal
set "PORT=%~1"
if "%PORT%"=="" set "PORT=8788"
echo Starting Delphi Behavior Contracts Local MCP Server (Streamable HTTP) on http://127.0.0.1:%PORT%/mcp ...
python "%~dp0server.py" --http --host 127.0.0.1 --port %PORT%
