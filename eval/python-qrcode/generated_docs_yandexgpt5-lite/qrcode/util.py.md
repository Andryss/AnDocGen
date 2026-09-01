# Модуль `qrcode/util.py`


Модуль содержит функции и классы для работы с QR-кодами, включая обработку данных, расчёт параметров и создание QR-кодов.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class BitBuffer`

Класс BitBuffer представляет собой инструмент для манипуляции битами.

**Назначение:**

Класс BitBuffer предназначен для работы с битами, включая их установку и получение по индексу.

**Использование:**

Для инициализации используйте метод __init__(). Для получения значения по индексу используйте метод get(index). Для установки последовательности битов используйте метод put(num, length). Для установки отдельного бита используйте метод put_bit(bit). Длину буфера можно узнать с помощью метода __len__()

#### Методы

##### `__init__()`

Инициализирует поля класса BitBuffer.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Инициализация полей класса BitBuffer

```python
self.buffer: list[int] = []
self.length = 0
```

##### `__len__()`

Возвращает длину буфера битов

**Возвращаемое значение:**

- `N/A` — длина буфера битов

**Примеры:**

Возвращает длину буфера битов

```python
return self.length
```

##### `__repr__()`

Возвращает строковое представление буфера в формате, разделённом точками.

**Возвращаемое значение:**

- `str` — строковое представление буфера

**Примеры:**

Возвращает строковое представление буфера в формате, разделённом точками

```python
return '.'.join([str(n) for n in self.buffer])
```

Пример инициализации буфера для демонстрации работы метода

```python
self.buffer = [1, 2, 3, 4]
```

##### `get(index)`

Возвращает значение по указанному индексу из буфера.

**Параметры:**

- `index` (`int`) — Индекс в буфере для получения значения

**Возвращаемое значение:**

- `bool` — Значение по указанному индексу

**Примеры:**

Получить значение по индексу из буфера

```python
BitBuffer.get(index)
```

##### `put_bit(bit)`

Метод устанавливает бит в буфере

**Параметры:**

- `bit` (`bool`) — Установить бит в буфере в значение True, если передано True, иначе не изменять буфер

**Возвращаемое значение:**

- `N/A` — N/A

**Побочные эффекты:**

Изменение внутреннего состояния объекта BitBuffer

**Примеры:**

Записать в буфер бит со значением True

```python
BitBuffer.put_bit(True)
```

##### `put(num, length)`

Метод устанавливает последовательность битов в буфере на основе числа num и длины length

**Параметры:**

- `num` (`N/A`) — Число, которое будет помещено в буфер
- `length` (`N/A`) — Длина, на которую будет помещено число num

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызов метода put_bit внутри цикла для установки битов в буфере

```python
self.put_bit(((num >> (length - i - 1)) & 1) == 1)
```

**Смотрите также:**

def put_bit(bit)

### `class QRData`

Класс для работы с данными в формате QR-кодов.

**Назначение:**

Класс QRData предназначен для хранения данных в формате, совместимом с QR-кодами.

**Использование:**

Для инициализации объекта используется метод __init__(data, mode = None, check_data = True). Метод write(buffer) записывает данные в буфер в зависимости от режима кодирования QR-кода. Для получения длины данных используется метод __len__(), а для получения строкового представления данных — метод __repr__().

#### Методы

##### `__len__()`

Возвращает длину данных в объекте QRData

**Возвращаемое значение:**

- `int` — длина данных в объекте QRData

**Примеры:**

Возвращает длину данных в объекте QRData

```python
return len(self.data)
```

##### `__repr__()`

Возвращает строковое представление данных QR-кода.

**Возвращаемое значение:**

- `str` — Строковое представление данных QR-кода

**Примеры:**

Возвращает строковое представление данных QR-кода

```python
return repr(self.data)
```

##### `write(buffer)`

Метод write() записывает данные в буфер в зависимости от режима кодирования QR-кода.

**Параметры:**

- `buffer` (`N/A`) — Буфер для записи данных

**Примеры:**

Запись данных в буфер в зависимости от режима кодирования

```python
buffer.put(int(chars), bit_length)
```

Запись данных в буфер для алфавитно-цифрового режима

```python
buffer.put(ALPHA_NUM.find(chars[0]) * 45 + ALPHA_NUM.find(chars[1]), 11)
```

##### `__init__(data, mode = None, check_data = True)`

Инициализирует объект QRData, выбирая оптимальный режим для данных, если не задан.

**Параметры:**

- `mode` (`None or int`) — Если не задан, выбирается наиболее компактный тип данных QR.
- `check_data` (`bool`) — Проверка и преобразование данных в байтовую строку.
- `data` (`str`) — Данные для инициализации объекта.

**Исключения:**

TypeError, ValueError

**Примеры:**

Инициализация объекта с данными, выбор оптимального режима, если не задан.

```python
QRData.__init__(data)
```

**Смотрите также:**

optimal_mode, to_bytestring

## Функции

### `def BCH_digit(data)`

Вычисляет количество бит в числе data.

**Параметры:**

- `data` (`int`) — данные, количество бит в которых нужно вычислить

**Возвращаемое значение:**

- `int` — количество бит в числе data

**Примеры:**

Вычисление количества бит в числе data

```python
BCH_digit(data)
```

### `def _data_count(block)`

Возвращает количество данных в переданном блоке.

**Параметры:**

- `block` (`RSBlock`) — Объект блока, для которого нужно посчитать количество данных

**Возвращаемое значение:**

- `int` — Количество данных в блоке

**Примеры:**

Вызвать функцию _data_count с блоком RSBlock

```python
_data_count(RSBlock())
```

### `def _lost_point_level1(modules, modules_count)`

Вычисляет количество потерянных точек уровня 1 в модулях QR-кода.

**Параметры:**

- `modules` (`list`) — список модулей для анализа
- `modules_count` (`int`) — количество модулей

**Возвращаемое значение:**

- `int` — количество потерянных точек

**Примеры:**

Вычисление потерянных точек уровня 1

```python
_lost_point_level1(modules, modules_count)
```

### `def _lost_point_level2(modules, modules_count)`

Вычисляет количество потерянных точек в модулях QR-кода.

**Параметры:**

- `modules` (`list`) — список модулей для анализа
- `modules_count` (`int`) — количество модулей

**Возвращаемое значение:**

- `int` — количество потерянных точек

**Примеры:**

Вычисление потерянных точек для заданного количества модулей.

```python
_lost_point_level2(modules, modules_count)
```

### `def _lost_point_level4(modules, modules_count)`

Вычисляет рейтинг на основе анализа тёмных модулей и их количества.

**Параметры:**

- `modules` (`list`) — список модулей для анализа
- `modules_count` (`int`) — количество модулей

**Возвращаемое значение:**

- `int` — рейтинг, рассчитанный на основе анализа модулей

**Примеры:**

Вычисление рейтинга на основе тёмных модулей и их количества

```python
_lost_point_level4(modules, modules_count)
```

### `def _optimal_split(data, pattern)`

Разбивает данные на части в соответствии с шаблоном.

**Параметры:**

- `pattern` (`str`) — шаблон для поиска в данных
- `data` (`str`) — данные для обработки

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример вызова функции _optimal_split

```python
while data:
 match = re.search(pattern, data)
 if not match:
 break
 start, end = match.start(), match.end()
 if start:
 yield False, data[:start]
 yield True, data[start:end]
 data = data[end:]
 if data:
 yield False, data
