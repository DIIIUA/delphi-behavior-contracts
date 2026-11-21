# Final compiler pass 1.1.0 (Series P15)

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi


20 November 2026. **Delphi 13 Community Edition (`IDE 37.0.60542.8024`, Windows `Win32`/`Win64 Debug`) through `MCP2Delphi`.**

The historical 1.1.0 report described series **`P15`** as closing the remaining language coverage gap. Revision 1.2.0 withdraws the percentage estimate: the number of builds does not measure language completeness. The report states **`41` live builds** (bringing the total for series `P1–P15` to exactly **`400` working builds**), of which **`35` portable text probes** are cryptographically bound to the receipt [`20261120-followup-110.json`](../../../evidence/compiler/demo-sample-receipts.json) and the catalog [`examples/probes/compiler-110/`](../../../examples/README.md).

## Principal empirical results of Series `P15`

1. **Compile-time metatyping intrinsics (`GetTypeKind`, `IsManagedType`, `HasWeakRef`):**
   - `P15_Intrinsics_TypeMeta32_V2` / `P15_Intrinsics_TypeMeta64_V2` (`Win32`/`Win64`, `0` diagnostics, `exit=0`): a unified 18-type table — including `TManagedRec` (`class operator Initialize/Finalize`), which gives **`tkMRecord` / `Managed=True`**; `TWeakIntfRec` (`[weak] F: IInterface`) gives `tkRecord` / `Managed=True`; **`TUnsafeIntfRec` (`[unsafe] F: IInterface`) gives `tkRecord` / `Managed=False`**; `TProc` (`reference to procedure`) gives `tkInterface` / `Managed=True`; `TMethod` gives `tkRecord` / `Managed=False`.
   - **Corrected in 1.2.0:** do not use the following earlier conclusion as an intrinsic rule; see the [independent pass](COMPILER_PASS_120.md) and [Chapter 31](../chapters/31-generics.md). The historical claim was: for `HasWeakRef(T)` on an unconstrained `T` (`P15_Intrinsics_TypeMeta32` / `64`), the compiler emits **`E2571 Type parameter 'T' doesn't have class or interface constraint`**, but contrary to the literal diagnostic text, BOTH `T: class` (`P15_HasWeakRef_GenClass32` -> `False` on non-ARC Windows) AND **`T: record`** (`P15_HasWeakRef_GenRec32`: `GenRec_Weak=True`, `GenRec_Plain=False`) compile cleanly in `Delphi 13 CE`. For concrete types, `P15_HasWeakRef_RecWeak32` confirmed `TWeakIntfRec=True`, `TUnsafeIntfRec=False`, whereas for classes `THolder = class [weak] W: IInterface; end;` (`P15_HasWeakRef_ClassIntf32`), the result is `False`.

2. **`IsConstValue(Expr)` and the subroutine scope of `{$INLINE OFF}`:**
   - `P15_IsConstValue_Inline32_V2` / `P15_IsConstValue_Inline64_V2`: inside an `inline` function, literal `42`, `const C = 10`, and `C + 5` give `TRUE`, whereas **typed constants (`{$J-} TC_RO` and `{$J+} TC_RW`)**, runtime variables, and the non-`inline` call (`ProbeNoInline(42)`) give `FALSE`.
   - `P15_IsConstValue_CallOff32`: direct proof of the subroutine scope of `{$INLINE OFF}` — the directive before the `CallWithInlineOff` header disables inlining (`calloff_lit=FALSE`), whereas `{$PUSHOPT}{$INLINE OFF}` inside an already opened `begin..end` does not disable inlining (`inloff_inline_body=TRUE`).

3. **Low-level `raise ... at ReturnAddress` and runtime hooks (`ExceptProc`, `ErrorProc`, `AssertErrorProc`):**
   - `P15_Raise_At_ReturnAddr32` / `P15_Raise_At_ReturnAddr64`: with `{$INLINE OFF}` on wrapper `FailAtCaller`, address `ExceptAddr` moves into the calling procedure `RunTest` (`diff=TRUE`, `caller_near_run=TRUE`).
   - `P15_RuntimeHooks_AssertError32` / `P15_RuntimeHooks_AssertError64`: referencing `System.SysUtils` initializes all three pointers (`has_ExceptProc=TRUE`, `has_ErrorProc=TRUE`, `has_AssertErrorProc=TRUE`); temporarily replacing `AssertErrorProc` and restoring it in `try..finally` intercepts `Assert(False, 'custom_trap')` with a nonzero address and line number, and after restoration the standard `EAssertionFailed` fires.

4. **Generic methods in nongeneric classes and the polymorphism restriction:**
   - `P15_GenericMethods_NonGenClass32` / `P15_GenericMethods_NonGenClass64`: `Swap<T>`, multiparameter `PairKinds<T1, T2>`, local constraint `SizeOfRec<T: record>`, instance `Echo<T>`, and overload priority (`Pick(10)` -> `NonGenInt:10`, explicit `Pick<Integer>(10)` -> `Gen<tkInteger>`, type inference `Pick('hi')` -> `Gen<tkUString>`).

---

*(Full research pass report is included in the full edition.)*
