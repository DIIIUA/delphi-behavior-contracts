# 42. Conditional compilation and configurations

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,592` words, `118` lines).

## Sections covered in the full chapter

- 1. Conditional text selection before construction of the syntax tree
- 2. `{$ENDIF}` vs `{$IFEND}` closers, `{$INCLUDE}`, `{$IFOPT}`, and `{$RESOURCE}`
- The terminator rule (`CONDITIONAL_TERMINATOR_WORDING` -> `DOCUMENTED_VERSION_BOUNDARY`)
- `{$INCLUDE}` inclusions at five grammatical positions (`INCLUDE_STATEMENT_PART`, `OPEN`)
- A table of 15 long `{$IFOPT ...}` forms (`P13_IfOpt_*`, [`IFOPT_TABLE_TYPOS`](../SOURCE_ISSUES.md#issue-ifopt-table-typos))
- Conditional `{$RESOURCE}` predicates (`RESOURCE_PREDICATE_VERSION`, `OPEN`)
- 3. Two open discrepancies between the live compiler and `{$IF}` documentation (`OPEN`)
- 1. An undeclared identifier in a comparison (`IF_UNDECLARED_IDENTIFIER_OBSERVATION`, `mismatch 32`, `OPEN`)
- 2. A typed constant in `{$IF}` (`IF_TYPED_CONSTANT_OBSERVATION`, `NEGATIVE 09`, `OPEN`)
- 4. A self-contained example
- 5. Version boundaries and protection against false analogies
- 6. Primary sources and confirmation status
- Verification 1.3.0: refined boundaries
- IF_UNDECLARED_IDENTIFIER_OBSERVATION
- IF_TYPED_CONSTANT_OBSERVATION

## Indexed topics

- `IFDEF IFNDEF`
- `IF ELSEIF`
- `DEFINE UNDEF`
- `IFOPT`
- `predefined conditionals`
- `INC and rebuild`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
