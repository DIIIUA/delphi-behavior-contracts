# Delphi Behavior Contracts

**Turn any AI coding agent into a principal Delphi engineer in 60 seconds.**
Compiler-verified Delphi / Object Pascal engineering suite: **74 EN & RU chapters**, **89 compiler directive cards**, **879+ live Delphi 13 proofs**, **8 native plugins**, **15 pure AI skill layouts**, and a zero-dependency **Local & Cloudflare Workers Code Mode MCP server**.

[Русский](README.ru.md) · [Official Website (EN)](https://silentfish.dev/delphi) · [Сайт (RU)](https://silentfish.dev/ru/delphi) · [Pricing (from $99)](https://silentfish.dev/delphi/buy) · [Download Free Demo](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest) · [Discussions](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)

[![Release: v1.0.1-demo](https://img.shields.io/badge/Free%20Demo-v1.0.1--demo-blue)](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)
[![Delphi 13 Verified](https://img.shields.io/badge/Delphi%2013-879%2B%20Compiler%20Proofs-C81E3A)](core/references/en/VERIFICATION.md)
[![Chapters](https://img.shields.io/badge/Chapters-74%20EN%20%26%20RU-2ea44f)](core/references/en/INDEX.md)
[![Plugins & Skills](https://img.shields.io/badge/Platforms-8%20Plugins%20%2B%2015%20Skill%20Layouts-7c3aed)](START_HERE.md)

[![Delphi Behavior Contracts (DEMO) MCP server](https://mcprush.com/badge/delphi-behavior-contracts-demo-mcp/card.svg)](https://mcprush.com/to/delphi-behavior-contracts-demo-mcp?ref=badge)

---

## Why Ordinary AI Models Silently Break Delphi Code

Most LLMs guess Delphi from C# syntax and 20-year-old forum posts. Your ported code compiles cleanly and passes happy-path tests — then financial totals drift months later because `System.Round` uses banker's rounding, `shr` is always logical, `Extended` drops from 80-bit x87 to 64-bit IEEE `Double` (53-bit significand mantissa) on Win64, and assigning a dynamic array shares the buffer **without** copy-on-write.

**Delphi Behavior Contracts eliminates the guesswork.** One prevented production bug pays for the entire suite ten times over.

- **Zero-drift migrations to C#, C++, Java, Go, Python & Rust:** maps every operation across 9 behavior dimensions (aliasing, ownership, rounding, evaluation order, unwind cleanup).
- **Painless legacy upgrades to Delphi 12–13, Win64 & Unicode:** catches every silent trap from Delphi 7 / 2007 / XE before it hits production.
- **Complete compiler directive mastery:** 89 deep cards separating parser syntax from actual target codegen across Win32, Win64 & Android ARM.
- **100% offline & enterprise-safe:** your proprietary Delphi code never leaves your machine or private network.

---

## Let Your Own AI Test-Drive the Free Demo in 60 Seconds

This public repository hosts the **FREE Evaluation DEMO (`< 1 MB`)** — with the **exact same 4-layer architecture** and working plugins/skills/MCP as the full commercial edition.

1. Download **[`delphi-behavior-contracts-demo-1.0.1.zip`](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)** (or clone this repo).
2. Point Claude Code, Codex, Antigravity, Gemini CLI, Cursor, Copilot, or Windsurf to **[`EVALUATE_FOR_USER.md`](EVALUATE_FOR_USER.md)** (Russian: **[`EVALUATE_FOR_USER.ru.md`](EVALUATE_FOR_USER.ru.md)**).
3. Ask: *"Inspect this Delphi Behavior Contracts DEMO (full 74-chapter index, 4 difficulty tiers, compiler receipts, local MCP) and tell me honestly: is the full edition what we need?"*

## One Canonical Core. Every AI Platform.

| Layer | What You Get |
| --- | --- |
| **Canonical Core (`core/`)** | Complete **74 EN & RU chapters** (`163K+` EN / `142K+` RU words in full edition), **89 directive cards**, full EN & RU single-file books, **879+ live Delphi 13 proofs** with JSON receipts & `.dpr` probes, and offline ranked search `lookup.py`. *(Demo includes full 74-chapter & 89-directive TOC, 6 multi-difficulty excerpts, 4 complete directive cards, 8 real receipts & 6 `.dpr` probes.)* |
| **8 Native Plugins (`plugins/`)** | **Claude Code**, **Claude Marketplace**, **OpenAI Codex**, **Codex Marketplace**, **Google Antigravity**, **Google Gemini CLI**, **Cursor**, **GitHub Copilot / VS Code**. |
| **15 Pure Skill Layouts (`skills/`)** | Strictly separate from plugins: single AAIF `SKILL.md`, 5 specialist skills, plus native layouts for **Windsurf**, **Cline**, **Roo Code**, **Kilo Code**, **OpenCode**, **Amp**, **JetBrains Junie**, **AWS Kiro**, **Amazon Q**, **Aider**, **Continue**, **Goose**, and **Web Chats** (Claude Projects, Custom GPT, Gemini Gems, NotebookLM). |
| **Universal Code Mode MCP (`mcp/`)** | Zero-dependency Python 3.8+ local offline server (`stdio` + Streamable HTTP, **Code Mode `delphi_execute`**, **SEP-2640 Skills over MCP**, 1-click `start-http.bat`/`.sh`, `Dockerfile`), self-hostable **Cloudflare Workers Code Mode**, and **14 client configs**. |

## Quick Start (Zero Symlinks — Windows / macOS / Linux)

```bash
python install.py --list
python core/scripts/lookup.py "dynamic array"

# Install a native plugin (add --standalone for a self-contained copy)
python install.py --plugin claude      # or: codex | antigravity | gemini | cursor | copilot

# Install pure standalone skills (no plugin manifests)
python install.py --skill single
python install.py --skill all --scope project --project-dir /path/to/delphi-repo

# Export self-contained standalone .zip for direct UI upload
python install.py --export-plugin claude ./delphi-claude-demo.zip
python install.py --export-skill single ./delphi-single-skill-demo.zip

# Launch the local offline HTTP MCP server in 1 click
mcp/local-mcp/start-http.bat      # Windows
./mcp/local-mcp/start-http.sh     # macOS / Linux
```

## Get the Full Commercial Suite (One-Time Purchase · Zero Subscriptions)

Every license includes the **exact same complete Universal Suite** (all 74 EN & RU chapters, all 89 directive cards, both books, all 879+ receipts, all plugins, skills & MCP) plus all `1.x` updates:

- **Solo Engineer — ~~$149~~ $99** *(launch price for first 30 licenses)*: 1 developer, all local plugins/skills/MCP & both books.
- **Team Suite — ~~$490~~ $349** *(launch price)*: up to 10 developers, shared internal Docker/Cloudflare MCP server & private company repo.
- **Agency / Integrator — $1,290**: unlimited internal seats + commercial rights across unlimited client migrations and technical audits.

👉 **[Get Full Suite at silentfish.dev/delphi/buy](https://silentfish.dev/delphi/buy)** · **[Download Free Demo](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)** · **[Discussions](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)**
