# Модуль `image/styles/moduledrawers/svg.py`


Модуль для рисования модулей в виде SVG.

**Содержание:**

- [Классы](#классы)

## Классы

### `class Coords(NamedTuple)`

Класс для представления координат в изображении.

**Поля:**

- `x0` (`Decimal`) — —
- `y0` (`Decimal`) — —
- `x1` (`Decimal`) — —
- `y1` (`Decimal`) — —
- `xh` (`Decimal`) — —
- `yh` (`Decimal`) — —

### `class BaseSvgQRModuleDrawer(QRModuleDrawer)`

Класс для рисования модулей QR-кода в формате SVG.

**Поля:**

- `img` (`'SvgFragmentImage'`) — —

**Наследование:**

- QRModuleDrawer

#### Методы

##### `__init__(**kwargs)`

Инициализирует экземпляр класса BaseSvgQRModuleDrawer с использованием именованных аргументов.

**Параметры:**

- `**kwargs` — —

##### `coords(box) -> Coords`

Вычисляет координаты для модуля QR-кода на основе заданного кортежа `box`.

**Параметры:**

- `box` (`tuple`) — кортеж, содержащий координаты верхнего левого угла ячейки в формате `(row, col)`

**Возвращаемое значение:**

- `Coords` — объект с координатами для модуля QR-кода

**Примеры:**

```python
drawer = BaseSvgQRModuleDrawer()
coords = drawer.coords((1, 2))
print(coords)  # Coords(x=3, y=4, x_end=7, y_end=8, x_mid=5, y_mid=6)
```

##### `initialize(*args, **kwargs) -> None`

Инициализирует объект `BaseSvgQRModuleDrawer`.

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

```python
drawer = BaseSvgQRModuleDrawer()
drawer.initialize()
```

### `class SvgQRModuleDrawer(BaseSvgQRModuleDrawer)`

Класс для рисования модулей QR-кода в формате SVG.

**Наследование:**

- `BaseSvgQRModuleDrawer`

#### Методы

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник на изображении.

**Параметры:**

- `box` (`NamedTuple`) — кортеж с координатами и размером прямоугольника (x, y, width, height)
- `is_active` (`bool`) — флаг активности прямоугольника

**Побочные эффекты:**

Изменяет внутреннее состояние объекта `img`, добавляя новый элемент.

**Примеры:**

```python
drawer = SvgQRModuleDrawer()
rect = NamedTuple('Box', [('x', int), ('y', int), ('width', int), ('height', int)])(0, 0, 10, 20)
drawer.drawrect(rect, True)
```

##### `el(box)`

N/A

**Параметры:**

- `box` (`object`) — N/A

##### `initialize(*args, **kwargs) -> None`

Инициализирует экземпляр класса SvgQRModuleDrawer.

**Параметры:**

- `*args` — переменное количество позиционных аргументов.
- `**kwargs` — переменное количество именованных аргументов.

**Примеры:**

```python
drawer = SvgQRModuleDrawer()
drawer.initialize()
```

### `class SvgSquareDrawer(SvgQRModuleDrawer)`

Класс для рисования квадратных модулей в изображении SVG.

**Наследование:**

- `QRModuleDrawer` (`base.QRModuleDrawer`) — базовый класс для модульных рисовальщиков QR-кодов

#### Методы

##### `el(box)`

Создает SVG-элемент для квадрата.

**Параметры:**

- `box` (`NamedTuple`) — кортеж с координатами и размерами квадрата

**Возвращаемое значение:**

- `ET.Element` — элемент SVG, представляющий квадрат

**Примеры:**

```python
drawer = SvgSquareDrawer()
square_element = drawer.el((0, 0, 10, 10))
```

##### `initialize(*args, **kwargs) -> None`

Инициализирует объект SvgSquareDrawer с параметрами.

**Параметры:**

- `*args` — позиционные аргументы
- `**kwargs` — именованные аргументы

**Побочные эффекты:**

Изменяет атрибут `unit_size` объекта SvgSquareDrawer.

**Примеры:**

```python
drawer = SvgSquareDrawer()
drawer.initialize(box_size=10)
```

### `class SvgCircleDrawer(SvgQRModuleDrawer)`

Класс для рисования кругов в SVG.

**Наследование:**

- `QRModuleDrawer` (`base.QRModuleDrawer`) — базовый класс для рисования модулей QR-кода

#### Методы

##### `el(box)`

Создает элемент SVG для круга на основе заданного бокса.

**Параметры:**

- `box` — —

**Возвращаемое значение:**

- `ET.Element` — элемент SVG с тегом `circle`

**Примеры:**

```python
# Пример использования
drawer = SvgCircleDrawer()
svg_element = drawer.el(box)
```

##### `initialize(*args, **kwargs) -> None`

Инициализирует объект для рисования кругов в SVG.

**Параметры:**

- `*args` — —
- `**kwargs` — —

### `class SvgPathQRModuleDrawer(BaseSvgQRModuleDrawer)`

Класс для отрисовки модулей QR-кода в формате SVG с использованием пути.

**Поля:**

- `img` (`'SvgPathImage'`) — —

**Наследование:**

- `BaseSvgQRModuleDrawer`

#### Методы

##### `drawrect(box, is_active: bool)`

Отрисовывает прямоугольник на SVG-путь в зависимости от активности.

**Параметры:**

- `box` (`NamedTuple`) — кортеж с параметрами прямоугольника
- `is_active` (`bool`) — флаг активности, если `False`, метод не выполняет ни каких действий

**Побочные эффекты:**

Изменяет внутреннее состояние объекта `self.img` путем добавления нового подпути.

**Примеры:**

```python
drawer = SvgPathQRModuleDrawer()
drawer.drawrect(box, is_active=True)
```

##### `subpath(box) -> str`

N/A

**Параметры:**

- `box` (`any`) — N/A

**Возвращаемое значение:**

- `str` — N/A

### `class SvgPathSquareDrawer(SvgPathQRModuleDrawer)`

Класс для рисования квадратных модулей в SVG формате.

**Наследование:**

- `QRModuleDrawer` — базовый класс для рисования модулей QR кода

#### Методы

##### `subpath(box) -> str`

Создает подпуть для квадрата на основе переданных координат и возвращает его в формате SVG.

**Параметры:**

- `box` (`NamedTuple`) — кортеж с координатами (x0, y0, x1, y1)

**Возвращаемое значение:**

- `str` — подпуть квадрата в формате SVG

**Примеры:**

```python
drawer = SvgPathSquareDrawer()
box = (0, 0, 10, 10)
path = drawer.subpath(box)
print(path)  # M0,0H10V10H0z
```

### `class SvgPathCircleDrawer(SvgPathQRModuleDrawer)`

Класс для рисования кругов в SVG путях.

**Наследование:**

- `QRModuleDrawer` (`base`) — базовый класс для модулей рисования QR-кодов

#### Методы

##### `initialize(*args, **kwargs) -> None`

Инициализирует объект класса SvgPathCircleDrawer.

**Параметры:**

- `*args` — —
- `**kwargs` — —

##### `subpath(box) -> str`

Формирует подпуть SVG для круга.

**Параметры:**

- `box` (`NamedTuple`) — кортеж с координатами границы, описывающий форму круга

**Возвращаемое значение:**

- `str` — строка, представляющая подпуть SVG для круга

**Примеры:**

```python
# Пример использования метода subpath
circle_path = SvgPathCircleDrawer.subpath(NamedTuple('Box', [('x0', 1), ('yh', 2), ('x1', 3)]))
print(circle_path)
```


---

[← image](README.md) | [← К проекту](../README.md)
