# Verification record

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

Delphi Behavior Contracts 1.0.0, built from research edition 1.5.2 (21 November 2026).
This record states what was measured, where, and what is **not** claimed.

## Version numbering

- **1.0.0** is the version of this product (the plugin, the skill package, `plugin.json`).
- **1.5.2** is the research edition of the reference it was built from.
- Numbers such as 0.8, 0.10, 1.2.0, 1.3.0 or 1.5.0 inside chapters, cards and
  `research/` name the **verification pass** in which an observation was made or a
  statement was corrected. They record where a fact came from; they are not the
  version of the product. The current state of every open question is the one in
  [source issues](SOURCE_ISSUES.md) and `evidence/source_issues.json`.

## Compiler

Embarcadero Delphi 13 Community Edition. IDE file versions 37.0.60542.8024 and
37.0.60952.8797. Builds used the standard IDE Build action; a command-line exit code
accompanied by a Community Edition restriction message was never counted as a build.

## Measured passes

| Pass | What was measured | Result |
|---|---|---|
| 1.2 | 564 build observations, 471 executions | All 82 standalone program listings of the book built and ran on Win32 and Win64: 164 runs with exit code 0 |
| 1.3 | 315 build observations: Win32 126, Win64 127, Android ARM32 31, Android ARM64 31 | 221 builds succeeded, 94 failed (negative language probes and two preserved linker-environment errors); 179 Windows runs: 175 exit 0, four exit 1 with an access violation after DLL unload (preserved); 30 ELF files produced but not executed; 8 generated HPP files; 6 debugger observations |
| 1.5 | 26 selected cases repeated on IDE build 37.0.60952.8797 | 18 executed Windows cases and 8 expected rejections match the earlier outcomes; a Linux build was blocked by a missing connection profile before the compiler ran (recorded as an environment blocker, not a language result) |

The 1.2 and 1.3 receipts together hold 879 observations and 650 executions. This is
the sum of passes with repetitions, not a count of distinct language features.

## Open questions register

30 registered questions where the official documentation is ambiguous, incomplete or
contradicted by the compiler: 8 `RESOLVED_SELECTED_PROFILE` (closed only for the
stated profile), 10 `PARTIALLY_RESOLVED`, 5 `OPEN`, 6 `DOCUMENTED_*`,
1 `PARTIALLY_DOCUMENTED`. Seven compiler options have only table-level documentation
and remain incomplete contracts. Details: [source issues](SOURCE_ISSUES.md),
[remaining questions](research/RESIDUE_23_130.md),
[latest pass](research/COMPILER_PASS_150.md).

## Evidence in this package

- Compiler receipts: `evidence/compiler/` (source hashes, targets, configurations,
  diagnostics, outputs). Local machine paths in receipts are replaced by neutral
  placeholders such as `<user>`, `<workspace>`, `<RADSTUDIO>` and `<PUBLIC_STUDIO>`;
  nothing else was changed. Two Android output-control project files and the 1.3
  receipt keep the output folder `D:\Delphi MCP\verification_130`: those project files
  are bound to the receipt by SHA-256, so they are shipped byte for byte. The folder
  name identifies the IDE bridge used for the builds, not a person.
- Example and probe sources with their IDE project files: `examples/`, byte for byte as
  measured. Compiled binaries (EXE/DLL/DCU/BPL/SO) are not supplied.
- Source registry and topic coverage: `evidence/sources.json`, `evidence/coverage.json`,
  `evidence/source_issues.json`.

## Not claimed

- Not 100% of the Delphi language, not 100% of any ABI, not zero warnings or hints.
- Not other compiler versions, macOS/iOS/Linux execution, or C++Builder consumers,
  unless a chapter states a specific observation.
- Program output without an independent oracle remains an observation, not proof of
  every semantic detail of an example.
- This is an independent reference. It is not an Embarcadero product and is not
  endorsed by Embarcadero.