```

Определение функции _optimal_split

```python
def _optimal_split(data, pattern):
 while data:
 match = re.search(pattern, data)
 if not match:
 break
 start, end = match.start(), match.end()
 if start:
 yield False, data[:start]
 yield True, data[start:end]
 data = data[end:]
 if data:
 yield False, data
```

### `def check_version(version)`

Проверяет, находится ли версия QR-кода в диапазоне от 1 до 40, и вызывает ValueError, если версия выходит за пределы допустимого диапазона.

**Параметры:**

- `version` (`int`) — версия QR-кода, которая должна быть в диапазоне от 1 до 40

**Исключения:**

ValueError

**Примеры:**

Проверить версию 41, которая выходит за пределы допустимого диапазона

```python
check_version(41)
```

Проверить допустимую версию 5

```python
check_version(5)
```

### `def _lost_point_level3(modules, modules_count)`

Вычисляет количество потерянных точек в массиве модулей.

**Параметры:**

- `modules` (`list`) — Массив модулей для обработки.
- `modules_count` (`int`) — Количество модулей.

**Возвращаемое значение:**

- `int` — Количество потерянных точек.

**Примеры:**

Пример вызова функции _lost_point_level3.

```python
def _lost_point_level3(modules, modules_count):
    modules_range = range(modules_count)
    modules_range_short = range(modules_count - 10)
    lost_point = 0

    for row in modules_range:
        this_row = modules[row]
        modules_range_short_iter = iter(modules_range_short)
        col = 0
        for col in modules_range_short_iter:
            if (
                not this_row[col + 1]
                and this_row[col + 4]
                and not this_row[col + 5]
                and this_row[col + 6]
                and not this_row[col + 9]
                and (
                    (
                        this_row[col + 0]
                        and this_row[col + 2]
                        and this_row[col + 3]
                        and not this_row[col + 7]
                        and not this_row[col + 8]
                        and not this_row[col + 10]
                    )
                    or (
                        not this_row[col + 0]
                        and not this_row[col + 2]
                        and not this_row[col + 3]
                        and this_row[col + 7]
                        and this_row[col + 8]
                        and this_row[col + 10]
                    )
                )
            ):
                lost_point += 40
            # horspool algorithm.
            # if this_row[col + 10]:
            #   pattern1 shift 4, pattern2 shift 2. So min=2.
            # else:
            #   pattern1 shift 1, pattern2 shift 1. So min=1.
            if this_row[col + 10]:
                next(modules_range_short_iter, None)

    for col in modules_range:
        modules_range_short_iter = iter(modules_range_short)
        row = 0
        for row in modules_range_short_iter:
            if (
                not modules[row + 1][col]
                and modules[row + 4][col]
                and not modules[row + 5][col]
                and modules[row + 6][col]
                and not modules[row + 9][col]
                and (
                    (
                        modules[row + 0][col]
                        and modules[row + 2][col]
                        and modules[row + 3][col]
                        and not modules[row + 7][col]
                        and not modules[row + 8][col]
                        and not modules[row + 10][col]
                    )
                    or (
                        not modules[row + 0][col]
                        and not modules[row + 2][col]
                        and not modules[row + 3][col]
                        and modules[row + 7][col]
                        and modules[row + 8][col]
                        and modules[row + 10][col]
                    )
                )
            ):
                lost_point += 40
            if modules[row + 10][col]:
                next(modules_range_short_iter, None)

    return lost_point
