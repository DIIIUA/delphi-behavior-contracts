# 55. Counterexamples for checking understanding

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,314` words, `120` lines).

## Sections covered in the full chapter

- 1. A dynamic array without COW versus `UnicodeString` with COW
- 2. Three cases that lose short-circuiting under `{$B-}`: `Variant`, `LogicalAnd`, and `IfThen`
- 3. A shallow `record` copy with an object reference
- 4. Capturing the `for` bound once and unsigned `0 - 1`
- 5. Polymorphic `override` versus static method hiding
- 6. Opposite asymmetries of partial failure: `TObject.Create` versus `CMR.Initialize`
- 7. Why `SizeOf(Ev)` invokes a function instead of measuring the pointer (`P6` / `P7`)
- 8. A quiet `W1074` warning for an unknown attribute and a dangling `with Arr[I]`
- 9. Three “default value” illusions and embedded `#0` in `PChar`
- A self-contained example (`program ... end.`)
- Primary sources and verification status

## Indexed topics

- `array string counterexample`
- `Variant Boolean counterexample`
- `record copy counterexample`
- `cached loop counterexample`
- `partial failure counterexample`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
