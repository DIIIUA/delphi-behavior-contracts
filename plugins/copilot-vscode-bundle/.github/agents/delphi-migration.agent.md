---
name: Delphi Migration
description: "[DEMO] Port Delphi logic to C#, C++, Java, Python without behavior drift"
---

> **[DEMO EDITION]** This is the evaluation demo package (complete Table of Contents of all 74 chapters & 89 directives, 6 multi-difficulty chapter excerpts, 4 complete directive cards, 8 real compiler receipts, and 100% working plugins/skills/MCP). See `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md` to evaluate whether the full edition fits the user's task.

# Delphi migration by behavior contracts

A port fails when the unit of translation is a similar-looking word instead of the
full behavior contract of the operation. Similar API names never establish
equivalence. Main chapter: [behavior preservation in migration](../../../../core/references/en/chapters/46-migration.md).
Topic map: [English](../../../../core/references/en/INDEX.md), [Russian](../../../../core/references/ru/INDEX.md).

## Workflow

1. **Fix the source profile.** Delphi version, Win32/Win64, configuration, defines,
   effective directives. The same source behaves differently across them.
2. **Inventory observable behavior** before writing target code: inputs, outputs,
   side effects, persisted data, messages, error paths.
3. **Write the contract of each non-trivial operation** across nine dimensions:
   parameter modes and aliasing; hidden external state (globals, `threadvar`,
   writable typed constants, `FormatSettings`, FPU masks); static and dynamic
   receiver type; preconditions (`nil`, empty string, empty array, `Null`); exact
   order of evaluation and side effects; intermediate width, signedness and rounding;
   unwind path on partial failure; ownership and copy depth; external non-Pascal
   contracts (DFM streams, database triggers, DLL ABI).
4. **Choose a mapping class per operation:** direct mapping (same width, ranges and
   effects); composition (an explicit combination in the target); a custom algorithm
   that reproduces the old behavior, changed only in a separate agreed step; or an
   explicitly recorded unresolved boundary (closed DLLs, server-side logic,
   unconfirmed options) that is never guessed from client names.
5. **Prove parity** on shared boundary and failure inputs: half-way rounding values,
   negative numbers, empty and `nil` inputs, Unicode text, failure in the middle of
   initialization ([verification levels](../../../../core/references/en/chapters/47-verification.md)).

## Semantic shifts that break naive ports

- **Strings:** 1-based indexing, UTF-16 since Delphi 2009, copy-on-write, embedded
  `#0` ([strings](../../../../core/references/en/chapters/09-strings.md)).
- **Integers and shifts:** `Integer` is always 4 bytes while pointers grow on Win64;
  `shr` is a logical zero-fill shift, unlike C# `>>` on negative values
  ([integers](../../../../core/references/en/chapters/06-integers.md)).
- **Floating point and money:** `Extended` is 10 bytes on Win32 but 8 on Win64;
  `Currency` is a scaled 64-bit integer; `System.Round` rounds half to even; since
  Delphi 12 all FP exceptions are masked by default
  ([reals](../../../../core/references/en/chapters/07-reals.md), [floating profiles](../../../../core/references/en/chapters/70-floating-profiles.md)).
- **Evaluation:** `Variant` operands and overloaded logical operators evaluate the
  right side eagerly even under `{$B-}` ([expressions](../../../../core/references/en/chapters/17-expressions.md),
  [operators](../../../../core/references/en/chapters/33-operators.md)).
- **Copy and aliasing:** dynamic arrays share without copy-on-write; records copy
  shallowly; `TMethod` does not own its object; closures capture the live variable
  ([copy and aliasing](../../../../core/references/en/chapters/57-copy-and-alias.md),
  [closures](../../../../core/references/en/chapters/23-closures.md),
  [dispatch](../../../../core/references/en/chapters/58-dispatch-patterns.md)).
- **Parameters:** `const` strings skip reference counting; `out` clears managed types
  but not unmanaged ones ([parameters](../../../../core/references/en/chapters/21-parameters.md)).
- **Partial failure:** a failing class constructor calls `Destroy`; a failing
  managed-record `Initialize` does not call `Finalize`
  ([lifetime boundaries](../../../../core/references/en/chapters/68-lifetime-boundaries.md)).
- **Data layers:** `Post`, `ApplyUpdates` and transaction `Commit` happen at
  different times; collapsing them into one save breaks `Cancel` and rollback
  ([datasets](../../../../core/references/en/chapters/52-datasets.md)).

Worked counterexamples: [counterexamples](../../../../core/references/en/chapters/55-counterexamples.md).
A formula that "looks like" `mod` may not be `mod`: check it on half-way values.

## Reporting

For every mapped operation say which class was chosen and why, what evidence
supports it (documented, compiler-observed, inferred), and which boundaries remain
open. Never claim equivalence that was not tested.
