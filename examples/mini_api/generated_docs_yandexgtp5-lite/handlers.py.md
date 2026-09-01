# Модуль `handlers.py`


Модуль handlers.py содержит классы ApiResponse и UserHandler для работы с HTTP-подобными API.

**Содержание:**

- [Классы](#классы)

## Классы

### `class ApiResponse`

Класс ApiResponse представляет собой структуру данных для хранения ответа от API.

**Поля:**

- `status` (`int`) — —
- `body` (`dict[str, Any]`) — —

### `class UserHandler`

Класс UserHandler предназначен для работы с пользовательскими данными и обработки API-запросов, связанных с пользователями.

**Назначение:**

Обрабатывает операции API, связанные с пользователями.

**Использование:**

Создайте экземпляр класса UserHandler, передав ему экземпляр класса InMemoryStorage, и используйте методы для работы с пользователями.

#### Методы

##### `__init__(storage: InMemoryStorage) -> None`

Инициализирует объект UserHandler, передавая ему экземпляр класса InMemoryStorage для хранения данных пользователей.

**Параметры:**

- `storage` (`InMemoryStorage`) — Ссылка на экземпляр класса InMemoryStorage для хранения данных пользователей

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Инициализация UserHandler с использованием InMemoryStorage

```python
UserHandler(storage=InMemoryStorage())
```

##### `get_user(user_id: int) -> ApiResponse`

Возвращает данные пользователя по его ID или сообщение об ошибке, если пользователь не найден.

**Параметры:**

- `user_id` (`int`) — Получить пользователя по его ID

**Возвращаемое значение:**

- `ApiResponse` — Ответ в формате ApiResponse с телом данных пользователя или сообщением об ошибке

**Примеры:**

Получить пользователя с указанным ID

```python
UserHandler.get_user(user_id=1)
```

##### `create_user(name: str, email: str) -> ApiResponse`

Создаёт пользователя с указанным именем и email.

**Параметры:**

- `name` (`str`) — Имя пользователя
- `email` (`str`) — Email пользователя

**Возвращаемое значение:**

- `ApiResponse` — Ответ в формате ApiResponse со статусом 201 и телом с идентификатором пользователя

**Примеры:**

Создать пользователя с именем 'Ivan' и email 'ivan@example.com'

```python
create_user('Ivan', 'ivan@example.com')
```

**Смотрите также:**

def normalize_email(email: str) -> str — Приводит адрес электронной почты к нижнему регистру и удаляет начальные и конечные пробелы для хранения.


---

[← Индекс](README.md)
