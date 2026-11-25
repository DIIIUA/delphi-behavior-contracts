# 72. Inline: declaration, call site, and value preservation

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`2,129` words, `135` lines).

## Sections covered in the full chapter

- 1. Two-sided control architecture: `{$INLINE ON|OFF|AUTO}`
- Open documentation discrepancy [`INLINE_DEFAULT_PROFILE`](../SOURCE_ISSUES.md#issue-inline-default-profile) (`OPEN`)
- 2. Physical machine-code evidence in `.text` and `.itext` (`series P13`)
- 3. `IsConstValue(Expr)` and compile-time branching inside `inline` routines
- 4. When the compiler declines to inline a body, and hint `H2443`
- 5. Cascading `.dcu` rebuilds and the effect on the stack frame
- 6. A self-contained verified project and a strict evidence boundary
- 7. Version and target boundaries, and protection against false analogies
- 8. Primary sources and verification status
- Verification 1.3.0: refined boundaries
- INLINE_DEFAULT_PROFILE

## Indexed topics

- `inline routine versus compiler option`
- `definition and call-site options`
- `inline AUTO threshold`
- `inlining eligibility`
- `inline value versus generated code`
- `inline dependency rebuild`
- `IsConstValue compile time folding`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
