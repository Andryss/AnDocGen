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

# Multi-module пример (mock ~1 с, Ollama ~3–5 мин)
andocgen ./examples/mini_library --config config.example.yaml
```

Результат сохраняется в `generated_docs/` (Markdown, README, logs, cache).

## Структура программной реализации

```text
src/andocgen/
├── pipeline.py         # оркестрация через фабрики модулей
├── config.py           # load_config() и helper-методы
├── config_models.py    # Pydantic-модели (генерируются из config.schema.yaml)
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

Скопируйте `config.example.yaml` в `config.yaml`.

**Спецификация:** [`config.schema.yaml`](config.schema.yaml) — единственный источник истины для полей, типов, дефолтов и описаний. Pydantic-модели в `src/andocgen/config_models.py` генерируются из неё:

```bash
./scripts/generate_config_models.sh
```

Для автодополнения в IDE установите расширение [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) (Red Hat) — в `config.example.yaml` уже указана директива `$schema`.

Основные блоки:

| Блок | Назначение |
|------|------------|
| `discovery.implementation` | scanner: `filesystem` |
| `extraction.implementation` | parser: `python_ast` (default) |
| `call_graph.implementation` | builder: `static` |
| `context.implementation` / `context.prompt` | context + prompt builders |
| `generation.implementation` / `generation.provider` | generator + LLM |
| `generation.workers` | Параллельные LLM-запросы по волнам call graph (default: 1) |
| `generation.max_retries` | Повтор при ошибке парсинга секций |
| `reporting.quiet` | Без прогресса и сводки в консоли |
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
andocgen ./examples/mini_library -c config.example.yaml
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
- Зависимости: typer, rich, pyyaml, httpx, pydantic
