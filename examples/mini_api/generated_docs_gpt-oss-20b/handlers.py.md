# Модуль `handlers.py`


Модуль handlers.py предоставляет HTTP‑подобные обработчики, включая класс ApiResponse и класс UserHandler для работы с пользователями.

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

N/A

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Класс UserHandler обеспечивает обработку операций, связанных с пользователями, включая получение и создание пользователей.

**Назначение:**

Обеспечивает интерфейс для взаимодействия с хранилищем пользователей, предоставляя API-ответы.

**Использование:**

Создайте экземпляр UserHandler, передав объект InMemoryStorage, и используйте методы get_user и create_user для работы с пользователями.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует UserHandler, сохраняет переданный объект хранения.

**Параметры:**

- `storage` (`InMemoryStorage`) — Объект для хранения данных пользователей.

**Побочные эффекты:**

Сохраняет объект хранения в атрибуте _storage.

**Примеры:**

Создание экземпляра UserHandler

```python
from handlers import UserHandler
from storage import InMemoryStorage
storage = InMemoryStorage()
handler = UserHandler(storage)
```

**Смотрите также:**

InMemoryStorage

##### `get_user(user_id: int) -> ApiResponse`

Возвращает пользователя по идентификатору из хранилища. Если пользователь не найден, возвращает ответ со статусом 404.

**Параметры:**

- `user_id` (`int`) — Идентификатор пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ API с данными пользователя или сообщением об ошибке

**Граничные случаи:**

Если пользователь с заданным идентификатором отсутствует в хранилище, возвращается статус 404 с телом {"error": "not found"}.

**Примеры:**

Получить пользователя с идентификатором 42.

```python
from handlers import UserHandler
from storage import InMemoryStorage

storage = InMemoryStorage()
handler = UserHandler(storage=storage)
response = handler.get_user(42)
print(response.status, response.body)
```

##### `create_user(name: str, email: str) -> ApiResponse`

Создает нового пользователя, сохраняет его в хранилище и возвращает ответ API с кодом 201 и идентификатором пользователя.

**Параметры:**

- `name` (`str`) — Имя пользователя
- `email` (`str`) — Электронная почта пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ API с кодом 201 и телом, содержащим id созданного пользователя

**Побочные эффекты:**

Записывает нового пользователя в хранилище

**Примеры:**

Создание пользователя

```python
handler.create_user('Alice', 'alice@example.com')
```

**Смотрите также:**

normalize_email


---

[← Индекс](README.md)
