# Модуль `handlers.py`


Модуль с обработчиками HTTP-like API, включая класс для управления пользователями.

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

N/A

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Класс для управления пользовательскими операциями API.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует объект UserHandler с хранилищем.

**Параметры:**

- `storage` (`InMemoryStorage`) — хранилище для хранения пользователей

##### `get_user(user_id: int) -> ApiResponse`

Получает информацию о пользователе по его ID.

**Параметры:**

- `user_id` (`int`) — ID пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ с информацией о пользователе или ошибкой

**Примеры:**

Получить информацию о пользователе.

```python
response = UserHandler.get_user(123)
```

##### `create_user(name: str, email: str) -> ApiResponse`

Создает нового пользователя и возвращает его ID.

**Параметры:**

- `name` (`str`) — имя пользователя
- `email` (`str`) — электронная почта пользователя

**Возвращаемое значение:**

- `ApiResponse` — ответ с ID созданного пользователя

**Примеры:**

Создать нового пользователя.

```python
UserHandler.create_user(name='Иван', email='ivan@example.com')
```

**Смотрите также:**

normalize_email


---

[← Индекс](README.md)
