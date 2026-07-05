# Модуль `filesize.py`


Модуль для форматирования числа байтов в человеко-читаемый размер файла.

**Содержание:**

- [Функции](#функции)

## Функции

### `def naturalsize(value: float | str, binary: bool = False, gnu: bool = False, format: str = '%.1f') -> str`

Форматирует число байтов в человеко-читаемый размер файла (например, 10 kB).

По умолчанию используются десятичные суффиксы (kB, MB).

Нон-GNU режимы совместимы с фильтром `filesizeformat` Jinja2.

**Параметры:**

- `value` (`int, float, str`) — Целое число для конвертации.
- `binary` (`bool`) — Если `True`, используются бинарные суффиксы (KiB, MiB) с основанием 2<sup>10</sup>, а не 10<sup>3</sup>.
- `gnu` (`bool`) — Если `True`, игнорируется аргумент binary и используются GNU-style префиксы (K, M) с определением 2**10.
- `format` (`str`) — Кастомный форматтер.

**Возвращаемое значение:**

- `str` — Человеко-читаемое представление размера файла.

**Примеры:**

```pycon
>>> naturalsize(3000000)
'3.0 MB'
>>> naturalsize(300, False, True)
'300B'
>>> naturalsize(3000, False, True)
'2.9K'
>>> naturalsize(3000, False, True, "%.3f")
'2.930K'
>>> naturalsize(3000, True)
'2.9 KiB'
>>> naturalsize(10**28)
'10.0 RB'
>>> naturalsize(10**34 * 3)
'30000.0 QB'
>>> naturalsize(-4096, True)
'-4.0 KiB'
```


---

[← Индекс](README.md)
