# Модуль `qrcode/image/styles/moduledrawers/svg.py`


Модуль содержит классы для генерации SVG-представлений QR-кодов, включая отрисовку квадратов, кругов и путей.

**Содержание:**

- [Классы](#классы)

## Классы

### `class BaseSvgQRModuleDrawer(QRModuleDrawer)`

Класс BaseSvgQRModuleDrawer является базовым классом для отрисовки модулей QR-кодов в формате SVG.

**Назначение:**

Класс BaseSvgQRModuleDrawer предназначен для отрисовки QR-кодов в формате SVG.

**Использование:**

Для использования класса необходимо создать его экземпляр и вызвать методы initialize и coords. Метод initialize инициализирует модуль отрисовки SVG для QR-кода, а метод coords возвращает кортеж координат, рассчитанных на основе переданного в него box.

**Поля:**

- `img` (`'SvgFragmentImage'`) — —

**Наследование:**

- `QRModuleDrawer`

#### Методы

##### `__init__(**kwargs)`

Инициализация объекта BaseSvgQRModuleDrawer с использованием переданных аргументов.

**Параметры:**

- `**kwargs` — —

**Примеры:**

Инициализация объекта с использованием kwargs

```python
super().__init__(**kwargs)
```

##### `coords(box) -> Coords`

Метод coords возвращает кортеж координат, рассчитанных на основе переданного в него box

**Параметры:**

- `box` (`list`) — Координаты, рассчитанные на основе box

**Возвращаемое значение:**

- `Coords` — Кортеж координат

**Примеры:**

Пример вызова метода coords с передачей в него box

```python
row, col = box[0]
x = row + self.box_delta
y = col + self.box_delta
return Coords(
x,
y,
x + self.box_size,
y + self.box_size,
x + self.box_half,
y + self.box_half,
)
```

Вызов метода coords с передачей в него box

```python
BaseSvgQRModuleDrawer.coords(box)
```

##### `initialize(*args, **kwargs) -> None`

Инициализация модуля отрисовки SVG для QR-кода

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Инициализация модуля отрисовки SVG для QR-кода

```python
super().initialize(*args, **kwargs)
self.box_delta = (1 - self.size_ratio) * self.img.box_size / 2
self.box_size = Decimal(self.img.box_size) * self.size_ratio
self.box_half = self.box_size / 2
```

Импорт зависимостей для работы с QR-кодом

```python
from abc import ABC
from decimal import Decimal
from typing import TYPE_CHECKING, NamedTuple
from qrcode.compat.etree import ET
from qrcode.image.styles.moduledrawers.base import QRModuleDrawer
```

### `class Coords(NamedTuple)`

Класс Coords является наследником NamedTuple и предназначен для работы в контексте генерации QR-кодов.

**Поля:**

- `x0` (`Decimal`) — —
- `y0` (`Decimal`) — —
- `x1` (`Decimal`) — —
- `y1` (`Decimal`) — —
- `xh` (`Decimal`) — —
- `yh` (`Decimal`) — —

### `class SvgCircleDrawer(SvgQRModuleDrawer)`

Класс SvgCircleDrawer является наследником класса SvgQRModuleDrawer и используется для отрисовки кругов в SVG.

**Назначение:**

Класс SvgCircleDrawer предназначен для отрисовки кругов в формате SVG в рамках генерации QR-кодов.

**Использование:**

Метод initialize используется для инициализации объекта класса SvgCircleDrawer. Метод el(box) создаёт элемент SVG для отрисовки круга.

**Наследование:**

- `SvgQRModuleDrawer`

#### Методы

##### `el(box)`

Создаёт элемент SVG для отрисовки круга.

**Параметры:**

- `box` (`object`) — Объект, содержащий координаты для отрисовки круга

**Возвращаемое значение:**

- `ET.Element` — Элемент SVG для отрисовки круга

**Примеры:**

Вызов метода el с параметром box

```python
svg_circle_drawer.el(box)
```

##### `initialize(*args, **kwargs) -> None`

Инициализация метода initialize для класса SvgQRModuleDrawer

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Инициализация метода initialize

```python
super().initialize(*args, **kwargs)
self.radius = self.img.units(self.box_half)
```

### `class SvgPathCircleDrawer(SvgPathQRModuleDrawer)`

Класс SvgPathCircleDrawer является наследником класса SvgPathQRModuleDrawer и используется для отрисовки дуг в формате SVG.

**Назначение:**

Класс предназначен для отрисовки дуг в формате SVG при генерации QR-кодов.

**Использование:**

Метод initialize вызывается через инициализацию родительского класса. Метод subpath(box) возвращает строковое представление подпути для отрисовки дуги в SVG формате.

**Наследование:**

- `SvgPathQRModuleDrawer`

#### Методы

##### `initialize(*args, **kwargs) -> None`

Инициализация метода через вызов метода initialize родительского класса.

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Инициализация метода через вызов родительского класса

```python
super().initialize(*args, **kwargs)
```

**Смотрите также:**

abc, Decimal, TYPE_CHECKING, NamedTuple, ET, QRModuleDrawer

##### `subpath(box) -> str`

Возвращает строковое представление подпути для отрисовки дуги в SVG формате

**Параметры:**

- `box` (`N/A`) — Координатная область для отрисовки дуги

**Возвращаемое значение:**

- `str` — Строковое представление подпути для отрисовки дуги в SVG формате

**Примеры:**

Пример вызова метода subpath для отрисовки дуги в SVG формате

```python
f'M{x0},{yh}A{h},{h} 0 0 0 {x1},{yh}A{h},{h} 0 0 0 {x0},{yh}z'
```

Пример использования метода coords для получения координат прямоугольника

```python
self.coords(box)
```

### `class SvgPathQRModuleDrawer(BaseSvgQRModuleDrawer)`

Класс SvgPathQRModuleDrawer предназначен для рисования SVG-представления QR-кодов.

**Назначение:**

Рисует SVG-представление QR-кода с использованием прямоугольников и подпутей.

**Использование:**

Используйте метод drawrect для рисования прямоугольника в SVG, если модуль активен. Метод subpath возвращает строку, используя параметр box.

**Поля:**

- `img` (`'SvgPathImage'`) — —

**Наследование:**

- `BaseSvgQRModuleDrawer`

#### Методы

##### `subpath(box) -> str`

Возвращает строку, используя параметр box

**Параметры:**

- `box` (`N/A`) — N/A

**Возвращаемое значение:**

- `str` — строка

**Примеры:**

Вызов метода subpath с передачей параметра box

```python
def subpath(self, box) -> str: ...
```

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник в SVG, если модуль активен

**Параметры:**

- `is_active` (`bool`) — Указывает, активен ли модуль
- `box` (`N/A`) — Прямоугольник, который нужно нарисовать

**Примеры:**

Вызвать метод drawrect с активным состоянием

```python
SvgPathQRModuleDrawer.drawrect(box, True)
```

### `class SvgPathSquareDrawer(SvgPathQRModuleDrawer)`

Класс SvgPathSquareDrawer предназначен для отрисовки квадратов в формате SVG, соответствующих заданным блокам в модуле QR-кода.

**Назначение:**

Рисует квадраты в формате SVG для модуля QR-кода.

**Использование:**

Используйте метод subpath для создания SVG-кода квадрата, соответствующего заданному блоку.

**Наследование:**

- `SvgPathQRModuleDrawer`

#### Методы

##### `subpath(box) -> str`

Создаёт строку с SVG-кодом для отрисовки квадрата, соответствующего заданному блоку.

**Параметры:**

- `box` (`N/A`) — Координаты блока, для которого нужно создать SVG-код.

**Возвращаемое значение:**

- `str` — Строка с SVG-кодом для отрисовки квадрата.

**Примеры:**

Возвращает строку с SVG-кодом для отрисовки квадрата, соответствующего заданному блоку.

```python
return f"M{x0},{y0}H{x1}V{y1}H{x0}z"
```

### `class SvgQRModuleDrawer(BaseSvgQRModuleDrawer)`

Класс SvgQRModuleDrawer является наследником класса BaseSvgQRModuleDrawer и предназначен для рисования SVG-модулей QR-кодов.

**Назначение:**

Класс предназначен для рисования SVG-модулей QR-кодов.

**Использование:**

Для использования класса необходимо создать его экземпляр и вызвать методы initialize, drawrect и el.

**Наследование:**

- `BaseSvgQRModuleDrawer`

#### Методы

##### `el(box)`

N/A

**Параметры:**

- `box` (`N/A`) — параметр, передаваемый в метод

**Примеры:**

Вызов метода el с передачей параметра box

```python
def el(self, box): ...
```

##### `initialize(*args, **kwargs) -> None`

Инициализация метода с переменным числом аргументов и словарем

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Инициализация метода

```python
super().initialize(*args, **kwargs)
```

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник в SVG формате, если флаг is_active установлен в True

**Параметры:**

- `box` (`N/A`) — Объект box, передаваемый в метод
- `is_active` (`bool`) — Флаг активности

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызвать метод drawrect с активным состоянием

```python
SvgQRModuleDrawer.drawrect(box, True)
```

### `class SvgSquareDrawer(SvgQRModuleDrawer)`

Класс SvgSquareDrawer является наследником класса SvgQRModuleDrawer и используется для отрисовки квадратов в формате SVG.

**Назначение:**

Класс SvgSquareDrawer предназначен для отрисовки квадратов в формате SVG.

**Использование:**

Для использования класса SvgSquareDrawer необходимо создать его экземпляр и вызвать метод initialize для инициализации объекта. Затем можно использовать метод el для создания элемента SVG, отображающего квадрат.

**Наследование:**

- `SvgQRModuleDrawer`

#### Методы

##### `el(box)`

Создаёт элемент SVG для отрисовки квадрата.

**Параметры:**

- `box` (`object`) — Объект box для отрисовки квадрата

**Возвращаемое значение:**

- `ET.Element` — Элемент SVG для квадрата

**Примеры:**

Создание элемента SVG для квадрата

```python
SvgSquareDrawer.el(box)
```

##### `initialize(*args, **kwargs) -> None`

Инициализация объекта класса SvgQRModuleDrawer

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Инициализация метода в классе SvgQRModuleDrawer

```python
super().initialize(*args, **kwargs)
self.unit_size = self.img.units(self.box_size)
```


---

[← qrcode](README.md) | [← К проекту](../README.md)
