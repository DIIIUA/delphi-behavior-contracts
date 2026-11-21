# Локальный офлайн MCP-сервер (`delphi-behavior-contracts-mcp`)

Автономный MCP-сервер на чистом Python 3.8+ (без сторонних зависимостей), который подключает весь корпус **Delphi Behavior Contracts** (74 главы EN/RU, 89 карточек директив, 30 спорных вопросов, 879+ квитанций компилятора, 5 профильных скиллов) к **любому MCP-клиенту** полностью офлайн.

## Возможности

- **Два транспорта:** `stdio` (по умолчанию, для Claude Code/Desktop, Codex, Antigravity, Gemini CLI, Cursor, Windsurf, VS Code Copilot, Cline, Roo, Zed, OpenCode) и Streamable HTTP (`--http --port 8788`).
- **4 компактных инструмента (< 1 400 токенов):**
  - `delphi_search` — ранжированный поиск (EN/RU) с нормализацией дефисов, алиасами и русским стеммингом.
  - `delphi_read` — чтение любой главы, карточки директивы, `VERIFICATION.md`, `SOURCE_ISSUES.md` или разбора проходов по пути или короткому имени (`"31"`, `"warn"`, `"10-arrays.md"`).
  - `delphi_skill` — загрузка любого из 5 скиллов по имени.
  - `delphi_execute` — **локальный Code Mode**: read-only песочница Python с жёсткой проверкой AST поверх SDK `delphi.*` (без импортов, сети и файловой системы), позволяющая за один вызов проанализировать главы, директивы и квитанции и вернуть компактный итог.
- **Skills over MCP (SEP-2640):** нативные `skills/list`, `skills/get`, ресурсы `skill://...` и `delphi://...`, а также 5 MCP-промптов.

## Запуск

```bash
# stdio (для CLI и IDE)
python server.py

# Локальный Streamable HTTP
python server.py --http --host 127.0.0.1 --port 8788
```

Готовые конфиги подключения для 14 клиентов лежат в `../client-configs/`.
