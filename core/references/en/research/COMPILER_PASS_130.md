# Compiler and documentation verification 1.3.0

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi


20 November 2026 (UTC). Based on the unchanged 1.2.0 archive. All earlier compiler-evidence JSON files are preserved byte for byte. All 23 original OPEN issues were examined; [individual results and required materials](RESIDUE_23_130.md).

## Scope and method

**315 new build observations**, comprising 126 Win32, 127 Win64, 31 ARM32, and 31 ARM64. 179 Windows executions: 175 with exit=0 and **4 preserved unsuccessful executions** of DLL consumers. 30 ELF libraries were produced without execution, along with 8 C++ headers. Six additional IDE-debugger observations do not count as six new compilations.

Each fixture has a separate directory, fixed DPR/DPROJ/PAS/INC/RES inputs, hashes, and a completion event for that specific project. The standard IDE Build action through MCP2Delphi was used. Direct CLI restrictions of Community Edition were not bypassed. Output and diagnostics are preserved separately from the original expectation; OBSERVATION_ONLY does not mean a normative PASS. ARM code was not deployed or run. An HPP header does not verify the external C++ ABI.

The IDE exited three times during early ARM attempts. These attempts and restart receipts are preserved in the private working audit. IDE failure was not counted as a language rejection. Two linker attempts that lost the relative working directory are retained with E2597/F2588; the same source bytes were built in fresh controls with absolute output paths. Two completed ELFs were found in the SDK working directory and associated with the completed call by name, time, sources, and hash. The public DPROJ files for those two controls fix the output paths as used during verification; local reruns must redirect those paths to their own directory.

In one session, the IDE panel returned an ordinary MSBuild log instead of the native Building line. The actual output is preserved; the profile is checked by project name, target compiler, and DEBUG/RELEASE define. No synthetic Building line was added.

## Substantive corrections

- `record` and `unmanaged`: 80 compile observations on four targets; plain array/pointer are important counterexamples to the “subset” relation. ARM here verifies acceptance and ELF output, rather than runtime behavior.
- Resource predicates are a list of conditional identifiers; `OR` can itself be an identifier. The earlier wording about Boolean OR was corrected.
- Three tabulated IFOPT names were corrected and checked independently. Numeric IFOPT is not equated with the final PE bits.
- The NOINCLUDE comparison was checked using new ConsumerU.hpp files, rather than merely the absence of DCC errors.
- D1/D2 were checked by the debugger consumer: breakpoint, Input=41, step, LocalValue=42. D0 did not reach the requested line. One API's intermediate line=0 is preserved alongside the actual thread line=10 during evaluation.
- Windows DLL: the earlier global-frame consumer printed TRUE, then crashed during termination after FreeLibrary. The scoped consumer completes managed work in a procedure before unload and passes with the same producer. The precise internal cause has not been invented.

---

*(Full research pass report is included in the full edition.)*
