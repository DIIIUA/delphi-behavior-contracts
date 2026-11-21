# Delphi Behavior Contracts

**Delphi по реальному поведению компилятора — выверенная база знаний (74 главы RU/EN, 89 карточек директив, 879+ живых наблюдений Delphi 13 CE), 8 нативных плагинов, 15 раскладок чистых скиллов и локальный / self-hosted MCP-сервер с Code Mode.**

[English](README.md) · [Сайт (RU)](https://silentfish.dev/ru/delphi) · [Website (EN)](https://silentfish.dev/delphi) · [Скачать бесплатное DEMO](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest) · [Гайд оценки для ИИ](EVALUATE_FOR_USER.ru.md) · [Обсуждения](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)

> **В этом публичном репозитории размещена бесплатная ознакомительная DEMO-версия (`v1.0.0-demo`, `< 1 МБ`).**
> Сохранено **полное оригинальное оглавление** всех 74 глав и 89 карточек директив, полный паспорт проверки `VERIFICATION.md`, **6 разноуровневых фрагментов** (от базовых ловушек до хардкорного ABI компилятора), **4 полные карточки директив**, **8 подлинных квитанций компилятора**, **6 `.dpr`-проб** и **на 100% рабочие плагины, чистые скиллы и MCP-сервер** — чтобы вы и ваш ИИ-агент могли проверить инструмент на практике до покупки полной версии на **[silentfish.dev/ru/delphi](https://silentfish.dev/ru/delphi)**.

---

## Дайте вашему ИИ оценить это DEMO за 60 секунд

Скачайте **[`delphi-behavior-contracts-demo-1.0.0.zip`](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)** (или клонируйте этот репозиторий), укажите вашему ИИ на файл **[`EVALUATE_FOR_USER.ru.md`](EVALUATE_FOR_USER.ru.md)** и спросите:

> *«Изучи это демо Delphi Behavior Contracts (оглавление, 4 уровня сложности, квитанции компилятора, локальный MCP и скиллы) и честно скажи: это то, что нам нужно для нашей задачи, или нет?»*

## 4 независимых слоя в одном пакете (структура 1-в-1 с полной версией)

1. **`core/`** — полное оригинальное оглавление всех **74 глав** ([RU](core/references/ru/INDEX.md) / [EN](core/references/en/INDEX.md)) и **89 карточек директив** ([указатель](core/references/ru/directives/INDEX.md)), полный паспорт проверки ([`VERIFICATION.md`](core/references/ru/VERIFICATION.md)), **6 примеров по 4 уровням сложности** (`10-arrays`, `13-managed-records`, `31-generics`, `41-directives`, `70-floating-profiles`, `73-evolution-old-to-new`), **4 полные карточки директив** (`warn`, `inline`, `extendedcompatibility`, `pushopt-popopt`), **8 подлинных компиляторных квитанций**, **6 `.dpr`-проб**, компактные демо-тома и живой ранжированный поиск [`lookup.py`](core/scripts/lookup.py).
2. **`plugins/`** — все **8 нативных плагинов, расширений и маркетплейсов**: Claude Code, Claude Marketplace, OpenAI Codex, Codex Marketplace, Google Antigravity, Google Gemini CLI, Cursor, GitHub Copilot / VS Code.
3. **`skills/`** — **чистые отдельные скиллы и правила** (строго отдельно от плагинов, `0` плагин-манифестов): `single-skill/`, `5-specialist-skills/` и **13 платформенных раскладок** в `by-platform/` (Claude, Codex, Antigravity, Gemini CLI, Cursor, Copilot, Windsurf, Cline/Roo/Kilo, OpenCode/Amp/Droid, JetBrains/Junie, Kiro/Amazon Q, Aider/Continue/Goose, веб-чаты).
4. **`mcp/`** — **единый MCP-сервер подо всех клиентов**: локальный офлайн-сервер на чистом Python 3.8+ (`0` зависимостей, `stdio` + Streamable HTTP, **Code Mode `delphi_execute`**, **SEP-2640 Skills over MCP**, 1-клик `start-http.bat`/`.sh`, `Dockerfile`), готовый self-host проект для [`cloudflare-worker/`](mcp/cloudflare-worker/README.ru.md) и **14 клиентских конфигов**.

## Быстрый старт (без симлинков — безопасно на Windows / macOS / Linux)

```bash
python install.py --list
python core/scripts/lookup.py --lang ru "динамический массив"

# Установить нативный плагин (или добавить --standalone для полностью автономной копии)
python install.py --plugin antigravity
python install.py --plugin codex
python install.py --plugin claude
python install.py --plugin gemini

# Установить только чистые скиллы (без плагина)
python install.py --skill single
python install.py --skill all --scope project --project-dir /path/to/delphi-repo

# Выгрузить автономный .zip для загрузки в UI
python install.py --export-plugin claude ./delphi-claude-demo.zip
python install.py --export-skill single ./delphi-single-skill-demo.zip

# Запустить локальный HTTP MCP-сервер в 1 клик
mcp/local-mcp/start-http.bat      # Windows
./mcp/local-mcp/start-http.sh     # macOS / Linux
```

## Ссылки и сообщество

- **Полная коммерческая версия (RU):** [https://silentfish.dev/ru/delphi](https://silentfish.dev/ru/delphi)
- **Full Commercial Edition (EN):** [https://silentfish.dev/delphi](https://silentfish.dev/delphi)
- **Скачать актуальное DEMO (релиз + `SHA-256`):** [https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)
- **Вопросы, отзывы и разборы от ИИ:** [GitHub Discussions](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)
- **Лицензия:** [`LICENSE.md`](LICENSE.md)
