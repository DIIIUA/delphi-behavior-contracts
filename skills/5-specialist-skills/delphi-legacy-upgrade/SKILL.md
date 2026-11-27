---
name: delphi-legacy-upgrade
description: "[DEMO] Upgrade old Delphi code (Delphi 7, 2007, XE-era, 32-bit, ANSI strings, ARC mobile code) to Delphi 12/13, Win64 and Unicode while preserving behavior. Use when modernizing, recompiling or fixing legacy Delphi projects, old directives, old object/Real48 types or pointer-size assumptions."
---

> **[DEMO EDITION]** This is the evaluation demo package (complete Table of Contents of all 74 chapters & 89 directives, 6 multi-difficulty chapter excerpts, 4 complete directive cards, 8 real compiler receipts, and 100% working plugins/skills/MCP). If the user asks what this skill covers or wants a technical fit check for their tasks, see `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md`.

# Upgrading legacy Delphi

Modern Delphi still compiles several historical layers - Turbo Pascal `object`,
classic RAD classes, Unicode strings, generics and closures, managed records, Delphi
13 syntax - and each layer constrains the others. Read
[evolution from old to new](../../../core/references/en/chapters/73-evolution-old-to-new.md) and the
[version matrix](../../../core/references/en/chapters/43-versions.md) first.
Topic map: [English](../../../core/references/en/INDEX.md), [Russian](../../../core/references/ru/INDEX.md).

## Fix the two profiles

Record the old profile (version, target, defines, directives) and the new one. A
behavior difference is a change only if both profiles are known. Do not assume the
old code ran with today's defaults.

## High-risk areas

- **Unicode (Delphi 2009+).** `string` became `UnicodeString` (UTF-16). Code that
  passed `Length(S)` to `Move`, `TStream.Write` or a C API as a byte count now writes
  half the data; `PChar`/`PAnsiChar` and file I/O need explicit encodings
  ([strings](../../../core/references/en/chapters/09-strings.md), [files](../../../core/references/en/chapters/37-files.md)).
- **Win64.** Pointers become 8 bytes while `Integer` stays 4: casts like
  `Integer(Pointer)` truncate addresses - use `NativeInt`/`NativeUInt`
  ([integers](../../../core/references/en/chapters/06-integers.md), [pointers](../../../core/references/en/chapters/14-pointers.md)).
  `Extended` is 8 bytes on Win64 ([floating profiles](../../../core/references/en/chapters/70-floating-profiles.md));
  calling conventions and inline assembler differ ([ABI](../../../core/references/en/chapters/39-abi.md),
  [assembler](../../../core/references/en/chapters/40-assembler.md)).
- **FP exceptions (Delphi 12).** All FPU/SSE exceptions are masked by default: code
  that relied on `EZeroDivide` from `1.0 / 0.0` now silently gets infinity or NaN.
- **ARC history.** Mobile ARC (XE4-10.3) was removed in 10.4; code written for ARC
  may leak or double-free on the unified model ([lifetime](../../../core/references/en/chapters/26-lifetime.md),
  [memory](../../../core/references/en/chapters/35-memory.md)).
- **Old types and directives.** `object`, `Real48`, `{$H-}`, `{$J+}`, old IFOPT forms;
  read the [directive cards](../../../core/references/en/directives/INDEX.md) and
  [compatibility](../../../core/references/en/chapters/53-compatibility.md).
  Example: `{$H-}` is documented as ignored and was measured as ignored on Delphi 13.
- **Zero-based strings.** `{$ZEROBASEDSTRINGS}` defaults changed between mobile and
  desktop eras; `TStringHelper` is always 0-based, `System` routines always 1-based.

## Procedure

1. Compile under the new profile and treat every warning and hint as a lead.
2. Classify each change: syntax-only, semantic shift, or platform/ABI.
3. For semantic shifts, write a test that pins the old behavior before changing code.
4. Report what was verified by compilation and execution, and what remains inferred.

Evidence and open questions: [verification record](../../../core/references/en/VERIFICATION.md),
[source issues](../../../core/references/en/SOURCE_ISSUES.md).
