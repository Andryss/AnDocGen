# Документация AnDocGen

Каталог `docs/` содержит проектную документацию системы автоматической генерации технической документации из исходного кода на основе больших языковых моделей. Документы соответствуют этапам индивидуального задания (см. [individual_assignment.md](individual_assignment.md)) и оформлены для конвертации в DOCX через Pandoc.

## Соответствие этапам задания

| Этап | Документ | Содержание |
|------|----------|------------|
| 2 | [requirements.md](requirements.md) | Функциональные и нефункциональные требования, сценарии использования, входные и выходные форматы |
| 3 | [architecture.md](architecture.md) | Архитектура, модули конвейера, потоки данных, диаграммы |
| 4 | [input_preparation.md](input_preparation.md) | Извлечение из кода, структура данных, схема формирования промпта, примеры |
| 5 | [prototype.md](prototype.md) | Реализация прототипа: стек, модули, примеры генерации, ограничения, запуск |
| 6 | [evaluation.md](evaluation.md) | Апробация: успешные и неуспешные примеры, анализ ошибок, ограничения подхода, развитие |

Все перечисленные документы — **готовы**.

## Рекомендуемый порядок чтения

1. [individual_assignment.md](individual_assignment.md) — тема и график работ
2. [requirements.md](requirements.md)
3. [architecture.md](architecture.md)
4. [input_preparation.md](input_preparation.md)
5. [prototype.md](prototype.md)
6. [evaluation.md](evaluation.md)
7. [README.md](../README.md) — установка и быстрый старт

## Конвертация в DOCX

```bash 
pandoc docs/requirements.md -o requirements.docx
pandoc docs/architecture.md -o architecture.docx
pandoc docs/input_preparation.md -o input_preparation.docx
pandoc docs/prototype.md -o prototype.docx
pandoc docs/evaluation.md -o evaluation.docx
```

## Связанные материалы в репозитории

| Путь | Описание                                                        |
|------|-----------------------------------------------------------------|
| [../README.md](../README.md) | Установка, запуск `andocgen`, обзор структуры кода              |
| [../src/andocgen/](../src/andocgen/) | Исходный код                                                    |
| [../config.example.yaml](../config.example.yaml) | Пример конфигурации                                             |
| [../examples/](../examples/) | Примеры для генерации и апробации                               |
