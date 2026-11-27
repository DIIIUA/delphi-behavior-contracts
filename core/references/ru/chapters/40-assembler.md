# 40. asm, машинный код и платформенные ограничения

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,223` слов, `101` строк).

## Разделы, разобранные в полной главе

- 1. Назначение, синтаксис BASM и платформенный контур
- 2. Критический перелом Win32 vs Win64 (`DCC64`) и псевдооператоры кадра
- 3. Управляемые локальные переменные, unwind и `WIN64_ASSEMBLER_DOC_DETAILS` (`OPEN`)
- Предупреждение о локальных управляемых типах и раскрутке
- Открытый вопрос `WIN64_ASSEMBLER_DOC_DETAILS` (`OPEN`) и живые пробы P3 и P13
- 4. Самодостаточный пример (кросс-архитектурный контур с Pascal-эталоном)
- 5. Границы версий и защита от ложных аналогий
- 6. Первоисточники и статус подтверждения
- Проверка 1.3.0: уточнённые границы
- WIN64_ASSEMBLER_DOC_DETAILS

## Адресованные темы главы

- `asm syntax`
- `assembly expressions and addressing`
- `register ABI`
- `CPU conditionals`
- `external object files`
- `Win64 whole assembler routine`
- `PARAMS PUSHNV SAVENV NOFRAME`
- `NOFRAME and XMM source conflict`
- `assembly cleanup and unwind`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
