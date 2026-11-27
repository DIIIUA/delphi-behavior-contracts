# 32. Ограничения generics

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,323` слов, `146` строк).

## Разделы, разобранные в полной главе

- Грамматика и семь видов ограничений
- Фабрика `class, constructor` (`46-constructor-constraint.dpr`)
- `T: IFoo` против `T: IFoo, interface` в Delphi 13.0 Florence (`E2667`)
- Граница `record` против `unmanaged` (`P1` и `RECORD_CONSTRAINT_MANAGED_BOUNDARY` — выбранный профиль закрыт)
- L-value приведения для обобщённых значений в Delphi 13
- Дополнительный авторский пример (`program ... end.`)
- Защита от ложных аналогий (C# / Java / C++)
- Границы версий и первоисточники
- Проверка 1.3.0: уточнённые границы
- RECORD_CONSTRAINT_MANAGED_BOUNDARY

## Адресованные темы главы

- `type constraints`
- `class constraint`
- `record constraint`
- `constructor constraint`
- `interface constraint`
- `unmanaged constraint`
- `generic Lvalue casts`
- `constraint parameter grouping`
- `simple type constraint exclusion`
- `managed record constraint ambiguity`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
