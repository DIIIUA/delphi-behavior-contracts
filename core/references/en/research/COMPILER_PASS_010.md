# Compiler verification: revision 0.10

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi


18 November 2026, Delphi 13 Community Edition, IDE 37.0.60542.8024.
Builds were invoked through MCP2Delphi using the ordinary IDE Build command. The compiler version,
target platform, and configuration apply to each entry separately.
A total of 35 builds were performed: 14 NEGATIVE branches and 21 additional probes.
Of the additional probes, 18 were run, two were built without running, and one was rejected.
Neither the negative pairs' control EXEs nor the two accepted NEGATIVE branches were run.

## All negative pairs

The controls for all 14 pairs were already built in 0.9. Their source hashes matched the tested
NEGATIVE branches. The NEGATIVE definition was also found in the actual IDE command.
A rejection counts only for the corresponding file and marked line;
the text of each diagnostic was checked for meaning. In 05, a subsequent
E2035 also occurs at line 12; that diagnostic is preserved as an additional diagnostic.

| ID | Actual Win32 Debug result |
|---|---|
| 01 | E2064 @11 |
| 02 | E2003 @10 |
| 03 | E2033 @11 |

---

*(Full research pass report is included in the full edition.)*
