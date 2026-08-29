# Модуль `handlers.py`


Модуль handlers.py содержит классы для обработки HTTP‑подобных запросов API, включая представление ответа и операции с пользователями.

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

Класс ApiResponse представляет ответ API.

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Класс UserHandler обеспечивает операции с пользователями через API, включая получение и создание пользователей, используя InMemoryStorage.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует экземпляр UserHandler, сохраняет переданное хранилище.

**Параметры:**

- `storage` (`InMemoryStorage`) — объект хранилища пользователей

**Возвращаемое значение:**

- `None` — ничего не возвращает

**Побочные эффекты:**

Инициализирует внутреннее поле _storage.

**Примеры:**

storage = InMemoryStorage(); handler = UserHandler(storage)

**Смотрите также:**

InMemoryStorage

##### `get_user(user_id: int) -> ApiResponse`

Возвращает пользователя по идентификатору.

**Параметры:**

- `user_id` (`int`) — Идентификатор пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ API со статусом 200 и телом пользователя, либо 404 с сообщением об ошибке

**Примеры:**

handler = UserHandler(storage)
response = handler.get_user(42)
print(response.status)
print(response.body)

##### `create_user(name: str, email: str) -> ApiResponse`

Создаёт нового пользователя в хранилище и возвращает ответ API.

**Параметры:**

- `name` (`str`) — Имя пользователя
- `email` (`str`) — Электронный адрес пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ API с кодом 201 и телом, содержащим id созданного пользователя

**Побочные эффекты:**

Записывает пользователя в внутреннее хранилище _storage.

**Примеры:**

handler = UserHandler(storage)
response = handler.create_user("Иван", "ivan@example.com")
print(response.status)  # 201
print(response.body)   # {'id': ...}

**Смотрите также:**

normalize_email


---

[← Индекс](README.md)
