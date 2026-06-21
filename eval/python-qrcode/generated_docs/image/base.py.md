# Модуль `image/base.py`


Модуль с базовыми классами для работы с изображениями.

**Содержание:**

- [Классы](#классы)

## Классы

### `class BaseImage(abc.ABC)`

Базовый класс для создания изображений кодов QR.

**Поля:**

- `kind` (`str | None`) — —
- `allowed_kinds` (`tuple[str, ...] | None`) — —

#### Методы

##### `__init__(border, width, box_size, *args, **kwargs)`

Инициализирует объект `BaseImage` с параметрами границы, ширины и размера ячеек. Создает изображение с учетом переданных аргументов.

**Параметры:**

- `border` (`int`) — толщина границы вокруг QR-кода
- `width` (`int`) — ширина QR-кода без учета границы
- `box_size` (`int`) — размер одной ячейки в пикселях
- `*args` — дополнительные позиционные аргументы, не используемые
- `**kwargs` — дополнительные именованные аргументы, передаваемые в метод `new_image`

**Примеры:**

```python
base_image = BaseImage(border=4, width=10, box_size=5)
```

##### `check_kind(kind, transform = None)`

Проверяет и возвращает тип изображения.

**Параметры:**

- `kind` (`Any`) — тип изображения для проверки
- `transform` (`Callable[[Any], Any], optional`) — функция преобразования типа изображения

**Возвращаемое значение:**

- `Any` — проверенный тип изображения

**Исключения:**

- `ValueError` — если заданный тип изображения не допустим

**Примеры:**

```python
image.check_kind('PNG')
image.check_kind('GIF', transform=lambda k: k.upper())
```

##### `drawrect(row, col)`

Рисует отдельный прямоугольник для кода QR.

**Параметры:**

- `row` — —
- `col` — —

##### `drawrect_context(row: int, col: int, qr: QRCode)`

Рисует отдельный прямоугольник для квадратного кода, основываясь на окружающем контексте.

**Параметры:**

- `row` (`int`) — номер строки, где будет рисоваться прямоугольник
- `col` (`int`) — номер столбца, где будет рисоваться прямоугольник
- `qr` (`QRCode`) — объект квадратного кода

##### `get_image(**kwargs)`

Возвращает класс изображения для дальнейшей обработки.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `Any` — класс изображения

**Примеры:**

```python
result = BaseImage.get_image()
```

##### `init_new_image()`

Инициализирует новый изображение.

##### `new_image(**kwargs) -> Any`

Создает новый класс изображения. Подклассы должны возвращать созданный класс.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `Any` — созданный класс изображения

##### `is_eye(row: int, col: int)`

Определяет, находится ли модуль в области глаза.

**Параметры:**

- `row` (`int`) — строка
- `col` (`int`) — столбец

**Возвращаемое значение:**

- `bool` — True, если модуль находится в области глаза, иначе False

**Примеры:**

```python
from image.base import BaseImage

image = BaseImage(width=10)
print(image.is_eye(row=3, col=3))  # True
print(image.is_eye(row=8, col=2))  # False
```

##### `pixel_box(row, col)`

Helper method for pixel-based image generators that specifies the four pixel coordinates for a single rect.

**Параметры:**

- `row` (`int`) — row index
- `col` (`int`) — column index

**Возвращаемое значение:**

- `tuple[tuple[int, int], tuple[int, int]]` — четыре координаты пикселей для одного прямоугольника

**Примеры:**

```python
image_drawer = BaseImage(pixel_box)
pixel_coordinates = image_drawer.pixel_box(row=1, col=2)
```

##### `process()`

Обрабатывает QR-код после завершения обработки.

**Исключения:**

- `NotImplementedError` — метод не реализован

**Примеры:**

```python
# N/A
```

##### `save(stream, kind = None)`

Сохраняет изображение в файл.

**Параметры:**

- `stream` (`Any`) — поток для записи изображения
- `kind` (`Any, optional`) — тип изображения (по умолчанию None)

**Примеры:**

```python
# Пример использования
with open('output.png', 'wb') as f:
    BaseImage.save(f)
```

### `class BaseImageWithDrawer(BaseImage)`

Класс для работы с изображениями с использованием модулей и рисовальщиков.

**Поля:**

- `default_drawer_class` (`type[QRModuleDrawer]`) — —
- `drawer_aliases` (`DrawerAliases`) — —
- `module_drawer` (`QRModuleDrawer`) — —
- `eye_drawer` (`QRModuleDrawer`) — —

**Наследование:**

- `BaseImage` (`image/base.py`) — базовый класс для изображений

#### Методы

##### `__init__(*args, **kwargs)`

Инициализирует экземпляр класса `BaseImageWithDrawer`, устанавливая атрибуты `module_drawer` и `eye_drawer`.

**Параметры:**

- `*args` — переменное количество позиционных аргументов, передаваемых родительскому классу.
- `**kwargs` — переменное количество именованных аргументов, передаваемых родительскому классу.

**Примеры:**

```python
drawer = BaseImageWithDrawer(module_drawer=my_module_drawer, eye_drawer=my_eye_drawer)
```

##### `drawrect_context(row: int, col: int, qr: QRCode)`

Отрисовывает прямоугольник на изображении с использованием контекста.

**Параметры:**

- `row` (`int`) — строка начала прямоугольника
- `col` (`int`) — столбец начала прямоугольника
- `qr` (`QRCode`) — объект QRCode для которого отрисовывается прямоугольник

**Побочные эффекты:**

Изменяет изображение в соответствии с параметрами.

**Примеры:**

```python
image = BaseImageWithDrawer()
qr_code = QRCode(...)
image.drawrect_context(row=5, col=10, qr=qr_code)
```

##### `get_default_eye_drawer() -> QRModuleDrawer`

Возвращает экземпляр класса по умолчанию для рисования глаз.

**Возвращаемое значение:**

- `QRModuleDrawer` — экземпляр класса по умолчанию для рисования глаз

**Примеры:**

```python
drawer = BaseImageWithDrawer.get_default_eye_drawer()
```

##### `get_default_module_drawer() -> QRModuleDrawer`

Возвращает экземпляр класса `QRModuleDrawer` по умолчанию.

**Возвращаемое значение:**

- `QRModuleDrawer` — экземпляр класса `QRModuleDrawer`

**Примеры:**

```python
drawer = BaseImageWithDrawer.get_default_module_drawer()
```

##### `get_drawer(drawer: QRModuleDrawer | str | None) -> QRModuleDrawer | None`

Возвращает объект рисовальщика для отрисовки элементов QR-кода.

**Параметры:**

- `drawer` (`QRModuleDrawer | str | None`) — объект рисовальщика или его строковое имя, либо значение `None`

**Возвращаемое значение:**

- `QRModuleDrawer | None` — объект рисовальщика или `None`, если задано значение `None`

**Примеры:**

```python
drawer = my_image.get_drawer("default")
```

##### `init_new_image()`

Инициализирует новый изображение и настраивает объекты для рисования.

**Возвращаемое значение:**

- `Any` — результат вызова родительского метода `init_new_image`

**Побочные эффекты:**

Инициализирует объекты `module_drawer` и `eye_drawer`.

**Примеры:**

```python
new_img = BaseImageWithDrawer()
new_img.init_new_image()
```


---

[← image](README.md) | [← К проекту](../README.md)
