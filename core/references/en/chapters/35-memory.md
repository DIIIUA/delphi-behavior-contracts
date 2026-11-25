# 35. Manual and managed memory

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,504` words, `121` lines).

## Sections covered in the full chapter

- Five storage regions and their lifecycles
- Contrasting `New`/`Dispose` with `GetMem`/`AllocMem`/`ReallocMem`/`FreeMem`
- The exact `System.Initialize` contract and heap corruption in `FillChar` / `Move`
- Compile-time guards before `Move`/`FillChar` and raw memory pools (`IsManagedType`, `HasWeakRef`, `GetTypeKind`)
- Reference counting versus GC, `.dll` boundaries, and the historical ARC arc
- A self-contained example (`program ... end.`)
- Primary sources and verification status

## Indexed topics

- `stack heap`
- `New Dispose`
- `GetMem FreeMem ReallocMem`
- `managed values`
- `Move FillChar hazard`
- `DLL memory manager`
- `historical ARC`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
