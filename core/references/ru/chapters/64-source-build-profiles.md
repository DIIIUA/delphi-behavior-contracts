# 64. Как читается профиль исходника

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,504` слов, `117` строк).

## Разделы, разобранные в полной главе

- 1. Три непересекающихся пространства состояния в одном файле
- 2. Граница `unit`, восстановление `-D` и 6 живых позиций `{$INCLUDE}` (`P1` и `P13`)
- 3. Проектный `-$H-` в `.dproj` (`P13`), матрицы `{$IF}` (`P13`) и `CODEPAGE`
- 4. Самодостаточный пример
- 5. Границы версий и защита от ложных аналогий
- 6. Первоисточники и статус подтверждения
- Проверка 1.3.0: уточнённые границы
- RANGECHECKS_DEFAULT_PROFILE
- INCLUDE_STATEMENT_PART
- CODEPAGE_SOURCE_FORM_UNCONFIRMED
- DEBUGINFO_PROFILE_DEPTH

## Адресованные темы главы

- `conditional symbols vs declarations`
- `unit define reset`
- `include support files`
- `typed constant in compile IF`
- `CODEPAGE classification`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
