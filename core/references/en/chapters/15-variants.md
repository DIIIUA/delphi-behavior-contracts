# 15. Variant, OleVariant, Null, and Automation

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,277` words, `122` lines).

## Sections covered in the full chapter

- 1. Purpose and binary structure of `TVarData` (32-bit versus 64-bit)
- 2. The distinction between `Variant` and `OleVariant`
- 3. Five distinct “empty” states and the `Null` trap
- Propagation of `Null` and the prohibition on `if V = Null then`
- 4. Variant arrays, `TCustomVariantType`, `IDispatch`, and complete evaluation of `and`/`or`
- A verified trap: `{$B-}` short-circuiting is disabled for `Variant`
- 5. A self-contained example
- 6. Version boundaries and avoiding false analogies
- Historical evolution
- Protection against false analogies
- 7. Primary sources and verification status

## Indexed topics

- `Variant`
- `OleVariant`
- `Null Unassigned EmptyParam`
- `variant arrays`
- `custom variants`
- `late binding`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
