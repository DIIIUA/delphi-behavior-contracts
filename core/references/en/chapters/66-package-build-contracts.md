# 66. Package graph and reproducible builds

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,337` words, `114` lines).

## Sections covered in the full chapter

- 1. The package graph invariant (`.dpk`): `contains`, `requires`, and control directives
- 2. The mechanics of `{$WEAKPACKAGEUNIT}` (`WEAK_PACKAGE_STATE_SCOPE`) and probe `P5`
- Prohibition on global state (`WEAK_PACKAGE_STATE_SCOPE` -> `DOCUMENTED_RULE`)
- 3. Output-name decoration (`LIBRARY_NAMING_DEFAULTS`), probe `P11_LibNaming_Dll32`, and the `.dpk` boundary
- 4. A self-contained example (a stateless computation core without global data)
- 5. Version boundaries and protection against false analogies
- 6. Primary sources and confirmation status
- The unit for building the package from the start of the chapter

## Indexed topics

- `package designation vs unit placement`
- `weak state restrictions`
- `implicit rebuild`
- `decorated image vs DCP`
- `artifact consumer proof`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
