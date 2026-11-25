# 26. Creation, destruction, and ownership

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,570` words, `166` lines).

## Sections covered in the full chapter

- 1. Purpose and the full instance-lifetime pipeline
- The normal eight-step route (`Create` -> `Free`)
- 2. An exception inside a constructor and the rules of `try ... finally`
- 3. Boundaries of `Free`, `FreeAndNil`, multiple ownership, and `class constructor`
- What `Free` and `FreeAndNil` do and do NOT do
- Intersecting ownership models and `class constructor` / `class destructor`
- 4. A self-contained example and a common pitfall
- 5. Version boundaries and protection against false analogies
- Evolution across versions (including the mobile ARC era)
- Protection against false analogies
- 6. Primary sources and confirmation status

## Indexed topics

- `constructor destructor`
- `partial construction`
- `Free FreeAndNil`
- `class constructor destructor`
- `component ownership`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
