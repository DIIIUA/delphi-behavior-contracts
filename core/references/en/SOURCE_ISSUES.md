> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi

# Source ambiguities and untested boundaries

Current verification pass 1.5.0: [results, boundaries, and missing materials](research/COMPILER_PASS_150.md).


RESOLVED_SELECTED_PROFILE closes only the explicitly specified current scope. PARTIALLY_RESOLVED preserves the exact remainder. OPEN denotes an unestablished part of the contract, rather than necessarily a compiler error. DOCUMENTED_* means a documentary clarification of a rule, syntax, or version/target boundary. PARTIALLY_DOCUMENTED preserves an explicit remainder. A documentary status does not replace a separate compiler receipt. The narrow observations of edition 0.8 are described in the [evidence matrix](chapters/62-compiler-evidence.md).

- [RANGECHECKS_DEFAULT_PROFILE](#issue-rangechecks-default-profile)
- [FINITEFLOAT_UNDERSPECIFIED](#issue-finitefloat-underspecified)
- [EXTENDED_TARGET_PROFILE](#issue-extended-target-profile)
- [LONGSTRINGS_DOC_CONFLICT](#issue-longstrings-doc-conflict)
- [WARNINGS_ERROR_PROFILE](#issue-warnings-error-profile)
- [INLINE_DEFAULT_PROFILE](#issue-inline-default-profile)
- [TYPEINFO_DOC_CONFLICT](#issue-typeinfo-doc-conflict)
- [IFOPT_TABLE_TYPOS](#issue-ifopt-table-typos)
- [PUSHOPT_TABLE_TYPOS](#issue-pushopt-table-typos)
- [EXTRA_DIRECTIVES_NOT_REVIEWED](#issue-extra-directives-not-reviewed)
- [IMAGEBASE_TARGET_SCOPE](#issue-imagebase-target-scope)
- [LIBRARY_NAMING_DEFAULTS](#issue-library-naming-defaults)
- [EXTENSION_LOCALIZATION_EXAMPLE](#issue-extension-localization-example)
- [INCLUDE_STATEMENT_PART](#issue-include-statement-part)
- [RESOURCE_PREDICATE_VERSION](#issue-resource-predicate-version)
- [CONDITIONAL_TERMINATOR_WORDING](#issue-conditional-terminator-wording)
- [NOINCLUDE_MATCHING_PROFILE](#issue-noinclude-matching-profile)
- [CODEPAGE_SOURCE_FORM_UNCONFIRMED](#issue-codepage-source-form-unconfirmed)
- [RESOURCERESERVE_CURRENT_TARGET](#issue-resourcereserve-current-target)
- [DEBUGINFO_PROFILE_DEPTH](#issue-debuginfo-profile-depth)
- [REFERENCEINFO_LONG_FORM_TEXT](#issue-referenceinfo-long-form-text)
- [PROGRAM_CONTROL_TARGET_COPY](#issue-program-control-target-copy)
- [RECORD_CONSTRAINT_MANAGED_BOUNDARY](#issue-record-constraint-managed-boundary)
- [NAMEOF_DETAILED_GRAMMAR](#issue-nameof-detailed-grammar)
- [WEAK_PACKAGE_STATE_SCOPE](#issue-weak-package-state-scope)
- [WIN64_ASSEMBLER_DOC_DETAILS](#issue-win64-assembler-doc-details)
- [NAMESPACE_LEGACY_AGGREGATION](#issue-namespace-legacy-aggregation)
- [IF_UNDECLARED_IDENTIFIER_OBSERVATION](#issue-if-undeclared-identifier-observation)
- [IF_TYPED_CONSTANT_OBSERVATION](#issue-if-typed-constant-observation)
- [GENERIC_ARGUMENT_DOC_COUNTEREXAMPLE](#issue-generic-argument-doc-counterexample)

<a id="issue-rangechecks-default-profile"></a>

## RANGECHECKS_DEFAULT_PROFILE

Status: RESOLVED_SELECTED_PROFILE. Related names: [RANGECHECKS](directives/rangechecks.md).

Without explicit R/Q in the DPROJ, Debug and Release give R-/Q- on Win32 and Win64; INLINE remains ON. Explicit Debug R+/Q+ enables checks. The configuration name alone does not determine directive states.

Confirmed part: Compiling additionally specifies True; Range checking retains release R+/debug R-. Configuration inheritance is confirmed by a separate page. No universal actual Debug/Release default has been assigned.


---

**[DEMO SUMMARY]** The full edition includes detailed compiler-backed findings, sources and resolutions for all 30 entries (`evidence/source_issues.json`).
