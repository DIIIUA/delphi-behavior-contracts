# Queue of checks with the real DCC

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi


**Current state in 1.2.0:** see the [new pass](COMPILER_PASS_120.md). The older lists below are queue history; complete language coverage does not follow from the number of builds. All 82 current program listings have been built and run on two Windows targets; the two book packages produced four BPLs, but the subsequent IDE load separately failed.

This is an observation plan and a log of its execution with the live Embarcadero toolchain.
It is based on the [question registry](../SOURCE_ISSUES.md) and the primary-source pages that were read.
The earlier author-written examples and negative pairs have their own manifests;
no outcome is assigned in advance to the residual cases below.

## Identify the environment first

Save the compiler version, edition, target, full command, working directory,
RTL/search/include paths, defines, source hashes, and actual diagnostics.
According to the official pages, `dcc32 -h`/`dcc64 -h` display help. Successful help output
does not by itself confirm the ability to compile or the correct target.

Host32/64 and Win32/Win64 output are different axes. Start with a minimal scalar DPR,
compile it, and run it in an isolated directory. Then select
appropriate example IDs: for example, 55 is intended only for Win64.
A file from another release or a previous build is no substitute for a new receipt.

## The earlier 18 questions

---

*(Full research pass report is included in the full edition.)*
