# Independent compiler verification, revision 1.2.0

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi


20 November 2026. Based on the unchanged original 1.1.0 archive with SHA-256
`fdfc9fb72158e7eacda2d43daf7131cacb699cfdab819e9f360fba3c1f11e9ce`.
Historical compiler-evidence JSON files are preserved byte for byte; new observations
are in a [separate receipt](../../../evidence/compiler/demo-sample-receipts.json).

## Method and limit

Actual Delphi 13 Community Edition was used, IDE file version
37.0.60542.8024. Synthetic projects were built using the standard IDE Build action
through MCP2Delphi; commercial CLI restrictions were not bypassed. Each probe
had a separate directory and ProjectGuid. No binary output existed
in the directory before the build. The source, DPROJ, all auxiliary inputs,
their SHA-256 hashes, the profile from build messages, the event for the probe's own project,
diagnostics, the new PE's hash, target machine, and a separate execution result were recorded.

Because of the Windows installer heuristic for a name containing Dispatch,
EXEs were run as a byte-for-byte identical copy named RunFixture.exe; elevation
was not required. Negative/control branches were not executed. RPC/IDE
summary success alone was not accepted as compiler success.

---

*(Full research pass report is included in the full edition.)*
