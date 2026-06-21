# Модуль `util.py`


Модуль с вспомогательными функциями и классами для работы с QR-кодами.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class QRData`

Класс для работы с данными в формате QR.

#### Методы

##### `__len__()`

Возвращает количество элементов в списке `data`.

**Возвращаемое значение:**

- `int` — количество элементов в списке `data`

**Примеры:**

```python
qr_data = QRData(data=[1, 2, 3])
print(len(qr_data))  # Output: 3
```

##### `__repr__()`

Возвращает строковое представление объекта QRData.

**Возвращаемое значение:**

- `str` — строковое представление данных QRCode

**Примеры:**

```python
# Пример использования
qr_data = QRData("Пример данных")
print(qr_data.__repr__())  # Выведет: 'Пример данных'
```

##### `write(buffer)`

Метод `write` записывает данные в буфер в зависимости от текущего режима.

**Параметры:**

- `buffer` (`object`) — объект для записи данных

**Примеры:**

```python
qr_data = QRData(mode=MODE_NUMBER, data="12345")
buffer = Buffer()
qr_data.write(buffer)
```

##### `__init__(data, mode = None, check_data = True)`

Инициализирует объект `QRData` с предоставленными данными и опциональным режимом.

**Параметры:**

- `data` (`any`) — данные для кодирования в QR-код
- `mode` (`int, optional`) — режим кодирования (по умолчанию: None)
- `check_data` (`bool, optional`) — проверять данные на соответствие выбранному режиму (по умолчанию: True)

**Исключения:**

- `TypeError` — если предоставленный режим недопустим
- `ValueError` — если данные не могут быть представлены в заданном режиме

**Примеры:**

```python
qr_data = QRData("123")  # автоматический выбор режима
qr_data = QRData("abc", MODE_ALPHA_NUM)  # явный выбор режима
qr_data = QRData(123, check_data=False)  # отключение проверки данных
```

**Смотрите также:**

- `optimal_mode`
- `to_bytestring`

### `class BitBuffer`

Класс для работы с битовым буфером.

#### Методы

##### `__init__()`

Инициализирует новый объект `BitBuffer`.

**Примеры:**

```python
bit_buffer = BitBuffer()
```

##### `__len__()`

Возвращает длину буфера бит.

**Возвращаемое значение:**

- `int` — длина буфера бит

**Примеры:**

```python
buffer = BitBuffer()
print(len(buffer))  # Выведет: 0
```

##### `__repr__()`

Возвращает строковое представление объекта BitBuffer.

**Возвращаемое значение:**

- `str` — строковое представление объекта BitBuffer, состоящее из элементов буфера, разделенных точками

**Примеры:**

```python
buffer = BitBuffer([1, 2, 3])
print(buffer.__repr__())  # Вывод: "1.2.3"
```

##### `get(index)`

Получает значение бита по указанному индексу в буфере.

**Параметры:**

- `index` (`int`) — индекс бита для получения

**Возвращаемое значение:**

- `bool` — значение бита (True или False)

**Примеры:**

```python
buffer = BitBuffer()
# Инициализация буфера и добавление данных...

