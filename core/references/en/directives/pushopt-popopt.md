> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

# PUSHOPT / POPOPT — saving and restoring options

**Syntax:** `{$PUSHOPT} ... {$POPOPT}`.

**Default in the specified source:** Compiler option-stack commands; they have no ON/OFF default of their own.

**Documented scope:** `Local` (a LIFO stack within the current unit).

## The option-stack mechanism and findings from series `P2`–`P3` (`0.11`)

The directives were introduced in **Delphi 13 Florence** to change switches (`{$R-}`, `{$Q-}`, `{$J+}`, `{$O-}`, `{$WARNINGS ...}`) locally and restore the original profile exactly without cumbersome `{$IFOPT}` tests ([example 29](../../../examples/README.md), `0.8`: `on`, `off`, `on`; [chapter 41](../chapters/41-directives.md), [chapter 59](../chapters/59-directive-profiles.md)). Nested pairs follow LIFO, but **do not** preserve `{$DEFINE}`/`{$UNDEF}` symbols, the `.inc` stream, or variable state.

The original comment “ВЕСЬ стек опций целиком” below is imprecise: `POPOPT` restores the top snapshot; lower snapshots remain on the stack. The original source is retained to match the compiler evidence.

```pascal
// Проверено в P2_PushOpt_Sel_Effect и P3_PushOpt_Discriminate (Delphi 13 CE 37.0)
{$PUSHOPT RANGECHECKS} // хвостовой аргумент не сужает снимок!
  {$R-}{$Q+}
{$POPOPT} // восстанавливает ВЕСЬ стек опций целиком: after_pop R=ON, Q=OFF
```

*English glosses of the retained source comments:*
- Verified in P2_PushOpt_Sel_Effect and P3_PushOpt_Discriminate (Delphi 13 CE 37.0)
- the trailing argument does not narrow the snapshot!
- restores the option states from the top saved snapshot: after_pop R=ON, Q=OFF



Live experiments in **series `P2` and `P3`** ([COMPILER_PASS_011](../research/COMPILER_PASS_011.md)) revealed two critical boundaries:
1. **Complete rollback rather than selective rollback (`PUSHOPT_TABLE_TYPOS`, status `OPEN`):** despite mentions of named arguments and typos `IMPOTEDDATA` / `FINITEFLOATT` in the *Option OPT* table, calling `{$POPOPT}` in probes `P2_PushOpt_Sel_Effect` and `P3_PushOpt_Discriminate` rolled back **all changed options (`R=ON; Q=OFF`)**.
2. **Silent ignoring of typos:** probes `P3_PushOpt_Bogus` (`BOGUS_OPT`), `P3_PushOpt_Typo1` (`FINITEFLOATT`), and `P3_PushOpt_Typo2` (`IMPOTEDDATA`) compiled with **`0` diagnostics** (unlike `{$IFOPT}`, where typos immediately caused `E1030`). Seven rare table names are examined separately in [`EXTRA_DIRECTIVES_NOT_REVIEWED`](../SOURCE_ISSUES.md#issue-extra-directives-not-reviewed) ([EXTRA_OPTIONS.md](../research/EXTRA_OPTIONS.md)).

## Protection against false analogies

Unlike MSVC `#pragma warning(push/pop)`, which saves only warnings, `{$PUSHOPT}` also captures code-generation checks; unlike Free Pascal `{$PUSH}`/`{$POP}`, Delphi 13 strictly uses `{$PUSHOPT}`/`{$POPOPT}` — write them **without arguments** ([SOURCE_ISSUES](../SOURCE_ISSUES.md#issue-pushopt-table-typos)).

Source: [Embarcadero](https://docwiki.embarcadero.com/RADStudio/Florence/en/Option_OPT_(Delphi)). Read on 18.11.2026.

Status: complete stack rollback and ignored trailing names are confirmed in `0.8` and `P2`–`P3` (`Delphi 13 CE`); `PUSHOPT_TABLE_TYPOS` remains `OPEN`.

## Verification 1.3.0: refined boundaries

**PUSHOPT_TABLE_TYPOS — PARTIALLY_RESOLVED.** A nested include restores R/Q through the stack. An unmatched PUSHOPT produces W1079, and POPOPT W1078, on Win32/64. The previous BOGUS_OPT/FINITEFLOATT trailing portions were accepted, but the entire set was restored, so this does not prove a selective subset.

Scope: A nested stack, include, and imbalance in the current Windows profile. Remainder: A selective subset requires an official exact grammar/correction to Option OPT, or an Embarcadero example with distinguishable partial restoration and a version-matched compiler. Acceptance of an ignored trailing portion is not an answer.


[All 23 results](../research/RESIDUE_23_130.md); [compiler receipt](../../../evidence/compiler/demo-sample-receipts.json).
