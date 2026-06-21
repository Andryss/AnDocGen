# Модуль `image/styles/moduledrawers/pil.py`


Модуль для настройки модулей рисования для кодов QR с использованием библиотеки Pillow (PIL).

**Содержание:**

- [Классы](#классы)

## Классы

### `class StyledPilQRModuleDrawer(QRModuleDrawer)`

Базовый класс для рисования модулей QR-кода с использованием стилизованных изображений.

**Поля:**

- `img` (`'StyledPilImage'`) — —

**Наследование:**

QRModuleDrawer

### `class SquareModuleDrawer(StyledPilQRModuleDrawer)`

Класс для рисования модулей в виде простых квадратов.

**Наследование:**

- `StyledPilQRModuleDrawer` — базовый класс, который наследует от `QRModuleDrawer`

#### Методы

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник на изображении.

**Параметры:**

- `box` (`tuple`) — кортеж координат (x1, y1, x2, y2) для прямоугольника
- `is_active` (`bool`) — флаг активности прямоугольника

**Побочные эффекты:**

Изменяет изображение в-place.

**Примеры:**

```python
drawer = SquareModuleDrawer()
drawer.drawrect((10, 10, 50, 50), is_active=True)
```

##### `initialize(*args, **kwargs)`

Инициализирует объект `SquareModuleDrawer` с помощью переданных аргументов и настраивает его для рисования модулей.

**Параметры:**

- `*args` — переменное количество позиционных аргументов, передаваемых родительскому классу
- `**kwargs` — переменное количество именованных аргументов, передаваемых родительскому классу

**Побочные эффекты:**

Инициализирует атрибут `imgDraw`, используя метод `ImageDraw.Draw` для рисования на изображении.

**Примеры:**

```python
drawer = SquareModuleDrawer()
drawer.initialize(img, size)
```

### `class GappedSquareModuleDrawer(StyledPilQRModuleDrawer)`

Класс для рисования модулей в виде простых квадратов, которые не соединены.

#### Методы

##### `__init__(size_ratio = 0.8)`

Инициализирует объект для рисования модулей квадратных qr-кодов с заданным соотношением размера.

**Параметры:**

- `size_ratio` (`float`) — коэффициент, определяющий пропорцию размера модуля к общему размеру qr-кода, по умолчанию 0.8

**Примеры:**

```python
drawer = GappedSquareModuleDrawer(size_ratio=0.9)
```

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник с учетом параметра активности.

**Параметры:**

- `box` (`tuple`) — кортеж из двух точек, задающих координаты противоположных углов прямоугольника
- `is_active` (`bool`) — флаг, указывающий на активность прямоугольника

**Побочные эффекты:**

Изменяет изображение, на котором рисуется прямоугольник.

**Примеры:**

```python
drawer = GappedSquareModuleDrawer()
drawer.drawrect(((0, 0), (100, 100)), True)
```

##### `initialize(*args, **kwargs)`

Инициализирует объект `GappedSquareModuleDrawer` с помощью переданных аргументов и ключевых слов.

**Параметры:**

- `*args` — переменное количество позиционных аргументов, передаваемых в родительский класс.
- `**kwargs` — переменное количество именованных аргументов, передаваемых в родительский класс.

**Побочные эффекты:**

Инициализирует объект для рисования на изображении и устанавливает значение `self.delta`.

**Примеры:**

```python
drawer = GappedSquareModuleDrawer(size_ratio=0.5, img=some_image)
drawer.initialize()
```

### `class CircleModuleDrawer(StyledPilQRModuleDrawer)`

Класс для рисования модулей в виде кругов.

**Наследование:**

- `StyledPilQRModuleDrawer` — базовый класс для рисования модулей с использованием PIL и стилизацией

#### Методы

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник на изображении.

**Параметры:**

- `box` (`list`) — список координат верхнего левого и правого нижнего углов прямоугольника, например, `[(x1, y1), (x2, y2)]`
- `is_active` (`bool`) — флаг, указывающий, нужно ли рисовать прямоугольник

**Побочные эффекты:**

Изменяет изображение, на котором вызывается метод.

**Примеры:**

```python
drawer = CircleModuleDrawer(image)
drawer.drawrect([(10, 20), (50, 60)], is_active=True)
```

##### `initialize(*args, **kwargs)`

Инициализирует объект CircleModuleDrawer.

**Параметры:**

- `*args` — переменное количество позиционных аргументов.
- `**kwargs` — переменное количество именованных аргументов.

**Побочные эффекты:**

Изменяет объект, вызывающий метод.

**Примеры:**

```python
drawer = CircleModuleDrawer()
drawer.initialize()
```

### `class GappedCircleModuleDrawer(StyledPilQRModuleDrawer)`

Класс для рисования модулей в виде непрерывных кругов.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `__init__(size_ratio = 0.9)`

Инициализирует объект GappedCircleModuleDrawer с заданным соотношением размеров.

**Параметры:**

- `size_ratio` (`float`) — коэффициент, определяющий отношение размеров модуля к общему размеру изображения. Значение по умолчанию — 0.9.

**Примеры:**

```python
drawer = GappedCircleModuleDrawer(size_ratio=0.8)
```

##### `drawrect(box, is_active: bool)`

Рисует прямоугольник на изображении в зависимости от состояния.

**Параметры:**

- `box` (`tuple`) — кортеж, содержащий координаты верхнего левого и нижнего правого углов прямоугольника.
- `is_active` (`bool`) — флаг активности.

**Побочные эффекты:**

Изменяет изображение, на котором рисуется прямоугольник.

**Примеры:**

```python
drawer = GappedCircleModuleDrawer(image)
drawer.drawrect(((10, 10), (50, 50)), is_active=True)
```

##### `initialize(*args, **kwargs)`

Инициализирует экземпляр класса GappedCircleModuleDrawer.

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Побочные эффекты:**

- Создает новый объект изображения с пустым эллипсом.
- Изменяет размер созданного изображения.

**Примеры:**

```python
drawer = GappedCircleModuleDrawer()
drawer.initialize()
```

### `class RoundedModuleDrawer(StyledPilQRModuleDrawer)`

Класс для рисования модулей с закругленными углами.

**Наследование:**

- `StyledPilQRModuleDrawer`

#### Методы

##### `__init__(radius_ratio = 1)`

Инициализирует объект RoundedModuleDrawer с заданным радиусом.

**Параметры:**

- `radius_ratio` (`float`) — коэффициент, определяющий отношение радиуса к половине размера модуля. По умолчанию равно 1.

**Примеры:**

```python
drawer = RoundedModuleDrawer(radius_ratio=0.5)
```

##### `drawrect(box: list[list[int]], is_active: 'ActiveWithNeighbors')`

Рисует прямоугольник с закругленными углами на изображении.

**Параметры:**

- `box` (`list[list[int]]`) — список координат верхнего левого и нижнего правого углов прямоугольника в формате `[[x1, y1], [x2, y2]]`
- `is_active` (`'ActiveWithNeighbors'`) — объект с информацией о состоянии модуля и его соседей

**Побочные эффекты:**

Изменяет изображение `_img` внутри объекта `self.img`, добавляя закругленные углы.

**Примеры:**

```python
drawer = RoundedModuleDrawer(image)
box = [[10, 10], [50, 50]]
active_state = ActiveWithNeighbors(W=False, N=True, E=True, S=False)
drawer.drawrect(box, active_state)
```

##### `initialize(*args, **kwargs)`

Инициализирует объект `RoundedModuleDrawer` и устанавливает ширину углов.

**Параметры:**

- `*args` — переменное количество позиционных аргументов
- `**kwargs` — переменное количество ключевых аргументов

**Побочные эффекты:**

Изменяет атрибуты объекта: `corner_width`.

**Примеры:**

```python
drawer = RoundedModuleDrawer()
drawer.initialize(img, box_size=10)
```

##### `setup_corners()`

Настройка углов для модуля отрисовки изображений с использованием библиотеки PIL.

**Побочные эффекты:**

Изменение атрибутов объекта, вызывающего метод.

**Примеры:**

```python
drawer = RoundedModuleDrawer(img)
drawer.setup_corners()
```

**Смотрите также:**

- `QRModuleDrawer`
- `PIL`

### `class VerticalBarsDrawer(StyledPilQRModuleDrawer)`

Класс для рисования вертикально соединенных групп модулей в виде длинных закругленных прямоугольников с интервалами между соседними группами (размеры этих интервалов обратно пропорциональны horizontal_shrink).

**Наследование:**

- `StyledPilQRModuleDrawer` (`QRModuleDrawer`)

#### Методы

##### `__init__(horizontal_shrink = 0.8)`

Инициализирует экземпляр класса VerticalBarsDrawer с параметром для горизонтального изменения размера.

**Параметры:**

- `horizontal_shrink` (`float`) — коэффициент, отвечающий за уменьшение горизонтальных модулей QR-кода по сравнению с исходным значением (по умолчанию 0.8)

**Примеры:**

```python
drawer = VerticalBarsDrawer(horizontal_shrink=0.5)
```

##### `drawrect(box, is_active: 'ActiveWithNeighbors')`

Отрисовывает прямоугольник с вертикальными бордюрами.

**Параметры:**

- `box` (`tuple`) — кортеж координат верхнего левого и нижнего правого углов прямоугольника
- `is_active` (`'ActiveWithNeighbors'`) — объект, содержащий информацию о состоянии модуля и его соседях

**Побочные эффекты:**

Изменяет изображение, на котором производится отрисовка.

**Примеры:**

```python
# Пример использования метода drawrect
drawer = VerticalBarsDrawer()
box = ((10, 20), (50, 60))
is_active = 'ActiveWithNeighbors'  # Пример значения is_active
drawer.drawrect(box, is_active)
```

##### `initialize(*args, **kwargs)`

Инициализирует объект для рисования вертикальных линий.

**Параметры:**

- `*args` — переменное количество позиционных аргументов, передаваемых родительскому классу.
- `**kwargs` — переменное количество именованных аргументов, передаваемых родительскому классу.

**Побочные эффекты:**

Изменяет атрибуты объекта:
- `self.half_height` — половина размера ячейки.
- `self.delta` — изменение, основанное на `horizontal_shrink`.

**Примеры:**

```python
drawer = VerticalBarsDrawer(img, horizontal_shrink=0.5)
drawer.initialize()
```

##### `setup_edges()`

Настройка краев изображения для рисования вертикальных полос.

**Побочные эффекты:**

Изменяет атрибуты объекта, такие как `SQUARE`, `ROUND_TOP` и `ROUND_BOTTOM`.

**Примеры:**

```python
drawer = VerticalBarsDrawer()
drawer.setup_edges()
```

### `class HorizontalBarsDrawer(StyledPilQRModuleDrawer)`

Класс для рисования горизонтальных групп модулей в виде длинных овальных прямоугольников с интервалами между соседними группами (размер этих интервалов обратно пропорционален vertical_shrink).

**Наследование:**

- `QRModuleDrawer` (`base`)

#### Методы

##### `__init__(vertical_shrink = 0.8)`

Инициализирует объект HorizontalBarsDrawer с параметром для изменения размера модулей.

**Параметры:**

- `vertical_shrink` (`float`) — коэффициент уменьшения вертикальных размеров модулей (по умолчанию 0.8)

**Примеры:**

```python
drawer = HorizontalBarsDrawer(vertical_shrink=0.7)
```

##### `drawrect(box, is_active: 'ActiveWithNeighbors')`

Отрисовывает прямоугольник с закругленными углами.

**Параметры:**

- `box` (`tuple`) — кортеж координат (верхний левый угол и правый нижний угол)
- `is_active` (`ActiveWithNeighbors`) — информация о состоянии модуля

**Побочные эффекты:**

Изменяет изображение, на котором отрисовывается прямоугольник.

**Примеры:**

```python
drawer = HorizontalBarsDrawer()
drawer.drawrect(((10, 20), (50, 60)), is_active)
```

##### `initialize(*args, **kwargs)`

Инициализирует объект HorizontalBarsDrawer.

**Параметры:**

- `*args` — переменное количество позиционных аргументов
- `**kwargs` — переменное количество именованных аргументов

**Побочные эффекты:**

Изменяет атрибуты объекта.

**Примеры:**

```python
drawer = HorizontalBarsDrawer()
drawer.initialize()
```

##### `setup_edges()`

Метод для настройки краев изображения.

**Примеры:**

```python
drawer = HorizontalBarsDrawer()
drawer.setup_edges()
```


---

[← image](README.md) | [← К проекту](../README.md)
