# 37. Standard procedures and file input/output

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,859` words, `188` lines).

## Sections covered in the full chapter

- 1. Purpose and three classic file types
- Why `file of T` rejects managed types and what makes `RecSize = 128` dangerous
- 2. Descriptor lifecycle, `FileMode`, and formatting
- 3. Error handling: `{$I+}` / `{$I-}` and one-time reset of `IOResult`
- 4. `System` compiler magic (intrinsics) and `Write`/`Writeln`/`Str` formatting (`:W:D`)
- 5. A self-contained example
- 6. Version boundaries and avoiding false analogies
- Evolution across versions
- Protection against false analogies
- 7. Primary sources and verification status

## Indexed topics

- `TextFile`
- `typed untyped files`
- `AssignFile Reset Rewrite Append CloseFile`
- `Read Write Readln Writeln`
- `BlockRead BlockWrite`
- `Seek Eof FileSize`
- `IOResult`
- `System compiler magic intrinsics and Write formatting`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
