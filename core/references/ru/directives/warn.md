> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.1** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

# WARN — конкретный класс предупреждений

**Синтаксис:** `{$WARN identifier ON|OFF|ERROR|DEFAULT}`.

**Default в указанном источнике:** страница говорит об enabled warnings; реальные проектные значения уточняют отдельно.

**Scope по документации:** `Local`, с позиции директивы в тексте.

## Точечная фильтрация против `{$WARNINGS}` и ловушка `DEFAULT`

В отличие от подпрограммного [`{$WARNINGS}`](warnings.md), `{$WARN}` настраивает **один конкретный класс предупреждений** по его каноническому ID (`SYMBOL_DEPRECATED`, `COMPARING_SIGNED_UNSIGNED`, `HIDDEN_VIRTUAL`, `IMPLICIT_STRING_CAST` и др.; полный каталог из **`76` проверенных в `Delphi 13 CE` ID** приведён в [главе 41](../chapters/41-directives.md), профили — в [главе 59](../chapters/59-directive-profiles.md)):
- **`ON` / `OFF`** включает или подавляет предупреждение ниже по тексту;
- **`ERROR`** повышает срабатывание этого класса с `Wxxxx` до ошибки компиляции `Exxxx`;
- **`DEFAULT`** возвращает состояние ID из **Project Options (`.dproj` / CLI)**, а не откатывает предыдущий локальный `{$WARN}` в файле; для точного локального отката в Delphi 13 используйте [`{$PUSHOPT}` / `{$POPOPT}`](pushopt-popopt.md).

## Контрасты `P12` / `P15` и ложная аналогия с MSVC

```pascal
// Проверено в P12_Warn_Granular32 / P12_Warn_Error32 (Delphi 13 CE, Win32 Debug)
{$PUSHOPT}
{$WARN SYMBOL_DEPRECATED OFF}
LegacyProc; // предупреждение W1000 подавлено (diags=[], stdout='legacy')
{$POPOPT}
// При {$WARN SYMBOL_DEPRECATED ERROR} -> отказ: E1000 Symbol 'LegacyProc' is deprecated
```

- **Серия `P12` (`Win32 Debug`):** `OFF` в `P12_Warn_Granular32` подавил `W1000` (`diags=[]`, `run_exit = 0`); `ERROR` в `P12_Warn_Error32` остановил сборку кодом **`E1000`**.
- **Серия `P15` (`Win32 Debug`):** `P15_Warn_Ids_Verified32` приняла без `W1030`/`E1030` **все `76/76`** ID (`run_exit = 0`); `COMPARING_SIGNED_UNSIGNED ERROR` дал **`E1023`** (`P15_Warn_SignedUnsigned_Err32`); скрытие `virtual`-метода без `override`/`reintroduce` относится к **`HIDDEN_VIRTUAL`** (**`W1010`** даже под `HIDING_MEMBER ERROR`, **`E1010`** под `HIDDEN_VIRTUAL ERROR`, `0` диагностик под `OFF`), тогда как не-`virtual` `HIDING_MEMBER` дал `0` диагностик.
- **Ложная аналогия (MSVC):** `#pragma warning(default: 4996)` сбрасывает правило к заводскому умолчанию компилятора, а `{$WARN ... DEFAULT}` подтягивает политику проекта.

Источник: [Embarcadero](https://docwiki.embarcadero.com/RADStudio/Florence/en/Warning_messages_(Delphi)). Прочитан 18.11.2026.

Статус: `W1000`/`E1000` подтверждены в `P12`, а каталог `76/76` ID, `E1023` и контраст `HIDDEN_VIRTUAL` (`W1010`/`E1010`) vs `HIDING_MEMBER` — в серии `P15` (`Delphi 13 CE`, `Win32 Debug`).
