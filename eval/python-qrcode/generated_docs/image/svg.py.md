# Модуль `image/svg.py`


Модуль для создания изображений SVG с различными элементами.

**Содержание:**

- [Классы](#классы)

## Классы

### `class SvgFragmentImage(qrcode.image.base.BaseImageWithDrawer)`

Класс для создания изображения QR-кода в формате SVG в виде фрагмента документа.

**Поля:**

- `default_drawer_class` (`type[QRModuleDrawer]`) — —

**Наследование:**

- `qrcode.image.base.BaseImageWithDrawer`

#### Методы

##### `__init__(*args, **kwargs)`

Инициализирует объект `SvgFragmentImage` и настраивает пространство имен SVG.

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Побочные эффекты:**

- Регистрирует пространство имен "svg" с использованием значения `_SVG_namespace`.
- Вызывает конструктор родительского класса `__init__(*args, **kwargs)`.

**Примеры:**

```python
# Пример использования не применим, так как метод __init__ не принимает аргументы.
```

##### `_svg(tag = None, version = '1.1', **kwargs)`

Создает элемент SVG с указанными параметрами.

**Параметры:**

- `tag` (`str | None`) — имя тега SVG (по умолчанию "svg")
- `version` (`str`) — версия формата SVG (по умолчанию '1.1')
- `**kwargs` — —

**Возвращаемое значение:**

- `Element` — созданный элемент SVG

**Примеры:**

```python
svg_element = SvgFragmentImage._svg(tag="rect", width=10, height=20)
```

##### `_write(stream)`

Записывает объект SVG в поток.

**Параметры:**

- `stream` (`io.IOBase`) — поток, куда записывается SVG

**Примеры:**

```python
svg_fragment_image = SvgFragmentImage()
with open('output.svg', 'wb') as f:
    svg_fragment_image._write(f)
```

##### `drawrect(row, col)`

N/A

**Параметры:**

- `row` (`int`) — N/A
- `col` (`int`) — N/A

##### `new_image(**kwargs)`

Создает новый объект изображения SVG.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `svg` — созданный объект изображения SVG

**Примеры:**

```python
new_image()
```

##### `save(stream, kind = None)`

Сохраняет SVG фрагмент изображения в поток.

**Параметры:**

- `stream` (`qrcode.image.base.QRCodeImage`) — поток для сохранения
- `kind` (`Literal['svg'], опционально`) — тип формата, по умолчанию 'svg'

**Примеры:**

```python
# Пример использования
from qrcode import QRCode
from image.svg import SvgFragmentImage

qr = QRCode()
image = SvgFragmentImage(qr)
with open('output.svg', 'wb') as stream:
    image.save(stream)
```

##### `to_string(**kwargs)`

Преобразует объект SvgFragmentImage в строку SVG.

**Параметры:**

- `**kwargs` — дополнительные аргументы, передаваемые в метод `ET.tostring`.

**Возвращаемое значение:**

- `str` — строковое представление объекта SVG.

**Примеры:**

```python
# Пример использования
svg_fragment = SvgFragmentImage()  # Предполагается, что SvgFragmentImage уже создан
svg_string = svg_fragment.to_string()
print(svg_string)
```

##### `units(pixels, text = True)`

Переводит количество пикселей в единицы измерения (миллиметры).

**Параметры:**

- `pixels` (`int`) — количество пикселей
- `text` (`bool, optional`) — если True, возвращает строку с единицами измерения; если False, возвращает Decimal

**Возвращаемое значение:**

- `str` — строка с количеством миллиметров (если text=True)

**Примеры:**

```python
# Пример использования метода units
result_str = SvgFragmentImage.units(100)  # Возвращает '10.000mm'
result_decimal = SvgFragmentImage.units(100, text=False)  # Возвращает Decimal('10')
```

### `class SvgImage(SvgFragmentImage)`

Класс для создания изображения QR-кода в формате SVG как отдельного документа.

**Поля:**

- `background` (`str | None`) — —
- `drawer_aliases` (`qrcode.image.base.DrawerAliases`) — —

#### Методы

##### `_svg(tag = 'svg', **kwargs)`

Создает SVG-элемент с заданным тегом и атрибутами.

**Параметры:**

- `tag` (`Literal['svg']`) — имя тега, по умолчанию 'svg'
- `**kwargs` (`dict`) — дополнительные атрибуты для элемента SVG

**Возвращаемое значение:**

- `ET.Element` — созданный SVG-элемент

**Примеры:**

```python
svg_element = SvgImage._svg(tag='circle', cx=50, cy=50, r=40)
```

##### `_write(stream)`

Записывает изображение в поток в формате SVG.

**Параметры:**

- `stream` (`object`) — объект потока, куда будет записано изображение

**Примеры:**

```python
img = SvgImage()
with open('output.svg', 'wb') as f:
    img._write(f)
```

### `class SvgPathImage(SvgImage)`

Класс для построения изображений в формате SVG с одним элементом `<path>`, который объединяет точки QR-кода без пробелов между ними.

**Поля:**

- `path` (`ET.Element | None`) — —
- `default_drawer_class` (`type[QRModuleDrawer]`) — —

**Наследование:**

SvgImage

#### Методы

##### `__init__(*args, **kwargs)`

Инициализирует экземпляр SvgPathImage.

**Параметры:**

- `*args` — переменное количество позиционных аргументов, передаваемых базовому классу.
- `**kwargs` — переменное количество именованных аргументов, передаваемых базовому классу.

**Примеры:**

```python
# Пример использования:
image = SvgPathImage()
```

##### `_svg(viewBox = None, **kwargs)`

Метод для создания SVG-представления изображения.

**Параметры:**

- `viewBox` (`Literal[str], optional`) — параметр viewBox SVG; если None, будет рассчитано автоматически
- `**kwargs` — —

**Возвращаемое значение:**

- `str` — строковое представление SVG

**Примеры:**

```python
img = SvgPathImage(pixel_size=100)
svg_str = img._svg(viewBox="0 0 100 100")
```

##### `process()`

Обрабатывает путь SVG и добавляет его к изображению.

**Побочные эффекты:**

Изменяет внутреннее состояние объекта, добавляя новый элемент пути SVG к изображению.

**Примеры:**

```python
obj = SvgPathImage()
obj.process()
```

### `class SvgFillImage(SvgImage)`

Класс для создания изображений SVG с заливкой фона в белый цвет.

**Наследование:**

```python
SvgFillImage(SvgImage)
```

### `class SvgPathFillImage(SvgPathImage)`

Класс для создания изображения SVG с заполненным фоном белым цветом.


---

[← image](README.md) | [← К проекту](../README.md)
