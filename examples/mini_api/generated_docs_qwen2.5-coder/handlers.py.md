# Модуль `handlers.py`


Модуль с обработчиками HTTP-подобного API, включающим класс для управления пользователями.

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

N/A

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Класс для управления пользователями через API.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует экземпляр класса UserHandler с объектом хранилища.

**Параметры:**

- `storage` (`InMemoryStorage`) — объект хранилища для управления пользователями

**Примеры:**

user_handler = UserHandler(InMemoryStorage())

##### `get_user(user_id: int) -> ApiResponse`

Получает пользователя по идентификатору.

**Параметры:**

- `user_id` (`int`) — идентификатор пользователя

**Возвращаемое значение:**

- `ApiResponse` — ответ сервера с пользователем или ошибкой

**Примеры:**

user_handler.get_user(123)

##### `create_user(name: str, email: str) -> ApiResponse`

Сущность `UserHandler.create_user` описана по сигнатуре и структуре исходного кода.

**Параметры:**

- `name` (`str`) — —
- `email` (`str`) — —

**Возвращаемое значение:**

- `ApiResponse` — —


---

[← Индекс](README.md)
