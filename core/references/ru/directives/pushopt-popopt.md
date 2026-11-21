> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.0** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

# PUSHOPT / POPOPT — сохранение и восстановление опций

**Синтаксис:** `{$PUSHOPT} ... {$POPOPT}`.

**Default в указанном источнике:** команды стека опций компилятора; собственного ON/OFF default нет.

**Scope по документации:** `Local` (LIFO-стек внутри текущего модуля).

## Механизм стека опций и открытия серий `P2`–`P3` (`0.11`)

Директивы введены в **Delphi 13 Florence** для локального изменения переключателей (`{$R-}`, `{$Q-}`, `{$J+}`, `{$O-}`, `{$WARNINGS ...}`) с точным возвратом исходного профиля без громоздких проверок `{$IFOPT}` ([пример 29](../../../examples/README.md), `0.8`: `on`, `off`, `on`; [глава 41](../chapters/41-directives.md), [глава 59](../chapters/59-directive-profiles.md)). Вложенные пары работают по принципу LIFO, но **не** сохраняют символы `{$DEFINE}`/`{$UNDEF}`, `.inc`-поток или состояние переменных.

Комментарий «ВЕСЬ стек опций целиком» в сохранённом исходнике ниже неточен: `POPOPT` восстанавливает верхний снимок; нижние снимки остаются в стеке. Сам исходный код сохранён для совпадения с компиляторным свидетельством.

```pascal
// Проверено в P2_PushOpt_Sel_Effect и P3_PushOpt_Discriminate (Delphi 13 CE 37.0)
{$PUSHOPT RANGECHECKS} // хвостовой аргумент не сужает снимок!
  {$R-}{$Q+}
{$POPOPT} // восстанавливает ВЕСЬ стек опций целиком: after_pop R=ON, Q=OFF
```

Живые эксперименты **серий `P2` и `P3`** ([COMPILER_PASS_011](../research/COMPILER_PASS_011.md)) выявили две критические границы:
1. **Полный откат вместо выборочного (`PUSHOPT_TABLE_TYPOS`, статус `OPEN`):** несмотря на упоминание именованных аргументов и опечатки `IMPOTEDDATA` / `FINITEFLOATT` в таблице *Option OPT*, в пробах `P2_PushOpt_Sel_Effect` и `P3_PushOpt_Discriminate` вызов `{$POPOPT}` откатил **все изменённые опции целиком (`R=ON; Q=OFF`)**.
2. **Тихое игнорирование опечаток:** пробы `P3_PushOpt_Bogus` (`BOGUS_OPT`), `P3_PushOpt_Typo1` (`FINITEFLOATT`) и `P3_PushOpt_Typo2` (`IMPOTEDDATA`) скомпилировались с **`0` диагностик** (в отличие от `{$IFOPT}`, где опечатки сразу вызвали `E1030`). Семь редких имён таблицы отдельно разобраны в [`EXTRA_DIRECTIVES_NOT_REVIEWED`](../SOURCE_ISSUES.md#issue-extra-directives-not-reviewed) ([EXTRA_OPTIONS.md](../research/EXTRA_OPTIONS.md)).

## Защита от ложных аналогий

В отличие от MSVC `#pragma warning(push/pop)`, сохраняющей только предупреждения, `{$PUSHOPT}` фиксирует и кодогенерационные проверки; в отличие от Free Pascal `{$PUSH}`/`{$POP}`, в Delphi 13 используется строго `{$PUSHOPT}`/`{$POPOPT}` — пишите их **без аргументов** ([SOURCE_ISSUES](../SOURCE_ISSUES.md#issue-pushopt-table-typos)).

Источник: [Embarcadero](https://docwiki.embarcadero.com/RADStudio/Florence/en/Option_OPT_(Delphi)). Прочитан 18.11.2026.

Статус: полный стековый откат и игнор хвостовых имён подтверждены в `0.8` и `P2`–`P3` (`Delphi 13 CE`); `PUSHOPT_TABLE_TYPOS` остаётся `OPEN`.

## Проверка 1.3.0: уточнённые границы

**PUSHOPT_TABLE_TYPOS — PARTIALLY_RESOLVED.** Вложенный include восстанавливает R/Q по стеку. Несогласованный PUSHOPT даёт W1079, POPOPT — W1078 на Win32/64. Прежние хвосты BOGUS_OPT/FINITEFLOATT принимались, но восстанавливался весь набор, поэтому это не доказательство selective subset.

Область: Вложенный стек, include и дисбаланс текущего Windows профиля. Остаток: Для selective subset нужны официальная точная грамматика/исправление Option OPT или пример Embarcadero с отличимым частичным восстановлением и version-matched compiler. Принятие игнорируемого хвоста ответом не является.

[Все 23 результата](../research/RESIDUE_23_130.md); [компиляторная квитанция](../../../evidence/compiler/demo-sample-receipts.json).
