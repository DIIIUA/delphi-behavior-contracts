# Delphi Behavior Contracts

**Преврати любого ИИ-агента в сеньора по Delphi за 60 секунд.**
Проверенная живым компилятором инженерная система по Delphi / Object Pascal: **74 главы (RU + EN)**, **89 карточек директив**, **879+ реальных доказательств Delphi 13**, **8 нативных плагинов**, **15 раскладок чистых скиллов** и офлайн / Cloudflare Workers **Code Mode MCP-сервер**.

[English](README.md) · [Официальный сайт (RU)](https://silentfish.dev/ru/delphi) · [Website (EN)](https://silentfish.dev/delphi) · [Тарифы (от $99)](https://silentfish.dev/ru/delphi/buy) · [Скачать бесплатное демо](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest) · [Обсуждения](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)

[![Delphi Behavior Contracts (DEMO) MCP server](https://mcprush.com/badge/delphi-behavior-contracts-demo-mcp/card.svg)](https://mcprush.com/to/delphi-behavior-contracts-demo-mcp?ref=badge)

---

## Почему обычные нейросети ломают проекты на Delphi

Стандартные LLM угадывают Delphi по аналогии с C# и старым форумам. Переписанный код компилируется, базовые тесты зелёные — а через полгода плывут финансовые итоги: `System.Round` округляет к чётному, `shr` всегда логический, `Extended` на Win64 переходит с 80-битного x87 на 64-битный IEEE `Double` (53-битная мантисса), а присваивание динамического массива делит общий буфер **без** copy-on-write.

**Delphi Behavior Contracts убирает догадки целиком.** Один пойманный тихий баг окупает весь пакет в десятки раз в первый же день.

- **Точный перенос на C#, C++, Java, Go, Python и Rust:** каждая операция разложена по 9 измерениям контракта поведения (алиасинг, владение, округление, порядок вычислений, очистка при исключениях).
- **Безопасный апгрейд легаси на Delphi 12–13, Win64 и Unicode:** ловит скрытые ловушки при переходе с Delphi 7 / 2007 / XE ещё до продакшена.
- **Полный контроль директив компилятора:** 89 подробных карточек чётко разделяют синтаксис парсера и реальный эффект в коде под Win32, Win64 и Android ARM.
- **100% офлайн и безопасно для коммерческого кода:** ваши исходники никогда не покидают ваш компьютер или внутренний контур компании.

---

## Дай своему ИИ проверить бесплатное демо за 60 секунд

В этом репозитории выложена **бесплатная ознакомительная DEMO-версия (`< 1 МБ`)** с точно такой же 4-слойной архитектурой и на 100% рабочими плагинами, скиллами и MCP-сервером:

1. Скачай **[`delphi-behavior-contracts-demo-1.0.2.zip`](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)** (или клонируй этот репозиторий).
2. Укажи Claude Code, Codex, Antigravity, Gemini CLI, Cursor, Copilot или Windsurf на файл **[`EVALUATE_FOR_USER.ru.md`](EVALUATE_FOR_USER.ru.md)**.
3. Спроси: *«Что покрывает этот скилл Delphi Behavior Contracts и полезен ли он для наших текущих задач по Delphi?»*

## Полная коммерческая версия (Разовая покупка · Без подписок)

В каждом тарифе — **один и тот же полный Universal Suite** (все 74 главы RU + EN, 89 карточек директив, обе книги, 879+ квитанций, 8 плагинов, 15 раскладок скиллов, локальный MCP, Docker и Cloudflare Worker) плюс все обновления `1.x`:

- **Solo Engineer — ~~$149~~ $99** *(стартовая цена для первых 30 лицензий)*: 1 разработчик, все локальные плагины/скиллы/MCP и обе книги RU/EN.
- **Team Suite — ~~$490~~ $349** *(стартовая цена)*: до 10 разработчиков, общий внутренний MCP-сервер (Docker / Cloudflare Worker) и закрытый репозиторий компании.
- **Agency / Integrator — $1,290**: безлимит внутри компании + коммерческое право на неограниченное число клиентских миграций и аудитов.

👉 **[Оформить полный пакет на silentfish.dev/ru/delphi/buy](https://silentfish.dev/ru/delphi/buy)** · **[Скачать бесплатное демо](https://github.com/DIIIUA/delphi-behavior-contracts/releases/latest)** · **[Обсуждения](https://github.com/DIIIUA/delphi-behavior-contracts/discussions)**
