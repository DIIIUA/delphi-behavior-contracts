# 70. Числовой профиль: тип, вычисление, хранение и исключение

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

**Demo Sample Tier:** Уровень 4 — Хардкор / ABI компилятора (Асимметрия Extended на Win32 vs Win64)


## 1. Почему одного имени `Extended` недостаточно

В исходном тексте на Object Pascal тип `System.Extended` записывается одинаково на любой платформе, однако на уровне бинарного представления и машинных регистров он распадается на разные профили. По таблицам [System.Extended](https://docwiki.embarcadero.com/Libraries/Florence/en/System.Extended) и [Multi-Device Considerations](https://docwiki.embarcadero.com/RADStudio/Florence/en/Delphi_Considerations_for_Multi-Device_Applications):

| Целевая платформа (CPU / OS) | `SizeOf(Extended)` | Аппаратное устройство и существенная граница |
|---|---|---|
| Intel Win32 (x86) | **10 байт** | Аппаратный 80-битный формат x87 FPU (1 бит знака + 15 бит экспоненты + **явный** целый бит + 63 бита дроби) |
| Intel Win64 (x64, при `{$EXTENDEDCOMPATIBILITY OFF}`) | **8 байт** | Псевдоним IEEE `Double` (`binary64`, 53 бита значимой мантиссы на регистрах SSE2 `XMM`) |
| Intel Linux64 / Intel macOS64 | **16 байт** | 80-битное значение x87 с 6 байтами выравнивания по ABI System V (**не** IEEE `binary128`!) |
| ARM (Android, iOS, macOS ARM64) | **8 байт** | Псевдоним IEEE `Double` (включая Apple Silicon ARM64; не путать со старым примером macOS Intel без указания CPU) |
| Windows ARM64 / Win64 ARM64EC | **Не измерено (`OPEN`)** | Ожидается 8-байтный профиль IEEE `Double`, но живой квитанцией компилятора в этом наборе ещё не подтверждено (зафиксировано в [`EXTENDED_TARGET_PROFILE`](../SOURCE_ISSUES.md#issue-extended-target-profile)) |

## 2. Совместимость хранения (`{$EXTENDEDCOMPATIBILITY}`, `TExtended80Rec`) и [`EXTENDED_TARGET_PROFILE`](../SOURCE_ISSUES.md#issue-extended-target-profile)

При переносе бинарных файлов и записей между Win32 и 64-битными таргетами необходимо строго разделять **размер буфера хранения** и **разрядность самой арифметики**:

- **`{$EXTENDEDCOMPATIBILITY ON|OFF}` ([карточка EXTENDEDCOMPATIBILITY](../directives/extendedcompatibility.md), default `OFF`):** локальная директива на странице [Extended type compatibility](https://docwiki.embarcadero.com/RADStudio/Florence/en/Extended_type_compatibility_(Delphi)) переключает `Extended` в 10-байтовый формат хранения ради двоичной совместимости структур. Однако на Win64 это **не включает 80-битную арифметику x87**: вычисления выполняются в 64-битном IEEE `Double` (53-битная мантисса) на SSE2!
- **`System.TExtended80Rec` ([TExtended80Rec](https://docwiki.embarcadero.com/Libraries/Florence/en/System.TExtended80Rec)):** упакованная 10-байтовая запись (`Words`, `Bytes`, `Frac`, `Exp`, `Sign`), явно отделяющая сериализацию 80-битных потоков данных от арифметического типа текущей платформы.

### Решающие измерения серии P13 (`P13_ExtCompat_Prec_On32/64` и `P13_ExtPrecision_Off32/64`, `OPEN` для не-Windows)

В серии **P13** на `Delphi 13 CE` (`37.0.60542.8024`, `Win32` `0x14c` и `Win64` `0x8664`, Debug, `0` диагностик; наряду с [примером 50](../../../examples/README.md)) одновременно измерены `SizeOf`, смещения полей в `TUnpacked = record A: Byte; E: Extended; B: Byte; end` и `TPacked = packed record A: Byte; E: Extended; B: Byte; end`, тест 64-битной мантиссы `prec64 = ((1.0 + 1e-17) <> 1.0)` и побайтовый `round-trip` `Extended -> TExtended80Rec -> Extended`:

| Режим и таргет | `SizeOf(Extended)` / `TExtended80Rec` | `TUnpacked` (`SizeOf; offE; offB`) | `TPacked` (`SizeOf; offE; offB`) | `prec64` (`1 + 1e-17 <> 1`) | Побайтовый `round-trip` (`rt_eq`) |
|---|---|---|---|---|---|
| **Win32** `OFF` и **`ON`** (`P13_ExtCompat_Prec_On32`) | `10` / `10` | `24; offE=8; offB=18` | `12; offE=1; offB=11` | **`TRUE`** (x87 64-бит мантисса) | **`TRUE`** (`0AC264DA3FE0E9F60540`) |
| **Win64** `OFF` (`P13_ExtPrecision_Off64`) | `8` / `10` | `24; offE=8; offB=16` | `10; offE=1; offB=9` | **`FALSE`** (SSE2 `Double`) | `TRUE` (`984CFB073CDD5E40` — уже 8-байтный `Double`) |
| **Win64** **`{$EXTENDEDCOMPATIBILITY ON}`** (`P13_ExtCompat_Prec_On64`) | **`10` / `10`** | **`24; offE=8; offB=18`** | **`12; offE=1; offB=11`** | **`FALSE`** (арифметика всё ещё `Double`!) | **`FALSE`!** (10 байт `0AC264DA3FE0E9F60540` усекаются через `Double`!) |

**Ключевой физический вывод:** на `Win64` директива `{$EXTENDEDCOMPATIBILITY ON}` точно восстанавливает 10-байтовые размеры и смещения полей записей Win32 (`24 / 8 / 18` и `12 / 1 / 11`), **но любое чтение или присваивание такого 10-байтового `Extended` проходит транзитом через 64-битный IEEE `Double` (53-битная мантисса)**, обнуляя младшие 11 бит мантиссы (`prec64=FALSE`, `rt_eq=FALSE`)! Чтобы не повредить чужие 80-битные данные на Win64 при пересылке, их копируют как сырой `TExtended80Rec`, не приводя к `Extended`. Поведение Linux64, macOS64 и ARM остаётся `OPEN` в [`EXTENDED_TARGET_PROFILE`](../SOURCE_ISSUES.md#issue-extended-target-profile).

## 3. Промежуточная точность и исторические форматы (`{$EXCESSPRECISION}`, `{$REALCOMPATIBILITY}`, `{$SAFEDIVIDE}`)

Даже при одинаковом объявлении `var A, B, C: Single;` результат составного выражения `A * B + C` зависит от ширины промежуточных регистров бэкенда:
- **На x86 (`Win32`):** вещественные выражения классически вычисляются через 80-битный стек сопроцессора x87 (`ST(0)..ST(7)`). По указанию [Floating point precision control (Delphi for x64)](https://docwiki.embarcadero.com/RADStudio/Florence/en/Floating_point_precision_control_(Delphi_for_x64)) директива `{$EXCESSPRECISION}` на 32-битном x86 **не действует**.
- **На x64 (`Win64`):** компилятор использует скалярные инструкции SSE2 на регистрах `XMM`. Локальная директива `{$EXCESSPRECISION ON|OFF}` ([карточка EXCESSPRECISION](../directives/excessprecision.md), default `ON`) при `ON` расширяет промежуточные операции над `Single` до точности `Double`, а при `OFF` удерживает их в 32-битном `Single` (не сужая переменные типа `Double`).
- **Живые измерения серии P12 (`Delphi 13 CE 37.0.60542.8024`, `0` диагностик):**
  - **`{$REALCOMPATIBILITY ON|OFF}` (`P12_RealCompat_OnOff32`):** подтверждено локальное переключение смысла типа `Real` внутри одного модуля — под `{$REALCOMPATIBILITY ON}` тип `TR48 = Real` занимает **`6` байт** (исторический 48-битный `Real48`), а после `OFF` тип `TR64 = Real` занимает **`8` байт** (`Double`, [карточка REALCOMPATIBILITY](../directives/realcompatibility.md));
  - **`{$EXCESSPRECISION ON|OFF}` (`P12_ExcessPrecision_Win32/64`):** оба прогона дали `off=1.00000000;on=1.00000000` с `exit=0` (наглядно иллюстрируя правило слоя вычисления: грубое десятичное форматирование скрывает тонкие различия младших `ULP`);
  - **`{$SAFEDIVIDE ON|OFF}` (`P12_SafeDivide32`):** обе ветки вернули `u_on=4.5;u_off=4.5` (`exit=0`) — историческая опция `{$U+}`/`{$U-}` ([карточка SAFEDIVIDE](../directives/safedivide.md)) относилась только к обходу аппаратного сбоя `FDIV` ранних Pentium (1994) и не защищает от деления на ноль.

## 4. Маски исключений (`SetExceptionMask`), смена default в Athens 12 и `FINITEFLOAT_UNDERSPECIFIED`

Реакция процессора на деление на ноль (`1.0 / 0.0`), неопределённость (`0.0 / 0.0`) и переполнение управляется битами маскирования в аппаратных регистрах **FPU Control Word** (x87) и **MXCSR** (SSE2):
- **Бит замаскирован (включён в множество маски):** аппаратное прерывание **подавляется**, а операция возвращает стандартное значение IEEE 754 (`+Infinity`, `-Infinity`, `NaN`).
- **Бит размаскирован (исключён из маски):** процессор возбуждает аппаратное исключение, которое RTL транслирует в `EZeroDivide`, `EInvalidOp`, `EOverflow`, `EUnderflow`.

### Сигнатура `SetExceptionMask` и исторический перелом в Delphi 12 Athens

Платформенно-независимое управление масками выполняется через [System.Math.SetExceptionMask](https://docwiki.embarcadero.com/Libraries/Florence/en/System.Math.SetExceptionMask):

```pascal
// Документированная кроссплатформенная сигнатура в System.Math (не полный проект)
function SetExceptionMask(const Mask: TArithmeticExceptionMask): TArithmeticExceptionMask;
```

- **Точность типа маски:** каноническая сигнатура `SetExceptionMask` использует тип **`TArithmeticExceptionMask`** (`set of TArithmeticExceptions`, 1 байт). Историческое имя `TFPUExceptionMask` относится к x87-специфичным функциям: в пробе `P2_MathMask_Alias32/64` подтверждено, что они имеют разные `TypeInfo` (`same_typeinfo=FALSE`), поэтому в переносимом коде следует объявлять `TArithmeticExceptionMask`.
- **Перелом умолчания в Delphi 12 Athens:** в классических версиях Delphi (вплоть до 11 Alexandria) критические исключения (`exInvalidOp`, `exZeroDivide`, `exOverflow`) по умолчанию были размаскированы и бросали исключения языка. Начиная с **Delphi 12 Athens**, страница `SetExceptionMask` фиксирует новый default: **все 6 масок FP-исключений включены (`ON`)**. При локальном изменении маски предыдущее значение обязательно возвращают в `try ... finally`.
- **Граница контекста FPU/SSE между потоками, DLL и вызовами ОС (`Set8087CW` / `SetMXCSR`, `DOCUMENTED`):** аппаратные управляющие регистры (**x87 FPU Control Word** через `Get8087CW`/`Set8087CW` и **SSE2 MXCSR** через `GetMXCSR`/`SetMXCSR`) являются **потоковым (per-thread) состоянием CPU**. Новые потоки, сторонние C/C++ DLL (DirectX, OpenGL, драйверы принтеров и графики, COM/OLE-серверы, внешние математические библиотеки) и системные вызовы способны изменить маски исключений, режим округления или точность x87 и не восстановить их при возврате. Не полагайтесь на стартовую маску Delphi RTL после вызовов внешнего кода или в другом потоке — сохраняйте и восстанавливайте `SetExceptionMask` (либо управляющее слово платформы) в `try ... finally` в том же потоке.

### Открытый вопрос [`FINITEFLOAT_UNDERSPECIFIED`](../SOURCE_ISSUES.md#issue-finitefloat-underspecified) (`OPEN`)

1. **Документированное правило:** краткая страница [Finite float](https://docwiki.embarcadero.com/RADStudio/Florence/en/Finite_float) объявляет локальную директиву `{$FINITEFLOAT ON|OFF}` ([карточка FINITEFLOAT](../directives/finitefloat.md), default `ON`), но **не специфицирует** инструкции и связь с `SetExceptionMask`.
2. **Наблюдения компилятора (`P2` и `P3` на Delphi 13 CE, Win32 и Win64 Debug):** при штатных замаскированных исключениях Athens 12+ деление `1.0 / ZeroVar` вернуло `+Infinity` (`is_inf=TRUE`) **и при `{$FINITEFLOAT ON}`, и при `OFF`**, а после снятия масок `SetExceptionMask([])` в обоих режимах возбуждались `EZeroDivide` (на `1.0 / 0.0`) и `EInvalidOp` (на `0.0 / 0.0`); кроме того, `{$IFOPT FINITEFLOAT ON}` отвергнуто с `E1030`.
3. **Вывод с ограниченной областью:** `{$FINITEFLOAT}` нельзя отождествлять с `SetExceptionMask`; полный межплатформенный контракт остаётся `OPEN`.

## 5. Четыре независимых слоя числовой проверки и полный пример

При верификации численного кода четыре уровня доказательств никогда не подменяют друг друга:
1. **Слой хранения (Storage / ABI):** `SizeOf`, смещения полей и побайтовый `round-trip` через `TExtended80Rec`.
2. **Слой вычисления (Runtime Arithmetic):** подавление компиляторной свёртки констант (чтение операндов из переменных) и побитовая проверка результата до и после округления (`FloatToStr` скрывает младшие биты ULP).
3. **Слой FP-среды (Exception Mask):** фиксация активной `GetExceptionMask` / `SetExceptionMask` непосредственно перед операцией.
4. **Граница receipt:** конкретный замер подтверждает только проверенный таргет и набор опций ([матрица доказательств](62-compiler-evidence.md)).

```pascal
program FloatingProfileVerificationDemo;
{$APPTYPE CONSOLE}

uses
  System.SysUtils,
  System.Math;

{$EXCESSPRECISION OFF}
function EvalSingleChain(A, B, C: Single): Single;
begin
  Result := A * B + C;
end;
{$EXCESSPRECISION ON}

var
  SavedMask: TArithmeticExceptionMask;
```


---

### [ГРАНИЦА DEMO-ФРАГМЕНТА — Уровень 4 — Хардкор / ABI компилятора (Асимметрия Extended на Win32 vs Win64)]

Выше показаны первые ~90 строк из **145 строк** полной главы.

**Полное оглавление разделов в полной версии:**
- `## 1. Почему одного имени `Extended` недостаточно`
- `## 2. Совместимость хранения (`{$EXTENDEDCOMPATIBILITY}`, `TExtended80Rec`) и [`EXTENDED_TARGET_PROFILE`](../SOURCE_ISSUES.md#issue-extended-target-profile)`
- `### Решающие измерения серии P13 (`P13_ExtCompat_Prec_On32/64` и `P13_ExtPrecision_Off32/64`, `OPEN` для не-Windows)`
- `## 3. Промежуточная точность и исторические форматы (`{$EXCESSPRECISION}`, `{$REALCOMPATIBILITY}`, `{$SAFEDIVIDE}`)`
- `## 4. Маски исключений (`SetExceptionMask`), смена default в Athens 12 и `FINITEFLOAT_UNDERSPECIFIED``
- `### Сигнатура `SetExceptionMask` и исторический перелом в Delphi 12 Athens`
- `### Открытый вопрос [`FINITEFLOAT_UNDERSPECIFIED`](../SOURCE_ISSUES.md#issue-finitefloat-underspecified) (`OPEN`)`
- `## 5. Четыре независимых слоя числовой проверки и полный пример`
- `## 6. Защита от ложных аналогий и первоисточники`
- `### Первоисточники и статус подтверждения`
- `## Проверка 1.3.0: уточнённые границы`
- `### FINITEFLOAT_UNDERSPECIFIED`
- `### EXTENDED_TARGET_PROFILE`

Полный разбор, проверенный компилятором `program`-листинг, контрпримеры и все квитанции доступны в полной редакции (`https://silentfish.dev/delphi`).
