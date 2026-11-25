# 72. Inline: объявление, место вызова и сохранение значения

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.1** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,872` слов, `128` строк).

## Разделы, разобранные в полной главе

- 1. Архитектура двухстороннего контроля: `{$INLINE ON|OFF|AUTO}`
- Открытое расхождение документации [`INLINE_DEFAULT_PROFILE`](../SOURCE_ISSUES.md#issue-inline-default-profile) (`OPEN`)
- 2. Физическое доказательство машинного кода в `.text` и `.itext` (`серия P13`)
- 3. `IsConstValue(Expr)` и compile-time ветвление внутри `inline`-подпрограмм
- 4. Когда компилятор отказывается встраивать тело и подсказка `H2443`
- 5. Каскадная пересборка `.dcu` и влияние на стековый кадр
- 6. Самодостаточный проверенный проект и строгая граница доказательства
- 7. Границы версий, таргетов и защита от ложных аналогий
- 8. Первоисточники и статус подтверждения
- Проверка 1.3.0: уточнённые границы
- INLINE_DEFAULT_PROFILE

## Адресованные темы главы

- `inline routine versus compiler option`
- `definition and call-site options`
- `inline AUTO threshold`
- `inlining eligibility`
- `inline value versus generated code`
- `inline dependency rebuild`
- `IsConstValue compile time folding`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
