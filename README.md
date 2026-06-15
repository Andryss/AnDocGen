# AnDocGen

Прототип системы автоматической генерации технической документации из исходного кода на основе больших языковых моделей.

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp config.example.yaml config.yaml

# Генерация документации
andocgen ./examples/mini_calculator --config config.example.yaml
```

Результат сохраняется в `generated_docs/` (Markdown, README, logs, cache).

## Структура программной реализации

```text
src/andocgen/
├── pipeline.py         # оркестрация через фабрики модулей
├── config.py           # implementation в каждом блоке конфигурации
├── scanner/            # base.py, factory.py, implementations/
├── parser/
├── call_graph/
├── context/
├── generator/
├── llm/                # base.py (Protocol), factory.py, providers/
├── validator/
├── output/
└── reporting/
```

Каждый пакет: **`base.py`** (интерфейс) → **`factory.py`** (выбор по config) → **`implementations/`** (код).

## Конфигурация

Скопируйте `config.example.yaml` в `config.yaml`. Основные блоки:

| Блок | Назначение |
|------|------------|
| `discovery.implementation` | scanner: `filesystem` |
| `extraction.implementation` | parser: `python_ast` (default) |
| `call_graph.implementation` | builder: `static` |
| `context.implementation` / `context.prompt` | context + prompt builders |
| `generation.implementation` / `generation.provider` | generator + LLM |
| `validation.implementation` | validator: `structured` |
| `output.implementation` | writer + formatter: `markdown` |
| `reporting.implementation` | reporter: `file` |

| Провайдер | Когда использовать |
|-----------|-------------------|
| `mock` | Локальная разработка, тесты, CI |
| `ollama` | Локальные модели через [Ollama](https://ollama.com) |
| `openai` | OpenAI или совместимые API |

## Примеры

```bash
andocgen ./examples/mini_calculator -c config.example.yaml
andocgen ./examples/mini_api -c config.example.yaml
pytest
```

## Документация проекта

- [Требования](docs/requirements.md)
- [Архитектура](docs/architecture.md)
- [Подготовка входных данных](docs/input_preparation.md)
- [Описание прототипа](docs/prototype.md)
- [Апробация](docs/evaluation.md)

## Требования

- Python 3.11+
- Зависимости: typer, rich, pyyaml, httpx
