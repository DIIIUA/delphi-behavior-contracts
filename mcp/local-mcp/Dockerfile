# Self-hosted Streamable HTTP MCP Server for your own VPS / Docker server
# Build from the suite root directory:
#   docker build -f mcp/local-mcp/Dockerfile -t delphi-behavior-contracts-mcp .
# Run:
#   docker run -d -p 8788:8788 -e DELPHI_MCP_API_KEY="change-me" delphi-behavior-contracts-mcp
FROM python:3.12-slim

WORKDIR /app
COPY core /app/core
COPY mcp/local-mcp/server.py /app/server.py

ENV DELPHI_CONTRACTS_ROOT=/app/core
EXPOSE 8788

CMD ["python", "-u", "/app/server.py", "--http", "--host", "0.0.0.0", "--port", "8788"]