value = buffer.get(5)
print(value)  # Вывод значения бита на позиции 5
```

##### `put(num, length)`

Добавляет битовое представление числа в буфер.

**Параметры:**

- `num` (`int`) — число для добавления
- `length` (`int`) — количество бит, которые нужно записать

**Примеры:**

```python
buffer = BitBuffer()
buffer.put(5, 3)
```

##### `put_bit(bit)`

Помещает бит в буфер BitBuffer.

**Параметры:**

- `bit` (`bool`) — бит, который нужно поместить в буфер

**Побочные эффекты:**

Изменяет состояние объекта `BitBuffer`, добавляя новый бит и увеличивая длину буфера.

**Примеры:**

```python
bb = BitBuffer()
bb.put_bit(True)
bb.put_bit(False)
```

## Функции

### `def BCH_digit(data)`

Возвращает количество бит в двоичном представлении числа.

**Параметры:**

- `data` (`int`) — число, для которого нужно определить количество бит

**Возвращаемое значение:**

- `int` — количество бит в двоичном представлении числа

**Примеры:**

```python
print(BCH_digit(0))  # Output: 0
print(BCH_digit(1))  # Output: 1
print(BCH_digit(2))  # Output: 2
```

### `def _data_count(block)`

Возвращает количество данных в блоке.

**Параметры:**

- `block` (`object`) — объект блока

**Возвращаемое значение:**

- `int` — количество данных в блоке

**Примеры:**

```python
# Пример использования
result = _data_count(block_instance)
```

### `def _lost_point_level1(modules, modules_count)`

Вычисляет количество "потерянных" точек на основе модулей и их длины.

**Параметры:**

- `modules` (`list`) — список модулей, где каждый модуль представлен как список строк
- `modules_count` (`int`) — общее количество модулей

**Возвращаемое значение:**

- `int` — количество "потерянных" точек

**Примеры:**

```python
# Пример вызова функции
modules = [
    ['A', 'A', 'A', 'A', 'A', 'B'],
    ['B', 'B', 'B', 'C', 'C', 'C']
]
modules_count = 6
print(_lost_point_level1(modules, modules_count))  # Output: 2
```

### `def _lost_point_level2(modules, modules_count)`

Функция `_lost_point_level2` вычисляет количество потеряных баллов в зависимости от модулей и их количества.

**Параметры:**

- `modules` (`list`) — список модулей
- `modules_count` (`int`) — количество модулей

**Возвращаемое значение:**

- `int` — количество потерянных баллов

**Примеры:**

```python
# Пример использования функции
lost_point = _lost_point_level2([[1, 2], [3, 4]], 2)
print(lost_point)  # Вывод будет зависеть от конкретной реализации и логики функции
```

### `def _lost_point_level3(modules, modules_count)`

Функция `_lost_point_level3` считает количество потерь очков на основе переданных модулей и их количества.

**Параметры:**

- `modules` (`list`) — двумерный список модулей
- `modules_count` (`int`) — количество модулей

**Возвращаемое значение:**

- `int` — общее количество потерянных очков

**Примеры:**

```python
lost_points = _lost_point_level3([[0, 1, 2], [3, 4, 5]], 2)
print(lost_points)  # Output будет зависеть от условий в функции
```

### `def _lost_point_level4(modules, modules_count)`

Вычисляет рейтинг на основе суммы значений в матрице модулей и количества модулей.

**Параметры:**

- `modules` (`list`) — двумерный список числовых значений, представляющий матрицу модулей.
- `modules_count` (`int`) — количество модулей в одной строке (или столбце) матрицы.

**Возвращаемое значение:**

- `int` — рейтинг от 0 до 100, где каждые 5% отклонения от 50% увеличивают рейтинг на 10 пунктов.

**Примеры:**

```python
# Пример использования функции:
result = _lost_point_level4([[1, 2, 3], [4, 5, 6]], 3)
print(result)  # Вывод будет зависеть от конкретных значений в матрице и их суммы
```

### `def _optimal_split(data, pattern)`

Рекурсивно разделяет данные на части в соответствии с заданным шаблоном.

**Параметры:**

- `data` (`str`) — входные данные для разделения
- `pattern` (`str`) — регулярное выражение для определения разделителя

**Примеры:**

```python
for part, is_match in _optimal_split("abc123def", r'\d+'):
    print(part, is_match)
```

### `def check_version(version)`

Проверяет корректность версии и выбрасывает исключение, если она не в диапазоне от 1 до 40.

**Параметры:**

- `version` (`int`) — версия для проверки

**Исключения:**

- `ValueError` — если версия меньше 1 или больше 40

**Примеры:**

```python
try:
    check_version(25)  # верно, ничего не произойдет
    check_version(0)   # выбросит ValueError: Invalid version (was 0, expected 1 to 40)
    check_version(41)  # выбросит ValueError: Invalid version (was 41, expected 1 to 40)
