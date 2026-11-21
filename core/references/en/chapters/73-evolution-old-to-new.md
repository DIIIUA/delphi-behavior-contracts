# 73. From old to new: the underlying logic of Delphi language evolution

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

**Demo Sample Tier:** Level 4 — Architectural Synthesis (Six Historical Strata: Turbo Pascal to Delphi 13)


At first acquaintance, modern `Delphi 13 Florence` may seem a paradoxical fusion of distant eras: the same `.pas` unit compiles, side by side, `ShortString` and the stack-based `object` from the MS-DOS era, heap-allocated `TObject` classes with VMT tables and `IInterface` COM interfaces, monomorphized `Generics<T>` generics, `reference to` closures, deterministic managed records with implicit `Self`, and lazy `if..then..else` conditional expressions. Behind this diversity lies a strict **cause-and-effect logic**, rather than an accidental accumulation of syntax: the physical and architectural constraints of each stratum inevitably gave rise to the next mechanism, while industrial continuity requirements kept all preceding strata within a single compiler (`dcc32`/`dcc64` `37.0`).

---

## 1. Six language strata: from a physical limit to a new solution

### Stratum I. The static foundation `Wirth Pascal -> Turbo / Borland Pascal 1–7`

- **The era's initial constraint:** single-pass compilation on weak machines, segmented 8086 addressing, and the hard DOS RAM ceiling (`640 KB`) without a protected virtual address space. Every construct had to have a compile-time-known `SizeOf` size and operate without a hidden heap manager.
- **The physical and grammatical response:**
  - **`ShortString` (`string[N]`):** a flat array of `1 + N` bytes directly on the stack or inside a structure, where byte `S[0]` stores the current length `0..255` (`O(1)` length reading, but a ceiling of `255` bytes and full buffer copying when passed by value — [chapter 09](09-strings.md));
  - **6-byte software `Real48`** for machines without a coprocessor, and hardware 80-bit `Extended` and 64-bit integer `Comp` for x87 ([chapter 07](07-reals.md));
  - **`set of` bitsets** with a fixed width of up to `256` elements (`32` bytes — [chapter 11](11-sets.md)) and flat `record` records with variant field overlays `case .. of`;
  - **stack-based `object` (`TP 5.5`):** a polymorphic value structure whose hidden VMT pointer lies inside the instance itself and must be initialized manually by calling `constructor`, along with 1-word procedural pointers and segmented-memory facilities `near`/`far`, `Mem`/`Port`, `inline($...)`.
- **Why stratum I reached its limit:** passing or assigning an `object` descendant to a base-type variable by value caused physical **object slicing**, cutting off the descendant's fields; the absence of a common hierarchy root and metadata prevented building a visual Windows component environment and form streaming, while the `255`-character limit blocked work with real texts.



### Stratum II. The classic RAD era, heap VMT, and COM (`Delphi 1–7`, `1995–2002`)

- **The era's initial constraint:** the move to event-driven Windows GUIs, component-based `.dfm` form construction, and binary interaction between system modules required reference polymorphism without slicing, long strings, and cross-language contracts.
- **The physical and grammatical response:**
  - **splitting the old `object` into value-based `record` and heap-based `class(TObject)`:** a class variable became a 1-word heap pointer; `TObject.InitInstance` guarantees zeroing memory before entering the constructor; a bidirectional table with negative offsets grew around the VMT pointer (RTTI, class name, `InstanceSize`, parent), type `class of` made a metaclass a first-class value with virtual constructors, and the `published` section under `{$M+}` provided the basis for `.dfm` serialization ([chapters 24–28](24-classes.md));
  - **2-word method pointer `TMethod` (`of object` = `Code + Data`):** linked a handler's code address to a particular receiver `Self` without owning the object's lifetime ([chapter 22](22-callables.md));
  - **heap-based `AnsiString` (Delphi 2):** a negative-offset header with reference count `refCount` and length + *copy-on-write* semantics (`UniqueString`) removed the `255`-byte barrier while preserving the illusion of a value type;
  - **dynamic array `array of T` (Delphi 4):** the same negative-offset header with `refCount` and a heap length, but **without *copy-on-write*** — writing to `B[0]` after `B := A` changes the shared buffer (the main source of false analogies with strings, [chapter 10](10-arrays.md));
  - **`Variant` / `OleVariant` and COM interfaces `IInterface` (Delphi 3):** automatic reference counting through `_AddRef`/`_Release`, interface method tables (IMT) at offsets inside the object, and `ADJUSTOR` thunks that shift the interface pointer back to the beginning of `TObject` ([chapter 29](29-interfaces.md)).
