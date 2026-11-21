# Delphi Behavior Contracts

**Delphi, by actual behavior — compiler-measured language reference (74 EN/RU chapters, 89 directive cards, 879+ Delphi 13 observations), native plugins, pure AI skills, and a local/self-hosted Code Mode MCP server.**

[Русский](README.ru.md) · [Website (EN)](https://silentfish.dev/delphi) · [Сайт (RU)](https://silentfish.dev/ru/delphi) · [Download Free Demo](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest) · [AI Evaluator Guide](EVALUATE_FOR_USER.md) · [Discussions](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)

[![Release: v1.0.0-demo](https://img.shields.io/badge/release-v1.0.0--demo-blue)](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)
[![Delphi 13 CE Verified](https://img.shields.io/badge/Delphi%2013%20CE-879%2B%20observations-C81E3A)](core/references/en/VERIFICATION.md)
[![Chapters](https://img.shields.io/badge/chapters-74%20EN%20%26%20RU-2ea44f)](core/references/en/INDEX.md)
[![Directives](https://img.shields.io/badge/directives-89%20cards-2ea44f)](core/references/en/directives/INDEX.md)
[![MCP Code Mode](https://img.shields.io/badge/MCP-Code%20Mode%20%2B%20SEP--2640-7c3aed)](mcp/local-mcp/README.md)

> **This public repository hosts the FREE Evaluation DEMO (`v1.0.0-demo`, `< 1 MB`).**
> It preserves the **complete original Table of Contents** of all 74 chapters & 89 directive cards, the full verification record, **6 curated multi-difficulty excerpts** (Basic → Hardcore Compiler ABI), **4 complete directive cards**, **8 authentic compiler receipts**, **6 runnable `.dpr` probes**, and **100% working plugins, pure skills, and MCP server** — so you and your AI coding agent can test the real workflow before getting the full commercial edition at **[silentfish.dev/delphi](https://silentfish.dev/delphi)**.

---

## Let Your AI Evaluate This Demo in 60 Seconds

Download **[`delphi-behavior-contracts-demo-1.0.0.zip`](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)** (or clone this repo), point your AI assistant to **[`EVALUATE_FOR_USER.md`](EVALUATE_FOR_USER.md)** (Russian: **[`EVALUATE_FOR_USER.ru.md`](EVALUATE_FOR_USER.ru.md)**), and ask:

> *"Inspect this Delphi Behavior Contracts DEMO (index, 4 difficulty tiers, compiler receipts, local MCP / skills) and tell me honestly: is the full edition what we need for our project, or not?"*

## What Is Inside (Identical 4-Layer Architecture to the Full Edition)

| Layer | Path | What You Get |
| --- | --- | --- |
| **1. Canonical Core** | [`core/`](core/references/en/INDEX.md) | Complete original TOC (**74 EN/RU chapters**, **89 directive cards**), full [`VERIFICATION.md`](core/references/en/VERIFICATION.md), **6 multi-difficulty excerpts**, **4 complete directive cards**, **8 authentic compiler receipts** (`demo-sample-receipts.json`), **6 `.dpr` probes**, compact EN/RU demo mini-books, and ranked search [`lookup.py`](core/scripts/lookup.py). |
| **2. Native Plugins (8)** | `plugins/` | Native manifests & bundles for **Claude Code**, **Claude Marketplace**, **OpenAI Codex**, **Codex Marketplace**, **Google Antigravity**, **Google Gemini CLI**, **Cursor**, and **GitHub Copilot / VS Code**. |
| **3. Pure Skills & Rules (15)** | `skills/` | Strictly separated from plugins (0 plugin manifests inside `skills/`): `single-skill/` (AAIF / `skills.sh` / Claude App), `5-specialist-skills/`, and **13 platform layouts** (`by-platform/`: Claude, Codex, Antigravity, Gemini CLI, Cursor, Copilot, Windsurf, Cline/Roo/Kilo, OpenCode/Amp/Droid, JetBrains/Junie, Kiro/Amazon Q, Aider/Continue/Goose, Web Chats). |
| **4. Universal MCP Server** | [`mcp/`](mcp/local-mcp/README.md) | Zero-dependency Python 3.8+ local offline MCP server (`stdio` + Streamable HTTP, **Code Mode `delphi_execute`**, **SEP-2640 Skills over MCP**, 1-click `start-http.bat`/`.sh`, `Dockerfile`), self-hostable [`cloudflare-worker/`](mcp/cloudflare-worker/README.md) (Dynamic Worker Loader Code Mode), and **14 client configs**. |

## Sample Difficulty Tiers Included in This Demo

1. **Level 1 — Basic / Everyday Trap:** [`10-arrays.md`](core/references/en/chapters/10-arrays.md) — dynamic array buffer aliasing (`Alias[0] := 10`) vs detachment on `SetLength`/`Insert`/`Delete`.
2. **Level 2 — Intermediate:** [`13-managed-records.md`](core/references/en/chapters/13-managed-records.md) + full [`warn.md`](core/references/en/directives/warn.md) — `Initialize`/`Finalize`/`Assign` rules and `HIDDEN_VIRTUAL` (`W1010`/`E1010`) vs `HIDING_MEMBER`.
3. **Level 3 — Advanced:** [`31-generics.md`](core/references/en/chapters/31-generics.md) + [`41-directives.md`](core/references/en/chapters/41-directives.md) — `HasWeakRef(T)` (`E2571`), `[unsafe]`, `E2533` on virtual generic methods, and 76 verified `$WARN` identifiers.
4. **Level 4 — Hardcore Compiler ABI & Evolution:** [`70-floating-profiles.md`](core/references/en/chapters/70-floating-profiles.md) + [`73-evolution-old-to-new.md`](core/references/en/chapters/73-evolution-old-to-new.md) + full [`extendedcompatibility.md`](core/references/en/directives/extendedcompatibility.md) — Win32 80-bit vs Win64 53-bit `Extended` asymmetry and 6 historical Delphi strata.
5. **Also included in full:** [`inline.md`](core/references/en/directives/inline.md) and [`pushopt-popopt.md`](core/references/en/directives/pushopt-popopt.md).

## Demo vs Full Commercial Edition

| Metric | Free DEMO (this repo & release) | Full Commercial Edition ([silentfish.dev/delphi](https://silentfish.dev/delphi)) |
| --- | --- | --- |
| Table of Contents & Scope Map | All 74 chapters + 89 directives | All 74 chapters + 89 directives |
| Full Chapter Prose (EN & RU) | 6 multi-difficulty excerpts + 68 section outlines | **All 74 complete chapters** (`163,257` EN / `142,697` RU words) |
| Compiler Directive Cards | 4 complete cards + 85 syntax stubs | **All 89 complete directive cards** |
| Compiler Evidence Receipts | 8 authentic receipts + 6 `.dpr` probes | **879+ live Delphi 13 CE observations, 650 runs, 1,250+ sources** |
| Source Discrepancies Register | 30-entry summary index | **Full 30 technical dossiers (`source_issues.json`)** |
| Plugins, Pure Skills, Local & Workers MCP | **100% identical working code** | **100% identical working code** |

## Quick Start (Zero Symlinks — Safe on Windows / macOS / Linux)

```bash
# List all 8 native plugins and 15 pure skill layouts
python install.py --list

# Test local ranked search on the DEMO corpus
python core/scripts/lookup.py "dynamic array"
python core/scripts/lookup.py --lang ru "динамический массив"

# Install a NATIVE PLUGIN (add --standalone to copy core/ directly into target)
python install.py --plugin antigravity
python install.py --plugin codex
python install.py --plugin claude
python install.py --plugin gemini

# Install PURE SKILLS (strictly without plugin manifests)
python install.py --skill single
python install.py --skill all --scope project --project-dir /path/to/delphi-repo

# Export self-contained standalone .zip packages for direct UI upload
python install.py --export-plugin claude ./delphi-claude-demo.zip
python install.py --export-skill single ./delphi-single-skill-demo.zip

# Start the local zero-dependency Streamable HTTP MCP server in 1 click
mcp/local-mcp/start-http.bat      # Windows
./mcp/local-mcp/start-http.sh     # macOS / Linux
```

## Links & Community

- **Official Product Page (EN):** [https://silentfish.dev/delphi](https://silentfish.dev/delphi)
- **Официальная страница продукта (RU):** [https://silentfish.dev/ru/delphi](https://silentfish.dev/ru/delphi)
- **Latest Demo Release (`SHA-256` verified):** [https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)
- **Questions, Feedback & AI Evaluation Results:** [GitHub Discussions](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)
- **License:** [Evaluation License (`LICENSE.md`)](LICENSE.md)
