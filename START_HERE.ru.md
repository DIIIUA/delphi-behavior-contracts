# Delphi Behavior Contracts — Бесплатный DEMO-пакет (v1.0.2-demo)

> **Хотите проверить, что покрывает этот скилл и подходит ли он под ваши задачи?**
> Покажите вашему ИИ файл [EVALUATE_FOR_USER.ru.md](EVALUATE_FOR_USER.ru.md) и спросите:
> *«Что покрывает этот скилл Delphi Behavior Contracts и полезен ли он для наших текущих задач по Delphi?»*

## Точно такая же 4-слойная архитектура, как в полной версии

Внутри DEMO — **та же 4-слойная инфраструктура**, чтобы можно было проверить работу плагинов, чистых скиллов и локального MCP-сервера на практике:

1. **`core/`** — **полное оригинальное оглавление** всех **74 глав** и **89 карточек директив**, полный паспорт `VERIFICATION.md` (879+ наблюдений Delphi 13 CE), **6 разноуровневых фрагментов от базового до хардкора** (`10-arrays`, `13-managed-records`, `31-generics`, `41-directives`, `70-floating-profiles`, `73-evolution-old-to-new`), **4 полные карточки директив** (`warn`, `inline`, `extendedcompatibility`, `pushopt-popopt`), **8 подлинных компиляторных квитанций**, **6 `.dpr`-проб**, компактные демо-книги (`core/book/`) и рабочий `core/scripts/lookup.py`.
2. **`plugins/`** — все **8 нативных плагинов, расширений и маркетплейсов** (Claude Code, Claude Marketplace, Codex, Codex Marketplace, Antigravity, Gemini CLI, Cursor, Copilot/VS Code).
3. **`skills/`** — чистые отдельные скиллы и правила (`single-skill/`, `5-specialist-skills/` и 13 раскладок в `by-platform/`, включая веб-чаты) — строго отдельно от плагинов.
4. **`mcp/`** — на 100% рабочий **локальный офлайн MCP-сервер** (`mcp/local-mcp/server.py`, 0 зависимостей, **Code Mode `delphi_execute`** + **SEP-2640 Skills over MCP**, 1-клик `start-http.bat`/`.sh`, `Dockerfile`), проект для своего `cloudflare-worker/` и **14 клиентских конфигов**.

Полная коммерческая версия (все 74 полные главы EN/RU, все 89 карточек, все 879+ квитанций и 1 250+ исходников): https://silentfish.dev/delphi
