# 31. Generic types and methods

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

**Demo Sample Tier:** Level 3 — Advanced (Generics, Generic Methods, HasWeakRef / GetTypeKind / E2533)


Generics (introduced in **Delphi 2009**, [Declaring Generics](https://docwiki.embarcadero.com/RADStudio/Florence/en/Declaring_Generics)) allow classes, records, interfaces, dynamic arrays, procedural types, and methods to be parameterized with formal type parameters. Within its own declaration, `TBox<T>` acts as an **open form**, and substituting a concrete type (`TBox<Integer>`, `TBox<string>`) produces a **closed specialization** (constructed type) with its own physical layout and class data.

## Specialization mechanics versus type erasure and C++ templates

Delphi generics differ fundamentally both from Java's type-erasure model and from textual, duck-typed template instantiation in C++:

1. **Checking the body at the declaration point (versus C++ `template`).** The compiler checks the open `TBox<T>` body once against its declared constraints ([chapter 32](32-constraints.md)). Without constraints, `T` is treated as an opaque value: it can be stored, copied through `:=`, passed, and returned, but `T.Create` cannot be called, `A + B` cannot be added, `A = B` cannot be compared, and unconfirmed members cannot be accessed.
2. **Actual distinct types in binary code (versus Java).** Each closed specialization receives its own runtime representation:
   - **Memory layout:** field `Value: T` occupies exactly `SizeOf(T)` bytes with `T` alignment, so `TBox<Byte>` and `TBox<Int64>` have different `InstanceSize` values.
   - **Managed-field table:** if argument `T` is managed (`string`, `IInterface`, a dynamic array, CMR), this specialization receives its own `vmtInitTable`, which automatically zeros and finalizes field `Value` ([chapter 35](35-memory.md)).
   - **Separate `class var`:** each closed specialization is allocated **its own independent static-data cell** ([Class Variable in Generics](https://docwiki.embarcadero.com/RADStudio/Florence/en/Class_Variable_in_Generics)). Because code is generated for each specialization, a large number of closed instantiations increases the size of the `.dcu` and executable file.

### Compile-time intrinsics for specialization optimization: `GetTypeKind(T)`, `IsManagedType(T)`, `HasWeakRef(T)`

Within a generic type or method body, compile-time expressions `SizeOf(T)`, `Default(T)`, `TypeInfo(T)` are available, and starting with **Delphi XE7**, so are compiler intrinsics `GetTypeKind(T)`, `IsManagedType(T)`, and `HasWeakRef(T)`. Since their results are constant in each closed specialization, branches such as `if IsManagedType(T) then ...` are folded at compile time without runtime branching overhead. Expression `Default(T)` returns the type's zero value (`0`, `False`, `nil`, `''`, a zeroed record), and assignment `Value := Default(T)` for managed `T` releases the previous string buffer or interface through the normal mechanism.

Selected types were measured in the live probe series **`P15_Intrinsics_TypeMeta32_V2` / `64_V2`** (`Win32` `0x14c` and `Win64` `0x8664`, `0` diagnostics, `exit=0`) and **`P15_HasWeakRef_*`** (`Win32` Debug, `0` diagnostics). The `System.HasWeakRef` column below was corrected by separate edition 1.2.0 probes; the earlier generalization of diagnostic `E2571` has been withdrawn:

| Tested type `T` | `GetTypeKind(T)` | `IsManagedType(T)` | `System.HasWeakRef(T)` *(P15 and separate 1.2.0 probes)* | Physical meaning and boundary |
|---|---|---|---|---|
| `Integer`, `Double`, `Pointer` | `tkInteger`, `tkFloat`, `tkPointer` | `False` | `False` (1.2.0, both architectures) | Scalars and raw pointers without hidden finalization |
| `ShortString` | `tkString` | **`False`** | `False` (1.2.0, both architectures) | An inline string type with a length byte (`string[1..255]`), without heap allocation |
| `AnsiString`, `string` (`UnicodeString`), `WideString` | `tkLString`, `tkUString`, `tkWString` | **`True`** | `False` (1.2.0, both architectures) | Managed string buffers (`RefCount` / COM BSTR) |
| `TBytes` (`array of Byte`) | `tkDynArray` | **`True`** | `False` (1.2.0, both architectures) | A reference-counted dynamic array |
| `TPlainRec` (`record A, B: Integer; end`) | `tkRecord` | `False` | `False` (`_RecOther32`, `_GenRec32`) | An unmanaged record without reference fields |
| `TStrRec` (`record S: string; end`) | `tkRecord` | **`True`** | `False` (`_RecPlain32`) | An ordinary record with a managed field, but without `[weak]` |
| `TManagedRec` *(CMR with `Initialize`/`Finalize` on `Integer`)* | **`tkMRecord`** | **`True`** | `False` (`_RecOther32`) | A separate `tkMRecord` category even without managed fields |
| `TWeakIntfRec` (`record [weak] F: IInterface; end`) | `tkRecord` | **`True`** | **`True`** (`_RecWeak32`, `_GenRec32`) | A `[weak]` field enrolls the record in the weak-reference registry and makes it managed |
| **`TUnsafeIntfRec` (`record [unsafe] F: IInterface; end`)** | `tkRecord` | **`False`** | **`False`** (`_RecWeak32`) | Attribute `[unsafe]` completely removes reference counting and managed status |
| `TObject` / `THolder = class [weak] W: IInterface; end` | `tkClass` | `False` | **`False`** (`_ClassIntf32`, `_GenClass32`) | On classic non-ARC Windows, class instances are managed manually |
| `IInterface` / `TProc` (`reference to procedure`) | **`tkInterface`** | **`True`** | `False` (`_ClassIntf32`) | A `reference to` closure is represented by the capture frame's interface |
| `Variant` / `TMethod` (`procedure of object`) | `tkVariant` / `tkRecord` | `True` / `False` | — | `Variant` is managed through the RTL; `TMethod` (`Code` + `Data`) is unmanaged |

**Name resolution and the verified scope of `HasWeakRef`:**

1. [The built-in operation `System.HasWeakRef`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.HasWeakRef) takes **a type name**. [The function `System.TypInfo.HasWeakRef`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.TypInfo.HasWeakRef) of the same name takes **`PTypeInfo`**. These are different operations. After `uses System.TypInfo`, write `System.HasWeakRef(T)` or `System.TypInfo.HasWeakRef(TypeInfo(T))` explicitly. In probes `QualifiedHasWeakRef_Win32/64`, both methods returned `True` for a record with a weak interface field and `False` for a plain record; the unqualified call with a type name did not compile.
2. **A prohibition on scalars and unconstrained `<T>` is not confirmed.** `ConcreteHasWeakRef_Win32/64` accepts `Integer`, `Double`, `ShortString`, `AnsiString`, `string`, `WideString`, `TBytes`, `Pointer`, `Variant` and returns `False`. `GenericWeakRefRun_Win32/64` accepts `TBox<T>` without a constraint: specializations with `Integer`, `string`, and a plain record return `False`; with a weak record, `True`. All these programs executed with `exit=0` on Delphi 13 CE `37.0.60542.8024`, Debug.
3. Historical `P15_Intrinsics_TypeMeta32/64` recorded `E2571`, but rebuilding the published source revealed a collision with the function from `System.TypInfo` and other diagnostics. The source text does not contain the earlier call at the described location. The old receipts are preserved, but they **are not proof of a general intrinsic restriction**. Constrained `T: class` and `T: record` from separate P15 probes also remain admissible in the measured profile.

The new [1.2.0 receipt](../../../evidence/compiler/demo-sample-receipts.json) records the sources and their dependencies. A Windows observation does not assign results to old or mobile compilers.

```pascal
// Синтаксический срез проверки HasWeakRef(T) при ограничении T: record (проба P15_HasWeakRef_GenRec32)
type
  TRecBox<T: record> = record
    class function Check: Boolean; static;
  end;

class function TRecBox<T>.Check: Boolean;
begin
  Result := HasWeakRef(T);
end;
```

*English glosses of the retained source comments:*
- Syntax excerpt of the HasWeakRef(T) check with constraint T: record (probe P15_HasWeakRef_GenRec32)



## Formal grammar and declaration restrictions

```pascal
// Синтаксический срез допустимых обобщённых конструкций (не полный проект)
type
  TBox<T> = class
    Value: T;
  end;
  TPair<TKey, TValue> = record
    Key: TKey;
    Value: TValue;
  end;
  IReader<T> = interface
    function Read: T;
  end;
  TItems<T> = array of T;                     // Обобщённый динамический массив (НЕ открытый массив!)
  THandler<T> = procedure(const Value: T);    // Обобщённый процедурный тип

  TIdentity = class
    class function Keep<T>(const Value: T): T; static; // Обобщённый метод внутри класса/записи
  end;
```

*English glosses of the retained source comments:*
- Syntax excerpt showing permitted generic constructs (not a complete project)
- Generic dynamic array (NOT an open array!)
- Generic procedural type
- Generic method inside a class/record



Five strict syntactic rules:
1. **No free (top-level) generic routines.** Unlike C++ and C# local functions, Delphi does not allow a free `function Max<T>(const A, B: T): T;` at unit level — generic routines are declared **only as class or record methods** ([example 10](../../../examples/README.md), `OBSERVED_PASS`: `TIdentity.Keep<Integer>(42)` outputs `42`). The type-parameter list is repeated in the implementation header (`class function TIdentity.Keep<T>(const Value: T): T;`), but without repeating constraints `: record` / `: class`.
2. **No polymorphic generic methods (`E2533`).** Constructors, destructors, and `virtual`, `dynamic`, `message` methods cannot declare their own type-parameter list `<U>` (the fixed table of class VMT slots cannot accommodate a set of future method specializations that is unknown in advance).
3. **Type-parameter scope and ancestry.** Parameter `T` from `TBox<T>` is not automatically inherited as a name in the descendant header: write `TChild<S> = class(TBox<S>)`. A class ancestor may be an ordinary class or a specialized generic class (`class(TBox<Integer>)`, `class(TBox<S>)`), but **not** a bare type parameter (`class(T)` is forbidden).
4. **Specialization aliases.** Declaration `type TIntCounter = TCounter<Integer>;` denotes the very same specialization, rather than a new distinct type.
5. **No partial specialization or nontype parameters.** Unlike C++ (`template<typename T, int N>`), parameters in `<...>` always denote only types, and explicitly overloading the template body for one concrete type is not supported.

## Specialization class data (`40-generic-class-state.dpr` and `P5_Generic_StaticVar`)

```pascal
program GenericClassState;
{$APPTYPE CONSOLE}
type
  TCounter<T> = class
```


---

### [DEMO EXCERPT BOUNDARY — Level 3 — Advanced (Generics, Generic Methods, HasWeakRef / GetTypeKind / E2533)]

Shown above: first ~105 lines out of **279 lines** in the full chapter.

**Complete section outline in the full edition:**
- `## Specialization mechanics versus type erasure and C++ templates`
- `### Compile-time intrinsics for specialization optimization: `GetTypeKind(T)`, `IsManagedType(T)`, `HasWeakRef(T)``
- `## Formal grammar and declaration restrictions`
- `## Specialization class data (`40-generic-class-state.dpr` and `P5_Generic_StaticVar`)`
- `## Specialization inheritance without variance and `overload` resolution`
- `### Generic methods in nongeneric classes and the polymorphism restriction (`P15_GenericMethods_*` and `E2533`)`
- `## An open documentation discrepancy: [`GENERIC_ARGUMENT_DOC_COUNTEREXAMPLE`](../SOURCE_ISSUES.md#issue-generic-argument-doc-counterexample) (`OPEN`) and ICE `NC2130``
- `## An additional authored example (`program ... end.`)`
- `## Version and target boundaries`
- `## Primary sources and verification status`
- `## Verification 1.3.0: refined boundaries`
- `### GENERIC_ARGUMENT_DOC_COUNTEREXAMPLE`

To inspect the complete chapter, verified runnable program, counterexamples and compiler receipts, use the full edition (`https://silentfish.dev/delphi`).
