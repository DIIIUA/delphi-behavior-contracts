# 71. От исходника до наблюдаемой программы

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.2** (полный корпус: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы можно было проверить технический охват и офлайн-работу инструмента на ваших задачах по Delphi. Страница проекта: https://silentfish.dev/delphi

Эта глава **входит полностью в платную редакцию** (`1,171` слов, `91` строк).

## Разделы, разобранные в полной главе

- 1. Дерево конфигураций `.dproj` / MSBuild и среда сборки
- 2. Архитектура хост-компилятора против целевой платформы (`Host` vs `Target`) и фазы конвейера
- 3. Слои отладочной информации и точная побайтовая лестница `.dcu` (`P12_Dcu_*`)
- Прямое побайтовое измерение слоёв `DbgProbeU.dcu` и `{$D0}`/`{$D1}`/`{$D2}` (`серия P12`, Win32)
- 4. Четыре уровня свидетельств в исследовании языка
- 5. Самодостаточный пример
- 6. Границы версий и защита от ложных аналогий
- 7. Первоисточники и статус подтверждения

## Адресованные темы главы

- `build configuration inheritance`
- `compile versus link`
- `resource resolution stage`
- `debug information layers`
- `numeric debug modes unresolved`
- `package target naming`
- `consumer and loader acceptance`
- `DCC host versus target architecture`
- `DCC32 V debug suboptions`
- `MSBuild configuration and environment`

## Где посмотреть реальную глубину прямо в этом DEMO?

Откройте 6 разноуровневых фрагментов, включённых в этот демо-пакет:
- Уровень 1 (Базовая ловушка): [10-arrays.md](10-arrays.md)
- Уровень 2 (Средний): [13-managed-records.md](13-managed-records.md)
- Уровень 3 (Продвинутый): [31-generics.md](31-generics.md) и [41-directives.md](41-directives.md)
- Уровень 4 (Хардкор ABI и эволюция): [70-floating-profiles.md](70-floating-profiles.md) и [73-evolution-old-to-new.md](73-evolution-old-to-new.md)
