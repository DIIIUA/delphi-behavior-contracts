# Delphi Behavior Contracts — DEMO MCP server (stdio by default).
# Registry: io.github.DIIIUA/delphi-behavior-contracts
#   docker run -i --rm ghcr.io/diiiua/delphi-behavior-contracts:1.0.0-demo
# HTTP mode: docker run -p 8788:8788 IMAGE python -u /app/server.py --http --host 0.0.0.0 --port 8788
FROM python:3.12-slim
LABEL io.modelcontextprotocol.server.name="io.github.DIIIUA/delphi-behavior-contracts"
LABEL org.opencontainers.image.source="https://github.com/DIIIUA/delphi-behavior-contracts"
LABEL org.opencontainers.image.description="Compiler-checked Delphi / Object Pascal semantics for AI agents (DEMO)"
LABEL org.opencontainers.image.licenses="LicenseRef-DBC-Demo"
WORKDIR /app
COPY core /app/core
COPY mcp/local-mcp/server.py /app/server.py
ENV DELPHI_CONTRACTS_ROOT=/app/core PYTHONUNBUFFERED=1
CMD ["python", "-u", "/app/server.py"]
