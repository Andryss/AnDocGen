# AnDocGen

Прототип системы автоматической генерации технической документации из исходного кода на основе больших языковых моделей.

## Быстрый старт

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

andocgen init

# Генерация документации
andocgen generate ./examples/mini_calculator --config config.yaml

# Multi-module пример (mock ~1 с, Ollama ~3–5 мин)
andocgen generate ./examples/mini_library --config config.yaml
```

Результат сохраняется в `generated_docs/` (Markdown, README, logs, cache, LLM trace).

Для проверки без записи файлов используйте:

```bash
andocgen inspect ./examples/mini_calculator --config config.yaml
andocgen generate ./examples/mini_calculator --config config.yaml --dry-run
```

Если нужно сохранить отчёты dry-run, добавьте `--write-report`.

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

Пути, переданные в CLI, считаются относительно текущей директории запуска. Относительные пути внутри config-файла (`output.directory`, `output.cache_path`, `reporting.logs_dir`) считаются относительно директории самого config-файла.

Основные блоки:

| Блок | Назначение |
|------|------------|
| `discovery.implementation` | scanner: `filesystem` |
| `extraction.implementation` | parser: `python_ast` (default) |
| `call_graph.implementation` | builder: `static` |
| `context.implementation` / `context.prompt` | context + prompt builders |
| `generation.implementation` / `generation.provider` | generator + LLM |
| `generation.workers` | Параллельные LLM-запросы по волнам call graph (default: 1) |
| `generation.max_retries` | Повтор при ошибке разбора JSON-ответа |
| `reporting.quiet` | Без прогресса и сводки в консоли |
| `reporting.log_llm_content` | Писать prompts/responses в `llm_responses.jsonl`; при `false` сохраняется только metadata |
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
andocgen config validate -c config.example.yaml
andocgen inspect ./examples/mini_calculator -c config.example.yaml
andocgen generate ./examples/mini_calculator -c config.example.yaml
andocgen eval ./examples/mini_calculator -c config.example.yaml --output eval_reports
andocgen generate ./examples/mini_library -c config.example.yaml
pytest --cov=andocgen --cov-report=term-missing --cov-fail-under=85
ruff check .
```

## Документация проекта

- [Рабочая документация](docs/README.md)
- [Инструкции для ИИ-агентов](AGENTS.md)
- [Исторический первый отчет](docs/first_report/README.md)

## Требования

- Python 3.11+
- Зависимости: typer, rich, pyyaml, httpx, pydantic
