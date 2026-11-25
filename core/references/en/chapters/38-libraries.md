# 38. library, package, and external symbols

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,547` words, `225` lines).

## Sections covered in the full chapter

- 1. Purpose: three fundamentally different module boundaries
- 2. `library` grammar, exporting `exports` overloads, and `external` import
- Exporting from `library` ([Export symbols](https://docwiki.embarcadero.com/RADStudio/Florence/en/Export_symbols_(Delphi)))
- Static and delayed `external` import ([External Symbols](https://docwiki.embarcadero.com/RADStudio/Florence/en/External_Symbols_(Delphi)))
- 3. The fatal mechanics of a raw `.dll`: isolated heaps and duplicate VMTs
- 4. Packages (`package`) and output-naming boundaries
- 5. A self-contained example (a symmetric buffer contract across the library boundary)
- 6. Version boundaries and avoiding false analogies
- 7. Primary sources and verification status
- The unit file for the package example
- A client that checks exported overloads

## Indexed topics

- `library`
- `exports name index`
- `external delayed`
- `dynamic loading`
- `package requires contains`
- `BPL DCP dependencies`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
