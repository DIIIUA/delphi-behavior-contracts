# HPPEMIT — вставка текста в generated C++ header

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

**Синтаксис:** `{$HPPEMIT 'text'}`, `{$HPPEMIT END 'text'}`; специализированные формы: `{$HPPEMIT LINKUNIT 'unitname'}`, а также (с **XE5 Update 2**) `{$HPPEMIT OPENNAMESPACE}`, `{$HPPEMIT CLOSENAMESPACE}`, `{$HPPEMIT NOUSINGNAMESPACE}`.

**Scope по документации:** Local (строки эмитируются в заголовок текущего модуля в порядке их следования в исходнике при активной генерации C++-вывода, например `-JPHNE` / `DCC_CBuilderOutput = JPHNE`).

Эта подробная карточка директивы (`304` слов с замерами компилятора и разбором ловушек) входит в полный набор из 89 карточек платной версии.

В этом DEMO целиком открыты 4 эталонные карточки директив, чтобы оценить глубину проработки:
- [warn.md](warn.md) (`$WARN`)
- [inline.md](inline.md) (`$INLINE`)
- [extendedcompatibility.md](extendedcompatibility.md) (`$EXTENDEDCOMPATIBILITY`)
- [pushopt-popopt.md](pushopt-popopt.md) (`$PUSHOPT` / `$POPOPT`)
