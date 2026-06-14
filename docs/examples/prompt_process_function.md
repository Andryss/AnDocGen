# Пример промпта: функция `process`

Полный промпт для одного запроса к провайдеру генерации. Сущность — функция `process` из модуля `app/service.py` (см. EntityContext в input_preparation, раздел 2.4). Язык текста секций ответа: `ru` (`output_language`).

---

## System message

```
You are a technical documentation generator.
Write section body text in ru.
Respond with Markdown using exactly these English section headers (in this order), with no extra sections:

For function/method:
## Summary
## Parameters
## Returns
## Raises
## Edge cases
## Side effects
## Examples
## See also

For class:
## Summary
## Fields
## Inheritance
## Methods overview

For module:
## Summary
## Exports

Use "N/A" in a section when it does not apply. Do not invent parameters, types, or behavior not present in the source code.
```

---

## User message

## Entity

Type: function  
Name: process  
Signature: `def process(data: dict) -> Result`  
Complexity: 2

## Source

Docstring: (none)

## Source code

```python
def process(data: dict) -> Result:
    validated = validate(data)
    return format_result(validated)
```

## Previous output

(none)

## Dependencies

```python
from app.utils import validate, format_result
```

## Called entities documentation

### validate(data: dict) -> bool

Проверяет корректность входных данных и возвращает признак успешной проверки.

### format_result(data: dict) -> Result

Форматирует результат обработки в объект Result.

## Base classes

(none)

## Project

my_app

---

## Expected model response

```markdown
## Summary

Обрабатывает входные данные: выполняет валидацию и возвращает отформатированный результат.

## Parameters

- `data` (`dict`) — входные данные для обработки

## Returns

- `Result` — отформатированный результат после успешной валидации

## Raises

N/A

## Edge cases

N/A

## Side effects

N/A

## Examples

N/A

## See also

N/A
```

---

## DocBlock после парсинга

```json
{
  "entity_type": "function",
  "entity_name": "process",
  "module_path": "app/service.py",
  "signature": "def process(data: dict) -> Result",
  "raw_response": "## Summary\n\nОбрабатывает входные данные...",
  "summary": "Обрабатывает входные данные: выполняет валидацию и возвращает отформатированный результат.",
  "parameters": [
    {"name": "data", "type": "dict", "description": "входные данные для обработки", "optional": false, "default": null}
  ],
  "returns": {"type": "Result", "description": "отформатированный результат после успешной валидации"},
  "raises": "N/A",
  "edge_cases": "N/A",
  "side_effects": "N/A",
  "examples": "N/A",
  "see_also": "N/A",
  "fields": null,
  "inheritance": null,
  "methods_overview": null,
  "exports": null,
  "content": "### `process(data: dict) -> Result`\n\nОбрабатывает входные данные: выполняет валидацию и возвращает отформатированный результат.\n\n**Параметры:**\n- `data` (`dict`) — входные данные для обработки\n\n**Возвращаемое значение:** `Result` — отформатированный результат после успешной валидации"
}
```

Поле `content` формируется компонентом подготовки представления для вывода из structured-полей DocBlock (шаблон выходного Markdown — input_preparation, раздел 3.3).