except ValueError as e:
    print(e)
```

### `def create_bytes(buffer: BitBuffer, rs_blocks: list[RSBlock])`

Создает байты из данных блоков RS и добавляет в список.

**Параметры:**

- `buffer` (`BitBuffer`) — буфер с данными для обработки
- `rs_blocks` (`list[RSBlock]`) — список блоков RS с информацией о количестве данных и общем количестве

**Примеры:**

```python
# Пример вызова функции create_bytes
buffer = BitBuffer()  # Создаем объект буфера
rs_blocks = [RSBlock(10, 25)]  # Создаем список блоков RS
create_bytes(buffer, rs_blocks)  # Вызываем функцию create_bytes
```

### `def mask_func(pattern)`

Возвращает функцию маскирования для заданного шаблона маски.

**Параметры:**

- `pattern` (`int`) — шаблон маскирования (0 до 7)

**Возвращаемое значение:**

- `function` — функция, возвращающая булево значение в зависимости от индексов i и j

**Исключения:**

- `TypeError` — если передан недопустимый шаблон маскирования

**Примеры:**

```python
mask_func(0)(1, 2)  # False
mask_func(1)(2, 4)  # True
mask_func(2)(3, 6)  # False
mask_func(3)(5, 7)  # False
mask_func(4)(8, 9)  # True
mask_func(5)(10, 12)  # True
mask_func(6)(14, 18)  # False
mask_func(7)(20, 22)  # False
```

### `def mode_sizes_for_version(version)`

Возвращает размер режима в зависимости от версии.

**Параметры:**

- `version` (`int`) — версия QR-кода

**Возвращаемое значение:**

- `str` — один из значений: MODE_SIZE_SMALL, MODE_SIZE_MEDIUM, MODE_SIZE_LARGE

**Примеры:**

```python
mode_sizes_for_version(5)  # вернёт 'MODE_SIZE_SMALL'
mode_sizes_for_version(15) # вернёт 'MODE_SIZE_MEDIUM'
mode_sizes_for_version(30) # вернёт 'MODE_SIZE_LARGE'
```

### `def optimal_mode(data)`

Рассчитывает оптимальный режим для данного набора данных.

**Параметры:**

- `data` (`str`) — набор данных

**Возвращаемое значение:**

- `int` — оптимальный режим (MODE_NUMBER, MODE_ALPHA_NUM или MODE_8BIT_BYTE)

**Примеры:**

```python
optimal_mode("123")  # вернет MODE_NUMBER
optimal_mode("abc")  # вернет MODE_ALPHA_NUM
optimal_mode("abc123")  # вернет MODE_8BIT_BYTE
```

### `def pattern_position(version)`

Возвращает позицию шаблона для указанной версии.

**Параметры:**

- `version` (`int`) — номер версии QR-кода

**Возвращаемое значение:**

- `int` — позиция шаблона

**Примеры:**

```python
pattern_position(1)  # Возвращает 20
```

### `def to_bytestring(data)`

Преобразует данные в байтовую строку (UTF-8) если она еще не является таковой.

**Параметры:**

- `data` (`any`) — данные для преобразования

**Возвращаемое значение:**

- `bytes` — данные, преобразованные в байтовую строку UTF-8

**Примеры:**

```python
to_bytestring("Hello")  # b'Hello'
to_bytestring(b"Hello") # b'Hello'
```

### `def BCH_type_info(data)`

Функция BCH_type_info выполняет определенные операции над входным данными для вычисления информации типа BCH.

**Параметры:**

- `data` (`int`) — входные данные, на которых будут выполнены операции

**Возвращаемое значение:**

- `int` — обработанные данные после выполнения операций

**Примеры:**

```python
# Пример использования функции BCH_type_info
result = BCH_type_info(0x1234)
print(result)  # Output: конкретное значение, зависящее от реализации и входных данных
```

**Смотрите также:**

- `BCH_digit`

### `def BCH_type_number(data)`

Функция `BCH_type_number` применяет алгоритм для определения типа числа с использованием метода BCH.

**Параметры:**

- `data` (`int`) — число, которое нужно обработать

**Возвращаемое значение:**

- `int` — тип числа после применения алгоритма BCH

**Примеры:**

```python
result = BCH_type_number(0x1234)
print(result)  # Output: определённое значение в зависимости от реализации
```

**Смотрите также:**

- `BCH_digit`

### `def lost_point(modules)`

Вычисляет общее количество "потерянных" точек на основе переданных модулей и их количества.

**Параметры:**

- `modules` (`list`) — двумерный список модулей, где каждый модуль представлен как список строк или числовых значений

**Возвращаемое значение:**

- `int` — общее количество "потерянных" точек

**Примеры:**

```python
# Пример вызова функции
modules = [
    ['A', 'A', 'A', 'A', 'A', 'B'],
    ['B', 'B', 'B', 'C', 'C', 'C']
]
print(lost_point(modules))  # Output будет зависеть от реализации _lost_point_level1, _lost_point_level2, _lost_point_level3 и _lost_point_level4
```

**Смотрите также:**

- `_lost_point_level1`
- `_lost_point_level2`
- `_lost_point_level3`
- `_lost_point_level4`

### `def length_in_bits(mode, version)`

Возвращает длину в битах для указанного режима и версии QR-кода.

**Параметры:**

- `mode` (`int`) — режим QR-кода (один из MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE, MODE_KANJI)
- `version` (`int`) — версия QR-кода

**Возвращаемое значение:**

- `int` — длина в битах для указанного режима и версии

**Исключения:**

- `TypeError` — если указанный режим не является одним из допустимых (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE, MODE_KANJI)

**Примеры:**

```python
length_in_bits(MODE_NUMBER, 5)   # вернёт длину в битах для режима MODE_NUMBER и версии 5
length_in_bits(MODE_ALPHA_NUM, 10) # вернёт длину в битах для режима MODE_ALPHA_NUM и версии 10
length_in_bits(MODE_8BIT_BYTE, 20) # вернёт длину в битах для режима MODE_8BIT_BYTE и версии 20
length_in_bits(MODE_KANJI, 30)   # вернёт длину в битах для режима MODE_KANJI и версии 30

