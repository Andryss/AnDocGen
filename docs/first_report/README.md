# Документация AnDocGen: первый отчёт

Каталог `docs/first_report/` содержит материалы первого отчёта по теме «Разработка прототипа системы автоматической генерации технической документации из исходного кода на основе больших языковых моделей».

Документы соответствуют этапам [индивидуального задания](individual_assignment.md) и оформлены в Markdown для конвертации в DOCX через Pandoc.

## Соответствие этапам задания

| Этап | Документ | Содержание |
|------|----------|------------|
| 2 | [requirements.md](requirements.md) | Функциональные и нефункциональные требования, сценарии использования, входные и выходные форматы |
| 3 | [architecture.md](architecture.md) | Архитектура, модули конвейера, потоки данных, диаграммы |
| 4 | [input_preparation.md](input_preparation.md) | Извлечение из кода, структура данных, схема формирования промпта, примеры |
| 5 | [prototype.md](prototype.md) | Реализация прототипа: стек, модули, примеры генерации, ограничения, запуск |
| 6 | [evaluation.md](evaluation.md) | Апробация: успешные и неуспешные примеры, анализ ошибок, ограничения подхода, развитие |

## Рекомендуемый порядок чтения

1. [individual_assignment.md](individual_assignment.md) — тема и рабочий план-график.
2. [requirements.md](requirements.md)
3. [architecture.md](architecture.md)
4. [input_preparation.md](input_preparation.md)
5. [prototype.md](prototype.md)
6. [evaluation.md](evaluation.md)
7. [README проекта](../../README.md) — установка и быстрый старт.

## Конвертация в DOCX

Команды выполняются из корня репозитория:

```bash
pandoc docs/first_report/individual_assignment.md -o individual_assignment.docx
pandoc docs/first_report/requirements.md -o requirements.docx
pandoc docs/first_report/architecture.md -o architecture.docx
pandoc docs/first_report/input_preparation.md -o input_preparation.docx
pandoc docs/first_report/prototype.md -o prototype.docx
pandoc docs/first_report/evaluation.md -o evaluation.docx
```

## Связанные материалы в репозитории

| Путь | Описание |
|------|----------|
| [../../README.md](../../README.md) | Установка, запуск `andocgen`, обзор структуры кода |
| [../README.md](../README.md) | Общий указатель документации проекта |
| [../../src/andocgen/](../../src/andocgen/) | Исходный код системы |
| [../../config.example.yaml](../../config.example.yaml) | Пример конфигурации |
| [../../config.schema.yaml](../../config.schema.yaml) | Спецификация конфигурации |
| [../../examples/](../../examples/) | Примеры для генерации и апробации |
