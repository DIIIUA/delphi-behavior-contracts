# Local Offline MCP Server (`delphi-behavior-contracts-mcp`)

Zero-dependency Python 3.8+ MCP server that exposes the entire **Delphi Behavior Contracts** corpus (74 EN/RU chapters, 89 directive cards, 30 source issues, 879+ compiler receipts, 5 specialist skills) to **any MCP-compatible AI client** completely offline.

## Features

- **Transports:** `stdio` (default, both newline-delimited and `Content-Length` framing) and Streamable HTTP (`--http --port 8788`).
- **4 Compact Tools (< 1,400 tokens):**
  - `delphi_search` — ranked EN/RU search with hyphen normalization, aliases and Russian stemming.
  - `delphi_read` — read any chapter, directive card, `VERIFICATION.md`, `SOURCE_ISSUES.md`, or research pass by path or shorthand (`"31"`, `"warn"`, `"10-arrays.md"`).
  - `delphi_skill` — load any of the 5 specialist skills on demand.
  - `delphi_execute` — **Local Code Mode**: AST-restricted read-only Python sandbox over the `delphi` SDK to cross-query multiple chapters, directives, issues and compiler receipts in one tool call.
- **Skills over MCP (SEP-2640):** supports `skills/list`, `skills/get`, `skill://<name>/SKILL.md` resources, `delphi://...` resources, and 5 MCP prompts.

## Quick Run

```bash
# stdio (used by Claude Desktop, Claude Code, Codex, Antigravity, Gemini CLI, Cursor, Windsurf, VS Code, Zed)
python server.py

# Streamable HTTP (local)
python server.py --http --host 127.0.0.1 --port 8788
```

Pass `--root /path/to/core` or set `DELPHI_CONTRACTS_ROOT` if you move `server.py` outside the suite folder.
Ready-to-paste client configs are in `../client-configs/`.
