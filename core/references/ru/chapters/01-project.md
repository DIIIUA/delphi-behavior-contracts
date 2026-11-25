# 01. Программа, модуль и единица сборки

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.1** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,708` слов, `177` строк).

## Разделы, разобранные в полной главе

- Структура единиц компиляции: `program`, `unit` и контракт `.dcu`
- Граф `uses`: видимость, циклы и разрешение конфликтующих имён
- Порядок `initialization` / `finalization` и частичная инициализация
- Самодостаточный проверенный проект жизненного цикла модулей
- Контракт частичной инициализации и особые границы завершения
- Unit Scope Names (`-NS`), Aliases (`-A`), Search Paths (`-U`) и вопрос `NAMESPACE_LEGACY_AGGREGATION`
- Открытый вопрос [`NAMESPACE_LEGACY_AGGREGATION`](../SOURCE_ISSUES.md#issue-namespace-legacy-aggregation) (`OPEN`) и защита от ложных аналогий
- Первоисточники и статус подтверждения

## Адресованные темы главы

- `program DPR`
- `unit interface implementation`
- `uses and namespaces`
- `initialization finalization`
- `unit cycles`
- `DCU and search paths`
- `unit partial initialization`
- `uses name resolution`
- `unit scope prefixes`
- `unit aliases`
- `qualified name and selected file`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
