# Модуль `exceptions.py`


Модуль исключений для мини-библиотеки `mini_library`.

**Содержание:**

- [Классы](#классы)

## Классы

### `class MiniLibraryError(Exception)`

Класс для базовых ошибок библиотеки `mini_library`.

**Наследование:**

- `Exception`

### `class NotFoundError(MiniLibraryError)`

Класс для обозначения ошибки при отсутствии запрошенного элемента. Экспортируется из модуля `exceptions.py`.

**Наследование:**

- `MiniLibraryError`

### `class ValidationError(MiniLibraryError)`

Класс для обозначения ошибки валидации входных данных. Выбрасывается при нарушении условий валидации.

N/A

**Наследование:**

- `MiniLibraryError`


---

[← Индекс](README.md)
