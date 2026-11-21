# 41. Compiler directives

> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

**Demo Sample Tier:** Level 3 — Advanced (Compiler Directives & 76 Verified $WARN Identifiers)


## 1. Classification, comma syntax, and overloaded short letters

Compiler directives in Embarcadero Delphi are written inside `{$...}` or `(*$...*)` comments, where the `$` character must follow the opening delimiter **immediately**, without a space (the `{ $R+}` form is an ordinary comment that the compiler silently skips). By nature, all directives fall into three families ([Compiler Directives List](https://docwiki.embarcadero.com/RADStudio/Florence/en/Delphi_Compiler_Directives_(List)_Index), [Delphi compiler directives](https://docwiki.embarcadero.com/RADStudio/Florence/en/Delphi_compiler_directives)):

1. **Switches (`Switch directives`):** have the single-letter `{$R+}` / `{$R-}` forms and the long `{$RANGECHECKS ON}` / `{$RANGECHECKS OFF}` forms.
   - **The comma rule ([example 45](../../../examples/README.md), `OBSERVED_PASS`):** single-letter switches may be grouped with commas and no spaces (`{$B+,R-}`), whereas in a long form, text after the first switch and a space/comma is treated as a trailing comment and **does not enable** a second directive! Long directives are therefore always written in separate `{$BOOLEVAL ON}{$RANGECHECKS OFF}` blocks.
2. **Parameterized directives (`Parameter directives`):** pass a filename, number, identifier, or filter to the compiler or linker (`{$ALIGN 8}`, `{$MINENUMSIZE 4}`, `{$APPTYPE CONSOLE}`, `{$WARN SYMBOL_DEPRECATED ERROR}`, `{$RTTI EXPLICIT ...}`).
3. **Conditional directives (`Conditional directives`):** control source-text selection before syntax analysis (`{$DEFINE}`, `{$UNDEF}`, `{$IFDEF}`, `{$IFNDEF}`, `{$IF}`, `{$ELSEIF}`, `{$ELSE}`, `{$ENDIF}`, `{$IFEND}`, `{$IFOPT}`; see [chapter 42](42-conditionals.md)).

### Collisions between single-letter forms

Historically, the same letter in a short form serves entirely different mechanisms depending on its argument:

| Letter | Switch (`+` / `-`) | Parameterized / other form |
|---|---|---|
| `$R` | `{$R+}` / `{$R-}` — range-bound checking (`RANGECHECKS`) | `{$R file.res [Pred]}` — linking a resource file (`RESOURCE`) |
| `$I` | `{$I+}` / `{$I-}` — generating file input/output checks (`IOCHECKS`) | `{$I file.inc}` — lexical source-text insertion (`INCLUDE`) |
| `$M` | `{$M+}` / `{$M-}` — classic RTTI for the `published` section (`TYPEINFO`) | `{$M minstack,maxstack}` — executable-image stack sizes (`MINSTACKSIZE`/`MAXSTACKSIZE`) |
| `$A` | `{$A+}` / `{$A-}` — default field alignment / no alignment | `{$A1}`, `{$A2}`, `{$A4}`, `{$A8}`, `{$A16}` — an explicit `ALIGN` step |
| `$D` | `{$D+}` / `{$D-}` — debugger line numbers (`DEBUGINFO`) | `{$D 'text'}` — a module description string (`DESCRIPTION`); `{$D0..D2}` — see [chapter 71](71-compilation-layers.md) |
| `$L` | `{$L+}` / `{$L-}` — local symbol table (`LOCALSYMBOLS`) | `{$L file.obj}` — including an external object module (`LINK`) |

## 2. Four scopes and changes in modern versions (`PUSHOPT` / `IFOPT`)

Besides the distinction between `Global` (for the whole unit, before `interface`/`uses`) and `Local` (from the point encountered downward through the text), it is critical to distinguish:
- **Whole-subroutine granularity:** options such as `{$OPTIMIZATION}` (`{$O}`) and `{$STACKFRAMES}` (`{$W}`) apply to the entire procedure, rather than one line inside `begin..end`.
- **Being fixed in the type declaration:** `{$ALIGN}`, `{$MINENUMSIZE}`, `{$SCOPEDENUMS}`, and the scaled address-arithmetic property of a typed pointer ([pointer-arithmetic card](../directives/pointermath.md), [example 26](../../../examples/README.md)) are retained by the type itself at the `type T = ...;` point.
- **Lexical literal directives (Delphi 12+):** control of multiline-literal line-break format `'''` (`CRLF` versus `LF`, [multiline-literal card](../directives/textblock.md), [example 28](../../../examples/README.md), and live probe `P7_TextBlock_CRLF_LF` with length `12` versus `11` and automatic removal of the closing `'''` indentation).

In **Delphi 13 Florence**, the option stack and state checking received key updates ([What's New](https://docwiki.embarcadero.com/RADStudio/Florence/en/What%27s_New), [Option OPT](https://docwiki.embarcadero.com/RADStudio/Florence/en/Option_OPT_(Delphi)), [IFOPT](https://docwiki.embarcadero.com/RADStudio/Florence/en/IFOPT_directive_(Delphi))):
- **`{$PUSHOPT}` and `{$POPOPT}`** ([PUSHOPT card](../directives/pushopt-popopt.md), [example 29](../../../examples/README.md), `OBSERVED_PASS`: `on`, `off`, `on`) save and restore supported compiler-option states without manual branching;
- **`{$IFOPT}` with long names** ([example 44](../../../examples/README.md), `OBSERVED_PASS`: `scoped`, `flat`) allows switches without a short single-letter code to be tested, for example `{$IFOPT SCOPEDENUMS ON}`.

## 3. Ambiguities in documentation tables and live P2 / P3 probes

1. **`PUSHOPT_TABLE_TYPOS` (`OPEN` in [`source_issues.json`](../../../evidence/source_issues.json)):**
   - The *Option OPT* table contains corrupted spellings `IMPOTEDDATA`, `FINITEFLOATT`, and duplicate `ASSERTIONS`, while selective syntax with an argument is incompletely described.
   - Live probes on Delphi 13 CE (`37.0.60542.8024`, Win32 Debug) showed two critical facts: (a) in `P2_PushOpt_Sel_Effect` and `P3_PushOpt_Discriminate`, `{$PUSHOPT RANGECHECKS}` before changing both `R` and `Q` **restored the measured R/Q option states from the top snapshot** when `{$POPOPT}` was called (`R=ON`, `Q=OFF`), rather than only `RANGECHECKS`; (b) in `P3_PushOpt_Bogus`, `P3_PushOpt_Typo1`, and `P3_PushOpt_Typo2`, the `BOGUS_OPT`, `FINITEFLOATT`, and `IMPOTEDDATA` arguments were **silently ignored by the compiler with `0` diagnostics**! Practical conclusion: use the plain argumentless `{$PUSHOPT}` ... `{$POPOPT}` pair.
2. **`IFOPT_TABLE_TYPOS` (`OPEN`):**
   - In the P3 probes, the correct long `{$IFOPT TYPEINFO ON}` and `{$IFOPT SCOPEDENUMS ON}` forms compiled cleanly, while table typo `{$IFOPT TYPEINF ON}` and unsupported form `{$IFOPT FINITEFLOAT ON}` were rejected with error **`E1030 Invalid compiler directive: '$IFOPT'`**.
3. **`CODEPAGE_SOURCE_FORM_UNCONFIRMED` (`OPEN`, [CODEPAGE card](../directives/codepage.md)):**
   - For Embarcadero, only the command-line `--codepage=nnn` switch ([E2424](https://docwiki.embarcadero.com/RADStudio/Florence/en/E2424_Codepage_%27%25s%27_is_not_installed_on_this_machine_(Delphi))) and the IDE editor/project setting are confirmed; the `{$CODEPAGE UTF8}` source-file directive (familiar from Free Pascal) was rejected in probe `P2_Codepage_UTF8` on `dcc32` 37.0 with error **`E1030 Invalid compiler directive: 'CODEPAGE'`**.
4. **`EXTRA_DIRECTIVES_NOT_REVIEWED` (`PARTIALLY_DOCUMENTED`, [EXTRA_OPTIONS](../research/EXTRA_OPTIONS.md)):**
   - Of 9 additional table names, `MAXPAGESIZE` and `VARPROPSETTER` were given separate cards, while all 7 others (`OLDOBJWARN`, `STACKCHECKS`, `AUTOBOX`, `UNSAFECODE` with platform warning `W1002`, `NATIVE_CPP_INTERFACES`, `COMPATIBLELITERALS`, `DUPLICATEENABLE`) passed the parser in series P2 without `E1030`/`W1030`; acceptance of the syntax alone, however, does not establish their native semantics (for example, the short `$E+`/`$E-` cannot be linked to `OLDOBJWARN` without a separate contract).

## 4. Systematic catalog of `{$WARN <ID> ON|OFF|ERROR|DEFAULT}` identifiers (76 verified IDs in `Delphi 13 CE`)

Unlike the whole-subroutine `{$WARNINGS}` switch ([Warnings](https://docwiki.embarcadero.com/RADStudio/Florence/en/Warnings_(Delphi))), the `{$WARN <ID> ON|OFF|ERROR|DEFAULT}` directive ([Warning messages](https://docwiki.embarcadero.com/RADStudio/Florence/en/Warning_messages_(Delphi)), [WARN card](../directives/warn.md)) controls an individual warning class by its canonical symbolic identifier, while `DEFAULT` restores the setting from the project profile (`.dproj`/CLI). In the live **`P15_Warn_Ids_Verified32`** probe (`Delphi 13 CE`, `Win32 Debug`, `pe=0x14c`, `0` diagnostics, `run_exit = 0`, `stdout='warn_verified_count=76'`), the parser accepted **all `76/76` verified identifiers** in the `{$PUSHOPT}{$WARN <ID> OFF}{$WARN <ID> DEFAULT}{$POPOPT}` form:

### 4.1. Symbol and unit lifecycles and member visibility (12 IDs)

| `{$WARN}` identifier | Purpose of the diagnostic |
|---|---|
| `SYMBOL_DEPRECATED`, `UNIT_DEPRECATED` | Use of a symbol or `unit` with the `deprecated` modifier (`W1000` / `E1000`) |
| `SYMBOL_LIBRARY`, `UNIT_LIBRARY` | Use of a symbol or `unit` with the `library` modifier (`W1001` and equivalents) |
| `SYMBOL_PLATFORM`, `UNIT_PLATFORM` | Use of a platform-dependent symbol or `unit` (`platform`, `W1002`) |
| `SYMBOL_EXPERIMENTAL`, `UNIT_EXPERIMENTAL` | Use of an experimental symbol or `unit` (`experimental`, `W1003`) |
| `HIDING_MEMBER` | Hiding a nonvirtual base-class member (under `{$WARN HIDING_MEMBER ERROR}`, non-`virtual` hiding of a method/field/parameter/local name in `P15` produced `0` diagnostics) |
| `HIDDEN_VIRTUAL` | Hiding a base-class `virtual` method without `override`/`reintroduce` (`W1010` / `E1010`) |
| `PRIVATE_PROPACCESSOR` | Restrictions on a private property getter/setter or a visibility conflict |
| `BAD_GLOBAL_SYMBOL` | A global symbol violating visibility or package-export rules |

### 4.2. Ranges, loops, constants, branching, and constructs (18 IDs)

| `{$WARN}` identifier | Purpose of the diagnostic |
|---|---|
| `BOUNDS_ERROR` | A constant index exceeds the static array/range bounds |
| `ZERO_NIL_COMPAT` | Historical implicit compatibility of integer zero and `nil` |
| `STRING_CONST_TRUNCED` | Truncation of a string constant when placed in a short `string[N]` buffer |
| `FOR_LOOP_VAR_VARPAR`, `FOR_VARIABLE`, `FOR_LOOP_VAR_UNDEF` | Passing a `for` counter by `var`, requirements for a local counter variable, and indeterminacy after the loop |
| `TYPED_CONST_VARPAR`, `ASG_TO_TYPED_CONST` | Passing a typed constant by `var` or assigning to it with `{$J+}` enabled (under `{$J-}`, writing is prohibited with code `E2064`) |
| `CASE_LABEL_RANGE` | A `case` branch label exceeds the selector type’s permitted range |
| `CONSTRUCTING_ABSTRACT` | Instantiating a class with unimplemented `abstract` methods (`W1020`) |
| `COMPARISON_FALSE`, `COMPARISON_TRUE` | A comparison that statically always gives `False` (`W1021`) or `True` (`W1022`) |
| `COMPARING_SIGNED_UNSIGNED`, `COMBINING_SIGNED_UNSIGNED` | Comparison (`W1023` / `E1023`) or arithmetic mixing of signed and unsigned integers |
| `UNSUPPORTED_CONSTRUCT` | A language construct unsupported or partly ignored on the selected target |
| `DUPLICATE_CTOR_DTOR` | Conflicting duplication of a constructor or destructor |
| `NO_RETVAL`, `USE_BEFORE_DEF` | `Result` is not assigned on all paths (`W1035`), or possible reading of a local variable before initialization (`W1036`) |

### 4.3. Type casts, unsafe code, and `Variant` (10 IDs)

| `{$WARN}` identifier | Purpose of the diagnostic |
|---|---|
| `HRESULT_COMPAT` | Compatibility and casting of `HRESULT` values |
| `IMPLICIT_VARIANTS` | Implicit inclusion of and operations on `Variant` |
| `SUSPICIOUS_TYPECAST`, `NON_PORTABLE_TYPECAST` | A suspicious cast between different sizes or a nonportable 32/64-bit cast |
| `UNSAFE_TYPE`, `UNSAFE_CODE`, `UNSAFE_CAST`, `UNSAFE_VOID_POINTER` | Markers of unsafe types, address arithmetic, casts, and untyped `Pointer` |
| `WIDECHAR_REDUCED` | Narrowing of a wide `WideChar` character to a narrow representation |
| `IMMUTABLE_STRINGS` | String-immutability model warnings |

---

### [DEMO EXCERPT BOUNDARY — Level 3 — Advanced (Compiler Directives & 76 Verified $WARN Identifiers)]

Shown above: first ~90 lines out of **185 lines** in the full chapter.

**Complete section outline in the full edition:**
- `## 1. Classification, comma syntax, and overloaded short letters`
- `### Collisions between single-letter forms`
- `## 2. Four scopes and changes in modern versions (`PUSHOPT` / `IFOPT`)`
- `## 3. Ambiguities in documentation tables and live P2 / P3 probes`
- `## 4. Systematic catalog of `{$WARN <ID> ON|OFF|ERROR|DEFAULT}` identifiers (76 verified IDs in `Delphi 13 CE`)`
- `### 4.1. Symbol and unit lifecycles and member visibility (12 IDs)`
- `### 4.2. Ranges, loops, constants, branching, and constructs (18 IDs)`
- `### 4.3. Type casts, unsafe code, and `Variant` (10 IDs)`
- `### 4.4. Strings and encoding conversions (10 IDs)`
- `### 4.5. Files, directives, linking, packages, and C++/RTTI (18 IDs)`
- `### 4.6. XML documentation in `///` comments (8 IDs)`
- `### Behavioral contrasts of `{$WARN}` in `P15` (`COMPARING_SIGNED_UNSIGNED` and `HIDDEN_VIRTUAL` vs `HIDING_MEMBER`)`
- `## 5. A self-contained example`
- `## 6. Version boundaries and avoiding false analogies`
- `## 7. Primary sources and verification status`
- `## Verification 1.3.0: refined boundaries`
- `### WARNINGS_ERROR_PROFILE`

To inspect the complete chapter, verified runnable program, counterexamples and compiler receipts, use the full edition (`https://silentfish.dev/delphi`).
