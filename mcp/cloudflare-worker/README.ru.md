# Облачный MCP-сервер на Cloudflare Workers (Code Mode + Skills over MCP)

Готовый удалённый **Streamable HTTP MCP-сервер** на **Cloudflare Workers**, который раздаёт весь корпус **Delphi Behavior Contracts** всем ИИ-клиентам по одному адресу (`/mcp`).

## Архитектура

- **Cloudflare Code Mode (`delphi_execute`):** выполняет присланный агентом JavaScript внутри одноразового изолированного **Dynamic Worker** (`worker_loaders` / `env.LOADER.load()`) с **`globalOutbound: null`** (полный запрет исходящей сети) и read-only RPC-биндингом `WorkerEntrypoint` (`DelphiCorpusRpc`).
- **Корпус в Workers Static Assets (`ASSETS`, `run_worker_first: true`):** все 74×2 глав, 89×2 карточек, 5 скиллов, `source_issues.json` и квитанции компилятора доступны только самому Worker (прямые запросы `GET /corpus/*` снаружи возвращают `404`).
- **Skills over MCP (SEP-2640):** поддерживает `skills/list`, `skills/get`, ресурсы `skill://...` и `delphi://...`, а также 5 MCP-промптов.
- **Гибкая защита лицензионным ключом (`ACCESS_MODE` + секрет `MCP_ACCESS_KEY`):**
  - Без `MCP_ACCESS_KEY` (или `ACCESS_MODE="open"`): открытый режим для тестов.
  - `ACCESS_MODE="freemium"` + `MCP_ACCESS_KEY`: без ключа доступны оглавление, `VERIFICATION` и поиск по заголовкам; с заголовком `Authorization: Bearer <key>` открывается весь корпус, квитанции, все 5 скиллов и Code Mode `delphi_execute`.
  - `ACCESS_MODE="strict"` + `MCP_ACCESS_KEY`: строгий `401` без ключа.

## Локальный запуск и деплой

```bash
npm install
npm run build:corpus   # собирает корпус из ../../core в public/corpus/
npm run typecheck      # проверка TypeScript
npm run dev            # локально на http://127.0.0.1:8787/mcp

# Выкладка на Cloudflare Workers:
npx wrangler secret put MCP_ACCESS_KEY
npm run deploy
```
