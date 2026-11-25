> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.1** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

# EXTENDEDCOMPATIBILITY — the Extended compatibility representation

**Syntax:** `{$EXTENDEDCOMPATIBILITY ON}` or `{$EXTENDEDCOMPATIBILITY OFF}`.

**Default in the cited source:** `OFF`.

**Documented scope:** Local (applies to subsequent declarations of types and data involving `Extended`).

The directive controls the **binary storage size** of [`System.Extended`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.Extended) on platforms where `Extended` is compressed by default to 8-byte IEEE-754 `Double` (`Win64` SSE2 and `ARM`; see [Multi-Device Considerations](https://docwiki.embarcadero.com/RADStudio/Florence/en/Delphi_Considerations_for_Multi-Device_Applications); on `Win32` x87, `Extended` is always 10 bytes, and on `Linux64` under the System V ABI, 16 bytes; [chapter 07](../chapters/07-reals.md), [chapter 70](../chapters/70-floating-profiles.md)):
- under **`OFF`**, on `Win64`, `Extended` occupies `8` bytes (`Double`);
- under **`ON`**, on `Win64`, the compiler allocates **10 bytes** (the [`TExtended80Rec`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.TExtended80Rec) layout), **but does NOT enable 80-bit x87 arithmetic**: computation uses 64-bit IEEE `Double` (53-bit significand mantissa) precision!

```pascal
{$EXTENDEDCOMPATIBILITY ON}
// Win32: SizeOf(Extended)=10, prec64=TRUE, round-trip TExtended80Rec=TRUE
// Win64: SizeOf(Extended)=10, но prec64=FALSE (SSE2) и round-trip TExtended80Rec=FALSE!
```

*English glosses of the retained source comments:*
- Win64: SizeOf(Extended)=10, but prec64=FALSE (SSE2) and round-trip through TExtended80Rec=FALSE!



**Live measurements (`Delphi 13 CE 37.0.60542.8024`, [0.11 pass](../research/COMPILER_PASS_011.md), and `P13`):**

| Probe / mode | `SizeOf` | `Unpacked` / `Packed` `(Byte, Extended, Byte)` | `prec64` (`1+1e-17<>1`) and round-trip |
|---|---|---|---|
| `OFF` `Win32` ([example 50](../../../examples/README.md), `P13_ExtPrecision_Off32`) | `10` | `24 (E:8,B:18)` / `12 (E:1,B:11)` | `prec64=TRUE`, `rt_eq=TRUE` |
| `OFF` `Win64` (`P13_ExtPrecision_Off64`) | `8` | `24 (E:8,B:16)` / `10 (E:1,B:9)` | `prec64=FALSE`, `rt_eq=TRUE` (`8B`) |
| **`ON` `Win32`** (`P13_ExtCompat_Prec_On32`) | `10` | `24 (E:8,B:18)` / `12 (E:1,B:11)` | `prec64=TRUE`, `rt_eq=TRUE` |
| **`ON` `Win64`** (`P2_ExtCompat_On64`, `P13_ExtCompat_Prec_On64`) | **`10`** | **`24 (E:8,B:18)` / `12 (E:1,B:11)`** | **`prec64=FALSE`, `rt_eq=FALSE`** |

**A false analogy:** unlike C `long double` on Linux x86-64, on `Win64` conversion through `Double` loses low mantissa bits (`EXTENDED_TARGET_PROFILE` = `OPEN` for non-Windows targets).

Source: [Embarcadero](https://docwiki.embarcadero.com/RADStudio/Florence/en/Extended_type_compatibility_(Delphi)). Read on 18.11.2026.

Status: cross-checked against the documentation; sizes, field offsets, `prec64=FALSE`, and `rt_eq=FALSE` under `ON` on `Win64` were measured in [example 50](../../../examples/README.md), `P2_ExtCompat_*`, and `P13_ExtCompat_Prec_*`.

## Verification 1.3.0: refined boundaries

**EXTENDED_TARGET_PROFILE — PARTIALLY_RESOLVED.** On ARM32/64, compile-time SizeOf: OFF=8, ON=10, packed record=12, ordinary record=24. This is storage size, not computational precision. DLL producers/consumers with ON/OFF were added on Win32/64, with matching types and a separate lifetime before FreeLibrary.

Scope: Windows DLL probes and compile-only ARM layout; the previous Windows precision/round-trip observations are preserved. Remainder: ARM precision/rounding/runtime ABI requires an Android device or a configured emulator with a harness; Linux/macOS requires the corresponding licensed Delphi compiler, SDK/PAServer, and receiving runtime. Other ABI signatures require a separate producer/consumer rather than SizeOf.


[All 23 results](../research/RESIDUE_23_130.md); [compiler receipt](../../../evidence/compiler/demo-sample-receipts.json).
