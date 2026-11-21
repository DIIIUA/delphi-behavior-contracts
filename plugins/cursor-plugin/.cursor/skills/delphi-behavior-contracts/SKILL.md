---
name: delphi-behavior-contracts
description: "[DEMO] Core skill for any Delphi / Object Pascal work - explaining, writing or changing Delphi code by its actual, version-specific behavior. Use when Delphi, Object Pascal, .pas/.dpr/.dpk/.dfm files or RAD Studio code appear and no narrower Delphi skill fits. Covers language semantics, versions and compiler-measured evidence on Delphi 13."
---

> **[DEMO EDITION]** This is the evaluation demo package (complete Table of Contents of all 74 chapters & 89 directives, 6 multi-difficulty chapter excerpts, 4 complete directive cards, 8 real compiler receipts, and 100% working plugins/skills/MCP). See `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md` to evaluate whether the full edition fits the user's task.

# Delphi Behavior Contracts

A version-aware Delphi / Object Pascal language reference for agents. Its unit of
translation is the **behavior contract of an operation**, not a similar keyword.
Topic map: [English](../../../../../core/references/en/INDEX.md), [Russian](../../../../../core/references/ru/INDEX.md).

Narrower skills in this plugin: `delphi-migration` (porting to another language),
`delphi-legacy-upgrade` (old Delphi to 12/13, Win64, Unicode), `delphi-directives`
(compiler options and build profiles), `delphi-code-review` (ownership, lifetime,
exceptions, review and debugging). Use them when the task matches.

## How to use the reference

1. Read only what the task needs. Find the topic in the index or search from the
   plugin root: `python scripts/lookup.py "dynamic array"`,
   `python scripts/lookup.py --lang ru "динамический массив"`. The one-file books in
   `book/` are for human reading; do not load them for a small task.
2. Establish the actual target first: compiler release, CPU/OS, configuration, active
   defines, unit search paths, effective directives and the real type or instance
   that owns each operation. An unidentified profile is an unknown, not permission to
   assume the latest Delphi. Free Pascal's Delphi mode is a different compiler.
3. State the status of each claim: documented, observed on a compiler, inferred, or
   unknown. A parsed file, passing linter or matching hash is not a compiled or
   behavioral result.

## Writing and changing Delphi

Inspect declarations, callers and affected consumers. Use syntax supported by the
target version: inline variables (10.3+), managed-record operators (10.4+),
multiline literals, and Delphi 13 conditional expressions, `NameOf` and new generic
constraints each need their own version check
([versions](../../../../../core/references/en/chapters/43-versions.md),
[syntax recipes](../../../../../core/references/en/chapters/54-syntax-recipes.md),
[declaration patterns](../../../../../core/references/en/chapters/56-declaration-patterns.md)).
Make a bounded change and compile/test with the real toolchain when available.

## Behavior that is easy to get wrong

- `B := A` has six physical models: dynamic arrays share a buffer without
  copy-on-write, long strings share with copy-on-write, records copy shallowly,
  class variables copy a pointer ([copy and aliasing](../../../../../core/references/en/chapters/57-copy-and-alias.md)).
- Assigning a method pointer is not invoking it; closures capture the variable cell
  ([callables](../../../../../core/references/en/chapters/22-callables.md), [closures](../../../../../core/references/en/chapters/23-closures.md)).
- `System.Round` rounds half to even; `shr` is always logical; `Extended` differs on
  Win32 and Win64 ([floating profiles](../../../../../core/references/en/chapters/70-floating-profiles.md)).
- Property getters and setters may run code; `with`, overloads, helpers and unit
  shadowing change name resolution ([scope](../../../../../core/references/en/chapters/04-scope.md)).

## Evidence discipline

Before relying on disputed behavior read the
[verification record](../../../../../core/references/en/VERIFICATION.md),
[source issues](../../../../../core/references/en/SOURCE_ISSUES.md) and
[compiler observations](../../../../../core/references/en/chapters/62-compiler-evidence.md).
`RESOLVED_SELECTED_PROFILE` closes only the stated profile; `PARTIALLY_RESOLVED` and
`OPEN` remain unknown. `OBSERVED_MISMATCH` is retained evidence, not permission to
rewrite the expectation. Never invent an effect or drop a counterexample to make a
result look complete. Receipts: `evidence/compiler/`.

## Boundaries

A language reference, not an encyclopedia of VCL/FMX/FireDAC APIs. Never publish a
user's proprietary source, schema, credentials or business rules as examples. Using
this skill grants no permission to publish, deploy, delete data or contact
production systems.
