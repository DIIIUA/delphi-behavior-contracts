# 20. Procedures and functions, Result, Exit, nesting, and overloading

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,769` words, `202` lines).

## Sections covered in the full chapter

- Declarations, the `implementation` section, and `forward` declarations
- Return-value mechanics: `Result`, the function name, and the “dirty `Result`” trap
- 1. `Result` versus historical `FuncName := Expr`
- 2. Critical memory mechanics: why a managed `Result` is NOT empty on entry!
- Early exit `Exit` / `Exit(Value)` and the `finally` section
- Nested routines and the stack
- Name overloading (`overload`) and unit boundaries
- The `noreturn` directive in Delphi 13.0 Florence
- A self-contained example (`program ... end.`)
- Version and target boundaries
- Primary sources and verification status

## Indexed topics

- `procedure function`
- `Result and function name`
- `forward`
- `external`
- `overload`
- `recursion`
- `nested routines`
- `inline`
- `noreturn`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
