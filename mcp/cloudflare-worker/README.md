# Cloudflare Workers Remote MCP Server (Code Mode + Skills over MCP)

Production-ready remote **Streamable HTTP MCP server** on **Cloudflare Workers** powering **Delphi Behavior Contracts** for all MCP clients from one edge endpoint (`/mcp`).

## Architecture

- **Cloudflare Code Mode (`delphi_execute`):** runs agent-authored async JavaScript inside an ephemeral isolated V8 **Dynamic Worker** (`worker_loaders` / `env.LOADER.load()`) with **`globalOutbound: null`** (zero outbound network access) and a read-only `WorkerEntrypoint` loopback RPC binding (`DelphiCorpusRpc`).
- **Static Assets Corpus (`ASSETS`, `run_worker_first: true`):** the packaged EN/RU chapters, 89 directive cards, 5 skills, `source_issues.json` and compiler receipts are served strictly internally to the Worker (`GET /corpus/*` always returns `404` externally).
- **Skills over MCP (SEP-2640):** exposes `skills/list`, `skills/get`, `skill://<name>/SKILL.md` resources, `delphi://...` resources, and 5 MCP prompts.
- **Flexible Access Control (`ACCESS_MODE` + `MCP_ACCESS_KEY`):**
  - No `MCP_ACCESS_KEY` set (or `ACCESS_MODE="open"`): open mode for private/local testing.
  - `ACCESS_MODE="freemium"` + secret `MCP_ACCESS_KEY`: unauthenticated clients see `INDEX`, `VERIFICATION` and title-only search; `Authorization: Bearer <key>` unlocks full text, compiler receipts, specialist skills and Code Mode `delphi_execute`.
  - `ACCESS_MODE="strict"` + secret `MCP_ACCESS_KEY`: returns `401` without a valid key.

## Local Development & Deploy

```bash
npm install
npm run build:corpus   # packs ../../core into public/corpus/
npm run typecheck      # TypeScript check
npm run dev            # local wrangler dev at http://127.0.0.1:8787/mcp

# Production deploy to Cloudflare Workers:
npx wrangler secret put MCP_ACCESS_KEY
npm run deploy
```
