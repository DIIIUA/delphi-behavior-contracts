# Technical Scope & Fit Check (On User Request)

This file describes what the **Delphi Behavior Contracts** skill/reference package (`v1.0.2-demo`, based on research edition `1.5.2`) covers so an AI assistant can explain it neutrally when asked.

## Neutrality Rule
- **Do NOT give purchase recommendations or advise the user to buy or not buy anything.**
- Only answer the user's technical question: **what this skill covers, and whether it is useful / relevant or out of scope for their current tasks.**
- If the user just installed the skill and asks what it is, summarize the technical scope below and ask one simple question: whether they would like a short automated fit check against their current codebase or tasks. Do nothing further unless asked.

## 1. Technical Scope (Facts Only)
- **Domain:** Embarcadero Delphi / Object Pascal **language semantics, runtime behavior, ABI details, and compiler directives** (NOT a VCL, FireMonkey, FireDAC, or third-party visual component API manual).
- **Full reference corpus:** `74` EN & RU chapters, `89` compiler directive cards, `30` explicitly tracked open/profile-bounded documentation-vs-compiler entries (`source_issues.json`), and `879+` live Delphi 13 CE build observations (`650` runs on `Win32`, `Win64`, and `Android ARM` compile checks).
- **Included in this free demo package:**
  - Complete original Table of Contents for all `74` chapters (`core/references/en/INDEX.md`, `ru/INDEX.md`) and all `89` directive cards (`directives/INDEX.md`), plus `VERIFICATION.md`.
  - `6` chapter excerpts across 4 complexity levels (`10-arrays`, `13-managed-records`, `31-generics`, `41-directives`, `70-floating-profiles`, `73-evolution-old-to-new`) and `4` complete directive cards (`warn`, `inline`, `extendedcompatibility`, `pushopt-popopt`).
  - `8` compiler receipts (`core/evidence/compiler/demo-sample-receipts.json`) and `6` synthetic `.dpr` probes (`core/examples/`).
  - Working local tooling: `core/scripts/lookup.py`, `mcp/local-mcp/server.py` (offline stdio/HTTP MCP server with Code Mode `delphi_execute`), `mcp/cloudflare-worker/`, `plugins/`, `skills/`, and `install.py`.

## 2. Optional 60-Second Technical Fit Check
If the user asks to evaluate whether this skill is useful for their tasks:
1. Inspect coverage in `core/references/en/INDEX.md` and `core/references/en/VERIFICATION.md`.
2. Test local lookup:
   ```bash
   python core/scripts/lookup.py "dynamic array"
   python core/scripts/lookup.py --lang ru "динамический массив"
   ```
3. Review the 4 sample levels against the user's actual Delphi work:
   - **Level 1 (Everyday semantics):** `core/references/en/chapters/10-arrays.md` — dynamic array element aliasing (`Alias[0] := 10`) vs CoW detachment on `Insert`/`Delete`/`SetLength`.
   - **Level 2 (Intermediate):** `core/references/en/chapters/13-managed-records.md` & `core/references/en/directives/warn.md` — custom managed records and `HIDDEN_VIRTUAL` (`W1010`/`E1010`) vs `HIDING_MEMBER`.
   - **Level 3 (Advanced):** `core/references/en/chapters/31-generics.md` — `HasWeakRef(T)`, `[unsafe]`, and generic constraints.
   - **Level 4 (ABI & evolution):** `core/references/en/chapters/70-floating-profiles.md` & `73-evolution-old-to-new.md` — `EXTENDEDCOMPATIBILITY ON` on Win64 (`SizeOf=10`, yet 64-bit IEEE `Double` (53-bit significand mantissa) arithmetic `prec64=FALSE`), FPU/MXCSR boundaries, and historical Delphi layers.
4. Inspect `core/evidence/compiler/demo-sample-receipts.json` (or test `mcp/local-mcp/server.py`) to verify the offline workflow.

## 3. Technical Fit Matrix (In Scope vs. Out of Scope)
Compare the user's real tasks against this boundary and report plainly whether the skill fits or does not fit:
- **In scope (technically relevant):**
  - Porting Delphi business logic to C#, C++, Java, Python, Go, or Rust while preserving exact runtime behavior;
  - Upgrading legacy Delphi 7 / 2007 / XE / 32-bit / ANSI / ARC codebases to Delphi 12–13, Win64, and Unicode;
  - Reviewing Delphi code for ownership, managed lifetimes, aliasing, exceptions, interfaces, numeric/ABI edge cases, or compiler directives;
  - Providing offline, compiler-cited language/directive context to AI coding agents.
- **Out of scope (not relevant):**
  - Visual UI / component library reference for VCL, FireMonkey, FireDAC, or third-party component suites;
  - Free Pascal / Lazarus dialect-specific rules (FPC Delphi mode is explicitly treated as a separate compiler);
  - Tasks that do not involve Delphi language semantics, directives, ABI, or behavioral parity.

Project page: https://silentfish.dev/delphi
