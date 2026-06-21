# Модуль `plugins/markdown.py`


Этот модуль содержит плагин для экспорта данных в формат Markdown.

**Содержание:**

- [Классы](#классы)

## Классы

### `class MarkdownExporter(PluginBase)`

Этот класс используется для экспорта сумм заказов в формат Markdown.

**Наследование:**

- `PluginBase`

#### Методы

##### `__init__(*args: Any, **kwargs: Any) -> None`

Инициализирует экземпляр класса MarkdownExporter.

**Параметры:**

- `*args` (`Any`) — переменное количество позиционных аргументов
- `**kwargs` (`Any`) — переменное количество именованных аргументов

**Примеры:**

```python
exporter = MarkdownExporter(heading="Example Heading")
```

##### `export(data: dict[str, Any]) -> str`

Экспортирует данные в формат Markdown.

**Параметры:**

- `data` (`dict[str, Any]`) — данные для экспорта, где ключи и значения представлены как строки

**Возвращаемое значение:**

- `str` — строка в формате Markdown

**Примеры:**

```python
exporter = MarkdownExporter()
data = {"name": "John", "age": 30, "city": "New York"}
markdown_output = exporter.export(data)
print(markdown_output)
```


---

[← plugins](README.md) | [← К проекту](../README.md)
