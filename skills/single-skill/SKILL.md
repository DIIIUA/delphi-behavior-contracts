---
name: delphi-behavior-contracts
description: "[DEMO] Read, write, review, debug and migrate Delphi / Object Pascal code by its actual behavior, not by similar-looking names. Use for any Delphi work, especially porting Delphi logic to C#, C++, Java or another language, upgrading old Delphi code, or explaining copying, aliasing, ownership, dispatch, exceptions, numeric rounding, strings, directives and version differences. Backed by a 74-chapter reference with compiler-measured observations on Delphi 13."
---

> **[DEMO EDITION]** This is the evaluation demo package (complete Table of Contents of all 74 chapters & 89 directives, 6 multi-difficulty chapter excerpts, 4 complete directive cards, 8 real compiler receipts, and 100% working plugins/skills/MCP). See `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md` to evaluate whether the full edition fits the user's task.

# Delphi Behavior Contracts

A version-aware Delphi / Object Pascal language reference for agents. Its unit of
translation is the **behavior contract of an operation**, not a similar keyword.
English reference: [references/en/INDEX.md](../../core/references/en/INDEX.md).
Russian reference: [references/ru/INDEX.md](../../core/references/ru/INDEX.md).

## How to use this skill

1. Read only what the task needs. Find the topic in the index, or search:
   `python scripts/lookup.py "dynamic array"` (English, default) or
   `python scripts/lookup.py --lang ru "динамический массив"`.
   The one-file books in `book/` are for continuous human reading; do not load them
   for a small task.
2. Establish the actual target first: compiler release, CPU/OS, build configuration,
   active defines, unit search paths, effective directives, and the real type or
   instance that owns each operation. An unidentified profile is an unknown, not
   permission to assume the latest Delphi. Free Pascal's Delphi mode is a different
   compiler and does not validate Delphi behavior.
3. Answer with the status of each claim: documented, observed on a compiler,
   inferred, or unknown. A parsed file, a passing linter or a matching hash is not a
   compiled or behavioral result.

## Working modes

- **Explain or teach.** Give syntax, actual semantics, version limits, a small
  example, and a case that exposes the common misunderstanding.
- **Implement or repair Delphi.** Inspect declarations, callers and affected
  consumers; use syntax supported by the target version; make a bounded change and
  compile/test with the real toolchain when available.
- **Review behavior.** Trace values, aliasing, ownership, dispatch, exceptions,
  managed-type cleanup and compiler-dependent operations. Include DFM/FMX or
  component source only when it participates in the requested flow.
- **Migrate.** Establish observable behavior first, then choose a direct mapping,
  a composite mechanism, a custom algorithm that reproduces the old behavior, or an
  explicitly recorded unresolved external contract. Read
  [behavior preservation in migration](../../core/references/en/chapters/46-migration.md).

## The nine dimensions of a behavior contract

Before replacing a routine or expression, fix: parameter modes and permitted
aliasing; hidden external state; static and dynamic receiver type; preconditions
(`nil`, empty string, empty array, `Null`); exact order of evaluation and side
effects; width of intermediate arithmetic, signedness and rounding; the unwind path
on partial failure; ownership and copy depth; external non-Pascal contracts (DFM
streams, database triggers, DLL ABI). Similar API names never establish equivalence.

## Decisions that require care

- **Copy versus alias.** `B := A` has six physical models across 13 type families:
  dynamic arrays share a buffer **without** copy-on-write, long strings share **with**
  copy-on-write, records copy shallowly, class variables copy a pointer. Say which
  object or buffer is shared and which variable still points to it.
  [Copy and aliasing table](../../core/references/en/chapters/57-copy-and-alias.md).
- **Callables.** Distinguish assigning a method pointer from invoking it; a method
  reference can receive a compatible method, but not the reverse into an `of object`
  event. Closures capture the variable cell, not a value copy.
  [Callables](../../core/references/en/chapters/22-callables.md),
  [closures](../../core/references/en/chapters/23-closures.md),
  [dispatch patterns](../../core/references/en/chapters/58-dispatch-patterns.md).
- **Lifetime.** Constructor failure, managed-record `Initialize` failure and unit
  finalization have different cleanup rules.
  [Lifetime boundaries](../../core/references/en/chapters/68-lifetime-boundaries.md).
- **Numbers.** Separate storage size, intermediate precision and FP exception masks;
  `Extended` differs between Win32 and Win64; `System.Round` rounds half to even;
  `Currency` is a scaled integer; `shr` is always a logical shift.
  [Floating profiles](../../core/references/en/chapters/70-floating-profiles.md),
  [integers](../../core/references/en/chapters/06-integers.md).
- **Strings and indices.** UTF-16 versus byte encodings, 1-based `System` routines
  versus 0-based `TStringHelper`, `{$ZEROBASEDSTRINGS}`.
  [Strings](../../core/references/en/chapters/09-strings.md).
- **Parameters.** `const`, `const [ref]`, `var`, `out` differ in reference counting,
  initialization and aliasing. [Parameters](../../core/references/en/chapters/21-parameters.md).
- **Data layers.** Do not merge `Post`, `ApplyUpdates`, transaction `Commit`,
  `Cancel`, rollback and window close: they have separate receivers and effects.
  [Datasets](../../core/references/en/chapters/52-datasets.md).
- **Evaluation.** `with`, overloads, helpers, unit shadowing and implicit operators
  change name resolution; `Variant` and overloaded logical operators may evaluate
  eagerly even under `{$B-}`. A property getter or setter may run code.

## Versions and directives

Modern constructs need their own version profile: Unicode defaults, anonymous
methods, generics, inline variables, managed-record operators, multiline literals,
and Delphi 13 conditional expressions, `NameOf` and new constraints. Historical ARC,
old `object`, `Real48`, pointer-size assumptions and old directives still matter
when reading legacy code. [Versions](../../core/references/en/chapters/43-versions.md),
[evolution from old to new](../../core/references/en/chapters/73-evolution-old-to-new.md).

For a compiler option read its [directive card](../../core/references/en/directives/INDEX.md).
Separate source directives, CLI options, IDE settings, DCU cache, linker artifacts
and runtime effects. A directive accepted by the parser may have no measured effect
on a target. [Source and build profiles](../../core/references/en/chapters/64-source-build-profiles.md).

## Evidence discipline

Before relying on disputed behavior, read the [verification record](../../core/references/en/VERIFICATION.md),
[source issues](../../core/references/en/SOURCE_ISSUES.md) and the
[latest compiler pass](../../core/references/en/research/COMPILER_PASS_150.md).
`RESOLVED_SELECTED_PROFILE` closes only the stated profile; `PARTIALLY_RESOLVED`
and `OPEN` remain unknown boundaries. Do not invent effects, and do not erase a
counterexample to make a result look complete. Distinguish an observed compiler
rejection from an environment-blocked build, and compile-only ARM/ELF or a generated
HPP from an executed consumer. `OBSERVED_MISMATCH` is retained evidence, not
permission to rewrite the expected result. Compiler receipts are in
[evidence/compiler/](../../core/evidence/compiler/demo-sample-receipts.json); read
[compiler observations](../../core/references/en/chapters/62-compiler-evidence.md) before
claiming an example was verified.

## Boundaries

This is a language reference, not an encyclopedia of VCL/FMX/FireDAC APIs; use
version-matched RTL or component source for library implementation details. Never
publish a user's proprietary source, schema, credentials or business rules as
examples. Using this skill grants no permission to publish, deploy, delete data or
contact production systems.
