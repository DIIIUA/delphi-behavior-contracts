# 39. ABI и взаимодействие с другими языками

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.0** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,359` слов, `120` строк).

## Разделы, разобранные в полной главе

- 1. Соглашения вызова (`calling conventions`) на Win32 и Win64
- 2. Скрытые параметры сигнатуры и живые замеры ABI (серии P3, P7 и P13)
- Точные замеры на живом компиляторе Delphi 13 CE (`37.0.60542.8024`)
- 3. Windows x64 ABI и открытый вопрос `PROGRAM_CONTROL_TARGET_COPY` (`OPEN`)
- 4. Практический чек-лист межъязыковой границы и полный пример
- 5. Границы версий и защита от ложных аналогий
- 6. Первоисточники и статус подтверждения
- Проверка 1.3.0: уточнённые границы
- PROGRAM_CONTROL_TARGET_COPY

## Адресованные темы главы

- `calling conventions`
- `hidden Self parameters`
- `ABI record layout`
- `external memory ownership`
- `C++ HPP interop`
- `exception boundaries`
- `Win32 eligible registers`
- `Windows x64 platform ABI`
- `argument evaluation vs placement`
- `copied target documentation`
- `Embarcadero Win64 assembler scalar contract`
- `RAX versus XMM0 result`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