try:
    length_in_bits(1, 5)  # выбросит TypeError: Invalid mode (was 1)
except TypeError as e:
    print(e)
```

**Смотрите также:**

- `check_version`
- `mode_sizes_for_version`

### `def optimal_data_chunks(data, minimum = 4)`

Возвращает итератор, который разделяет данные на QRData части, оптимизированные в соответствии с их содержимым.

**Параметры:**

- `data` (`any`) — входные данные для разделения.
- `minimum` (`int`) — минимальное количество байтов в строке, которое должно быть разделено как отдельная часть; по умолчанию 4.

**Примеры:**

```python
import util

# Пример использования функции optimal_data_chunks
data = "abc123def"
for chunk in util.optimal_data_chunks(data, minimum=4):
    print(chunk)
```

**Смотрите также:**

- `_optimal_split`
- `to_bytestring`

### `def create_data(version, error_correction, data_list)`

Создает данные для QR-кода на основе заданной версии, режима исправления ошибок и списка данных.

**Параметры:**

- `version` (`int`) — версия QR-кода
- `error_correction` (`int`) — уровень исправления ошибок (например, `qrcode.constants.ERROR_CORRECT_L`)
- `data_list` (`list`) — список объектов с данными для записи в QR-код

**Возвращаемое значение:**

- `bytes` — данные QR-кода в виде байтового массива

**Исключения:**

- `exceptions.DataOverflowError` — если размер данных превышает доступное пространство

**Примеры:**

```python
# Пример вызова функции create_data
data_list = [QRData(10, MODE_NUMBER), QRData(256, MODE_8BIT_BYTE)]
qr_code_data = create_data(5, qrcode.constants.ERROR_CORRECT_L, data_list)
print(qr_code_data)  # Выведет данные QR-кода в виде байтового массива
```


---

[← Индекс](README.md)
