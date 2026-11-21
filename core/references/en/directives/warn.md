> **[DEMO EDITION — Evaluation Sample]** This package is the free evaluation demo of **Delphi Behavior Contracts v1.0.0** (full edition: 74 complete EN/RU chapters, 89 full directive cards, 879+ compiler observations). The complete original Table of Contents, verification record, working plugins, pure skills, and local/self-hosted MCP Code Mode server are included so you (and your AI) can test the real workflow and evaluate whether the full edition fits your Delphi task. Full version: https://silentfish.dev/delphi

# WARN — a specific warning class

**Syntax:** `{$WARN identifier ON|OFF|ERROR|DEFAULT}`.

**Default in the cited source:** the page refers to enabled warnings; actual project values are determined separately.

**Scope according to the documentation:** `Local`, from the directive's position in the text.

## Selective filtering versus `{$WARNINGS}` and the `DEFAULT` pitfall

Unlike routine-scoped [`{$WARNINGS}`](warnings.md), `{$WARN}` configures **one specific warning class** by its canonical ID (`SYMBOL_DEPRECATED`, `COMPARING_SIGNED_UNSIGNED`, `HIDDEN_VIRTUAL`, `IMPLICIT_STRING_CAST`, etc.; the complete catalog of **`76` IDs verified in `Delphi 13 CE`** is given in [chapter 41](../chapters/41-directives.md), and profiles in [chapter 59](../chapters/59-directive-profiles.md)):
- **`ON` / `OFF`** enables or suppresses the warning further down the text;
- **`ERROR`** promotes an occurrence of this class from `Wxxxx` to compilation error `Exxxx`;
- **`DEFAULT`** restores the ID's state from **Project Options (`.dproj` / CLI)**, rather than reverting to the preceding local `{$WARN}` in the file; for exact local restoration in Delphi 13, use [`{$PUSHOPT}` / `{$POPOPT}`](pushopt-popopt.md).

## `P12` / `P15` contrasts and a false analogy with MSVC

```pascal
// Проверено в P12_Warn_Granular32 / P12_Warn_Error32 (Delphi 13 CE, Win32 Debug)
{$PUSHOPT}
{$WARN SYMBOL_DEPRECATED OFF}
LegacyProc; // предупреждение W1000 подавлено (diags=[], stdout='legacy')
{$POPOPT}
// При {$WARN SYMBOL_DEPRECATED ERROR} -> отказ: E1000 Symbol 'LegacyProc' is deprecated
```

*English glosses of the retained source comments:*
- Tested in P12_Warn_Granular32 / P12_Warn_Error32 (Delphi 13 CE, Win32 Debug)
- warning W1000 is suppressed (diags=[], stdout='legacy')
- With {$WARN SYMBOL_DEPRECATED ERROR} -> rejection: E1000 Symbol 'LegacyProc' is deprecated



- **Series `P12` (`Win32 Debug`):** `OFF` in `P12_Warn_Granular32` suppressed `W1000` (`diags=[]`, `run_exit = 0`); `ERROR` in `P12_Warn_Error32` stopped the build with code **`E1000`**.
- **Series `P15` (`Win32 Debug`):** `P15_Warn_Ids_Verified32` accepted **all `76/76`** IDs without `W1030`/`E1030` (`run_exit = 0`); `COMPARING_SIGNED_UNSIGNED ERROR` produced **`E1023`** (`P15_Warn_SignedUnsigned_Err32`); hiding a `virtual` method without `override`/`reintroduce` belongs to **`HIDDEN_VIRTUAL`** (**`W1010`** even under `HIDING_MEMBER ERROR`, **`E1010`** under `HIDDEN_VIRTUAL ERROR`, `0` diagnostics under `OFF`), whereas non-`virtual` `HIDING_MEMBER` produced `0` diagnostics.
- **False analogy (MSVC):** `#pragma warning(default: 4996)` resets the rule to the compiler's factory default, while `{$WARN ... DEFAULT}` retrieves the project's policy.

Source: [Embarcadero](https://docwiki.embarcadero.com/RADStudio/Florence/en/Warning_messages_(Delphi)). Read on 18.11.2026.

Status: `W1000`/`E1000` confirmed in `P12`, and the catalog of `76/76` IDs, `E1023`, and the contrast of `HIDDEN_VIRTUAL` (`W1010`/`E1010`) vs `HIDING_MEMBER` in series `P15` (`Delphi 13 CE`, `Win32 Debug`).