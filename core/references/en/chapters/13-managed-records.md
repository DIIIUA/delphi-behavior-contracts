# 13. Custom managed records

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi

**Demo Sample Tier:** Level 2 — Intermediate (Managed Records Initialize/Finalize/Assign)


## 1. Two levels of record management: from automatic fields to CMR

In the Delphi memory model ([Memory Management](https://docwiki.embarcadero.com/RADStudio/Florence/en/Memory_Management), [Custom Managed Records](https://docwiki.embarcadero.com/RADStudio/Florence/en/Custom_Managed_Records)), the compiler manages the lifetime of a record (`record`) at two levels:

1. **An automatically managed record (a record with built-in managed fields):** as soon as an ordinary `record` includes at least one field of type `string`, a dynamic array, `IInterface`, `Variant`, or a nested managed record, the compiler creates an RTTI table of managed-field offsets for it and automatically inserts calls to RTL procedures (`_InitializeRecord`, `_FinalizeRecord`, `_CopyRecord`), wrapping the variable’s lifetime in a hidden `try ... finally` block.
2. **Custom Managed Records (CMR, introduced in Delphi 10.4 Sydney):** allow the developer to declare custom lifecycle hooks — `class operator Initialize`, `Finalize`, and `Assign`. This turns the record into a deterministic lifetime container (for OS handles, unmanaged buffers, locks, state logs), integrated directly into code generation for prologues, epilogues, arrays, and exception unwinding.

## 2. Operator syntax: the classic 10.4+ form and implicit `Self` in Delphi 13

### Full signatures (Delphi 10.4 Sydney+)

```pascal
// Фрагмент объявления CMR в стиле 10.4+ (проверенные проекты — examples/19, 37, 39, 47)
type
  TManagedResource = record
  strict private
    FRawHandle: Pointer;
  public
    class operator Initialize(out Dest: TManagedResource);
    class operator Finalize(var Dest: TManagedResource);
    class operator Assign(var Dest: TManagedResource; const [ref] Src: TManagedResource);
  end;
```

*English glosses of the retained source comments:*
- 10.4+ style CMR declaration fragment (verified projects: examples/19, 37, 39, 47)



The compiler’s signature requirements are strict:
- **`Initialize(out Dest: TRec)`:** must take exactly one `out` parameter of the record’s own type. The `out` modifier emphasizes that on entry, the scalar fields of `Dest` contain **uninitialized stack/heap bytes** (the compiler zero-initializes nested automatically managed fields before entering user code).
- **`Finalize(var Dest: TRec)`:** takes one `var` parameter of the record type; called when leaving scope, unwinding an exception, destroying the containing object/array, or during unit `finalization`.
- **`Assign(var Dest: TRec; const [ref] Src: TRec)`:** intercepts `Dest := Src` copying (unlike the `Implicit`/`Explicit` type-cast operators discussed in [chapter 33](33-operators.md)). The second parameter must have the **`const [ref]`** qualifier; otherwise, passing `Src` by value would cause infinite recursive `Assign` calls!

### Abbreviated syntax with implicit `Self` (Delphi 13 Florence+)

Starting with **Delphi 13.0 Florence** ([What's New](https://docwiki.embarcadero.com/RADStudio/Florence/en/What%27s_New)), declarations of `Initialize` and `Finalize` may omit the formal `Dest` parameter; inside the operator body, the record instance is available through implicit `Self`:

```pascal
// Синтаксис Delphi 13+ (полный проверенный проект — examples/38-managed-implicit-self.dpr)
type
  TObserved = record
    Value: Integer;
    class operator Initialize;
    class operator Finalize;
  end;
```

*English glosses of the retained source comments:*
- Delphi 13+ syntax (the full verified project is examples/38-managed-implicit-self.dpr)



The abbreviated form is confirmed by [example 38](../../../examples/README.md) (`OBSERVED_PASS` on Delphi 13 Win32 Debug: `7`, `final`, `end`), while the full 10.4+ form remains fully functional ([examples 19, 37, 39, 47](../../../examples/README.md)) and is required if the code must compile in Delphi 10.4–12.

## 3. Hidden call sites, `Assign` invariants, and parameter passing

### Where the compiler calls CMR operators and why copies must not be counted

- **Local `var` versus `inline var`:** an ordinary local variable is initialized in the subroutine prologue and finalized on exit ([example 19](../../../examples/19-managed-record.dpr), `OBSERVED_PASS`: `5`, `1`); a block-scoped `inline var R: TRec` is initialized at its declaration point within a nested `begin ... end` and finalized on leaving that block ([chapter 16](16-variables.md)).
- **Arrays, objects, and the heap:** when a class is created or an array is extended with `SetLength`, `Initialize` is called for each element; on destruction/shrinking, `Finalize` is called (if an exception occurs while initializing the `K`th array element, only the successfully created `0..K-1` elements will be finalized). For manual heap storage, `New(P)` and `Dispose(P)` automatically call `Initialize`/`Finalize`, whereas raw `GetMem`/`FreeMem` **ignore** them and require explicit [System.Initialize](https://docwiki.embarcadero.com/Libraries/Florence/en/System.Initialize) / `System.Finalize` ([chapter 14](14-pointers.md)).
- **Do not rely on the exact number of copies:** returning a function through `Result`, passing temporary expressions, and optimizations (copy elision) may change the number of `Initialize`/`Assign`/`Finalize` calls between versions and platforms. Ownership logic must rely on correct reference counting or ownership transfer, rather than an expected fixed call count.

### Two mandatory protections inside `Assign`

On entry into `Assign(var Dest; const [ref] Src)`, the `Dest` variable **is already initialized** and may own an active resource. Therefore, any resource-handling implementation of `Assign` must:
1. **Guard against self-assignment (`A := A`):** first check `if @Dest = @Src then Exit;` (otherwise, releasing the old `Dest` resource will destroy the `Src` source!). [Example 39](../../../examples/README.md) (`OBSERVED_PASS`: `9`, `9`) shows this address check on a scalar field, but a real handle or buffer requires the second step as well;
2. **Release the previous `Dest` resource** (or decrement its reference count) before writing the new resource from `Src`; otherwise, the previous handle will leak.

### Parameter-passing matrix (confirmed by [example 47](../../../examples/README.md))

| Parameter declaration | Lifetime and copying behavior |
|---|---|
| `ByValue(R: TRec)` | A separate local copy is created (`Initialize` + `Assign` or copying), finalized on leaving `ByValue`; the caller’s original does not change |
| `ByVar(var R: TRec)` | A direct reference to the existing instance is passed without `Initialize`/`Assign`/`Finalize` |
| `ByConstRef(const [ref] R: TRec)` | Guarantees read-only passing by reference without creating a temporary copy or calling `Assign` |
| `ByConst(const R: TRec)` | Passed without a copy in the CMR documentation examples, but in the general ABI, `const` without `[ref]` depends on size/platform; for predictably avoiding copying with CMR, `const [ref]` is preferable |

## 4. The critical failure contract: an exception inside `Initialize`

Under the official [Custom Managed Records](https://docwiki.embarcadero.com/RADStudio/Florence/en/Custom_Managed_Records) contract, confirmed by a live run of [example 37](../../../examples/README.md) (`OBSERVED_PASS` on Delphi 13 Win32 Debug: output `caught` and `FinalizeCount = 0`):

> **If the user-defined `class operator Initialize` raises an exception, the paired `class operator Finalize` is NOT called for that record!**

---

### [DEMO EXCERPT BOUNDARY — Level 2 — Intermediate (Managed Records Initialize/Finalize/Assign)]

Shown above: first ~85 lines out of **170 lines** in the full chapter.

**Complete section outline in the full edition:**
- `## 1. Two levels of record management: from automatic fields to CMR`
- `## 2. Operator syntax: the classic 10.4+ form and implicit `Self` in Delphi 13`
- `### Full signatures (Delphi 10.4 Sydney+)`
- `### Abbreviated syntax with implicit `Self` (Delphi 13 Florence+)`
- `## 3. Hidden call sites, `Assign` invariants, and parameter passing`
- `### Where the compiler calls CMR operators and why copies must not be counted`
- `### Two mandatory protections inside `Assign``
- `### Parameter-passing matrix (confirmed by [example 47](../../../examples/README.md))`
- `## 4. The critical failure contract: an exception inside `Initialize``
- `## 5. C++ (`.hpp`) and generics (`RECORD_CONSTRAINT_MANAGED_BOUNDARY`) boundaries`
- `## 6. A self-contained example`
- `## 7. Protection against false analogies and primary sources`
- `### Primary sources and confirmation status`

To inspect the complete chapter, verified runnable program, counterexamples and compiler receipts, use the full edition (`https://silentfish.dev/delphi`).
