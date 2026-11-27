# 42. Условная компиляция и конфигурации

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,457` слов, `119` строк).

## Разделы, разобранные в полной главе

- 1. Условный отбор текста до построения синтаксического дерева
- 2. Закрыватели `{$ENDIF}` vs `{$IFEND}`, `{$INCLUDE}`, `{$IFOPT}` и `{$RESOURCE}`
- Правило терминаторов (`CONDITIONAL_TERMINATOR_WORDING` -> `DOCUMENTED_VERSION_BOUNDARY`)
- Включения `{$INCLUDE}` в пяти позициях грамматики (`INCLUDE_STATEMENT_PART`, `OPEN`)
- Таблица 15 длинных форм `{$IFOPT ...}` (`P13_IfOpt_*`, [`IFOPT_TABLE_TYPOS`](../SOURCE_ISSUES.md#issue-ifopt-table-typos))
- Условные предикаты `{$RESOURCE}` (`RESOURCE_PREDICATE_VERSION`, `OPEN`)
- 3. Два открытых расхождения живого компилятора с документацией `{$IF}` (`OPEN`)
- 1. Необъявленный идентификатор в сравнении (`IF_UNDECLARED_IDENTIFIER_OBSERVATION`, `mismatch 32`, `OPEN`)
- 2. Типизированная константа в `{$IF}` (`IF_TYPED_CONSTANT_OBSERVATION`, `NEGATIVE 09`, `OPEN`)
- 4. Самодостаточный пример
- 5. Границы версий и защита от ложных аналогий
- 6. Первоисточники и статус подтверждения
- Проверка 1.3.0: уточнённые границы
- IF_UNDECLARED_IDENTIFIER_OBSERVATION
- IF_TYPED_CONSTANT_OBSERVATION

## Адресованные темы главы

- `IFDEF IFNDEF`
- `IF ELSEIF`
- `DEFINE UNDEF`
- `IFOPT`
- `predefined conditionals`
- `INC and rebuild`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
