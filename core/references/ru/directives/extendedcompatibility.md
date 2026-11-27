> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

# EXTENDEDCOMPATIBILITY — представление совместимости Extended

**Синтаксис:** `{$EXTENDEDCOMPATIBILITY ON}` или `{$EXTENDEDCOMPATIBILITY OFF}`.

**Default в указанном источнике:** `OFF`.

**Scope по документации:** Local (применяется к последующим объявлениям типов и данных с `Extended`).

Директива управляет **бинарным размером хранения** типа [`System.Extended`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.Extended) на платформах, где по умолчанию `Extended` сжат до 8-байтного IEEE-754 `Double` (`Win64` SSE2 и `ARM`, см. [Multi-Device Considerations](https://docwiki.embarcadero.com/RADStudio/Florence/en/Delphi_Considerations_for_Multi-Device_Applications); на `Win32` x87 `Extended` всегда 10 байт, на `Linux64` по System V ABI — 16 байт; [глава 07](../chapters/07-reals.md), [глава 70](../chapters/70-floating-profiles.md)):
- при **`OFF`** на `Win64` `Extended` занимает `8` байт (`Double`);
- при **`ON`** на `Win64` компилятор выделяет **10 байт** (раскладка [`TExtended80Rec`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.TExtended80Rec)), **но НЕ включает 80-битную арифметику x87**: вычисления идут в точности 64-битного IEEE `Double` (53-битная мантисса)!

```pascal
{$EXTENDEDCOMPATIBILITY ON}
// Win32: SizeOf(Extended)=10, prec64=TRUE, round-trip TExtended80Rec=TRUE
// Win64: SizeOf(Extended)=10, но prec64=FALSE (SSE2) и round-trip TExtended80Rec=FALSE!
```

**Живые измерения (`Delphi 13 CE 37.0.60542.8024`, [проход 0.11](../research/COMPILER_PASS_011.md) и `P13`):**

| Проба / режим | `SizeOf` | `Unpacked` / `Packed` `(Byte, Extended, Byte)` | `prec64` (`1+1e-17<>1`) и round-trip |
|---|---|---|---|
| `OFF` `Win32` ([пример 50](../../../examples/README.md), `P13_ExtPrecision_Off32`) | `10` | `24 (E:8,B:18)` / `12 (E:1,B:11)` | `prec64=TRUE`, `rt_eq=TRUE` |
| `OFF` `Win64` (`P13_ExtPrecision_Off64`) | `8` | `24 (E:8,B:16)` / `10 (E:1,B:9)` | `prec64=FALSE`, `rt_eq=TRUE` (`8B`) |
| **`ON` `Win32`** (`P13_ExtCompat_Prec_On32`) | `10` | `24 (E:8,B:18)` / `12 (E:1,B:11)` | `prec64=TRUE`, `rt_eq=TRUE` |
| **`ON` `Win64`** (`P2_ExtCompat_On64`, `P13_ExtCompat_Prec_On64`) | **`10`** | **`24 (E:8,B:18)` / `12 (E:1,B:11)`** | **`prec64=FALSE`, `rt_eq=FALSE`** |

**Ложная аналогия:** в отличие от C `long double` на Linux x86-64, на `Win64` конверсия через `Double` теряет младшие биты мантиссы (`EXTENDED_TARGET_PROFILE` = `OPEN` для не-Windows целей).

Источник: [Embarcadero](https://docwiki.embarcadero.com/RADStudio/Florence/en/Extended_type_compatibility_(Delphi)). Прочитан 18.11.2026.

Статус: сверено с документацией; размеры, смещения полей, `prec64=FALSE` и `rt_eq=FALSE` при `ON` на `Win64` измерены в [примере 50](../../../examples/README.md), `P2_ExtCompat_*` и `P13_ExtCompat_Prec_*`.

## Проверка 1.3.0: уточнённые границы

**EXTENDED_TARGET_PROFILE — PARTIALLY_RESOLVED.** На ARM32/64 compile-time SizeOf: OFF=8, ON=10, packed запись=12, обычная=24. Это размер хранения, не точность вычислений. Добавлены DLL producer/consumer ON/OFF на Win32/64 с согласованными типами и отдельным временем жизни до FreeLibrary.

Область: Windows DLL-пробы и compile-only ARM layout; прежние Windows precision/round-trip сохранены. Остаток: Для ARM precision/rounding/runtime ABI нужен Android-девайс или настроенный эмулятор с harness; для Linux/macOS — соответствующий лицензированный Delphi compiler, SDK/PAServer и принимающий runtime. Другие ABI-signatures требуют отдельного producer/consumer, а не SizeOf.

[Все 23 результата](../research/RESIDUE_23_130.md); [компиляторная квитанция](../../../evidence/compiler/demo-sample-receipts.json).
