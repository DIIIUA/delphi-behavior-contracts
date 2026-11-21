> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

# INLINE — inlineability and the call site

**Syntax:** directive `{$INLINE ON}` / `{$INLINE OFF}` / `{$INLINE AUTO}`; the word `inline;` in a routine header is part of its declaration.

**Default in the cited source:** A conflict between layers ([`INLINE_DEFAULT_PROFILE`](../SOURCE_ISSUES.md#issue-inline-default-profile), `OPEN`): the *Language Guide* specifies `ON`, while *Compiling* specifies `off` for the IDE (set the mode explicitly).

**Scope according to the documentation:** Two-sided — the state at the **definition point** and at **each call site** is considered.

The `inline` mechanism (since **Delphi 2005**) operates on typed IR inside `.dcu` ([chapter 72](../chapters/72-inline-semantics.md)):
- **`ON`:** marks a routine with `inline;` in `.dcu` and expands its body instead of `call`/`ret` at the call site;
- **`OFF`:** suppresses marking or substitution on the corresponding side;
- **`AUTO`:** considers small unmarked routines for inlining (up to **32 bytes** of code according to the help).

```pascal
{$INLINE ON}
function MagicAdd(N: Integer): Integer; inline;
begin
  Result := N + $13572468;
end;
```

**Physical machine-code measurements (`P13_Inline_*`, `Delphi 13 CE` `Win32`):**
Counting constant `$13572468` (`m1`, 3 calls to `MagicAdd; inline;`) and `$24681357` (`m2`, 1 call to ordinary `PlainAdd`) in PE-image sections `.text` / `.itext`:
- **`P13_IfOpt_INLINE` / `P13_Inline_IfOpt_Rel`:** `{$IFOPT INLINE ON}` returned **`ON`** in both IDE templates (`Debug` and `Release`);
- **`P13_Inline_Default_Dbg` / `_Rel`:** `.text: m1=0, m2=1`; **`.itext: m1=3, m2=0`** (all 3 calls physically expanded in `.itext` in both `Debug` and `Release`!);
- **`P13_Inline_DefOn_CallOff` and `P13_Inline_DefOff_CallOn`:** **`.text: m1=1, m2=1`; `.itext: 0`** (`{$INLINE OFF}` on *either* side cancels substitution);
- **`P13_Inline_DefAuto_CallOn`:** `.text: m1=0, m2=1`; `.itext: m1=3, m2=0` (`PlainAdd` without `inline;` **is NOT automatically inlined across units**!).

**Limitations:** changing an `inline` body requires a full rebuild (`Build`) of dependent `.dcu` files; `virtual`/`asm`/open arrays/`.bpl` boundaries are not inlined; missing units in `uses` produce `H2443`. Do not confuse this with C++ ODR, `.dfm` `inline`, or TP `inline($8B/...)`.

Source: [Embarcadero](https://docwiki.embarcadero.com/RADStudio/Florence/en/Calling_Procedures_and_Functions). Read on 18.11.2026.

Status: checked against the documentation; result preservation ([example 49](../../../examples/README.md)) and physical substitution/cancellation in `.itext` measured in `P13_Inline_*` on `Win32 Debug/Release`.

## Verification 1.3.0: refined boundaries

**INLINE_DEFAULT_PROFILE — RESOLVED_SELECTED_PROFILE.** Without an explicit switch, IFOPT INLINE ON is true in both Windows Debug/Release configurations. With O+, the new ON/AUTO/OFF and marked/plain forms produce the same computed result; this alone does not prove inlining; the earlier physical marker/count probes across units remain. This is a recommendation to the compiler, rather than a guarantee that every call will be inlined.

Scope: The effective current default and finite within-unit/cross-unit controls on Win32/Win64. Remainder: A precise decision about another call requires its source, profile, and machine code. The optimizer's algorithm across releases has not been reconstructed and is not required as an invented language rule.

[All 23 results](../research/RESIDUE_23_130.md); [compiler receipt](../../../evidence/compiler/demo-sample-receipts.json).
