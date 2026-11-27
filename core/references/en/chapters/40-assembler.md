# 40. asm, machine code, and platform restrictions

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,369` words, `106` lines).

## Sections covered in the full chapter

- 1. Purpose, BASM syntax, and platform scope
- 2. The critical Win32/Win64 boundary (`DCC64`) and frame pseudo-operations
- 3. Managed local variables, unwinding, and `WIN64_ASSEMBLER_DOC_DETAILS` (`OPEN`)
- Warning about local managed types and unwinding
- Open question `WIN64_ASSEMBLER_DOC_DETAILS` (`OPEN`) and live probes P3 and P13
- 4. A self-contained example (a cross-architecture framework with a Pascal reference)
- 5. Version boundaries and protection against false analogies
- 6. Primary sources and confirmation status
- Verification 1.3.0: refined boundaries
- WIN64_ASSEMBLER_DOC_DETAILS

## Indexed topics

- `asm syntax`
- `assembly expressions and addressing`
- `register ABI`
- `CPU conditionals`
- `external object files`
- `Win64 whole assembler routine`
- `PARAMS PUSHNV SAVENV NOFRAME`
- `NOFRAME and XMM source conflict`
- `assembly cleanup and unwind`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
