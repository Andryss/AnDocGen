# Модуль `qrcode/image/styles/moduledrawers/pil.py`


Модуль qrcode/image/styles/moduledrawers/pil.py содержит классы для рисования различных модулей в формате QR-кода.

**Содержание:**

- [Классы](#классы)

## Классы

### `class CircleModuleDrawer(StyledPilQRModuleDrawer)`

Класс CircleModuleDrawer предназначен для отрисовки модулей в виде кругов в QR-коде

**Назначение:**

Рисует модули в виде кругов для QR-кода с использованием PIL

**Использование:**

Инициализируйте модуль отрисовки круга для QR-кода с использованием PIL и вызывайте метод drawrect для отрисовки прямоугольника с использованием круга в указанной коробке, если модуль активен

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник с использованием круга в указанной коробке, если модуль активен.

**Параметры:**

- `box` (`N/A`) — Коробка для размещения круга
- `is_active` (`bool`) — Указывает, активен ли модуль

**Примеры:**

Вызвать метод drawrect с активным состоянием

```python
CircleModuleDrawer.drawrect(box, True)
```

##### `initialize(*args, **kwargs)`

Инициализация модуля отрисовки круга для QR-кода с использованием PIL.

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Вызов метода initialize с переменным числом аргументов

```python
super().initialize(*args, **kwargs)
```

### `class GappedCircleModuleDrawer(StyledPilQRModuleDrawer)`

Класс GappedCircleModuleDrawer предназначен для рисования модулей в виде кругов, которые не являются смежными. Параметр size_ratio определяет ширину кругов относительно ширины пространства, в котором они печатаются.

**Назначение:**

Рисует модули в виде не смежных кругов.

**Использование:**

Создайте экземпляр класса GappedCircleModuleDrawer и используйте методы для рисования модулей.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `__init__(size_ratio = 0.9)`

Инициализация объекта GappedCircleModuleDrawer с параметром размера соотношения.

**Параметры:**

- `size_ratio` (`float`) — Параметр, определяющий соотношение размера

**Примеры:**

Инициализация размера соотношения

```python
self.size_ratio = size_ratio
```

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник с использованием заданного модуля.

**Параметры:**

- `box` (`N/A`) — N/A
- `is_active` (`bool`) — Указывает, активен ли модуль

**Примеры:**

Вызвать метод drawrect с параметром is_active=True

```python
drawrect(box, True)
```

##### `initialize(*args, **kwargs)`

Инициализация метода с использованием аргументов *args и **kwargs

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация метода с использованием аргументов *args и **kwargs

```python
super().initialize(*args, **kwargs)
```

### `class GappedSquareModuleDrawer(StyledPilQRModuleDrawer)`

Класс GappedSquareModuleDrawer предназначен для рисования модулей в виде квадратов с заданным коэффициентом размера.

**Назначение:**

Рисует модули в виде простых квадратов, которые не являются смежными.

**Использование:**

Инициализируйте экземпляр класса с заданным коэффициентом размера и вызывайте методы для выполнения рисования.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `__init__(size_ratio = 0.8)`

Инициализирует экземпляр класса с заданным коэффициентом размера.

**Параметры:**

- `size_ratio` (`float`) — Коэффициент размера

**Примеры:**

Инициализация параметра size_ratio

```python
self.size_ratio = size_ratio
```

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник с учётом координат и состояния активности.

**Параметры:**

- `is_active` (`bool`) — Указывает, является ли прямоугольник активным
- `box` (`tuple`) — Координаты прямоугольника

**Примеры:**

Вызвать метод drawrect с активным состоянием

```python
from PIL import Image, ImageDraw
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer

drawer = GappedSquareModuleDrawer()
box = (10, 10, 20, 20)
drawer.drawrect(box, True)
```

##### `initialize(*args, **kwargs)`

Инициализация метода в классе GappedSquareModuleDrawer

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация метода в классе GappedSquareModuleDrawer

```python
super().initialize(*args, **kwargs)
self.imgDraw = ImageDraw.Draw(self.img._img)
self.delta = (1 - self.size_ratio) * self.img.box_size / 2
```

### `class HorizontalBarsDrawer(StyledPilQRModuleDrawer)`

Класс HorizontalBarsDrawer предназначен для отрисовки горизонтально расположенных групп модулей в формате длинных округлых прямоугольников с промежутками между ними.

**Назначение:**

Рисует горизонтально непрерывные группы модулей в виде длинных округлых прямоугольников с промежутками между соседними полосами (размер промежутков обратно пропорционален vertical_shrink).

**Использование:**

Инициализируйте объект HorizontalBarsDrawer с заданным коэффициентом вертикального сжатия и используйте методы для выполнения отрисовки.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `__init__(vertical_shrink = 0.8)`

Инициализирует объект HorizontalBarsDrawer с заданным коэффициентом вертикального сжатия.

**Параметры:**

- `vertical_shrink` (`float`) — коэффициент вертикального сжатия

**Примеры:**

Инициализация HorizontalBarsDrawer с параметром vertical_shrink

```python
HorizontalBarsDrawer.__init__(vertical_shrink = 0.8)
```

##### `setup_edges()`

Метод setup_edges выполняет внутренние настройки для работы с краями в модуле отрисовки горизонтальных полос.

**Примеры:**

Вызов метода setup_edges

```python
HorizontalBarsDrawer.setup_edges()
```

##### `drawrect(box, is_active: 'ActiveWithNeighbors')`

Метод drawrect выполняет отрисовку прямоугольника в зависимости от флага активности is_active

**Параметры:**

- `box` (`N/A`) — Объект box, передаваемый в метод
- `is_active` (`ActiveWithNeighbors`) — Флаг активности с соседями

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызвать метод drawrect с передачей box и is_active

```python
HorizontalBarsDrawer.drawrect(box, is_active)
```

##### `initialize(*args, **kwargs)`

Инициализация объекта HorizontalBarsDrawer

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация метода HorizontalBarsDrawer

```python
super().initialize(*args, **kwargs)
self.half_width = int(self.img.box_size / 2)
self.delta = int((1 - self.vertical_shrink) * self.half_width)
self.setup_edges()
```

**Смотрите также:**

setup_edges()

### `class RoundedModuleDrawer(StyledPilQRModuleDrawer)`

Класс RoundedModuleDrawer предназначен для рисования модулей с закруглёнными углами.

**Назначение:**

Рисует модули с заменой всех углов в 90 градусов на закруглённые края.

**Использование:**

Инициализируйте объект RoundedModuleDrawer с заданным коэффициентом радиуса и используйте методы для рисования модулей.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `__init__(radius_ratio = 1)`

Инициализирует объект RoundedModuleDrawer с заданным коэффициентом радиуса.

**Параметры:**

- `radius_ratio` (`float`) — Коэффициент радиуса

**Примеры:**

Инициализация объекта с параметром radius_ratio

```python
RoundedModuleDrawer.__init__(radius_ratio = 1)
```

##### `setup_corners()`

Настройка углов в модуле рисования QR-кодов с использованием библиотеки PIL.

**Примеры:**

Вызов метода setup_corners

```python
setup_corners()
```

##### `drawrect(box: list[list[int]], is_active: 'ActiveWithNeighbors')`

Рисует прямоугольник с закругленными углами, если флаг активности установлен.

**Параметры:**

- `box` (`list[list[int]]`) — Список списков координат углов прямоугольника
- `is_active` (`ActiveWithNeighbors`) — Флаг активности с учётом соседей

**Примеры:**

Вызвать метод drawrect с прямоугольником и флагом активности

```python
drawrect([[0, 0], [0, 1]], ActiveWithNeighbors())
```

##### `initialize(*args, **kwargs)`

Инициализация модуля рисования QR-кодов с использованием библиотеки PIL

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация модуля рисования QR-кодов с использованием библиотеки PIL

```python
super().initialize(*args, **kwargs)
self.corner_width = int(self.img.box_size / 2)
self.setup_corners()
```

**Смотрите также:**

def setup_corners() — Настройка углов в модуле рисования QR-кодов с использованием библиотеки PIL

### `class SquareModuleDrawer(StyledPilQRModuleDrawer)`

Класс SquareModuleDrawer предназначен для рисования модулей в виде квадратов.

**Назначение:**

Рисует модули в виде простых квадратов

**Использование:**

Используйте метод initialize для инициализации объекта и метод drawrect для рисования прямоугольника при условии, что параметр is_active имеет значение True.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник, если параметр is_active имеет значение True

**Параметры:**

- `is_active` (`bool`) — Если параметр is_active имеет значение True, то метод рисует прямоугольник с помощью метода rectangle объекта self.imgDraw
- `box` (`N/A`) — Прямоугольник, который нужно нарисовать

**Примеры:**

Нарисовать прямоугольник, если параметр is_active имеет значение True

```python
self.imgDraw.rectangle(box, fill=self.img.paint_color)
```

##### `initialize(*args, **kwargs)`

Инициализация объекта методом initialize с передачей переменных через позиционные аргументы и ключевые слова

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация метода в классе StyledPilQRModuleDrawer

```python
super().initialize(*args, **kwargs)
self.imgDraw = ImageDraw.Draw(self.img._img)
```

**Смотрите также:**

from PIL import Image, ImageDraw
from qrcode.image.styles.moduledrawers.base import QRModuleDrawer

### `class StyledPilQRModuleDrawer(QRModuleDrawer)`

Класс StyledPilQRModuleDrawer предназначен для работы с модулями drawer в стиле StyledPilImage.

**Назначение:**

Базовый класс для StyledPilImage модуля drawer.

**Поля:**

- `img` (`'StyledPilImage'`) — —

**Наследование:**

- `QRModuleDrawer`

### `class VerticalBarsDrawer(StyledPilQRModuleDrawer)`

Класс VerticalBarsDrawer предназначен для рисования вертикально смежных групп модулей в формате QR-кода.

**Назначение:**

Рисует вертикально смежные группы модулей в виде длинных закруглённых прямоугольников с промежутками между соседними полосами (размер промежутков обратно пропорционален параметру horizontal_shrink).

**Использование:**

Инициализируйте объект VerticalBarsDrawer с параметром horizontal_shrink и используйте методы для выполнения рисования.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `__init__(horizontal_shrink = 0.8)`

Инициализация объекта VerticalBarsDrawer с параметром horizontal_shrink.

**Параметры:**

- `horizontal_shrink` (`float`) — коэффициент сжатия по горизонтали

**Примеры:**

Инициализация объекта с параметром horizontal_shrink

```python
VerticalBarsDrawer.__init__(horizontal_shrink = 0.8)
```

##### `drawrect(box, is_active: 'ActiveWithNeighbors')`

Метод drawrect рисует прямоугольник в зависимости от параметра is_active

**Параметры:**

- `is_active` (`ActiveWithNeighbors`) — Параметр is_active определяет, нужно ли искать закруглённые края
- `box` (`N/A`) — Прямоугольник для отрисовки

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызвать метод drawrect с параметрами box и is_active

```python
VerticalBarsDrawer.drawrect(box, is_active)
```

##### `setup_edges()`

Настройка границ в методе setup_edges

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызов метода setup_edges

```python
VerticalBarsDrawer.setup_edges()
```

##### `initialize(*args, **kwargs)`

Инициализация метода с передачей аргументов через *args и **kwargs

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Инициализация метода

```python
super().initialize(*args, **kwargs)
self.half_height = int(self.img.box_size / 2)
self.delta = int((1 - self.horizontal_shrink) * self.half_height)
self.setup_edges()
```

Пример использования метода initialize в классе StyledPilQRModuleDrawer

```python
from PIL import Image, ImageDraw
from qrcode.image.styles.moduledrawers.base import QRModuleDrawer
from typing import TYPE_CHECKING
class StyledPilQRModuleDrawer(QRModuleDrawer):
    def initialize(*args, **kwargs):
        super().initialize(*args, **kwargs)
        self.half_height = int(self.img.box_size / 2)
        self.delta = int((1 - self.horizontal_shrink) * self.half_height)
        self.setup_edges()
```

**Смотрите также:**

def setup_edges() — Настройка границ в методе setup_edges


---

[← qrcode](README.md) | [← К проекту](../README.md)
