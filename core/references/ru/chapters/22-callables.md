# 22. Процедурные типы и события

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.0** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,267` слов, `106` строк).

## Разделы, разобранные в полной главе

- Три семейства вызываемых типов и их раскладка в памяти
- События Delphi (`OnClick`) — не специальная сущность и не мультикаст
- Асимметрия конверсий и запрет на вложенные процедуры
- Совместимость сигнатур, конвенций вызова и C-callbacks
- Контекст без скобок: вызов против адреса, `@F`, `@@F` и сравнение `TMethod`
- Границы версий и таргетов
- Первоисточники и статус подтверждения

## Адресованные темы главы

- `procedural variable`
- `method pointer of object`
- `callback assignment vs invocation`
- `ABI callable compatibility`
- `procedural expression invocation`
- `at and double-at address`
- `method to method-reference conversion`
- `nested procedure-pointer exclusion`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
