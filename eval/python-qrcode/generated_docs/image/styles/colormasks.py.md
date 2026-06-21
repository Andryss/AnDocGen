# Модуль `image/styles/colormasks.py`


Модуль для создания различных масок с цветовыми эффектами.

**Содержание:**

- [Классы](#классы)

## Классы

### `class QRColorMask`

QRColorMask используется для раскрашивания QR-кода.

#### Методы

##### `apply_mask(image, use_cache = False)`

Применяет маску к изображению, изменяя цвет пикселей в зависимости от заданных условий.

**Параметры:**

- `image` (`PIL.Image`) — исходное изображение
- `use_cache` (`bool, optional`) — использовать кэш для ускорения обработки (по умолчанию False)

**Побочные эффекты:**

Изменяет цвета пикселей в исходном изображении.

**Примеры:**

```python
from PIL import Image

image = Image.open('path_to_image.jpg')
mask = QRColorMask(back_color=(255, 0, 0), paint_color=(0, 255, 0))
mask.apply_mask(image)
```

##### `extrap_color(col1, col2, interped_color)`

Вычисляет дополненный цвет на основе двух исходных цветов и интерполированного цвета.

**Параметры:**

- `col1` (`tuple[int]`) — первый исходный цвет в формате RGB
- `col2` (`tuple[int]`) — второй исходный цвет в формате RGB
- `interped_color` (`tuple[float]`) — интерполированный цвет в формате RGB

**Возвращаемое значение:**

- `float` — дополненный цвет

**Примеры:**

```python
mask = QRColorMask()
result = mask.extrap_color((255, 0, 0), (0, 255, 0), (128, 128, 128))
print(result)
```

##### `extrap_num(n1, n2, interped_num)`

Вычисляет интерполированное число между двумя значениями.

**Параметры:**

- `n1` (`float`) — первое значение
- `n2` (`float`) — второе значение
- `interped_num` (`float`) — интерполированное значение

**Возвращаемое значение:**

- `float` — результат вычисления или None, если n1 равно n2

**Примеры:**

```python
result = QRColorMask.extrap_num(1.0, 5.0, 3.0)
print(result)  # Вывод: 0.4
```

##### `get_bg_pixel(image, x, y)`

Возвращает цвет фона изображения.

**Параметры:**

- `image` (`Image`) — изображение
- `x` (`int`) — координата x пикселя
- `y` (`int`) — координата y пикселя

**Примеры:**

```python
color_mask = QRColorMask()
bg_color = color_mask.get_bg_pixel(image, x, y)
```

##### `get_fg_pixel(image, x, y)`

N/A

**Параметры:**

- `image` (`Image.Image`) — изображение, в котором нужно получить пиксель
- `x` (`int`) — координата x пикселя
- `y` (`int`) — координата y пикселя

**Исключения:**

- `NotImplementedError`

**Примеры:**

```python
# Пример использования не применим, так как метод выбрасывает NotImplementedError
```

##### `initialize(styledPilImage, image)`

Инициализирует маску цвета с основным изображением.

**Параметры:**

- `styledPilImage` (`object`) — объект с рисованным цветом
- `image` (`object`) — основное изображение

**Примеры:**

```python
from image.styles.colormasks import QRColorMask
from PIL import Image

styledPilImage = StyledPilImage()
image = Image.open('path_to_image.jpg')
mask = QRColorMask.initialize(styledPilImage, image)
```

##### `interp_color(col1, col2, norm)`

Интерполяция двух цветов на основе нормализованного значения.

**Параметры:**

- `col1` (`tuple`) — первый цвет в формате (R, G, B)
- `col2` (`tuple`) — второй цвет в формате (R, G, B)
- `norm` (`float`) — нормализованное значение от 0 до 1, определяющее степень интерполяции

**Возвращаемое значение:**

- `tuple` — интерполированный цвет в формате (R, G, B)

**Примеры:**

```python
color1 = (255, 0, 0)  # Красный
color2 = (0, 0, 255)  # Синий
norm_value = 0.5     # Средняя интерполяция
interpolated_color = QRColorMask.interp_color(color1, color2, norm_value)
# Результат: (127, 0, 127) — серебристо-голубая комбинация
```

##### `interp_num(n1, n2, norm)`

Интерполирует два числа на основе нормализованного значения.

**Параметры:**

- `n1` (`float`) — первое число
- `n2` (`float`) — второе число
- `norm` (`float`) — нормализованное значение от 0 до 1

**Возвращаемое значение:**

- `int` — интерполированное значение

**Примеры:**

```python
result = QRColorMask.interp_num(5, 10, 0.5)  # Результат: 7
```

### `class SolidFillColorMask(QRColorMask)`

Класс для создания маски с однородным заполнением фона и переднего плана.

**Наследование:**

- `QRColorMask` — базовый класс

#### Методы

##### `__init__(back_color = (255, 255, 255), front_color = (0, 0, 0))`

Инициализирует объект `SolidFillColorMask` с заданными фоновым и передним цветами.

**Параметры:**

- `back_color` (`tuple`) — кортеж из трех целых чисел, представляющий RGB-цвет фона (по умолчанию `(255, 255, 255)`).
- `front_color` (`tuple`) — кортеж из трех целых чисел, представляющий RGB-цвет переднего плана (по умолчанию `(0, 0, 0)`).

**Примеры:**

```python
mask = SolidFillColorMask(back_color=(255, 0, 0), front_color=(0, 255, 0))
```

##### `apply_mask(image)`

Применяет маску к изображению, заменяя пиксели в зависимости от значения черного и белого цветов.

**Параметры:**

- `image` — —

**Побочные эффекты:**

Изменяет изображение, на которое применяется маска.

**Примеры:**

```python
mask = SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0))
image = Image.new("RGB", (100, 100), (127, 127, 127))
mask.apply_mask(image)
```

##### `get_fg_pixel(image, x, y)`

Возвращает цвет фонального пикселя.

**Параметры:**

- `image` (`Image`) — изображение, на котором находится пиксель.
- `x` (`int`) — координата x пикселя.
- `y` (`int`) — координата y пикселя.

**Примеры:**

```python
mask = SolidFillColorMask(front_color=(255, 0, 0))
image = Image.open('example.jpg')
fg_pixel = mask.get_fg_pixel(image, 10, 20)
```

### `class RadialGradiantColorMask(QRColorMask)`

Класс для создания радиального градиентного цветового маски.

#### Методы

##### `__init__(back_color = (255, 255, 255), center_color = (0, 0, 0), edge_color = (0, 0, 255))`

Инициализирует объект RadialGradiantColorMask с указанными цветами для фона, центра и края.

**Параметры:**

- `back_color` (`tuple`) — цвет фона в формате (R, G, B[, A])
- `center_color` (`tuple`) — цвет центра в формате (R, G, B[, A])
- `edge_color` (`tuple`) — цвет края в формате (R, G, B[, A])

**Примеры:**

```python
mask = RadialGradiantColorMask(back_color=(255, 0, 0), center_color=(0, 255, 0), edge_color=(0, 0, 255))
```

##### `get_fg_pixel(image, x, y)`

Возвращает пиксель переднего плана изображения в зависимости от расстояния до центра изображения.

**Параметры:**

- `image` (`Image`) — изображение, из которого нужно получить пиксель
- `x` (`int`) — координата x пикселя
- `y` (`int`) — координата y пикселя

**Возвращаемое значение:**

- `tuple` — RGB значение пикселя переднего плана

**Примеры:**

```python
from PIL import Image
from image.styles.colormasks import RadialGradiantColorMask

# Создаем изображение и маску
image = Image.new('RGB', (256, 256), color='white')
mask = RadialGradiantColorMask(center_color=(0, 0, 255), edge_color=(255, 0, 0))

# Получаем пиксель переднего плана
pixel = mask.get_fg_pixel(image, 128, 128)
print(pixel)  # Output: (0, 0, 255)
```

### `class SquareGradiantColorMask(QRColorMask)`

Класс для создания изображения с градиентом от центра до края.

#### Методы

##### `__init__(back_color = (255, 255, 255), center_color = (0, 0, 0), edge_color = (0, 0, 255))`

Инициализирует объект `SquareGradiantColorMask` с заданными цветами для фона, центра и края.

**Параметры:**

- `back_color` (`tuple`) — цвет фона в формате RGB или RGBA (по умолчанию `(255, 255, 255)`)
- `center_color` (`tuple`) — цвет центра в формате RGB (по умолчанию `(0, 0, 0)`)
- `edge_color` (`tuple`) — цвет края в формате RGB (по умолчанию `(0, 0, 255)`)

**Примеры:**

```python
mask = SquareGradiantColorMask(back_color=(255, 0, 0), center_color=(0, 255, 0), edge_color=(0, 0, 255))
```

##### `get_fg_pixel(image, x, y)`

Возвращает пиксель переднего плана изображения на основе расстояния до центра.

**Параметры:**

- `image` (`Image`) — изображение
- `x` (`int`) — координата x пикселя
- `y` (`int`) — координата y пикселя

**Возвращаемое значение:**

- `tuple` — RGB значение пикселя переднего плана

**Примеры:**

```python
from PIL import Image

# Создаем изображение и объект SquareGradiantColorMask
image = Image.new("RGB", (200, 200))
mask = SquareGradiantColorMask(center_color=(255, 0, 0), edge_color=(0, 0, 255))

# Получаем пиксель переднего плана на позиции (100, 100)
fg_pixel = mask.get_fg_pixel(image, 100, 100)
print(fg_pixel)  # Выводит RGB значение пикселя
```

### `class HorizontalGradiantColorMask(QRColorMask)`

Класс для создания горизонтального градиента на маске цвета фона.

**Наследование:**

QRColorMask

#### Методы

##### `__init__(back_color = (255, 255, 255), left_color = (0, 0, 0), right_color = (0, 0, 255))`

Инициализирует объект `HorizontalGradiantColorMask` с указанными цветами и определяет наличие прозрачности.

**Параметры:**

- `back_color` (`tuple`) — основной фоновый цвет в формате RGB или RGBA (по умолчанию (255, 255, 255))
- `left_color` (`tuple`) — левый цвет градиента в формате RGB (по умолчанию (0, 0, 0))
- `right_color` (`tuple`) — правый цвет градиента в формате RGB (по умолчанию (0, 0, 255))

**Примеры:**

```python
mask = HorizontalGradiantColorMask((255, 0, 0), (0, 255, 0))
```

##### `get_fg_pixel(image, x, y)`

Возвращает пиксель переднего плана изображения на основе линейного градиента от левого к правому цвету.

**Параметры:**

- `image` (`Image`) — изображение
- `x` (`int`) — горизонтальная координата пикселя
- `y` (`int`) — вертикальная координата пикселя (не используется)

**Возвращаемое значение:**

- `tuple[int, int, int]` — RGB значение пикселя переднего плана

**Примеры:**

```python
# Пример использования метода
from PIL import Image
from image.styles.colormasks import HorizontalGradiantColorMask

# Создаем изображение и маску
image = Image.new('RGB', (100, 100))
mask = HorizontalGradiantColorMask(left_color=(255, 0, 0), right_color=(0, 255, 0))

# Получаем пиксель переднего плана
fg_pixel = mask.get_fg_pixel(image, x=50, y=0)
print(fg_pixel)  # Выведет примерно (127, 127, 0), т.к. это середина градиента от красного к зелени
```

### `class VerticalGradiantColorMask(QRColorMask)`

Класс для создания вертикального градиентного цветового маски.

#### Методы

##### `__init__(back_color = (255, 255, 255), top_color = (0, 0, 0), bottom_color = (0, 0, 255))`

Инициализирует объект `VerticalGradiantColorMask` с заданными цветами.

**Параметры:**

- `back_color` (`tuple`) — начальный цвет градиента (RGB или RGBA), по умолчанию `(255, 255, 255)`
- `top_color` (`tuple`) — верхний цвет градиента (RGB или RGBA), по умолчанию `(0, 0, 0)`
- `bottom_color` (`tuple`) — нижний цвет градиента (RGB или RGBA), по умолчанию `(0, 0, 255)`

**Примеры:**

```python
mask = VerticalGradiantColorMask(back_color=(255, 255, 0), top_color=(0, 255, 0), bottom_color=(0, 0, 255))
```

##### `get_fg_pixel(image, x, y)`

Возвращает пиксель фона изображения в зависимости от координаты x и y.

**Параметры:**

- `image` (`Image`) — исходное изображение
- `x` (`int`) — горизонтальная координата пикселя
- `y` (`int`) — вертикальная координата пикселя

**Возвращаемое значение:**

- `Color` — цвет фона в заданной точке

**Примеры:**

```python
mask = VerticalGradiantColorMask(...)
pixel_color = mask.get_fg_pixel(image, 100, 200)
```

### `class ImageColorMask(QRColorMask)`

Класс для создания маски цвета изображения.

#### Методы

##### `__init__(back_color = (255, 255, 255), color_mask_path = None, color_mask_image = None)`

Инициализирует объект класса ImageColorMask.

**Параметры:**

- `back_color` (`tuple`) — основной цвет фона, по умолчанию (255, 255, 255)
- `color_mask_path` (`str`) — путь к файлу изображения маски цветов
- `color_mask_image` (`Image.Image`) — объект изображения маски цветов

**Побочные эффекты:**

Изменяет атрибуты объекта.

**Примеры:**

```python
mask = ImageColorMask(back_color=(0, 0, 255), color_mask_path='path/to/mask.png')
```

##### `get_fg_pixel(image, x, y)`

Возвращает пиксель переднего плана из изображения.

**Параметры:**

- `image` (`Image`) — изображение, из которого нужно получить пиксель
- `x` (`int`) — координата x пикселя
- `y` (`int`) — координата y пикселя

**Возвращаемое значение:**

- `tuple` — RGB значение пикселя переднего плана

**Примеры:**

```python
from PIL import Image
mask = ImageColorMask()
fg_pixel = mask.get_fg_pixel(image, 10, 20)
```

##### `initialize(styledPilImage, image)`

Инициализирует объект `ImageColorMask` с помощью изображения и цветового маски.

**Параметры:**

- `styledPilImage` (`object`) — объект, содержащий свойство `paint_color`
- `image` (`object`) — изображение для которого будет изменен размер маски

**Побочные эффекты:**

Изменяет размер свойства `color_img` на размер переданного изображения.

**Примеры:**

```python
# Пример использования
styled_image = StyledPilImage(paint_color="red")
mask = ImageColorMask()
mask.initialize(styled_image, image)
```


---

[← image](README.md) | [← К проекту](../README.md)
