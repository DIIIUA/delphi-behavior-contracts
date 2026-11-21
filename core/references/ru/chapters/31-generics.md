# 31. Обобщённые типы и методы

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.0** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

**Demo Sample Tier:** Уровень 3 — Продвинутый (Дженерики, generic-методы, HasWeakRef / GetTypeKind / E2533)


Обобщения (*generics*, введены в **Delphi 2009**, [Declaring Generics](https://docwiki.embarcadero.com/RADStudio/Florence/en/Declaring_Generics)) позволяют параметризовать классы, записи, интерфейсы, динамические массивы, процедурные типы и методы формальными параметрами типа. Внутри собственного объявления `TBox<T>` выступает как **открытая форма**, а после подстановки конкретного типа (`TBox<Integer>`, `TBox<string>`) порождает **закрытую специализацию** (*constructed type*) со своей физической раскладкой и собственными классовыми данными.

## Физика специализаций против стирания типов и шаблонов C++

Обобщения в Delphi принципиально отличаются как от модели стирания типов в Java (*type erasure*), так и от текстово-утиной инстанциации шаблонов в C++:

1. **Проверка тела в точке объявления (против C++ `template`).** Компилятор проверяет открытое тело `TBox<T>` один раз против объявленных ограничений ([глава 32](32-constraints.md)). Без ограничений `T` трактуется как непрозрачное значение: его можно хранить, копировать через `:=`, передавать и возвращать, но нельзя вызывать `T.Create`, складывать `A + B`, сравнивать `A = B` или обращаться к неподтверждённым членам.
2. **Настоящие раздельные типы в бинарном коде (против Java).** Каждая закрытая специализация получает собственное представление времени выполнения:
   - **Раскладка памяти:** поле `Value: T` занимает ровно `SizeOf(T)` байт с выравниванием `T`, поэтому `TBox<Byte>` и `TBox<Int64>` имеют разный `InstanceSize`.
   - **Таблица управляемых полей:** если аргумент `T` управляемый (`string`, `IInterface`, динамический массив, CMR), данная специализация получает собственную `vmtInitTable`, автоматически зануляющую и финализирующую поле `Value` ([глава 35](35-memory.md)).
   - **Раздельные `class var`:** у каждой закрытой специализации выделяется **собственная независимая ячейка статических данных** ([Class Variable in Generics](https://docwiki.embarcadero.com/RADStudio/Florence/en/Class_Variable_in_Generics)). За счёт кодогенерации для каждой специализации большое число закрытых инстанциаций увеличивает объём `.dcu` и исполняемого файла.

### Compile-time intrinsics оптимизации специализаций: `GetTypeKind(T)`, `IsManagedType(T)`, `HasWeakRef(T)`

Внутри тела обобщённого типа или метода доступны выражения этапа компиляции `SizeOf(T)`, `Default(T)`, `TypeInfo(T)`, а начиная с **Delphi XE7** — компиляторные интринсики `GetTypeKind(T)`, `IsManagedType(T)` и `HasWeakRef(T)`. Поскольку в каждой закрытой специализации их результат константен, ветки вида `if IsManagedType(T) then ...` сворачиваются на этапе компиляции без накладных расходов перехода во время выполнения. Выражение `Default(T)` возвращает нулевое значение типа (`0`, `False`, `nil`, `''`, обнулённую запись), а присваивание `Value := Default(T)` для управляемого `T` штатно освобождает прежний строковый буфер или интерфейс.

В сериях живых проб **`P15_Intrinsics_TypeMeta32_V2` / `64_V2`** (`Win32` `0x14c` и `Win64` `0x8664`, `0` диагностик, `exit=0`) и **`P15_HasWeakRef_*`** (`Win32` Debug, `0` диагностик) измерены выбранные типы. Колонка `System.HasWeakRef` ниже исправлена отдельными пробами редакции 1.2.0; старое обобщение диагностики `E2571` снято:

| Проверяемый тип `T` | `GetTypeKind(T)` | `IsManagedType(T)` | `System.HasWeakRef(T)` *(P15 и отдельные пробы 1.2.0)* | Физический смысл и граница |
|---|---|---|---|---|
| `Integer`, `Double`, `Pointer` | `tkInteger`, `tkFloat`, `tkPointer` | `False` | `False` (1.2.0, обе архитектуры) | Скаляры и сырые указатели без скрытой финализации |
| `ShortString` | `tkString` | **`False`** | `False` (1.2.0, обе архитектуры) | Встроенный строковый тип с байтом длины (`string[1..255]`) без кучи |
| `AnsiString`, `string` (`UnicodeString`), `WideString` | `tkLString`, `tkUString`, `tkWString` | **`True`** | `False` (1.2.0, обе архитектуры) | Управляемые строковые буферы (`RefCount` / COM BSTR) |
| `TBytes` (`array of Byte`) | `tkDynArray` | **`True`** | `False` (1.2.0, обе архитектуры) | Динамический массив со счётчиком ссылок |
| `TPlainRec` (`record A, B: Integer; end`) | `tkRecord` | `False` | `False` (`_RecOther32`, `_GenRec32`) | Неуправляемая запись без ссылочных полей |
| `TStrRec` (`record S: string; end`) | `tkRecord` | **`True`** | `False` (`_RecPlain32`) | Обычная запись с управляемым полем, но без `[weak]` |
| `TManagedRec` *(CMR с `Initialize`/`Finalize` на `Integer`)* | **`tkMRecord`** | **`True`** | `False` (`_RecOther32`) | Отдельная категория `tkMRecord` даже без managed-полей |
| `TWeakIntfRec` (`record [weak] F: IInterface; end`) | `tkRecord` | **`True`** | **`True`** (`_RecWeak32`, `_GenRec32`) | `[weak]`-поле включает запись в реестр слабых ссылок и делает её managed |
| **`TUnsafeIntfRec` (`record [unsafe] F: IInterface; end`)** | `tkRecord` | **`False`** | **`False`** (`_RecWeak32`) | Атрибут `[unsafe]` полностью снимает подсчёт ссылок и признак managed |
| `TObject` / `THolder = class [weak] W: IInterface; end` | `tkClass` | `False` | **`False`** (`_ClassIntf32`, `_GenClass32`) | На классическом non-ARC Windows экземпляры классов управляются вручную |
| `IInterface` / `TProc` (`reference to procedure`) | **`tkInterface`** | **`True`** | `False` (`_ClassIntf32`) | Замыкание `reference to` представлено интерфейсом кадра захвата |
| `Variant` / `TMethod` (`procedure of object`) | `tkVariant` / `tkRecord` | `True` / `False` | — | `Variant` управляем через RTL, `TMethod` (`Code` + `Data`) неуправляем |

**Разрешение имени и проверенная область `HasWeakRef`:**

1. [Встроенная операция `System.HasWeakRef`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.HasWeakRef) принимает **имя типа**. Одноимённая [функция `System.TypInfo.HasWeakRef`](https://docwiki.embarcadero.com/Libraries/Florence/en/System.TypInfo.HasWeakRef) принимает **`PTypeInfo`**. Это разные операции. После `uses System.TypInfo` пишите `System.HasWeakRef(T)` либо `System.TypInfo.HasWeakRef(TypeInfo(T))` явно. В пробах `QualifiedHasWeakRef_Win32/64` оба способа дали `True` для записи со слабым интерфейсным полем и `False` для простой записи; неквалифицированный вызов с именем типа не скомпилировался.
2. **Запрет скаляров и неограниченного `<T>` не подтверждается.** `ConcreteHasWeakRef_Win32/64` принимает `Integer`, `Double`, `ShortString`, `AnsiString`, `string`, `WideString`, `TBytes`, `Pointer`, `Variant` и возвращает `False`. `GenericWeakRefRun_Win32/64` принимает `TBox<T>` без ограничения: специализации с `Integer`, `string`, простой записью дают `False`, со слабой записью — `True`. Все эти программы выполнены с `exit=0` на Delphi 13 CE `37.0.60542.8024`, Debug.
3. Исторические `P15_Intrinsics_TypeMeta32/64` записывали `E2571`, но при повторной сборке опубликованного исходника наблюдалась коллизия с функцией из `System.TypInfo` и другие диагностики. Текст исходника не содержит прежнего вызова в описанном месте. Старые квитанции сохранены, но они **не являются доказательством общего ограничения intrinsic**. Ограниченные `T: class` и `T: record` из отдельных P15-проб также остаются допустимыми в измеренном профиле.

Новая [квитанция 1.2.0](../../../evidence/compiler/demo-sample-receipts.json) фиксирует исходники и их зависимости. Наблюдение Windows не назначает результаты старым или мобильным компиляторам.

```pascal
// Синтаксический срез проверки HasWeakRef(T) при ограничении T: record (проба P15_HasWeakRef_GenRec32)
type
  TRecBox<T: record> = record
    class function Check: Boolean; static;
  end;

class function TRecBox<T>.Check: Boolean;
begin
  Result := HasWeakRef(T);
end;
```

## Формальная грамматика и ограничения объявлений

```pascal
// Синтаксический срез допустимых обобщённых конструкций (не полный проект)
type
  TBox<T> = class
    Value: T;
  end;
  TPair<TKey, TValue> = record
    Key: TKey;
    Value: TValue;
  end;
  IReader<T> = interface
    function Read: T;
  end;
  TItems<T> = array of T;                     // Обобщённый динамический массив (НЕ открытый массив!)
  THandler<T> = procedure(const Value: T);    // Обобщённый процедурный тип

  TIdentity = class
    class function Keep<T>(const Value: T): T; static; // Обобщённый метод внутри класса/записи
  end;
```

Пять строгих синтаксических правил:
1. **Запрет свободных (top-level) generic-подпрограмм.** В отличие от C++ и C# local functions, на уровне модуля в Delphi нельзя объявить свободную `function Max<T>(const A, B: T): T;` — обобщённые подпрограммы оформляются **только как методы класса или записи** ([пример 10](../../../examples/README.md), `OBSERVED_PASS`: `TIdentity.Keep<Integer>(42)` выводит `42`). В заголовке реализации список параметров типа повторяется (`class function TIdentity.Keep<T>(const Value: T): T;`), но без повторной записи ограничений `: record` / `: class`.
2. **Запрет полиморфных generic-методов (`E2533`).** Конструкторы, деструкторы, а также `virtual`, `dynamic` и `message`-методы не могут объявлять собственный список параметров типа `<U>` (фиксированная таблица слотов VMT класса не может вместить заранее неизвестное множество будущих специализаций метода).
3. **Область видимости параметра типа и предок.** Параметр `T` из `TBox<T>` не наследуется автоматически как имя в заголовке потомка: пишут `TChild<S> = class(TBox<S>)`. Предком класса может быть обычный класс или специализированный generic-класс (`class(TBox<Integer>)`, `class(TBox<S>)`), но **не** голый параметр типа (`class(T)` запрещён).
4. **Псевдонимы специализаций.** Объявление `type TIntCounter = TCounter<Integer>;` обозначает ту же самую специализацию, а не новый отдельный тип.
5. **Отсутствие частичной специализации и нетиповых параметров.** В отличие от C++ (`template<typename T, int N>`), параметры в `<...>` всегда обозначают только типы, а явная перегрузка тела шаблона под один конкретный тип не поддерживается.

## Классовые данные специализаций (`40-generic-class-state.dpr` и `P5_Generic_StaticVar`)

```pascal
program GenericClassState;
{$APPTYPE CONSOLE}
type
  TCounter<T> = class
    class var Count: Integer;
  end;
  TIntCounter = TCounter<Integer>;
begin
  TIntCounter.Count := 3;
  TCounter<string>.Count := 9;
  Writeln(TCounter<Integer>.Count);
  Writeln(TCounter<string>.Count);
  Writeln(TIntCounter.Count);
end.
```

- **Наблюдение компилятора:** на Delphi 13 Community IDE `37.0.60542.8024` (`Win32 Debug`) [пример 40](../../../examples/README.md) выводит `3`, `9`, `3` (`OBSERVED_PASS`, [receipt 0.8](../../../evidence/compiler/demo-sample-receipts.json)): псевдоним `TIntCounter` и прямое имя `TCounter<Integer>` разделяют одну ячейку (`3`), тогда как `TCounter<string>` хранит отдельную (`9`). В дополнительной живой пробе `P5_Generic_StaticVar` (`Win32 Debug`, `0` диагностик) запись `TBox<Integer>.Count := 77` оставила `TBox<string>.Count = 0`.

---

### [ГРАНИЦА DEMO-ФРАГМЕНТА — Уровень 3 — Продвинутый (Дженерики, generic-методы, HasWeakRef / GetTypeKind / E2533)]

Выше показаны первые ~105 строк из **262 строк** полной главы.

**Полное оглавление разделов в полной версии:**
- `## Физика специализаций против стирания типов и шаблонов C++`
- `### Compile-time intrinsics оптимизации специализаций: `GetTypeKind(T)`, `IsManagedType(T)`, `HasWeakRef(T)``
- `## Формальная грамматика и ограничения объявлений`
- `## Классовые данные специализаций (`40-generic-class-state.dpr` и `P5_Generic_StaticVar`)`
- `## Наследование специализаций без вариантности и разрешение `overload``
- `### Generic-методы в не-generic классах и ограничение полиморфизма (`P15_GenericMethods_*` и `E2533`)`
- `## Открытое расхождение документации: [`GENERIC_ARGUMENT_DOC_COUNTEREXAMPLE`](../SOURCE_ISSUES.md#issue-generic-argument-doc-counterexample) (`OPEN`) и ICE `NC2130``
- `## Дополнительный авторский пример (`program ... end.`)`
- `## Границы версий и таргетов`
- `## Первоисточники и статус подтверждения`
- `## Проверка 1.3.0: уточнённые границы`
- `### GENERIC_ARGUMENT_DOC_COUNTEREXAMPLE`

Полный разбор, проверенный компилятором `program`-листинг, контрпримеры и все квитанции доступны в полной редакции (`https://silentfish.dev/delphi`).
