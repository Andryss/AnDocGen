# Модуль `handlers.py`


Модуль с HTTP-подобными обработчиками API (упрощённый пример).

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

Класс для работы с ответами API.

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Класс для обработки операций, связанных с пользователями.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует объект UserHandler с передачей хранилища данных.

**Параметры:**

- `storage` (`InMemoryStorage`) — хранилище данных для пользователя

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Инициализация UserHandler с использованием InMemoryStorage

```python
UserHandler(InMemoryStorage())
```

##### `get_user(user_id: int) -> ApiResponse`

Возвращает данные пользователя по его ID или сообщение об ошибке, если пользователь не найден.

**Параметры:**

- `user_id` (`int`) — ID пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ в формате ApiResponse с кодом состояния 200 и данными пользователя или с кодом состояния 404 и сообщением об ошибке 'not found' если пользователь не найден

**Примеры:**

Получить пользователя с указанным ID

```python
UserHandler.get_user(user_id=1)
```

##### `create_user(name: str, email: str) -> ApiResponse`

Создаёт пользователя в системе с указанным именем и email.

**Параметры:**

- `name` (`str`) — Имя пользователя
- `email` (`str`) — Email пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ в формате ApiResponse со статусом 201 и телом, содержащим идентификатор созданного пользователя

**Примеры:**

Создать пользователя с именем 'John Doe' и email 'john.doe@example.com'.

```python
user_handler.create_user('John Doe', 'john.doe@example.com')
```

**Смотрите также:**

def normalize_email(email: str) -> str — Приводит адрес электронной почты к нижнему регистру и убирает лишние пробелы для хранения.


---

[← Индекс](README.md)
