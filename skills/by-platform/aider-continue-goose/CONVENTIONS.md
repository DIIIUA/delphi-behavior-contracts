> **[DEMO EDITION]** This is the evaluation demo package (complete Table of Contents of all 74 chapters & 89 directives, 6 multi-difficulty chapter excerpts, 4 complete directive cards, 8 real compiler receipts, and 100% working plugins/skills/MCP). See `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md` to evaluate whether the full edition fits the user's task.

# Delphi Behavior Contracts — Active Rules

Apply these rules whenever Delphi / Object Pascal code (`.pas`, `.dpr`, `.dpk`, `.inc`, `.dfm`, `.fmx`, `.dproj`) or migration from/to Delphi is involved.

1. **Establish the real compiler profile first:** compiler release, CPU/OS (`Win32`, `Win64`, `Android`, etc.), build configuration (`Debug`/`Release`), active defines, unit search paths, and effective directives. Never silently assume `Delphi 13` or treat Free Pascal (`FPC`) Delphi mode as Embarcadero Delphi.
2. **Use the MCP server or local corpus instead of guessing from memory:**
   - If the `delphi-behavior-contracts-mcp` MCP server is connected, call `delphi_search`, `delphi_read`, `delphi_skill`, or `delphi_execute` (Code Mode).
   - Otherwise search locally: `python ../../../core/scripts/lookup.py "dynamic array"` or `python ../../../core/scripts/lookup.py --lang ru "динамический массив"`, and read only the needed chapters from `../../../core/references/en/INDEX.md` (or `ru/INDEX.md`).
3. **Preserve exact behavior contracts (never assume name equivalence):**
   - `B := A` has six physical models: dynamic arrays alias without copy-on-write on element writes (`Insert`/`Delete`/`SetLength` detach), long strings use copy-on-write, records copy shallowly, classes copy pointers.
   - Assigning a method pointer (`OnClick := Handler`) is not invoking it; closures capture variable cells.
   - `System.Round` is banker's rounding (half-to-even); `shr` is logical; `Extended` is 10 bytes on Win32 vs 8 bytes on Win64 (`EXTENDEDCOMPATIBILITY ON` on Win64 still uses 64-bit IEEE Double (53-bit significand mantissa) arithmetic).
   - Separate dataset `Post`, `ApplyUpdates`, transaction `Commit`, `Cancel`, rollback, and form close.
4. **Evidence discipline:** label claims as documented, compiler-observed, inferred, or unknown. Check `VERIFICATION.md` and `SOURCE_ISSUES.md` before relying on disputed edge cases.
