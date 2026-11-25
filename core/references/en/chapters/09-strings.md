# 09. Strings, encodings, and indices

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,877` words, `154` lines).

## Sections covered in the full chapter

- 1. String type families and their memory organization
- The hidden `UnicodeString` / `AnsiString` header and constant literals
- 2. Declaration syntax and legacy directives `{$V}` and `{$P}`
- 3. Copy-on-Write, `UniqueString`, `const` aliasing, and `PChar` lifetime
- COW mechanics and dangerous bypasses
- The `PChar(S)` contract, empty strings, and embedded `#0`
- 4. String indexing and `{$ZEROBASEDSTRINGS}`
- 5. The open question `LONGSTRINGS_DOC_CONFLICT` (`{$H-}` on Delphi 13)
- 6. A self-contained example
- 7. Version boundaries and protection against false analogies
- Historical evolution
- Protection against false analogies
- 8. Primary sources and verification status
- Verification 1.3.0: refined boundaries
- LONGSTRINGS_DOC_CONFLICT

## Indexed topics

- `ShortString`
- `AnsiString code pages`
- `UnicodeString`
- `WideString BSTR`
- `RawByteString`
- `copy on write`
- `PChar lifetime`
- `string indices`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
