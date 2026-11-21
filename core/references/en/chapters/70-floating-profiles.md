# 70. Numeric profile: type, computation, storage, and exception

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

**Demo Sample Tier:** Level 4 — Hardcore Compiler ABI (Extended Win32 80-bit vs Win64 53-bit Asymmetry)


## 1. Why the name `Extended` alone is insufficient

In Object Pascal source text, type `System.Extended` is written the same way on every platform, but at the binary-representation and machine-register levels it splits into different profiles. According to the [System.Extended](https://docwiki.embarcadero.com/Libraries/Florence/en/System.Extended) and [Multi-Device Considerations](https://docwiki.embarcadero.com/RADStudio/Florence/en/Delphi_Considerations_for_Multi-Device_Applications) tables:

| Target platform (CPU / OS) | `SizeOf(Extended)` | Hardware organization and significant boundary |
|---|---|---|
| Intel Win32 (x86) | **10 bytes** | Hardware 80-bit x87 FPU format (1 sign bit + 15 exponent bits + an **explicit** integer bit + 63 fraction bits) |
| Intel Win64 (x64, under `{$EXTENDEDCOMPATIBILITY OFF}`) | **8 bytes** | An alias of IEEE `Double` (`binary64`, 53 significant mantissa bits in SSE2 `XMM` registers) |
| Intel Linux64 / Intel macOS64 | **16 bytes** | An 80-bit x87 value with 6 padding bytes under the System V ABI (**not** IEEE `binary128`!) |
| ARM (Android, iOS, macOS ARM64) | **8 bytes** | An alias of IEEE `Double` (including Apple Silicon ARM64; do not confuse it with an old macOS Intel example lacking a CPU specification) |

## 2. Storage compatibility (`{$EXTENDEDCOMPATIBILITY}`, `TExtended80Rec`) and [`EXTENDED_TARGET_PROFILE`](../SOURCE_ISSUES.md#issue-extended-target-profile)

When porting binary files and records between Win32 and 64-bit targets, strictly distinguish **storage-buffer size** from **the precision of the arithmetic itself**:

- **`{$EXTENDEDCOMPATIBILITY ON|OFF}` ([EXTENDEDCOMPATIBILITY card](../directives/extendedcompatibility.md), default `OFF`):** the local directive on [Extended type compatibility](https://docwiki.embarcadero.com/RADStudio/Florence/en/Extended_type_compatibility_(Delphi)) switches `Extended` to a 10-byte storage format for binary compatibility of structures. On Win64, however, it **does not enable 80-bit x87 arithmetic**: calculations use a 53-bit `Double` mantissa on SSE2!
- **`System.TExtended80Rec` ([TExtended80Rec](https://docwiki.embarcadero.com/Libraries/Florence/en/System.TExtended80Rec)):** a packed 10-byte record (`Words`, `Bytes`, `Frac`, `Exp`, `Sign`), explicitly separating serialization of 80-bit data streams from the current platform's arithmetic type.

### Decisive measurements in series P13 (`P13_ExtCompat_Prec_On32/64` and `P13_ExtPrecision_Off32/64`, `OPEN` for non-Windows)

Series **P13** on `Delphi 13 CE` (`37.0.60542.8024`, `Win32` `0x14c` and `Win64` `0x8664`, Debug, `0` diagnostics; alongside [example 50](../../../examples/README.md)) simultaneously measured `SizeOf`, field offsets in `TUnpacked = record A: Byte; E: Extended; B: Byte; end` and `TPacked = packed record A: Byte; E: Extended; B: Byte; end`, the 64-bit-mantissa test `prec64 = ((1.0 + 1e-17) <> 1.0)`, and the bytewise `round-trip` `Extended -> TExtended80Rec -> Extended`:

| Mode and target | `SizeOf(Extended)` / `TExtended80Rec` | `TUnpacked` (`SizeOf; offE; offB`) | `TPacked` (`SizeOf; offE; offB`) | `prec64` (`1 + 1e-17 <> 1`) | Bytewise `round-trip` (`rt_eq`) |
|---|---|---|---|---|---|
| **Win32** `OFF` and **`ON`** (`P13_ExtCompat_Prec_On32`) | `10` / `10` | `24; offE=8; offB=18` | `12; offE=1; offB=11` | **`TRUE`** (x87 64-bit mantissa) | **`TRUE`** (`0AC264DA3FE0E9F60540`) |
| **Win64** `OFF` (`P13_ExtPrecision_Off64`) | `8` / `10` | `24; offE=8; offB=16` | `10; offE=1; offB=9` | **`FALSE`** (SSE2 `Double`) | `TRUE` (`984CFB073CDD5E40` is already an 8-byte `Double`) |
| **Win64** **`{$EXTENDEDCOMPATIBILITY ON}`** (`P13_ExtCompat_Prec_On64`) | **`10` / `10`** | **`24; offE=8; offB=18`** | **`12; offE=1; offB=11`** | **`FALSE`** (the arithmetic is still `Double`!) | **`FALSE`!** (10 bytes `0AC264DA3FE0E9F60540` are truncated through `Double`!) |

**Key physical conclusion:** on `Win64`, directive `{$EXTENDEDCOMPATIBILITY ON}` exactly restores Win32's 10-byte record-field sizes and offsets (`24 / 8 / 18` and `12 / 1 / 11`), **but any reading or assignment of such a 10-byte `Extended` passes through a 53-bit `Double`**, zeroing the low 11 mantissa bits (`prec64=FALSE`, `rt_eq=FALSE`)! To avoid damaging someone else's 80-bit data when forwarding it on Win64, copy it as raw `TExtended80Rec` without casting to `Extended`. Linux64, macOS64, and ARM behavior remains `OPEN` in [`EXTENDED_TARGET_PROFILE`](../SOURCE_ISSUES.md#issue-extended-target-profile).

## 3. Intermediate precision and historical formats (`{$EXCESSPRECISION}`, `{$REALCOMPATIBILITY}`, `{$SAFEDIVIDE}`)

Even with the same `var A, B, C: Single;` declaration, the result of compound expression `A * B + C` depends on the width of the backend's intermediate registers:
- **On x86 (`Win32`):** real expressions are traditionally computed through the x87 coprocessor's 80-bit stack (`ST(0)..ST(7)`). According to [Floating point precision control (Delphi for x64)](https://docwiki.embarcadero.com/RADStudio/Florence/en/Floating_point_precision_control_(Delphi_for_x64)), directive `{$EXCESSPRECISION}` **has no effect** on 32-bit x86.
- **On x64 (`Win64`):** the compiler uses scalar SSE2 instructions on `XMM` registers. Local directive `{$EXCESSPRECISION ON|OFF}` ([EXCESSPRECISION card](../directives/excessprecision.md), default `ON`), when `ON`, widens intermediate operations on `Single` to `Double` precision; when `OFF`, it keeps them in 32-bit `Single` (without narrowing `Double` variables).
- **Live measurements in series P12 (`Delphi 13 CE 37.0.60542.8024`, `0` diagnostics):**
  - **`{$REALCOMPATIBILITY ON|OFF}` (`P12_RealCompat_OnOff32`):** local switching of the meaning of type `Real` within a single unit was confirmed — under `{$REALCOMPATIBILITY ON}`, type `TR48 = Real` occupies **`6` bytes** (historical 48-bit `Real48`), while after `OFF`, type `TR64 = Real` occupies **`8` bytes** (`Double`, [REALCOMPATIBILITY card](../directives/realcompatibility.md));
  - **`{$EXCESSPRECISION ON|OFF}` (`P12_ExcessPrecision_Win32/64`):** both runs produced `off=1.00000000;on=1.00000000` with `exit=0` (clearly illustrating the computation-layer rule: coarse decimal formatting conceals subtle differences in the low `ULP`);
  - **`{$SAFEDIVIDE ON|OFF}` (`P12_SafeDivide32`):** both branches returned `u_on=4.5;u_off=4.5` (`exit=0`) — the historical `{$U+}`/`{$U-}` option ([SAFEDIVIDE card](../directives/safedivide.md)) only concerned working around the hardware `FDIV` defect in early Pentium processors (1994) and does not protect against division by zero.

## 4. Exception masks (`SetExceptionMask`), the default change in Athens 12, and `FINITEFLOAT_UNDERSPECIFIED`

The processor's response to division by zero (`1.0 / 0.0`), an indeterminate result (`0.0 / 0.0`), and overflow is controlled by masking bits in the hardware **FPU Control Word** (x87) and **MXCSR** (SSE2) registers:
- **Bit masked (included in the mask set):** the hardware interrupt is **suppressed**, and the operation returns a standard IEEE 754 value (`+Infinity`, `-Infinity`, `NaN`).
- **Bit unmasked (excluded from the mask):** the CPU raises a hardware exception, which the RTL maps to `EZeroDivide`, `EInvalidOp`, `EOverflow`, `EUnderflow`.

### The `SetExceptionMask` signature and the historical change in Delphi 12 Athens

Platform-independent mask control is performed through [System.Math.SetExceptionMask](https://docwiki.embarcadero.com/Libraries/Florence/en/System.Math.SetExceptionMask):

```pascal
// Документированная кроссплатформенная сигнатура в System.Math (не полный проект)
function SetExceptionMask(const Mask: TArithmeticExceptionMask): TArithmeticExceptionMask;
```

*English glosses of the retained source comments:*
- Documented cross-platform signature in System.Math (not a complete project)



- **The exact mask type:** the canonical `SetExceptionMask` signature uses type **`TArithmeticExceptionMask`** (`set of TArithmeticExceptions`, 1 byte). Historical name `TFPUExceptionMask` belongs to x87-specific functions: probe `P2_MathMask_Alias32/64` confirmed that their `TypeInfo` values differ (`same_typeinfo=FALSE`), so portable code should declare `TArithmeticExceptionMask`.
- **The default change in Delphi 12 Athens:** in classic Delphi versions (through 11 Alexandria), critical exceptions (`exInvalidOp`, `exZeroDivide`, `exOverflow`) were unmasked by default and threw language exceptions. Starting with **Delphi 12 Athens**, page `SetExceptionMask` records a new default: **all 6 FP-exception masks are enabled (`ON`)**. When changing the mask locally, always restore its previous value in `try ... finally`.

### Open question [`FINITEFLOAT_UNDERSPECIFIED`](../SOURCE_ISSUES.md#issue-finitefloat-underspecified) (`OPEN`)

1. **Documented rule:** the short [Finite float](https://docwiki.embarcadero.com/RADStudio/Florence/en/Finite_float) page declares local directive `{$FINITEFLOAT ON|OFF}` ([FINITEFLOAT card](../directives/finitefloat.md), default `ON`), but **does not specify** the instructions or relationship with `SetExceptionMask`.
2. **Compiler observations (`P2` and `P3` on Delphi 13 CE, Win32 and Win64 Debug):** with ordinary Athens 12+ masked exceptions, division `1.0 / ZeroVar` returned `+Infinity` (`is_inf=TRUE`) **under both `{$FINITEFLOAT ON}` and `OFF`**; after unmasking through `SetExceptionMask([])`, both modes raised `EZeroDivide` (on `1.0 / 0.0`) and `EInvalidOp` (on `0.0 / 0.0`); additionally, `{$IFOPT FINITEFLOAT ON}` was rejected with `E1030`.
3. **Scoped conclusion:** `{$FINITEFLOAT}` cannot be equated with `SetExceptionMask`; the complete cross-platform contract remains `OPEN`.

## 5. Four independent numeric-verification layers and a complete example

When verifying numeric code, four evidence levels never substitute for one another:
1. **Storage / ABI layer:** `SizeOf`, field offsets, and a bytewise `round-trip` through `TExtended80Rec`.
2. **Runtime Arithmetic layer:** preventing compiler constant folding (reading operands from variables) and checking the result bitwise before and after rounding (`FloatToStr` hides low ULP bits).
3. **FP-environment layer (Exception Mask):** recording active `GetExceptionMask` / `SetExceptionMask` immediately before the operation.
4. **Receipt boundary:** a particular measurement confirms only the tested target and option set ([evidence matrix](62-compiler-evidence.md)).

```pascal
program FloatingProfileVerificationDemo;
{$APPTYPE CONSOLE}

uses
  System.SysUtils,
  System.Math;

{$EXCESSPRECISION OFF}
function EvalSingleChain(A, B, C: Single): Single;
begin
  Result := A * B + C;
```


---

### [DEMO EXCERPT BOUNDARY — Level 4 — Hardcore Compiler ABI (Extended Win32 80-bit vs Win64 53-bit Asymmetry)]

Shown above: first ~90 lines out of **147 lines** in the full chapter.

**Complete section outline in the full edition:**
- `## 1. Why the name `Extended` alone is insufficient`
- `## 2. Storage compatibility (`{$EXTENDEDCOMPATIBILITY}`, `TExtended80Rec`) and [`EXTENDED_TARGET_PROFILE`](../SOURCE_ISSUES.md#issue-extended-target-profile)`
- `### Decisive measurements in series P13 (`P13_ExtCompat_Prec_On32/64` and `P13_ExtPrecision_Off32/64`, `OPEN` for non-Windows)`
- `## 3. Intermediate precision and historical formats (`{$EXCESSPRECISION}`, `{$REALCOMPATIBILITY}`, `{$SAFEDIVIDE}`)`
- `## 4. Exception masks (`SetExceptionMask`), the default change in Athens 12, and `FINITEFLOAT_UNDERSPECIFIED``
- `### The `SetExceptionMask` signature and the historical change in Delphi 12 Athens`
- `### Open question [`FINITEFLOAT_UNDERSPECIFIED`](../SOURCE_ISSUES.md#issue-finitefloat-underspecified) (`OPEN`)`
- `## 5. Four independent numeric-verification layers and a complete example`
- `## 6. Protection against false analogies and primary sources`
- `### Primary sources and verification status`
- `## Verification 1.3.0: refined boundaries`
- `### FINITEFLOAT_UNDERSPECIFIED`
- `### EXTENDED_TARGET_PROFILE`

To inspect the complete chapter, verified runnable program, counterexamples and compiler receipts, use the full edition (`https://silentfish.dev/delphi`).
