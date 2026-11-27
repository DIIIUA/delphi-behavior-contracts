# 34. Исключения и гарантированная очистка

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,512` слов, `175` строк).

## Разделы, разобранные в полной главе

- Грамматика `try..except`, `try..finally` и `raise`
- Платформенная физика раскрутки стека (`Win32 SEH` против `Win64 PC-mapped`)
- Точка выброса `raise ... at ReturnAddress` и глобальные runtime-хуки (`ExceptProc`, `ErrorProc`, `AssertErrorProc`)
- Владение объектом исключения и живые наблюдения `P5_Exception_AcquireOuter`
- Строгие границы `finally`, запрет `E2126`, `Abort`, `Halt` и `Assert`
- Дополнительный авторский пример (`program ... end.`)
- Границы версий и первоисточники

## Адресованные темы главы

- `try except`
- `on exception handlers`
- `try finally`
- `raise and reraise`
- `raise at`
- `exception ownership`
- `Assert`
- `ReturnAddress ExceptProc ErrorProc AssertErrorProc`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
