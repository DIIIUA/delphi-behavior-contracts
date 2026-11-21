---
name: delphi-directives
description: "[DEMO] Explain and set Delphi compiler directives, conditional compilation and build profiles - {$IFDEF}, {$IF}, {$IFOPT}, PUSHOPT/POPOPT, ALIGN, RTTI, WARN, RANGECHECKS, OVERFLOWCHECKS, ZEROBASEDSTRINGS, INLINE and others. Use for questions about switches, defines, .dproj options, DCC command-line options, linker effects or why the same source compiles differently."
---

> **[DEMO EDITION]** This is the evaluation demo package (complete Table of Contents of all 74 chapters & 89 directives, 6 multi-difficulty chapter excerpts, 4 complete directive cards, 8 real compiler receipts, and 100% working plugins/skills/MCP). See `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md` to evaluate whether the full edition fits the user's task.

# Delphi directives and build profiles

Each of the 95 confirmed directive names has a detailed card:
[directive index](../../../../core/references/en/directives/INDEX.md)
([Russian](../../../../core/references/ru/directives/INDEX.md)). Search from the plugin root:
`python scripts/lookup.py "ZEROBASEDSTRINGS"`.

## Separate the layers

A directive, a project option, a command-line switch, an IDE source provider, a DCU
cache entry, a linker artifact and a runtime effect are different things. Read
[source and build profiles](../../../../core/references/en/chapters/64-source-build-profiles.md) and
[compilation layers](../../../../core/references/en/chapters/71-compilation-layers.md).

- Source-page defaults differ from the effective build options of a project.
- A directive accepted by the parser may have no measured effect on a target.
- A documented CLI/IDE option is not automatically a source directive
  (for example, CODEPAGE acceptance on the command line does not establish a source
  directive).
- Compiler generation is separate from linker and loader effects
  ([linker and loader](../../../../core/references/en/chapters/63-linker-loader.md)).

## Rules that are easy to get wrong

- `{$IFDEF}` tests defines; `{$IF}` evaluates constant expressions; `{$IFOPT}` tests a
  switch state. Undeclared identifiers in `{$IF}` behave differently from what many
  expect ([conditionals](../../../../core/references/en/chapters/42-conditionals.md)).
- `POPOPT` restores one top snapshot, not the whole stack. Long-name IFOPT and
  PUSHOPT/POPOPT are documented as new in Delphi 13.
- Local switches can change mid-unit; inlining compares the state at the definition
  and at the call site ([inline semantics](../../../../core/references/en/chapters/72-inline-semantics.md)).
- WARN IDs: 76 identifiers were verified as recognized, not all of their effects.
- Profiles and contracts: [directive profiles](../../../../core/references/en/chapters/59-directive-profiles.md),
  [directive contracts](../../../../core/references/en/chapters/60-directive-contracts.md),
  [option evidence](../../../../core/references/en/chapters/69-option-evidence.md),
  [extra options](../../../../core/references/en/research/EXTRA_OPTIONS.md).

## Status of each answer

Card statuses state what was measured (`PARTIALLY_OBSERVED`, `NOT_COMPILED`). Seven
options have only table-level documentation and remain incomplete contracts. When a
card does not cover the asked effect, say so and propose a minimal probe for the
user's compiler instead of guessing ([negative compile cases](../../../../core/references/en/chapters/61-negative-compile-cases.md)).