- **Why stratum II reached its limit:** single-byte `AnsiString` depended on the Windows system code page and lost characters between locales; collections such as `TList` were built on untyped `Pointer` values; 2-word `TMethod` could not capture local variables of the calling procedure; classic RTTI saw only the `published` section, and manual `Create`/`Free` of classes required `try..finally` discipline.

### Stratum III. Unicode, monomorphized Generics, closures, and extended RTTI (`Delphi 2005–2010`)

- **The era's initial constraint:** software globalization, a need for strongly typed containers at native speed, asynchronous callbacks with context capture, and universal reflection.
- **The physical and grammatical response:**
  - **the `string -> UnicodeString` transition (UTF-16LE, Delphi 2009):** extending the string header with `codePage` and `elemSize` fields (`12` bytes on `Win32`, `16` bytes on `Win64`), literals in the constant segment with `refCount = -1`, code-page-specific `AnsiString(CP)`, and transport type `RawByteString` ([String Types](https://docwiki.embarcadero.com/RADStudio/Florence/en/String_Types_(Delphi)));
  - **`Generics<T>` monomorphization** (following the preparatory step of `advanced record` with methods and `class operator` in 2006): for each closed specialization (`TMonoBox<Integer>`, `TMonoBox<string>`), the compiler generates **separate machine code, its own VMT, and independent `class var` fields** — the direct opposite of Java's *type erasure* ([Declaring Generics](https://docwiki.embarcadero.com/RADStudio/Florence/en/Declaring_Generics), [chapter 31](31-generics.md));
  - **anonymous methods `reference to`:** because a procedure's stack is destroyed on return, the compiler lowers a closure into a hidden heap object with a COM-interface reference count and moves captured local *variables* (rather than copies of them!) into a shared heap capture frame ([Anonymous Methods](https://docwiki.embarcadero.com/RADStudio/Florence/en/Anonymous_Methods_in_Delphi), [chapter 23](23-closures.md));
  - **extended RTTI (`System.Rtti`, Delphi 2010):** universal container `TValue`, custom attributes `[CustomAttribute]`, control of table emission through `{$RTTI EXPLICIT}` ([chapter 36](36-rtti.md)), and direct recovery of an instance through `Intf as TObject`.
- **Why stratum III reached its limit:** the entire binary foundation was still designed around 32-bit `Win32` (`SizeOf(Pointer) = 4`, 10-byte x87 `Extended`, stack exception chain `FS:[0]`), creating a barrier to moving onto 64-bit servers and mobile ARM processors.

### Stratum IV. Multi-target ABI and the architectural lesson of mobile ARC (`XE2–10.3`)

- **The era's initial constraint:** porting the language to `Win64`, `macOS`, `iOS`, `Android`, and `Linux64` with different register conventions, address widths, and hardware stack-unwinding rules.
- **The physical and grammatical response:**
  - introducing `Unit Scope Names` (`System.SysUtils`), pointer-width types `NativeInt`/`NativeUInt`, moving to `SizeOf(Pointer) = 8`, expanding **`TMethod` (`8 -> 16` bytes)** and **`TVarData` (`16 -> 24` bytes)**, platform-dependent splitting of **`Extended`** (`10` bytes on `Win32`, `8`-byte `Double` on `Win64`/`ARM`, `16` bytes on `Linux64` — [chapter 70](70-floating-profiles.md)), and replacing `FS:[0]` stack frames with table-based **`PC-Mapped` exception unwinding** ([PC-Mapped Exceptions](https://docwiki.embarcadero.com/RADStudio/Florence/en/PC-Mapped_Exceptions));
  - attempting to adopt the mobile memory model in **`XE4–10.3` through ARC for `TObject`** on iOS/Android/Linux: each object acquired `FRefCount`, breaking cycles required `[Weak]` (zeroed through a global registry) or `[Unsafe]`, and forced resource cleanup used `DisposeOf`, putting the object into a partially destroyed *zombie state*.
- **Why stratum IV caused a reversal:** living with two incompatible memory models for the same `class` (`Free` on Windows versus ARC and `DisposeOf` on mobile targets) split libraries' common source code and undermined destructor predictability.

### Stratum V. Memory unification and deterministic stack-based RAII (`10.3 Rio – 10.4 Sydney`)

- **The era's initial constraint:** the desktop/mobile split had to be removed while giving the language lightweight deterministic RAII without heap allocations or cumbersome cascades of `try..finally`.
- **The physical and grammatical response:**
  - **block-local `var` declarations (`10.3 Rio`):** the *inline variable declaration* mechanism (written as `var X := ...` or `for var I := ...` **without** the word `inline` in code!) narrowed the scope and lifetime of managed variables to a specific `begin..end` block or a single loop iteration ([Inline Variable Declaration](https://docwiki.embarcadero.com/RADStudio/Florence/en/Inline_Variable_Declaration));
  - **unification of the class model (`10.4 Sydney`):** removing ARC from `TObject` on all platforms (the same classic ownership through `Free` / `Owner` everywhere), while retaining reference counting and `[weak]`/`[unsafe]` attributes for interfaces ([Memory Management](https://docwiki.embarcadero.com/RADStudio/Florence/en/Memory_Management));
  - **Custom Managed Records (`10.4 Sydney`):** operators `class operator Initialize`, `Finalize`, `Assign`, and `const [ref]` parameter passing brought automatic deterministic RAII directly onto the stack and into arrays — with a fundamental failure asymmetry: an exception inside `TObject.Create` automatically calls `Destroy`, whereas an exception inside `CMR.Initialize` **does not call `Finalize`** ([Custom Managed Records](https://docwiki.embarcadero.com/RADStudio/Florence/en/Custom_Managed_Records), [chapter 13](13-managed-records.md), [chapter 68](68-lifetime-boundaries.md)).

### Stratum VI. Hardware realism of FP masks and semantic precision (`11 Alexandria – 13 Florence`)

- **The era's initial constraint:** unmasked FPU exceptions conflicting with external C/C++/SIMD libraries, inconvenient multiline templates, excessive temporary variables in branching, and fragile string literals during refactoring and local directive switching.
- **The physical and grammatical response:**
  - **`11 Alexandria`:** binary literals `%` and digit separators `_` for self-documenting bit masks;
  - **`12 Athens`:** enabling all six FP-exception masks by default in the RTL (`SetExceptionMask`, returning IEEE values `+Infinity`/`NaN` instead of a failing `EZeroDivide` — [12 Athens Release 3](https://docwiki.embarcadero.com/RADStudio/Florence/en/12_Athens_-_Release_3), [chapter 70](70-floating-profiles.md)), and multiline literals `'''` with the [TEXTBLOCK](../directives/textblock.md) line-ending profile;
  - **`13 Florence` (`CompilerVersion = 37.0`):** lazy conditional expression `if..then..else` (evaluating only the selected branch), operators `is not` and `not in` ([Conditional Operators](https://docwiki.embarcadero.com/RADStudio/Florence/en/Conditional_Operators_(Delphi))), directive `noreturn` in the control-flow graph to prevent spurious `W1035` ([chapter 20](20-routines.md)), expression `NameOf(...)` resolved at the symbol-table phase before analysis of unused assignments `H2077` ([chapter 67](67-nameof.md)), concise CMR operator syntax with **implicit `Self`** (`class operator Initialize;` / `Finalize;`), strict generic constraints `: interface` and `: unmanaged` (the latter rejecting any managed fields and CMR with `E2668` — [chapter 32](32-constraints.md)), full option-stack restoration `{$PUSHOPT}`/`{$POPOPT}`, and long `{$IFOPT}` predicates ([What's New (Florence)](https://docwiki.embarcadero.com/RADStudio/Florence/en/What%27s_New)).

---

## 2. The geology of modern Delphi 13: six eras coexisting in one program

| Language axis | Old and classic stratum (`I–II`) | Transitional and cross-platform stratum (`III–IV`) | Modern stratum (`V–VI`) | Rule for coexistence in one unit |
|---|---|---|---|---|
| **Strings** | `ShortString` (`1+N` bytes, `[0]` length); heap-based `AnsiString` (`refCount`, COW) | `UnicodeString` (`string`, UTF-16LE, `codePage`/`elemSize`), `AnsiString(CP)`, `RawByteString` | Multiline literals `'''` ([TEXTBLOCK](../directives/textblock.md)) | `string[N]` remains a flat buffer without a heap inside `packed record`; `string` is UTF-16LE on the heap (taking account of status `OPEN` of `LONGSTRINGS_DOC_CONFLICT` for `{$H-}`) |
| **Composite types** | Flat `record` (`case .. of`, `packed`/`$A`), stack-based `object` (VMT + *slicing*) | `advanced record` with methods and `class operator`, generic `TRec<T>` | Custom Managed Records (`Initialize`/`Finalize`/`Assign`, implicit `Self` in 13) | Old `object`, flat `record`, and managed CMR freely coexist with their `SizeOf` and copying rules strictly distinguished |
| **Polymorphism and constraints** | `class(TObject)` (`virtual`/`override`, `dynamic`, `message`, `class of`), `IInterface` (IMT) | Monomorphized `Generics<T>` (separate VMTs and `class var`), `: class` / `: record` / `: constructor` | Constraints `: interface` and `: unmanaged` (`E2668`), operators `is not` / `not in` | Dynamic polymorphism goes through VMT/IMT on the heap; parametric polymorphism goes through compile-time code specialization |
| **Callable types** | 1-word procedural pointer, 2-word `TMethod` (`of object` = `Code + Data`) | Anonymous methods `reference to` (COM object on the heap + shared variable frame) | Working together with block-local `var` and conditional `if` expressions | A free function, an instance method, and a closure are compatible in calling, but have different ABI sizes and memory ownership |
| **Memory and lifetime** | Routine stack, `GetMem`/`FreeMem`, manual `Create`/`Free`, `IInterface` reference counting | The mobile class ARC experiment (`XE4–10.3`, removed in `10.4`), `[weak]`/`[unsafe]` | Block-local `var` (`10.3`), CMR on the stack (`10.4+`), a unified `TObject` model on all OSes | `class` instances are always freed explicitly (`Free`/`Owner`), strings and interfaces by `refCount`, CMR automatically at the block boundary |
| **Metadata and RTTI** | `published` section under `{$M+}`, compiler `TypeInfo` | `System.Rtti`, `TValue`, attributes, `{$RTTI EXPLICIT}` | `NameOf(Ident)` at the symbol phase, strict rejection of sparse enums in `TypeInfo` (`E2134`) | `NameOf` protects against typos during refactoring with zero runtime cost and without bloating RTTI tables |
| **Errors and arithmetic** | Flag `{$I-}` + `IOResult`, `FS:[0]` SEH frames on Win32, 10-byte `Extended`, `EZeroDivide` | Table-based `PC-Mapped` unwind on Win64, `Extended = Double` (`8B` Win64), `RaiseOuterException` | All 6 FP masks enabled by default (`12 Athens`), `noreturn`, prohibition on exiting `finally` (`E2126`) | Machine exceptions, IEEE `+Inf`/`NaN`, and return codes do not conflict if the check and mask profile is explicitly recorded |
| **Directives and building** | `{$IFDEF}`, `{$R+}`, `{$Q+}`, writable constants `{$J+}` | `{$IF}`/`{$IFEND}`, `{$LEGACYIFEND OFF}`, `{$SCOPEDENUMS ON}` | Stack-based `{$PUSHOPT}`/`{$POPOPT}`, long `{$IFOPT}` predicates (`{$IFOPT WARNINGS ERROR}`) | The `{$PUSHOPT}`/`{$POPOPT}` pair encapsulates inherited modes (`{$J+}`, `{$Q-}`), preventing them from leaking into the unit's modern code |

---

## 3. Five engineering rules at the junctions between eras

Where mechanisms from different generations meet in a single line or structure, strict physical boundaries apply:

1. **`ShortString` versus `UnicodeString` and `{$H-}`:** `ShortString` remains a single-byte `1 + N` buffer on the stack, whereas unqualified `string` in the tested `Delphi 13 CE` profiles remained UTF-16LE `UnicodeString` even under `{$H-}` ([chapter 09](09-strings.md)).
2. **Four structure models (`object` vs `record` vs `CMR` vs `class`):** `object` is copied by value with a hidden VMT pointer and loses descendant fields when sliced; an ordinary `record` is trivial or automatically managed by its fields; `CMR` adds custom `Initialize`/`Finalize`/`Assign` without a VMT and **without calling `Finalize` on an exception inside `Initialize`**; `class` always lives on the heap and calls `Destroy` on an exception in `Create`.
3. **`TMethod` (`of object`) versus `reference to`:** `TMethod` (`8` or `16` bytes) does not keep an object from being destroyed, whereas `reference to` retains a heap COM frame through reference counting and shares captured local *variables* among all copies of the closure ([chapter 23](23-closures.md)).
4. **`: record` versus `: unmanaged` in generics:** the old `: record` constraint admits records with strings and CMR, whereas the new `Delphi 13` `: unmanaged` constraint requires pure bitwise triviality and rejects managed records with code `E2668` ([chapter 32](32-constraints.md)).
5. **Stratum I's 256-element foundation inside stratum VI's `not in` operator:** the new `X not in [...]` operator (`Delphi 13`) is built on the classic `set of` set constructor (`0..255`, `32` bytes). For narrow enumerations and small integers (`0..255`), it expands into a fast bit check, but values outside `0..255` exceed the physical limit of a Pascal set ([chapter 11](11-sets.md), [chapter 17](17-expressions.md)).

---

## 4. An integrated synthesis of six eras in one program (`EvolutionStrataSynthesisDemo`)

---

### [DEMO EXCERPT BOUNDARY — Level 4 — Architectural Synthesis (Six Historical Strata: Turbo Pascal to Delphi 13)]

Shown above: first ~95 lines out of **324 lines** in the full chapter.

**Complete section outline in the full edition:**
- `## 1. Six language strata: from a physical limit to a new solution`
- `### Stratum I. The static foundation `Wirth Pascal -> Turbo / Borland Pascal 1–7``
- `### Stratum II. The classic RAD era, heap VMT, and COM (`Delphi 1–7`, `1995–2002`)`
- `### Stratum III. Unicode, monomorphized Generics, closures, and extended RTTI (`Delphi 2005–2010`)`
- `### Stratum IV. Multi-target ABI and the architectural lesson of mobile ARC (`XE2–10.3`)`
- `### Stratum V. Memory unification and deterministic stack-based RAII (`10.3 Rio – 10.4 Sydney`)`
- `### Stratum VI. Hardware realism of FP masks and semantic precision (`11 Alexandria – 13 Florence`)`
- `## 2. The geology of modern Delphi 13: six eras coexisting in one program`
- `## 3. Five engineering rules at the junctions between eras`
- `## 4. An integrated synthesis of six eras in one program (`EvolutionStrataSynthesisDemo`)`

To inspect the complete chapter, verified runnable program, counterexamples and compiler receipts, use the full edition (`https://silentfish.dev/delphi`).