```

N/A

```N/A
N/A
```

### `def create_bytes(buffer: BitBuffer, rs_blocks: list[RSBlock])`

Создаёт список байтов на основе переданного буфера и списка блоков RS.

**Параметры:**

- `buffer` (`BitBuffer`) — Буфер данных для обработки
- `rs_blocks` (`list[RSBlock]`) — Список блоков RS для обработки

**Возвращаемое значение:**

- `list[int]` — Список данных

**Примеры:**

Пример вызова функции create_bytes с передачей буфера и списка блоков RS

```python
create_bytes(buffer, rs_blocks)
```

### `def mode_sizes_for_version(version)`

Определяет размер режима для заданной версии QR-кода

**Параметры:**

- `version` (`int`) — Версия QR-кода

**Возвращаемое значение:**

- `str` — Возвращает один из трёх предопределённых размеров режима в зависимости от версии QR-кода

**Примеры:**

Возвращает MODE_SIZE_SMALL для версии 1

```python
mode_sizes_for_version(1)
```

Возвращает MODE_SIZE_MEDIUM для версии 20

```python
mode_sizes_for_version(20)
```

Возвращает MODE_SIZE_LARGE для версии 40

```python
mode_sizes_for_version(40)
```

### `def mask_func(pattern)`

Возвращает функцию маски для заданного шаблона маски.

**Параметры:**

- `pattern` (`int`) — Возвращает функцию маски для заданного шаблона маски

**Возвращаемое значение:**

- `lambda` — Функция маски для заданного шаблона

**Исключения:**

TypeError: Bad mask pattern: pattern

**Примеры:**

Возвращает функцию маски для шаблона 0

```python
mask_func(0)
```

Возвращает функцию маски для шаблона 1

```python
mask_func(1)
```

Возвращает функцию маски для шаблона 2

```python
mask_func(2)
```

Возвращает функцию маски для шаблона 3

```python
mask_func(3)
```

Возвращает функцию маски для шаблона 4

```python
mask_func(4)
```

Возвращает функцию маски для шаблона 5

```python
mask_func(5)
```

Возвращает функцию маски для шаблона 6

```python
mask_func(6)
```

Возвращает функцию маски для шаблона 7

```python
mask_func(7)
```

### `def optimal_mode(data)`

Вычисляет оптимальный режим для заданного блока данных

**Параметры:**

- `data` (`str`) — данные, для которых вычисляется оптимальный режим

**Возвращаемое значение:**

- `str` — оптимальный режим данных

**Примеры:**

Вычисление оптимального режима для числовых данных

```python
optimal_mode('123')
```

Вычисление оптимального режима для алфавитно-числовых данных

```python
optimal_mode('abc123')
```

### `def pattern_position(version)`

Возвращает позицию паттерна для заданной версии QR-кода.

**Параметры:**

- `version` (`int`) — Версия QR-кода, целое число от 1 до 40

**Возвращаемое значение:**

- `int` — Позиция паттерна для заданной версии QR-кода

**Примеры:**

Получить позицию паттерна для версии 1 QR-кода

```python
pattern_position(1)
```

### `def to_bytestring(data)`

Преобразует данные в байтовую строку (utf-8 кодировка), если они не являются байтовой строкой.

**Параметры:**

- `data` (`any`) — Данные, которые нужно преобразовать в байтовую строку, если они ещё не являются байтовой строкой.

**Возвращаемое значение:**

- `bytes` — Байтовая строка (utf-8 кодировка).

**Примеры:**

Преобразовать строку в байтовую строку.

```python
to_bytestring('some data')
```

### `def BCH_type_info(data)`

N/A

**Параметры:**

- `data` (`N/A`) — Данные для обработки

**Возвращаемое значение:**

- `N/A` — Результат обработки данных

**Примеры:**

Вызвать функцию BCH_type_info с аргументом data

```python
BCH_type_info(data)
```

**Смотрите также:**

def BCH_digit(data) — Вычисляет количество бит в числе data.

### `def BCH_type_number(data)`

N/A

**Параметры:**

- `data` (`N/A`) — Данные для обработки

**Возвращаемое значение:**

- `N/A` — Результат обработки данных

**Примеры:**

Пример вызова функции BCH_type_number

```python
BCH_type_number(data)
```

**Смотрите также:**

def BCH_digit(data) — Вычисляет количество бит в числе data.

### `def lost_point(modules)`

Вычисляет общее количество потерянных точек в модулях QR-кода.

**Параметры:**

- `modules` (`list`) — Список модулей QR-кода

**Возвращаемое значение:**

- `int` — Общее количество потерянных точек

**Примеры:**

Вычисление количества потерянных точек в модулях QR-кода

```python
lost_point(modules)
```

**Смотрите также:**

def _lost_point_level1(modules, modules_count), def _lost_point_level2(modules, modules_count), def _lost_point_level3(modules, modules_count), def _lost_point_level4(modules, modules_count)

### `def length_in_bits(mode, version)`

Возвращает количество бит, соответствующее заданному режиму и версии QR-кода

**Параметры:**

- `mode` (`str`) — Режим QR-кода, может быть одним из следующих значений: MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE, MODE_KANJI
- `version` (`int`) — Версия QR-кода, должна быть в диапазоне от 1 до 40

**Возвращаемое значение:**

- `int` — Количество бит, соответствующее заданному режиму и версии QR-кода

**Исключения:**

TypeError

**Примеры:**

Вычисление длины в битах для заданного режима и версии QR-кода

```python
length_in_bits(MODE_NUMBER, 1)
```

**Смотрите также:**

check_version, mode_sizes_for_version

### `def optimal_data_chunks(data, minimum = 4)`

Возвращает итератор, который возвращает чанки QRData, оптимизированные под содержимое данных.

**Параметры:**

- `minimum` (`int`) — минимальное количество байт в строке для разделения на чанки
- `data` (`bytes`) — данные для разделения на чанки

**Возвращаемое значение:**

- `iterator` — итератор, возвращающий чанки QRData, оптимизированные под содержимое данных

**Примеры:**

Вызов функции с минимальным количеством байт равным 4

```python
optimal_data_chunks(b'some data')
```

**Смотрите также:**

_optimal_split(data, pattern), to_bytestring(data)

### `def create_data(version, error_correction, data_list)`

Создаёт данные для QR-кода, используя заданную версию, уровень коррекции ошибок и список данных.

**Параметры:**

- `version` (`int`) — Версия QR-кода, целое число от 1 до 40, контролирующее размер QR-кода
- `error_correction` (`qrcode.constants.ERROR_CORRECT_L`) — Уровень коррекции ошибок
- `data_list` (`list`) — Список данных для кодирования

**Возвращаемое значение:**

- `bytes` — Созданные байты на основе буфера и блоков RS

**Исключения:**

exceptions.DataOverflowError

**Примеры:**

Создание данных для QR-кода версии 1 с коррекцией ошибок уровня L и списком данных ['some_data']

```python
create_data(1, qrcode.constants.ERROR_CORRECT_L, ['some_data'])
```

**Смотрите также:**

create_bytes(buffer: BitBuffer, rs_blocks: list[RSBlock]), length_in_bits(mode, version)


---

[← qrcode](README.md) | [← К проекту](../README.md)
