# Changelog — Delphi Behavior Contracts

## v1.0.2 (2026-11-27) — Neutral Technical Fit-Check Guide (No Buying Advice)

- **Removed all purchase-recommendation wording from `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md` and demo banners:**
  Rewrote the assistant evaluation guide into a strictly neutral on-request technical scope and fit check (`in scope` vs. `out of scope` for the user's actual Delphi tasks), with an explicit neutrality rule instructing AI assistants never to give buying advice or recommend whether to purchase anything.
- **Updated `README.md`, `README.ru.md`, `START_HERE.md`, `START_HERE.ru.md`, and `[DEMO EDITION]` banners** to match the neutral technical scope/fit framing and bumped demo package metadata to `1.0.2`.

## v1.0.1 (2026-11-25) — Technical Precision & Documented Edge-Case Refinements

Documentation and wording refinement release based on community technical review.
**Verification scope notice:** All existing Delphi 13 CE compiler receipts (`879+` build observations, `650` runs from `v1.0.0` / research edition `1.5.2`) remain unchanged. Newly added edge-case notes in `v1.0.1` are explicitly marked as `DOCUMENTED` (IEEE 754 / Embarcadero DocWiki) or `OPEN` (unmeasured target profile) — no new compiler runs are claimed in this release.

### Changes
- **IEEE 754 `Double` wording precision (EN & RU, all books, chapters, directive cards, demo guides, plugins & skill rules):**
  Replaced shorthand phrasing such as `53-bit Double` / `80-bit to 53-bit` with the exact wording **`64-bit IEEE Double (53-bit significand mantissa)`** (`64-битный IEEE Double (53-битная мантисса)`).
- **Float-bearing records & `CompareMem` / raw byte-sorting (`07-reals.md`, `12-records.md`, EN & RU, `DOCUMENTED`):**
  Unified the prohibition on `CompareMem`/`memcmp` and raw byte-sorting for structures containing `Single`/`Double`/`Extended`: beyond uninitialized alignment padding, `-0.0` vs `+0.0` compare equal (`=`) with different sign bits, `NaN` has multiple bit patterns and is never equal to itself (`NaN = NaN` is `False`), and little-endian byte order plus sign-magnitude IEEE layout break raw lexicographic byte comparison.
- **Per-thread FPU/SSE control word boundaries & `Win64 ARM64EC` (`70-floating-profiles.md`, `SOURCE_ISSUES.md`, `evidence/source_issues.json`, EN & RU, `DOCUMENTED` / `OPEN`):**
  - Added an explicit boundary note on per-thread `FPU Control Word` (`Get8087CW`/`Set8087CW`) and `MXCSR` (`GetMXCSR`/`SetMXCSR`) state when crossing thread boundaries, third-party C/C++ DLLs, COM/drivers, or OS calls.
  - Explicitly listed **`Win64 ARM64EC`** (and Windows ARM64) as an unmeasured target profile (`OPEN`) in `EXTENDED_TARGET_PROFILE` and Chapter 70.
- **`TDateTime = Double` iterative drift (`44-rtl.md` & cross-reference in `07-reals.md`, EN & RU, `DOCUMENTED`):**
  Strengthened the binary-drift note with the concrete iterative accumulation trap (`NextTime := NextTime + EncodeTime(0, 5, 0, 0)`, where `5 min = 1/288` of a day is non-terminating in base 2, breaking exact `=` boundary checks vs integer step counters / ticks / `IncMinute` from an anchor or `SameDateTime` / `CompareDateTime`).
- **Packaging & hygiene fixes:**
  - Synced the short-path Docker `/app/server.py` root-lookup fix into `mcp/local-mcp/server.py` across both Universal Suite and Demo.
  - Redacted two remaining `MCP\verification_130\` build-log path prefixes in `core/evidence/compiler/20261120-followup-130.json` to `<ide-bridge>\verification_130\`.

## v1.0.0 (2026-11-21)

- Initial release of Delphi Behavior Contracts (Universal Suite and Free Evaluation Demo), compiled from research edition `1.5.2`: 74 EN & RU chapters, 89 compiler directive cards, 30 tracked source issues, 879+ live Delphi 13 CE compiler observations, 8 native plugins, 15 pure skill layouts, and local/Cloudflare Workers Code Mode MCP server.
