# Модуль `main.py`


Модуль для создания и работы с QR-кодами.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class ActiveWithNeighbors(NamedTuple)`

Класс для представления активного элемента с его соседями.

**Поля:**

- `NW` (`bool`) — —
- `N` (`bool`) — —
- `NE` (`bool`) — —
- `W` (`bool`) — —
- `me` (`bool`) — —
- `E` (`bool`) — —
- `SW` (`bool`) — —
- `S` (`bool`) — —
- `SE` (`bool`) — —

#### Методы

##### `__bool__() -> bool`

Возвращает значение `self.me`.

**Возвращаемое значение:**

- `bool` — значение `self.me`

**Примеры:**

```python
# Пример использования метода __bool__
obj = ActiveWithNeighbors()
print(bool(obj))  # Вывод будет значением obj.me
```

## Функции

### `def _check_border(size)`

Проверяет значение границы и выбрасывает исключение ValueError, если значение меньше 0.

**Параметры:**

- `size` (`int`) — значение границы для проверки

**Исключения:**

- `ValueError` — если значение меньше 0

**Примеры:**

```python
_check_border(5)  # Допустимо, не выбрасывает исключение
_check_border(-1)  # Выбрасывает ValueError: Invalid border value (was -1, expected 0 or larger than that)
```

### `def _check_box_size(size)`

Проверяет валидность размера коробки и выбрасывает исключение, если размер не является положительным числом.

**Параметры:**

- `size` (`int`) — размер коробки

**Исключения:**

- `ValueError` — если `size` меньше или равен 0

**Примеры:**

```python
_check_box_size(5)  # Нет исключения
_check_box_size(-1) # Вызывает ValueError: Invalid box size (was -1, expected larger than 0)
```

### `def _check_mask_pattern(mask_pattern)`

Проверяет валидность маски шаблона.

**Параметры:**

- `mask_pattern` (`int`) — паттерн маски

**Исключения:**

- `TypeError` — если `mask_pattern` не является целым числом
- `ValueError` — если значение `mask_pattern` не в диапазоне от 0 до 7

**Примеры:**

```python
# Правильный пример использования
_check_mask_pattern(4)

# Пример с ошибкой типа
try:
    _check_mask_pattern("invalid")
except TypeError as e:
    print(e)  # Вывод: Invalid mask pattern (was <class 'str'>, expected int)

# Пример с ошибкой значения
try:
    _check_mask_pattern(8)
except ValueError as e:
    print(e)  # Вывод: Mask pattern should be in range(8) (got 8)
```

### `def copy_2d_array(x)`

Копирует двумерный массив и возвращает его копию.

**Параметры:**

- `x` (`list`) — двумерный массив, который нужно скопировать

**Возвращаемое значение:**

- `list` — копия двумерного массива `x`

**Примеры:**

```python
original = [[1, 2], [3, 4]]
copied = copy_2d_array(original)
print(copied)  # Output: [[1, 2], [3, 4]]
```

### `def make(data = None, **kwargs)`

Создает изображение QR-кода на основе предоставленных данных и параметров.

**Параметры:**

- `data` (`str, optional`) — данные для кодирования в QR-коде. По умолчанию `None`.
- `**kwargs` — дополнительные аргументы, передаваемые при создании экземпляра `QRCode`.

**Возвращаемое значение:**

- `BaseImage` — изображение QR-кода.

**Примеры:**

```python
from main import make

qr_image = make(data="https://example.com", border=4)
qr_image.show()
```

**Смотрите также:**

- `qrcode.QRCode`


---

[← Индекс](README.md)
