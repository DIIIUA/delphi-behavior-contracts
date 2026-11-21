# Итоговый компиляторный проход 1.1.0 (Серия P15)

> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.0** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi


20 ноября 2026. **Delphi 13 Community Edition (`IDE 37.0.60542.8024`, Windows `Win32`/`Win64 Debug`) через `MCP2Delphi`.**

Исторический отчёт 1.1.0 описывал серию **`P15`** как закрытие остатка языка. Редакция 1.2.0 снимает процентную оценку: количество сборок не измеряет полноту языка. В отчёте заявлена **`41` живая сборка** (доводя суммарный объём серий `P1–P15` ровно до **`400` рабочих сборок**), из которых **`35` переносимых текстовых проб** криптографически привязаны к квитанции [`20261120-followup-110.json`](../../../evidence/compiler/demo-sample-receipts.json) и каталогу [`examples/probes/compiler-110/`](../../../examples/README.md).

## Главные эмпирические результаты Серии `P15`

1. **Compile-time intrinsics мета-типизации (`GetTypeKind`, `IsManagedType`, `HasWeakRef`):**
   - `P15_Intrinsics_TypeMeta32_V2` / `P15_Intrinsics_TypeMeta64_V2` (`Win32`/`Win64`, `0` диагностик, `exit=0`): единая 18-типовая таблица — в том числе `TManagedRec` (`class operator Initialize/Finalize`) даёт **`tkMRecord` / `Managed=True`**, `TWeakIntfRec` (`[weak] F: IInterface`) даёт `tkRecord` / `Managed=True`, **`TUnsafeIntfRec` (`[unsafe] F: IInterface`) даёт `tkRecord` / `Managed=False`**, `TProc` (`reference to procedure`) даёт `tkInterface` / `Managed=True`, `TMethod` даёт `tkRecord` / `Managed=False`.
   - **Исправлено в 1.2.0:** следующий прежний вывод не использовать как правило intrinsic; см. [независимый проход](COMPILER_PASS_120.md) и [главу 31](../chapters/31-generics.md). Исторически утверждалось: `HasWeakRef(T)` на неограниченном `T` (`P15_Intrinsics_TypeMeta32` / `64`) компилятор выдаёт **`E2571 Type parameter 'T' doesn't have class or interface constraint`**, но вопреки буквальному тексту диагностики в `Delphi 13 CE` чисто компилируются И `T: class` (`P15_HasWeakRef_GenClass32` -> `False` на non-ARC Windows), И **`T: record`** (`P15_HasWeakRef_GenRec32`: `GenRec_Weak=True`, `GenRec_Plain=False`). На конкретных типах `P15_HasWeakRef_RecWeak32` подтвердил `TWeakIntfRec=True`, `TUnsafeIntfRec=False`, тогда как для классов `THolder = class [weak] W: IInterface; end;` (`P15_HasWeakRef_ClassIntf32`) результат `False`.

2. **`IsConstValue(Expr)` и подпрограммная область `{$INLINE OFF}`:**
   - `P15_IsConstValue_Inline32_V2` / `P15_IsConstValue_Inline64_V2`: внутри `inline`-функции литерал `42`, `const C = 10` и `C + 5` дают `TRUE`, тогда как **типизированные константы (`{$J-} TC_RO` и `{$J+} TC_RW`)**, runtime-переменные и не-`inline` вызов (`ProbeNoInline(42)`) дают `FALSE`.
   - `P15_IsConstValue_CallOff32`: прямое доказательство подпрограммного scope `{$INLINE OFF}` — директива перед заголовком `CallWithInlineOff` отключает встраивание (`calloff_lit=FALSE`), тогда как `{$PUSHOPT}{$INLINE OFF}` внутри уже открытого `begin..end` встраивание не отключает (`inloff_inline_body=TRUE`).

3. **Низкоуровневый `raise ... at ReturnAddress` и runtime-хуки (`ExceptProc`, `ErrorProc`, `AssertErrorProc`):**
   - `P15_Raise_At_ReturnAddr32` / `P15_Raise_At_ReturnAddr64`: при `{$INLINE OFF}` на обёртке `FailAtCaller` адрес `ExceptAddr` смещается в вызывающую процедуру `RunTest` (`diff=TRUE`, `caller_near_run=TRUE`).
   - `P15_RuntimeHooks_AssertError32` / `P15_RuntimeHooks_AssertError64`: подключение `System.SysUtils` инициализирует все три указателя (`has_ExceptProc=TRUE`, `has_ErrorProc=TRUE`, `has_AssertErrorProc=TRUE`); временная подмена `AssertErrorProc` с восстановлением в `try..finally` перехватывает `Assert(False, 'custom_trap')` с ненулевым адресом и номером строки, а после восстановления срабатывает стандартный `EAssertionFailed`.

4. **Generic-методы в не-generic классах и ограничение полиморфизма:**
   - `P15_GenericMethods_NonGenClass32` / `P15_GenericMethods_NonGenClass64`: `Swap<T>`, многопараметрический `PairKinds<T1, T2>`, локальное ограничение `SizeOfRec<T: record>`, экземплярный `Echo<T>` и приоритет перегрузки (`Pick(10)` -> `NonGenInt:10`, явный `Pick<Integer>(10)` -> `Gen<tkInteger>`, вывод типа `Pick('hi')` -> `Gen<tkUString>`).

---

*(Full research pass report is included in the full edition.)*
