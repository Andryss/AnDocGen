# Модуль `exceptions.py`


Модуль исключений для мини-библиотеки с базовыми ошибками.

**Содержание:**

- [Классы](#классы)

## Классы

### `class MiniLibraryError(Exception)`

Базовый класс ошибок для библиотеки.

**Наследование:**

- `Exception`

### `class NotFoundError(MiniLibraryError)`

Класс ошибки, выбрасываемой при запросе несуществующего сущности.

**Наследование:**

- `MiniLibraryError`

### `class ValidationError(MiniLibraryError)`

Класс для представления ошибок валидации входных данных.

**Наследование:**

- `MiniLibraryError`


---

[← Индекс](README.md)
