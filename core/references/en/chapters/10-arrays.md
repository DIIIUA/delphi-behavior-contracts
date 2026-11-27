# 10. Static, dynamic, and open arrays

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.2** (full corpus: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you can inspect coverage and test the offline workflow on your own Delphi tasks. Project page: https://silentfish.dev/delphi

**Demo Sample Tier:** Level 1 — Basic / Everyday Trap (Dynamic Arrays, Aliasing vs Detachment)


## 1. Three distinct mechanisms behind the keyword `array`

In Object Pascal, the keyword `array` represents three fundamentally different mechanisms with different memory placement, type identity, and calling conventions (ABI). Two of them use the same notation `array of T`, whose meaning is determined entirely by its syntactic position ([Structured Types](https://docwiki.embarcadero.com/RADStudio/Florence/en/Structured_Types_(Delphi)), [Parameters](https://docwiki.embarcadero.com/RADStudio/Florence/en/Parameters_(Delphi))):

| Construct | Where written | Memory and descriptor | Indices and `SizeOf` | Behavior on `:=` and passing |
|---|---|---|---|---|
| **Static array** (`array[Low..High] of T`) | Type, field, or variable declaration | A contiguous inline block of values (stack, data segment, record); no header | Any ordinal range `Low..High`; `SizeOf = Count * SizeOf(T)` | A complete copy of every element (by value) |
| **Dynamic array** (`array of T`) | Type, field, or variable declaration | A pointer to `[0]` on the heap (`nil` at length `0`); a header at negative offsets, `(refCount, length)` | Always `0..Length - 1`; `SizeOf(Var) = SizeOf(Pointer)` (`4`/`8` bytes) | One shared buffer (`refCount`), **without Copy-on-Write on element writes** |
| **Open array** (`array of T`, `array of const`) | **Only** in a formal parameter declaration | At the ABI level, a pair `(PtrToFirst, HighIndex)` without a heap descriptor | Always rebased within the call to **`0..High(Param)`** | Depends on `value` / `const` / `var`; calling `SetLength` is forbidden |

## 2. Syntax, nominal identity, and the formal-parameter trap

```pascal
// Фрагмент грамматики массивов и параметров (не полный проект)
type
  TWeekHours = array[1..7] of Integer;             // статический 1-индексный массив
  TGrid2x3   = array[0..1, 0..2] of Double;        // прямоугольный статический блок
  TNumbers   = array of Integer;                   // именованный динамический массив
  TJagged    = array of array of Integer;          // зубчатый динамический массив

procedure UseDynamic(const A: TNumbers);           // принимает ТОЛЬКО TNumbers (или nil)
procedure UseOpen(const A: array of Integer);      // открытый массив: примет TWeekHours, TNumbers, [1, 2], Slice(...)
procedure UseVarArgs(const Args: array of const);  // вариантный открытый массив (array of TVarRec)
```

*English glosses of the retained source comments:*
- Array and parameter grammar fragment (not a complete project)
- static array indexed from 1
- rectangular static block
- named dynamic array
- jagged dynamic array
- accepts ONLY TNumbers (or nil)
- open array: accepts TWeekHours, TNumbers, [1, 2], Slice(...)
- variant open array (array of TVarRec)



**Two critical typing boundaries:**
1. **`P(A: TNumbers)` is not equivalent to `P(A: array of Integer)`:** the first parameter requires the specific dynamic type `TNumbers` (allows `nil`, and without `const` passes the descriptor with an increment to `refCount` without copying elements); the second is an open array accepting any static or dynamic array of the same element type, a slice `Slice(Arr, Count)`, and a constructor `[10, 20]`, rebasing indices within the procedure body to `0..High(A)`.
2. **Incompatibility of anonymous arrays for `var`/`out`:** two separate declarations `var A: array[0..3] of Integer;` and `var B: array[0..3] of Integer;` create different anonymous types, incompatible with a named `var` parameter (`E2033`). Always declare a shared named type in the `type` section for passing by reference.

## 3. Dynamic-array memory, absence of COW, depth of `Copy`, and open parameters

### Heap descriptor, aliasing, and `SetLength`

Under the [Internal Data Formats](https://docwiki.embarcadero.com/RADStudio/Florence/en/Internal_Data_Formats_(Delphi)) rules, a dynamic-array variable occupies `4` bytes on 32-bit and `8` bytes on 64-bit platforms (`nil` corresponds to an empty array of length `0`). Before element `[0]` on the heap lies a header with reference count `refCount` and length `length` (widened to the platform width on 64-bit targets):
- **No Copy-on-Write for elements:** assignment `B := A` increments `refCount`, after which writing `B[0] := 9` **immediately changes `A[0]`**, because both variables refer to one buffer!
- **Making a buffer unique through `SetLength` ([System.SetLength](https://docwiki.embarcadero.com/Libraries/Florence/en/System.SetLength)):** a call to `SetLength(B, NewLen)` — including `SetLength(B, Length(B))` with the previous length — guarantees `refCount = 1`: if the buffer was shared (`refCount > 1`), a new block is allocated and the elements are copied, isolating `B` from `A` (confirmed by [example 01](../../../examples/01-array-alias.dpr), `OBSERVED_PASS` on Delphi 13 Win32 Debug: output `9`, `9`, `12`). New cells are zeroed on extension (`Default(T)`), and discarded cells are finalized on truncation.

### The shallowness of `Copy` and multidimensional arrays

- **`Copy(A)` / `Copy(A, Index, Count)`:** creates a new outer dynamic array, but performs a **shallow copy** of the elements. If the elements are references to `class` instances, interfaces, or nested dynamic arrays (`TJagged`), the inner rows and objects remain shared between `A` and the copy!
- **Rectangular versus jagged arrays:** static `array[0..1, 0..2] of Double` is one contiguous memory block (row-major); dynamic `array of array of Integer` is an array of pointers to independent one-dimensional heap arrays, where each row may have its own length or be `nil`.

### Dynamic-array operations (XE7+): `Insert`, `Delete`, `Concat`, operator `+`, `Copy`, and aliasing vs detachment

Starting with the **Delphi XE7+** line, dynamic arrays gained built-in concatenation and structural-modification operations without manual `Move` and `SetLength` loops. The dual-architecture probes **`P15_DynArray_Ops32`** (`Win32`, `pe=0x14c`, `0` diagnostics, `run_exit = 0`) and **`P15_DynArray_Ops64`** (`Win64`, `pe=0x8664`, `0` diagnostics, `run_exit = 0`) verified every operation and the exact boundary between buffer sharing (*aliasing*) and detaching a copy (*detachment*):

```pascal
// Иллюстративный фрагмент (проверено в P15_DynArray_Ops32 / P15_DynArray_Ops64)
A := [1, 2, 3];
B := [4, 5];
C := A + B;                  // C_plus=[1,2,3,4,5]
D := Concat(A, B, [6]);      // D_concat=[1,2,3,4,5,6]
Insert(99, C, 1);            // C_ins1=[1,99,2,3,4,5] — вставка одного элемента по 0-индексу
Insert([77, 88], C, 0);      // C_ins_sub=[77,88,1,99,2,3,4,5] — вставка подмассива
Delete(C, 2, 2);             // C_del=[77,88,2,3,4,5] — удаление 2 элементов с индекса 2
E := Copy(C, 1, 3);          // E_copy=[88,2,3] — срез 3 элементов с индекса 1
```

*English glosses of the retained source comments:*
- Illustrative fragment (tested in P15_DynArray_Ops32 / P15_DynArray_Ops64)
- C_ins1=[1,99,2,3,4,5] — inserting one element using 0-based indexing
- C_ins_sub=[77,88,1,99,2,3,4,5] — inserting a subarray
- C_del=[77,88,2,3,4,5] — deleting 2 elements starting at index 2
- E_copy=[88,2,3] — a slice of 3 elements starting at index 1



| Operation on an alias (`Alias* := A`, where `A = [10, 2, 3]`, `refCount > 1`) | Does it change the original `A`? | Measured `stdout` in `P15_DynArray_Ops32` / `64` |
|---|---|---|
| Element write `Alias[0] := 10` (on original `[1, 2, 3]`) | **Yes** (writes to the shared buffer) | `A_after_alias=[10,2,3]` |
| Insertion `Insert(55, Alias2, 0)` | **No** (detaches a new copy) | `A_after_insert=[10,2,3];Alias2=[55,10,2,3]` |
| Deletion `Delete(Alias3, 0, 1)` | **No** (detaches a new copy) | `A_after_delete=[10,2,3];Alias3=[2,3]` |
| Length change `SetLength(Alias4, 5)` | **No** (detaches a new copy) | `A_after_setlength=[10,2,3];Alias4_len=5` |

The fundamental conclusion from these probes: indexed writing `Alias[I] := X` changes the shared buffer in place. In the tested structure/size-changing calls (`Insert`, `Delete`, `SetLength`) under `refCount > 1`, the target variable's buffer becomes unique (*detachment*); other variables continue to reference the former buffer. These observations do not establish behavior for all arguments, including no-op operations.

### Cost and limitations of open arrays (`value` / `const` / `var`)

- **An open array by value (`procedure P(A: array of Integer)`):** on procedure entry, the compiler allocates a local buffer and **copies every element** of the supplied sequence (freeing the copy on exit); for large arrays, this creates hidden overhead (while objects within the elements are still not cloned).
- **By `const` (`const A: array of Integer`):** no element copy is made — only the pair `(Ptr, High)` is passed, and writing to `A[i]` is forbidden by the compiler (but the array's contents are not protected against modification through an external alias).
- **By `var` (`var A: array of Integer`):** directly mutates the caller's original array; passing temporary constructor `[1, 2]` to a `var` parameter is forbidden and rejected with error `E2197` (confirmed by [negative pair 06](../../../examples/README.md) on Delphi 13 Win32 Debug).

---

### [DEMO EXCERPT BOUNDARY — Level 1 — Basic / Everyday Trap (Dynamic Arrays, Aliasing vs Detachment)]

Shown above: first ~95 lines out of **181 lines** in the full chapter.

**Complete section outline in the full edition:**
- `## 1. Three distinct mechanisms behind the keyword `array``
- `## 2. Syntax, nominal identity, and the formal-parameter trap`
- `## 3. Dynamic-array memory, absence of COW, depth of `Copy`, and open parameters`
- `### Heap descriptor, aliasing, and `SetLength``
- `### The shallowness of `Copy` and multidimensional arrays`
- `### Dynamic-array operations (XE7+): `Insert`, `Delete`, `Concat`, operator `+`, `Copy`, and aliasing vs detachment`
- `### Cost and limitations of open arrays (`value` / `const` / `var`)`
- `## 4. `array of const` and the mechanics of `TVarRec``
- `## 5. A self-contained example`
- `## 6. Version boundaries, open observations, and protection against false analogies`
- `### Historical evolution and the `GENERIC_ARGUMENT_DOC_COUNTEREXAMPLE` observation`
- `### Protection against false analogies`
- `## 7. Primary sources and verification status`

To inspect the complete chapter, verified runnable program, counterexamples and compiler receipts, use the full edition (`https://silentfish.dev/delphi`).
