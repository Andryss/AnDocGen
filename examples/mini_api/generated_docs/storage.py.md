# Модуль `storage.py`


Ин-Memory key-value storage (ключ-значение) в памяти.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class InMemoryStorage`

Простое хранилище в памяти для демонстрационных целей.

#### Методы

##### `__init__() -> None`

Инициализирует объект `InMemoryStorage`.

##### `create(payload: dict[str, Any]) -> int`

Создает новый элемент в хранилище и возвращает его уникальный идентификатор.

**Параметры:**

- `payload` (`dict[str, Any]`) — данные для нового элемента

**Возвращаемое значение:**

- `int` — уникальный идентификатор созданного элемента

**Примеры:**

```python
storage = InMemoryStorage()
item_id = storage.create({'key': 'value'})
print(item_id)  # Output will be the unique ID of the created item
```

##### `get(item_id: int) -> dict[str, Any] | None`

Возвращает данные из хранилища по заданному идентификатору.

**Параметры:**

- `item_id` (`int`) — уникальный идентификатор элемента

**Возвращаемое значение:**

- `dict[str, Any] | None` — данные элемента или None если элемент не найден

**Примеры:**

```python
storage = InMemoryStorage()
item = storage.get(1)
print(item)  # Output: {'name': 'value'}
```

## Функции

### `def normalize_email(email: str) -> str`

Приводит адрес электронной почты к стандартному формату для хранения.

**Параметры:**

- `email` (`str`) — адрес электронной почты для нормализации

**Возвращаемое значение:**

- `str` — нормализованный адрес электронной почты


---

[← Индекс](README.md)
