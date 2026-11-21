# 65. Delphi unit, C++ header и object-код

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.0** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,205` слов, `102` строк).

## Разделы, разобранные в полной главе

- 1. Четыре артефакта межъязыковой поставки для C++Builder
- 2. Эталонный модуль `HeaderContract.pas`, ключи `DCC32` и инспекция `.hpp`/`.obj` (`P5` + `P12`)
- 1. Модуль контракта ([`HeaderContract.pas`](../../../examples/README.md)) и ключи генерации
- 2. Полная 6-вариантная матрица `NOINCLUDE` (`P5` и `P12_NoInc_*`, `OPEN`)
- 3. Прямая инспекция `.hpp` и `.obj` для `EXTERNALSYM`, `NODEFINE`, `OBJTYPENAME`, `OBJEXPORTALL` (`P12`)
- 3. Что НЕ исправляется правкой `.hpp` и граница Custom Managed Records
- 4. Самодостаточный пример (идентичность `= type` на стороне Delphi)
- 5. Границы версий и защита от ложных аналогий
- 6. Первоисточники и статус подтверждения
- Проверка 1.3.0: уточнённые границы
- NOINCLUDE_MATCHING_PROFILE

## Адресованные темы главы

- `HPP vs object symbols`
- `NODEFINE manual type`
- `HPPEMIT namespace`
- `alias vs distinct mangling`
- `producer consumer validation`
- `DCC32 JL package generation`
- `DCC32 JPHNE unit generation`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
