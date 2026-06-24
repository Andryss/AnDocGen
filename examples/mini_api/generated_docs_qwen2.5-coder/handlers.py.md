# Модуль `handlers.py`


Модуль с обработчиками HTTP-подобного API, включающий классы для представления ответов и управления пользователями.

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

Класс для представления ответов от API.

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Класс для управления пользовательскими операциями API.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует объект `UserHandler` с параметром `storage`.

**Параметры:**

- `storage` (`InMemoryStorage`) — хранилище для управления пользователями

**Примеры:**

```python
storage = InMemoryStorage()
user_handler = UserHandler(storage)
```

##### `get_user(user_id: int) -> ApiResponse`

Извлекает информацию о пользователе по его ID и возвращает отформатированный ответ.

**Параметры:**

- `user_id` (`int`) — уникальный идентификатор пользователя

**Возвращаемое значение:**

- `ApiResponse` — ответ с информацией о пользователе или ошибкой, если пользователь не найден

**Примеры:**

```python
user_handler = UserHandler(storage=InMemoryStorage())
response = user_handler.get_user(1)
print(response)  # ApiResponse(status=200, body={'id': 1, 'name': 'John Doe', ...})
```

##### `create_user(name: str, email: str) -> ApiResponse`

Создает нового пользователя и возвращает информацию о нем.

**Параметры:**

- `name` (`str`) — имя пользователя
- `email` (`str`) — адрес электронной почты пользователя

**Возвращаемое значение:**

- `ApiResponse` — ответ сервера с статусом 201 и телом {"id": user_id}

**Примеры:**

```python
response = UserHandler.create_user("John Doe", "john.doe@example.com")
```

**Смотрите также:**

- `normalize_email(email: str) -> str`


---

[← Индекс](README.md)
