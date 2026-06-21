# Модуль `handlers.py`


HTTP-like API handlers (простой пример).

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

N/A

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Обработчик API для работы с пользователями.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует объект класса `UserHandler` с параметром `storage`.

**Параметры:**

- `storage` (`InMemoryStorage`) — объект хранилища данных

**Примеры:**

```python
storage = InMemoryStorage()
user_handler = UserHandler(storage)
```

##### `get_user(user_id: int) -> ApiResponse`

Возвращает пользователя по идентификатору.

**Параметры:**

- `user_id` (`int`) — идентификатор пользователя

**Возвращаемое значение:**

- `ApiResponse` — ответ с информацией о пользователе или ошибкой

**Примеры:**

```python
# Пример вызова метода
user_info = UserHandler.get_user(123)
print(user_info)
```

##### `create_user(name: str, email: str) -> ApiResponse`

Создает нового пользователя и возвращает ответ с информацией о созданном пользователе.

**Параметры:**

- `name` (`str`) — имя пользователя
- `email` (`str`) — адрес электронной почты пользователя

**Возвращаемое значение:**

- `ApiResponse` — ответ, содержащий статус 201 и ID созданного пользователя

**Примеры:**

```python
response = UserHandler.create_user("John Doe", "john.doe@example.com")
```

**Смотрите также:**

- `normalize_email`


---

[← Индекс](README.md)
