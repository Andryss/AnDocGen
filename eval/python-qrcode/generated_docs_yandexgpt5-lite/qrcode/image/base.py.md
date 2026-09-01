# Модуль `qrcode/image/base.py`


Модуль содержит базовые классы для работы с изображениями QR-кодов: BaseImage и BaseImageWithDrawer.

**Содержание:**

- [Классы](#классы)

## Классы

### `class BaseImage(abc.ABC)`

Базовый класс для вывода изображений QR-кодов.

**Назначение:**

Класс BaseImage представляет собой базовый класс для вывода изображений QR-кодов. Он инициализирует и обрабатывает параметры для создания и отображения QR-кодов.

**Использование:**

Создайте экземпляр класса BaseImage с заданными параметрами границы, ширины, размера блока и дополнительными аргументами. Используйте методы для рисования прямоугольников, обработки QR-кода и сохранения изображений.

**Поля:**

- `kind` (`str | None`) — —
- `allowed_kinds` (`tuple[str, ...] | None`) — —

**Наследование:**

- `abc.ABC`

#### Методы

##### `check_kind(kind, transform = None)`

Проверяет тип изображения.

**Параметры:**

- `transform` (`Any`) — Преобразование типа изображения
- `kind` (`Any`) — Проверяемый тип изображения

**Возвращаемое значение:**

- `Any` — Возвращает проверенный тип изображения

**Исключения:**

ValueError

**Примеры:**

Проверка типа изображения

```python
BaseImage.check_kind(kind, transform = None)
```

##### `drawrect(row, col)`

Рисует отдельный прямоугольник QR-кода.

**Параметры:**

- `row` (`int`) — Координаты начала прямоугольника
- `col` (`int`) — Координаты начала прямоугольника

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызвать метод для рисования прямоугольника

```python
BaseImage.drawrect(row, col)
```

##### `get_image(**kwargs)`

Возвращает класс изображения для дальнейшей обработки.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `object` — Класс изображения для дальнейшей обработки

**Примеры:**

Возвращает класс изображения для дальнейшей обработки

```python
return self._img
```

##### `drawrect_context(row: int, col: int, qr: QRCode)`

Рисует отдельный прямоугольник QR-кода в заданном контексте

**Параметры:**

- `row` (`int`) — координата строки
- `col` (`int`) — координата столбца
- `qr` (`QRCode`) — экземпляр QRCode

**Исключения:**

NotImplementedError

**Примеры:**

Вызов метода drawrect_context

```python
raise NotImplementedError("BaseImage.drawrect_context")
```

##### `init_new_image()`

Инициализирует новое изображение без выполнения каких-либо действий.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Инициализация нового изображения.

```python
pass
```

##### `is_eye(row: int, col: int)`

Определяет, находится ли модуль в зоне глаза по переданным координатам строки и столбца

**Параметры:**

- `row` (`int`) — Проверяет, находится ли модуль в зоне глаза по переданным координатам строки и столбца
- `col` (`int`) — Проверяет, находится ли модуль в зоне глаза по переданным координатам строки и столбца

**Возвращаемое значение:**

- `bool` — Возвращает True, если модуль находится в зоне глаза, иначе False

**Примеры:**

Проверить, находится ли модуль в зоне глаза, передав координаты строки и столбца

```python
BaseImage.is_eye(row, col)
```

##### `new_image(**kwargs) -> Any`

Создаёт класс изображения

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `Any` — Созданный класс изображения

**Примеры:**

Создание QR-кода с заданными параметрами и генерация изображения

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

Генерация QR-кода с помощью функции make и сохранение изображения

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

##### `pixel_box(row, col)`

Метод для генераторов изображений на основе пикселей, задающий четыре координаты пикселей для одиночного прямоугольника.

**Параметры:**

- `row` (`int`) — Задаёт строку для определения координат верхнего левого угла прямоугольника
- `col` (`int`) — Задаёт столбец для определения координат верхнего левого угла прямоугольника

**Возвращаемое значение:**

- `tuple` — Возвращает кортеж с координатами верхнего левого и нижнего правого угла прямоугольника

**Примеры:**

Получить координаты верхнего левого угла прямоугольника

```python
pixel_box(0, 0)
```

##### `process()`

Обрабатывает QR-код после завершения

**Исключения:**

NotImplementedError

**Примеры:**

Пример вызова метода process

```python
raise NotImplementedError("BaseImage.drawimage") # pragma: no cover
```

##### `save(stream, kind = None)`

Сохраняет файл изображения.

**Параметры:**

- `kind` (`N/A`) — Тип файла для сохранения изображения
- `stream` (`N/A`) — Поток для сохранения изображения

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример использования метода save() для сохранения изображения QR-кода

```python
import qrcode
qr = qrcode.QRCode()
qr.add_data('Some data')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("some_file.png")
```

Пример вызова метода save() для сохранения изображения

```python
img.save("some_file.png")
```

##### `__init__(border, width, box_size, *args, **kwargs)`

Инициализирует экземпляр класса BaseImage с заданными параметрами границы, ширины, размера блока и дополнительными аргументами.

**Параметры:**

- `border` (`N/A`) — Инициализирует экземпляр класса с параметрами границы, ширины, размера блока и дополнительными аргументами
- `width` (`N/A`) — Ширина изображения
- `box_size` (`N/A`) — Размер блока
- `*args` (`N/A`) — Дополнительные аргументы
- `**kwargs` (`N/A`) — Дополнительные аргументы в виде ключевых слов

**Возвращаемое значение:**

- `N/A` — N/A

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

Инициализация метода __init__

```python
self.border = border
self.width = width
self.box_size = box_size
self.pixel_size = (self.width + self.border * 2) * self.box_size
self.modules = kwargs.pop("qrcode_modules")
self._img = self.new_image(**kwargs)
self.init_new_image()
```

**Смотрите также:**

def init_new_image(), def new_image(**kwargs) -> Any

### `class BaseImageWithDrawer(BaseImage)`

Класс BaseImageWithDrawer предназначен для работы с модулями отрисовки QR-кодов.

**Использование:**

Инициализируйте объект BaseImageWithDrawer и используйте методы для управления модулями отрисовки и отрисовки элементов QR-кода.

**Поля:**

- `default_drawer_class` (`type[QRModuleDrawer]`) — —
- `drawer_aliases` (`DrawerAliases`) — —
- `module_drawer` (`QRModuleDrawer`) — —
- `eye_drawer` (`QRModuleDrawer`) — —

**Наследование:**

- `BaseImage`

#### Методы

##### `drawrect_context(row: int, col: int, qr: QRCode)`

Отрисовывает прямоугольник в контексте QR-кода

**Параметры:**

- `row` (`int`) — строка, с которой начинается отрисовка прямоугольника
- `col` (`int`) — столбец, с которого начинается отрисовка прямоугольника
- `qr` (`QRCode`) — экземпляр QR-кода

**Примеры:**

Создание QR-кода и его визуализация

```python
import qrcode
qr = qrcode.QRCode()
qr.add_data('Some data')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
```

Вызов метода drawrect_context

```python
def drawrect_context(row: int, col: int, qr: QRCode)
```

##### `get_default_module_drawer() -> QRModuleDrawer`

Возвращает экземпляр класса модуля отрисовки по умолчанию.

**Возвращаемое значение:**

- `QRModuleDrawer` — Экземпляр класса QRModuleDrawer

**Примеры:**

Получить экземпляр класса модуля отрисовки по умолчанию.

```python
return self.default_drawer_class()
```

##### `get_default_eye_drawer() -> QRModuleDrawer`

Возвращает экземпляр класса по умолчанию для отрисовки глазка QR-кода

**Возвращаемое значение:**

- `QRModuleDrawer` — Экземпляр класса QRModuleDrawer

**Примеры:**

Получить экземпляр класса по умолчанию для отрисовки глазка QR-кода

```python
return self.default_drawer_class()
```

##### `get_drawer(drawer: QRModuleDrawer | str | None) -> QRModuleDrawer | None`

Возвращает экземпляр QRModuleDrawer на основе переданного параметра drawer

**Параметры:**

- `drawer` (`QRModuleDrawer | str | None`) — Параметр drawer может быть экземпляром QRModuleDrawer, строкой или None

**Возвращаемое значение:**

- `QRModuleDrawer | None` — Возвращает экземпляр QRModuleDrawer или None

**Примеры:**

Пример вызова метода get_drawer

```python
if not isinstance(drawer, str):
 return drawer
drawer_cls, kwargs = self.drawer_aliases[drawer]
return drawer_cls(**kwargs)
```

##### `init_new_image()`

Инициализирует новое изображение, вызывая методы initialize для модуля drawer и eye drawer, а затем возвращает результат вызова метода init_new_image родительского класса.

**Возвращаемое значение:**

- `null` — Возвращает результат вызова метода init_new_image родительского класса

**Примеры:**

Инициализация нового изображения с использованием методов initialize для модуля drawer и eye drawer

```python
self.module_drawer.initialize(img=self)
self.eye_drawer.initialize(img=self)
return super().init_new_image()
```

##### `__init__(*args, **kwargs)`

Инициализирует объект BaseImageWithDrawer, устанавливая модули отрисовки для QR-кода

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация модуля отрисовки

```python
self.module_drawer = (self.get_drawer(module_drawer) or self.get_default_module_drawer())
```

Инициализация модуля отрисовки глазка

```python
self.eye_drawer = self.get_drawer(eye_drawer) or self.get_default_eye_drawer()
```

**Смотрите также:**

def get_default_eye_drawer() -> QRModuleDrawer, def get_default_module_drawer() -> QRModuleDrawer, def get_drawer(drawer: QRModuleDrawer | str | None) -> QRModuleDrawer | None


---

[← qrcode](README.md) | [← К проекту](../README.md)
