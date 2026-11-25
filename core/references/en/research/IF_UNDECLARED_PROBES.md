# An undeclared name in $IF: measurements in revision 0.9

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi


Tested with Delphi13 Community, IDE37.0.60542.8024, CompilerVersion37.0,
Win32 Debug and Win64 Debug. These are observations of two small programs;
expected stdout was not assigned in advance. IDE diagnostics:0 errors/0 warnings.
The PE machine and SizeOf(Pointer) confirmed different targets.

| Case | Win32 | Win64 |
|---|---|---|
| IF Unknown > 5 without ELSE | true branch executed | true branch executed |
| IF Unknown > 5 with ELSE | true branch executed | true branch executed |
| IF Declared(Unknown) | False | False |
| IF Declared(Unknown) and (Unknown > 5) | False | False |
| Nested IF Unknown > 5 inside IF Declared(Unknown) | Outer ELSE:missing | Outer ELSE:missing |
| IF KnownValue > 5, KnownValue=2 | False | False |
| IF KnownValue=2 | True | True |
| IF Unknown without comparison | False | False |

The unknown name here is NoSuchBookConstant009, which is not declared in the
source files. The fact that Declared returned False was also observed in the same builds.
The divergence from example32 was reproduced even without ELSE and on both architectures.
It cannot be reduced to every unknown name always being True: a separate

---

*(Full research pass report is included in the full edition.)*
