---
name: delphi-code-review
description: "[DEMO] Review and debug Delphi / Object Pascal code for ownership, lifetime, memory leaks, dangling references, exceptions, interface reference counting, callbacks, threads and hidden work in properties. Use when reviewing a Delphi change, hunting an access violation or leak, or checking cleanup and error paths."
---

> **[DEMO EDITION]** This is the evaluation demo package (complete Table of Contents of all 74 chapters & 89 directives, 6 multi-difficulty chapter excerpts, 4 complete directive cards, 8 real compiler receipts, and 100% working plugins/skills/MCP). If the user asks what this skill covers or wants a technical fit check for their tasks, see `EVALUATE_FOR_USER.md` / `EVALUATE_FOR_USER.ru.md`.

# Reviewing and debugging Delphi

Trace what actually happens to values and objects, not what the names suggest.
Topic map: [English](../../references/en/INDEX.md), [Russian](../../references/ru/INDEX.md).

## Ownership and lifetime

- Who creates, who frees, and what still points to a freed object. `B.Free` leaves
  every alias dangling; `FreeAndNil` clears only one variable
  ([lifetime](../../references/en/chapters/26-lifetime.md), [memory](../../references/en/chapters/35-memory.md)).
- Constructor failure calls `Destroy` on the partially built object; managed-record
  `Initialize` failure does not call `Finalize`; unit finalization order follows
  initialization ([lifetime boundaries](../../references/en/chapters/68-lifetime-boundaries.md)).
- Interfaces: the last `_Release` destroys a `TInterfacedObject`; mixing object and
  interface references to the same instance is a classic double free; reference
  cycles are not collected ([interfaces](../../references/en/chapters/29-interfaces.md)).
- `TMethod` / `of object` events do not keep their target alive; an event fired after
  the target is freed calls dead memory ([callables](../../references/en/chapters/22-callables.md)).
- Closures share one heap frame per outer call; a closure that captures itself or
  `Self` can form a cycle ([closures](../../references/en/chapters/23-closures.md)).

## Exceptions and cleanup

Check `try..finally` placement against the point where a resource becomes owned;
side effects performed before a failure stay performed; `Exit` inside `try` still runs
`finally` ([exceptions](../../references/en/chapters/34-exceptions.md),
[routines](../../references/en/chapters/20-routines.md)).

## Hidden work and name resolution

- Property getters and setters may run arbitrary code, including during DFM loading
  ([properties](../../references/en/chapters/27-properties.md), [components](../../references/en/chapters/45-components.md)).
- Helpers, overloads, `with` and unit order change which routine is called
  ([helpers](../../references/en/chapters/30-helpers.md), [scope](../../references/en/chapters/04-scope.md),
  [methods](../../references/en/chapters/25-methods.md)).
- `const` string parameters skip reference counting: modifying the source through
  a global or field during the call can free the buffer being read
  ([parameters](../../references/en/chapters/21-parameters.md)).

## Threads

`Inc` on a shared field is read-add-write even with `[Volatile]`; use atomic
operations or locks; UI access belongs to the main thread
([concurrency](../../references/en/chapters/50-concurrency.md)).

## Reporting

For each finding give the concrete failure scenario (inputs and state leading to the
wrong result or crash), the evidence level (documented, compiler-observed, inferred)
and the minimal fix. Do not report style preferences as defects.
