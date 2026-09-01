# Модуль `qrcode/main.py`


Модуль python-qrcode для генерации QR-кодов. Содержит функции для проверки параметров и классы для создания QR-кодов с различными настройками.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class ActiveWithNeighbors(NamedTuple)`

Класс ActiveWithNeighbors является наследником NamedTuple.

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

Возвращает значение self.me в виде логического значения

**Возвращаемое значение:**

- `bool` — Возвращает значение self.me

**Примеры:**

Проверка истинности объекта ActiveWithNeighbors

```python
return self.me
```

### `class QRCode(Generic[GenericImage])`

Класс QRCode предназначен для создания QR-кодов с различными настройками и параметрами.

**Назначение:**

Класс для генерации QR-кодов с заданными параметрами версии, коррекции ошибок, размера бокса, границы и фабрики изображений.

**Использование:**

Для использования класса QRCode необходимо создать его экземпляр и вызвать методы для инициализации параметров, добавления данных, компиляции данных в массив QR-кода и создания изображения QR-кода. Методы класса позволяют настраивать различные параметры QR-кода, такие как версия, коррекция ошибок, размер бокса, граница и шаблон маски.

**Поля:**

- `modules` (`ModulesType`) — —
- `_version` (`int | None`) — —

#### Методы

##### `clear()`

Сбрасывает внутренние данные объекта QRCode.

**Побочные эффекты:**

Сброс внутренних данных объекта QRCode

**Примеры:**

Сброс внутренних данных объекта QRCode

```python
qr.clear()
```

##### `add_data(data, optimize = 20)`

Добавляет данные в QR-код.

**Параметры:**

- `optimize` (`int`) — Данные будут разделены на несколько частей для оптимизации размера QR-кода путём поиска более сжатых режимов длиной не менее этого значения. Установите в 0, чтобы избежать оптимизации.
- `data` (`util.QRData`) — Данные для добавления в QR-код.

**Примеры:**

Пример использования метода add_data для добавления данных в QR-код

```python
import qrcode
qr = qrcode.QRCode(
version=1,
error_correction=qrcode.constants.ERROR_CORRECT_L,
box_size=10,
border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
```

##### `is_constrained(row: int, col: int) -> bool`

Проверяет, что координаты строки и столбца соответствуют допустимым значениям в QR-коде.

**Параметры:**

- `row` (`int`) — Проверка, что строка и столбец находятся в допустимых пределах
- `col` (`int`) — Проверка, что строка и столбец находятся в допустимых пределах

**Возвращаемое значение:**

- `bool` — True, если координаты допустимы, False - иначе

**Примеры:**

Проверка ограничения координат для QR-кода

```python
import qrcode
qr = qrcode.QRCode()
qr.add_data('Some data')
qr.make(fit=True)
img = qr.is_constrained(0, 0)
```

##### `map_data(data, mask_pattern)`

Отображает данные в QR-коде с использованием шаблона маски.

**Параметры:**

- `data` (`N/A`) — Данные для отображения в QR-коде
- `mask_pattern` (`N/A`) — Шаблон маски для отображения в QR-коде

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример вызова метода map_data

```python
QRCode.map_data(data, mask_pattern)
```

##### `setup_position_adjust_pattern()`

Метод setup_position_adjust_pattern выполняет настройку паттерна для корректировки положения в QR-коде.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызов метода setup_position_adjust_pattern

```python
import qrcode
qr = qrcode.QRCode()
qr.setup_position_adjust_pattern()
```

##### `setup_timing_pattern()`

Настройка временного шаблона QR-кода.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Настройка временного шаблона QR-кода

```python
QRCode.setup_timing_pattern()
```

##### `setup_position_probe_pattern(row, col)`

Настройка шаблона для определения позиции

**Параметры:**

- `row` (`int`) — Настройка шаблона для определения позиции по строке и столбцу
- `col` (`int`) — Настройка шаблона для определения позиции по строке и столбцу

**Примеры:**

Настройка шаблона для определения позиции

```python
QRCode.setup_position_probe_pattern(row, col)
```

##### `setup_type_number()`

Метод setup_type_number выполняет внутренние вычисления для настройки типа и номера в QR-коде.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызов метода setup_type_number

```python
QRCode.setup_type_number()
```

##### `setup_type_info(mask_pattern)`

Настройка информации о типе в QR-коде с использованием заданного шаблона маски.

**Параметры:**

- `mask_pattern` (`N/A`) — Шаблон маски для настройки информации о типе

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Настройка информации о типе с использованием mask_pattern

```python
QRCode.setup_type_info(mask_pattern)
```

##### `active_with_neighbors(row: int, col: int) -> ActiveWithNeighbors`

Проверяет активность элемента QR-кода в заданном ряду и столбце и возвращает соответствующий контекст

**Параметры:**

- `row` (`int`) — Проверяет активность элемента QR-кода в заданном ряду и столбце
- `col` (`int`) — Проверяет активность элемента QR-кода в заданном ряду и столбце

**Возвращаемое значение:**

- `ActiveWithNeighbors` — Возвращает объект ActiveWithNeighbors, содержащий контекст активности элемента

**Примеры:**

Вызвать метод active_with_neighbors для проверки активности элемента QR-кода

```python
import qrcode
qr = qrcode.QRCode()
qr.active_with_neighbors(2, 2)
```

**Смотрите также:**

def is_constrained(row: int, col: int) -> bool

##### `mask_pattern(pattern)`

Устанавливает шаблон маски и проверяет его корректность.

**Параметры:**

- `pattern` (`N/A`) — Устанавливает шаблон маски

**Примеры:**

Установка шаблона маски

```python
_check_mask_pattern(pattern) 
 self._mask_pattern = pattern
```

**Смотрите также:**

def _check_mask_pattern(mask_pattern)

##### `__init__(version = None, error_correction = constants.ERROR_CORRECT_M, box_size = 10, border = 4, image_factory: type[GenericImage] | None = None, mask_pattern = None)`

Инициализирует объект QRCode с заданными параметрами версии, коррекции ошибок, размера бокса, границы и фабрики изображений.

**Параметры:**

- `version` (`int`) — Версия QR-кода, целое число от 1 до 40, контролирующее размер QR-кода
- `error_correction` (`int`) — Уровень коррекции ошибок
- `box_size` (`int`) — Размер бокса
- `border` (`int`) — Ширина границы
- `image_factory` (`type[GenericImage] | None`) — Фабрика изображений
- `mask_pattern` (`None`) — Шаблон маски

**Примеры:**

Создание экземпляра QRCode и генерация изображения QR-кода

```python
import qrcode
qr = qrcode.QRCode(
version=1,
error_correction=qrcode.constants.ERROR_CORRECT_L,
box_size=10,
border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
```

Генерация QR-кода с использованием функции make

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

##### `makeImpl(mask_pattern)`

Метод makeImpl выполняет внутреннюю настройку параметров QR-кода в соответствии с заданным шаблоном маски.

**Параметры:**

- `mask_pattern` (`N/A`) — Шаблон маски, используемый для настройки информации о типе в QR-коде

**Примеры:**

Использование класса QRCode для создания QR-кода

```python
import qrcode
qr = qrcode.QRCode(
version=1,
error_correction=qrcode.constants.ERROR_CORRECT_L,
box_size=10,
border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
```

Использование функции make для создания QR-кода

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

**Смотрите также:**

copy_2d_array, map_data, setup_position_adjust_pattern, setup_position_probe_pattern, setup_timing_pattern, setup_type_info, setup_type_number

##### `best_mask_pattern()`

Находит наиболее эффективный шаблон маски для QR-кода.

**Возвращаемое значение:**

- `int` — наиболее эффективный шаблон маски

**Примеры:**

Найти наиболее эффективный шаблон маски для QR-кода.

```python
import qrcode
qr = qrcode.QRCode()
qr.best_mask_pattern()
```

**Смотрите также:**

def makeImpl(mask_pattern)

##### `best_fit(start = None)`

Находит минимальный размер, необходимый для размещения данных.

**Параметры:**

- `start` (`int`) — Начальное значение для поиска минимального размера, если не задано, используется 1

**Возвращаемое значение:**

- `int` — Версия QRCode, соответствующая минимальному размеру для данных

**Исключения:**

exceptions.DataOverflowError

**Примеры:**

Создание экземпляра класса QRCode с заданными параметрами

```python
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
```

Добавление данных в экземпляр QRCode

```python
qr.add_data('Some data')
```

Поиск минимального размера для данных

```python
qr.best_fit(start=1)
```

##### `get_matrix()`

Возвращает QR Code в виде многомерного массива, включая границу. Для возврата массива без границы сначала установите self.border равным 0.

**Возвращаемое значение:**

- `list` — Многомерный массив, представляющий QR Code, включая границу

**Примеры:**

Создание экземпляра класса QRCode с заданными параметрами

```python
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
```

Добавление данных в экземпляр QRCode

```python
qr.add_data('Some data')
```

Создание QRCode с автоматическим определением размера

```python
qr.make(fit=True)
```

Получение QRCode в виде многомерного массива

```python
img = qr.get_matrix()
```

##### `make(fit = True)`

Компилирует данные в массив QR-кода.

**Параметры:**

- `fit` (`bool`) — Если True (или если размер не был предоставлен), найти наилучшее соответствие для данных, чтобы избежать ошибок переполнения данных

**Возвращаемое значение:**

- `array` — QR-код в виде массива

**Примеры:**

Пример использования функции make для создания QR-кода из строки

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

Пример использования класса QRCode для создания QR-кода с заданными параметрами

```python
import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
```

**Смотрите также:**

def best_mask_pattern(), def makeImpl(mask_pattern)

##### `make_image(image_factory = None, **kwargs)`

Создаёт изображение QR-кода из данных. Если данные ещё не были скомпилированы, делает это сначала.

**Параметры:**

- `image_factory` (`BaseImage`) — Фабрика изображений для создания изображения QR-кода. Если не указан, используется стандартная фабрика изображений.
- `**kwargs` — —

**Возвращаемое значение:**

- `BaseImage` — Изображение QR-кода

**Исключения:**

ValueError

**Примеры:**

Создание QR-кода с заданными параметрами и генерация изображения из него

```python
import qrcode
qr = qrcode.QRCode(
 version=1,
 error_correction=qrcode.constants.ERROR_CORRECT_L,
 box_size=10,
 border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
```

Создание QR-кода с помощью функции make и сохранение его в файл

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

**Смотрите также:**

def _check_box_size(size)

##### `print_ascii(out = None, tty = False, invert = False)`

Выводит QR-код, используя ASCII-символы.

**Параметры:**

- `out` (`object`) — вывод, по умолчанию sys.stdout
- `tty` (`bool`) — использовать фиксированные TTY цветовые коды (приводит к invert=True)
- `invert` (`bool`) — инвертировать ASCII-символы (сплошной <-> прозрачный)

**Исключения:**

OSError: Not a tty

**Примеры:**

Вывести QR-код с использованием ASCII-символов по умолчанию

```python
QRCode.print_ascii()
```

Вывести QR-код с использованием ASCII-символов и фиксированных TTY цветовых кодов

```python
QRCode.print_ascii(tty=True)
```

##### `print_tty(out = None)`

Выводит QR-код, используя только цвета TTY.

**Параметры:**

- `out` (`object`) — Вывод, используемый для печати QR-кода в TTY. Если не указано, используется sys.stdout.

**Исключения:**

OSError: Not a tty

**Примеры:**

Вывести QR-код, используя только цвета TTY.

```python
QRCode.print_tty()
```

**Смотрите также:**

def make(fit = True) — компилирует данные в массив QR-кода.

##### `version(value) -> None`

Устанавливает версию QR-кода

**Параметры:**

- `value` (`int`) — Устанавливает версию QR-кода, целое число от 1 до 40, которое контролирует размер QR-кода

**Возвращаемое значение:**

- `None` — N/A

**Примеры:**

Создание QR-кода с указанием версии

```python
import qrcode
qr = qrcode.QRCode(version=1)
qr.add_data('Some data')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
```

Создание QR-кода с указанием версии через прямое присвоение

```python
import qrcode
qr = qrcode.QRCode()
qr.version = 1
qr.add_data('Some data')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
```

**Смотрите также:**

def best_fit(start = None)

## Функции

### `def _check_border(size)`

Проверяет, что значение размера границы неотрицательное, иначе вызывает ошибку ValueError.

**Параметры:**

- `size` (`str`) — Проверяет, что значение размера границы неотрицательное

**Исключения:**

ValueError

**Примеры:**

Проверка отрицательного значения размера границы

```python
_check_border(-1)
```

### `def _check_box_size(size)`

Проверяет, что переданный размер бокса больше нуля. Если условие не выполняется, возбуждается исключение ValueError.

**Параметры:**

- `size` (`str`) — Проверка корректности размера бокса, передаваемого в функцию

**Исключения:**

ValueError

**Примеры:**

Проверка корректности размера бокса

```python
_check_box_size(10)
```

### `def _check_mask_pattern(mask_pattern)`

Проверяет корректность шаблона маски. Если шаблон не задан, функция завершает работу. Если шаблон не является целым числом, выбрасывает TypeError. Если шаблон выходит за пределы диапазона от 0 до 7, выбрасывает ValueError.

**Параметры:**

- `mask_pattern` (`int`) — Проверяемый шаблон маски (должен быть целым числом в диапазоне от 0 до 7)

**Исключения:**

TypeError, ValueError

**Примеры:**

Проверка корректности значения параметра mask_pattern

```python
_check_mask_pattern(5)
```

### `def copy_2d_array(x)`

Создаёт копию двумерного массива.

**Параметры:**

- `x` (`list`) — двумерный массив для копирования

**Возвращаемое значение:**

- `list` — копия двумерного массива x

**Примеры:**

Копирование двумерного массива

```python
return [row[:] for row in x]
```

### `def make(data = None, **kwargs)`

Создаёт QR-код на основе переданных данных и дополнительных аргументов.

**Параметры:**

- `data` (`N/A`) — Данные для кодирования в QR-код
- `**kwargs` — —

**Возвращаемое значение:**

- `BaseImage` — Созданный QR-код в виде изображения

**Примеры:**

Использование функции make для создания QR-кода с данными

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

Использование класса QRCode для более детального контроля над созданием QR-кода

```python
import qrcode
qr = qrcode.QRCode(
version=1,
error_correction=qrcode.constants.ERROR_CORRECT_L,
box_size=10,
border=4,
)
qr.add_data('Some data')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
```


---

[← qrcode](README.md) | [← К проекту](../README.md)
