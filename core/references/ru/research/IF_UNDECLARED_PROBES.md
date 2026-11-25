# Необъявленное имя в $IF: измерения редакции 0.9

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.1** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi


Проверено на Delphi13 Community, IDE37.0.60542.8024, CompilerVersion37.0,
Win32 Debug и Win64 Debug. Это наблюдения двух маленьких программ;
ожидаемый stdout заранее не назначался. Диагностика IDE:0 errors/0 warnings.
PE machine и SizeOf(Pointer) подтвердили разные targets.

| Случай | Win32 | Win64 |
|---|---|---|
| IF Unknown > 5 без ELSE | true-ветка исполнена | true-ветка исполнена |
| IF Unknown > 5 с ELSE | true-ветка исполнена | true-ветка исполнена |
| IF Declared(Unknown) | False | False |
| IF Declared(Unknown) and (Unknown > 5) | False | False |
| Вложенный IF Unknown > 5 внутри IF Declared(Unknown) | Внешняя ELSE:missing | Внешняя ELSE:missing |
| IF KnownValue > 5, KnownValue=2 | False | False |
| IF KnownValue=2 | True | True |
| IF Unknown без сравнения | False | False |

Неизвестное имя здесь — NoSuchBookConstant009, которое не объявлено в
исходниках. То,что Declared вернул False,также наблюдено в тех же сборках.
Расхождение из примера32 воспроизвелось даже без ELSE и на обеих архитектурах.
Оно не сводится к тому,что любое неизвестное имя всегда True: отдельное

---

*(Full research pass report is included in the full edition.)*
