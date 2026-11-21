> **[DEMO-РЕДАКЦИЯ — Ознакомительный пакет]** Это бесплатная демо-версия **Delphi Behavior Contracts v1.0.0** (в полной версии: 74 полные главы EN/RU, 89 полных карточек директив, 879+ наблюдений компилятора). Сохранено полное оригинальное оглавление, паспорт проверки, все рабочие плагины, чистые скиллы и локальный MCP-сервер с Code Mode — чтобы ваш ИИ мог сразу проверить инструмент на практике и честно сказать, подходит ли вам полная версия. Полная версия: https://silentfish.dev/delphi

# Неоднозначности источников и непроверенные границы

Актуальный проверочный проход 1.5.0: [результаты, границы и недостающие материалы](research/COMPILER_PASS_150.md).


RESOLVED_SELECTED_PROFILE закрывает только явно указанную текущую область. PARTIALLY_RESOLVED сохраняет точный остаток. OPEN обозначает неустановленную часть контракта,а не обязательную ошибку
компилятора. DOCUMENTED_* означает документальное уточнение правила,синтаксиса
или version/target boundary. PARTIALLY_DOCUMENTED сохраняет явный остаток.
Документальный статус не заменяет отдельный compiler receipt. Узкие наблюдения
редакции0.8 описаны в [матрице доказательств](chapters/62-compiler-evidence.md).

- [RANGECHECKS_DEFAULT_PROFILE](#issue-rangechecks-default-profile)
- [FINITEFLOAT_UNDERSPECIFIED](#issue-finitefloat-underspecified)
- [EXTENDED_TARGET_PROFILE](#issue-extended-target-profile)
- [LONGSTRINGS_DOC_CONFLICT](#issue-longstrings-doc-conflict)
- [WARNINGS_ERROR_PROFILE](#issue-warnings-error-profile)
- [INLINE_DEFAULT_PROFILE](#issue-inline-default-profile)
- [TYPEINFO_DOC_CONFLICT](#issue-typeinfo-doc-conflict)
- [IFOPT_TABLE_TYPOS](#issue-ifopt-table-typos)
- [PUSHOPT_TABLE_TYPOS](#issue-pushopt-table-typos)
- [EXTRA_DIRECTIVES_NOT_REVIEWED](#issue-extra-directives-not-reviewed)
- [IMAGEBASE_TARGET_SCOPE](#issue-imagebase-target-scope)
- [LIBRARY_NAMING_DEFAULTS](#issue-library-naming-defaults)
- [EXTENSION_LOCALIZATION_EXAMPLE](#issue-extension-localization-example)
- [INCLUDE_STATEMENT_PART](#issue-include-statement-part)
- [RESOURCE_PREDICATE_VERSION](#issue-resource-predicate-version)
- [CONDITIONAL_TERMINATOR_WORDING](#issue-conditional-terminator-wording)
- [NOINCLUDE_MATCHING_PROFILE](#issue-noinclude-matching-profile)
- [CODEPAGE_SOURCE_FORM_UNCONFIRMED](#issue-codepage-source-form-unconfirmed)
- [RESOURCERESERVE_CURRENT_TARGET](#issue-resourcereserve-current-target)
- [DEBUGINFO_PROFILE_DEPTH](#issue-debuginfo-profile-depth)
- [REFERENCEINFO_LONG_FORM_TEXT](#issue-referenceinfo-long-form-text)
- [PROGRAM_CONTROL_TARGET_COPY](#issue-program-control-target-copy)
- [RECORD_CONSTRAINT_MANAGED_BOUNDARY](#issue-record-constraint-managed-boundary)
- [NAMEOF_DETAILED_GRAMMAR](#issue-nameof-detailed-grammar)
- [WEAK_PACKAGE_STATE_SCOPE](#issue-weak-package-state-scope)
- [WIN64_ASSEMBLER_DOC_DETAILS](#issue-win64-assembler-doc-details)
- [NAMESPACE_LEGACY_AGGREGATION](#issue-namespace-legacy-aggregation)
- [IF_UNDECLARED_IDENTIFIER_OBSERVATION](#issue-if-undeclared-identifier-observation)
- [IF_TYPED_CONSTANT_OBSERVATION](#issue-if-typed-constant-observation)
- [GENERIC_ARGUMENT_DOC_COUNTEREXAMPLE](#issue-generic-argument-doc-counterexample)

<a id="issue-rangechecks-default-profile"></a>

## RANGECHECKS_DEFAULT_PROFILE

Статус: RESOLVED_SELECTED_PROFILE. Связанные имена: [RANGECHECKS](directives/rangechecks.md).


---

**[СВОДКА DEMO]** Полная редакция содержит подробные разборы, первоисточники и статусы по всем 30 записям (`evidence/source_issues.json`).
