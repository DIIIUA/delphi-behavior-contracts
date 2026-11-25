# 16. Variables, initialization, threadvar, and block-scoped var

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

This chapter is **included in full in the paid edition** (`1,630` words, `160` lines).

## Sections covered in the full chapter

- Five storage classes and initial-state guarantees
- The critical stack-garbage trap and the difference from C#
- Declaration syntax and initialization rules
- Exact visibility and finalization boundaries of `inline var` and `for var`
- Thread variables (`threadvar`) and memory overlay (`absolute`)
- Restrictions and cost of `threadvar`
- The mechanism and hazards of `absolute`
- A self-contained example (`program ... end.`)
- Version and target boundaries
- Primary sources and verification status

## Indexed topics

- `local and global initialization`
- `threadvar`
- `inline variables`
- `type inference`
- `block lifetime`

## Want to evaluate real depth right now?

Read the 6 multi-difficulty demo excerpts included in this package:
- Level 1 (Basic trap): [10-arrays.md](10-arrays.md)
- Level 2 (Intermediate): [13-managed-records.md](13-managed-records.md)
- Level 3 (Advanced): [31-generics.md](31-generics.md) and [41-directives.md](41-directives.md)
- Level 4 (Hardcore ABI & Evolution): [70-floating-profiles.md](70-floating-profiles.md) and [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
