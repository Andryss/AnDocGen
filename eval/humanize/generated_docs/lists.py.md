# Модуль `lists.py`


Модуль для человеческого форматирования списков.

**Экспорт:**

- `natural_list` — —

**Содержание:**

- [Функции](#функции)

## Функции

### `def natural_list(items: list[Any]) -> str`

Преобразует список элементов в читаемую строку с помощью запятых и 'and'.

**Параметры:**

- `items` (`list[Any]`) — список элементов

**Возвращаемое значение:**

- `str` — строка, содержащая элементы через запятые и 'and'

**Примеры:**

```python
assert natural_list(["one", "two", "three"]) == 'one, two and three'
assert natural_list(["one", "two"]) == 'one and two'
assert natural_list(["one"]) == 'one'
```


---

[← Индекс](README.md)
