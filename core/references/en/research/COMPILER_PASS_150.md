# Verification 1.5.0: new build and exact boundaries

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi


21 November 2026. The book covers the Delphi language. Its 74 chapters and 89 detailed cards are retained; Russian and English are maintained in pairs. This is a completed reference edition with explicit unknowns, not a formal specification of every release and platform. New edits received paired author self-review; the independent 1.4 review belongs to the previous translation and is not presented as a new independent review.

## New measurements

Using supported IDE Build/MCP2Delphi in IDE `37.0.60952.8797`, 26 comparisons were completed: 13 Win32 and 13 Win64. All matched the earlier actual results: 18 successful builds followed by execution with exit=0 and eight expected rejections. Every executable case also matched its previous stdout. This compares observations; it does not erase original mismatches against documentation/expectations. Input source and supporting files were hash-checked; fresh directories contained no old EXEs. The IDE subsequently rewrote two CP1251 source files: the input bytes and post-IDE bytes are retained separately. An IDE stall while opening one project was recovered by restarting the IDE and was not counted as a language error.

- `FINITEFLOAT`: the selected ON/OFF and FP-mask pairs repeated the previous results; the complete directive effect remains unknown.
- `CODEPAGE`: ambiguous bytes `C6 88` produced one UTF-16 code unit `392`; the BOM control produced `1046` and `8364`. This observes the IDE route, not an independent permitted CLI.
- `WARNINGS`: inner OFF/ERROR before the deprecated call changes the result; whole-procedure granularity cannot be promised universally.
- `PUSHOPT`/`POPOPT`: the nested include restored R/Q by layer, confirming removal of one top snapshot.
- `NameOf`: the closed generic nested type produced `TInner`, the formal parameter produced `Value`; the selected scoped-enum expression was rejected with `E2372`.
- Namespace: full qualification produced `33`, partial qualification produced `E2003`/`E2014`, and importing a scope alone produced `F2613`.

## Editorial corrections

Four semantic points were clarified: the release boundary for long-name IFOPT and PUSHOPT/POPOPT is 13.0; documented WARNINGS granularity is separated from counterexamples; the top option snapshot is distinguished from the entire stack; and the documented Athens 12 FP default is separated from a universal result guarantee. Only verbatim duplicated scope paragraphs were removed. Original fences, diagnostic strings, and statuses were not changed. The imprecise comment in the old PUSHOPT example is retained byte-for-byte and explained next to the example.

## Environment boundary

The installation now contains Linux compiler/lib files, but before compiler invocation the IDE opened Create a Connection Profile. No profile/PAServer was configured; the wizard was cancelled and no ELF was produced. This is `ENVIRONMENT_BLOCKED`, not rejection of a language construct. `wsl --list --quiet` showed no distribution registered for the current user. No older compiler was found in the installed Studio 23 folder or the full available GetIt catalog; access to separate previous-version installers depends on the license. This account entitlement was not established. No license restriction was bypassed.

---

*(Full research pass report is included in the full edition.)*
