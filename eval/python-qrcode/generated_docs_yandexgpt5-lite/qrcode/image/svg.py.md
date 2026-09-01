# Модуль `qrcode/image/svg.py`


Модуль для создания SVG-изображений QR-кодов.

**Содержание:**

- [Классы](#классы)

## Классы

### `class SvgFillImage(SvgImage)`

Класс SvgFillImage является наследником класса SvgImage и предназначен для создания SVG-изображений с белым фоном.

**Назначение:**

Класс SvgFillImage представляет собой SvgImage, который заполняет фон белым цветом.

**Наследование:**

- `SvgImage`

### `class SvgFragmentImage(qrcode.image.base.BaseImageWithDrawer)`

Класс SvgFragmentImage предназначен для построения SVG-изображения QR-кода.

**Назначение:**

Создаёт изображение QR-кода в виде фрагмента SVG-документа.

**Использование:**

Инициализируйте объект SvgFragmentImage с передачей аргументов и используйте методы для работы с изображением, такие как drawrect, units, save, to_string, new_image, _svg и _write.

**Поля:**

- `default_drawer_class` (`type[QRModuleDrawer]`) — —

**Наследование:**

- `qrcode.image.base.BaseImageWithDrawer`

#### Методы

##### `_write(stream)`

Записывает SVG-изображение в указанный поток.

**Параметры:**

- `stream` (`N/A`) — Поток для записи SVG-изображения

**Примеры:**

Записать SVG-изображение в поток

```python
ET.ElementTree(self._img).write(stream, xml_declaration=False)
```

##### `drawrect(row, col)`

N/A

**Параметры:**

- `row` (`int`) — Строка, задающая позицию прямоугольника
- `col` (`int`) — Столбец, задающий позицию прямоугольника

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызов метода drawrect с указанием строки и столбца

```python
SvgFragmentImage.drawrect(row, col)
```

##### `to_string(**kwargs)`

Преобразует SVG фрагмент в строку с использованием функции ET.tostring

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `str` — Строковое представление SVG фрагмента

**Примеры:**

Преобразование SVG фрагмента в строку

```python
return ET.tostring(self._img, **kwargs)
```

##### `units(pixels, text = True)`

Преобразует количество пикселей в миллиметры.

**Параметры:**

- `text` (`bool`) — Если False, возвращает значение без преобразования в строку.
- `pixels` (`int`) — Количество пикселей, соответствующее 1 мм.

**Возвращаемое значение:**

- `str` — Возвращает значение в миллиметрах в виде строки.

**Примеры:**

Вызов метода с одним аргументом по умолчанию.

```python
units(10)
```

Вызов метода с одним аргументом без преобразования в строку.

```python
units(10, text=False)
```

##### `save(stream, kind = None)`

Сохраняет SVG-изображение в указанный поток.

**Параметры:**

- `kind` (`None`) — Параметр, который определяет вид сохранения
- `stream` (`N/A`) — Поток, в который записывается SVG-изображение

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Сохранить SVG-изображение в указанный поток

```python
SvgFragmentImage.save(stream, kind=None)
```

**Смотрите также:**

def _write(stream)

##### `__init__(*args, **kwargs)`

Инициализирует объект SvgFragmentImage с передачей аргументов.

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация объекта с передачей аргументов

```python
super().__init__(*args, **kwargs)
```

**Смотрите также:**

def units(pixels, text = True) — Преобразует количество пикселей в миллиметры.

##### `_svg(tag = None, version = '1.1', **kwargs)`

Создаёт элемент SVG с заданными параметрами тега, версии и дополнительными аргументами.

**Параметры:**

- `tag` (`ET.QName`) — тег для создания элемента SVG
- `version` (`str`) — версия SVG
- `**kwargs` — —

**Возвращаемое значение:**

- `ET.Element` — элемент SVG

**Примеры:**

Создание элемента SVG с заданными параметрами

```python
if tag is None:
tag = ET.QName(self._SVG_namespace, "svg")
dimension = self.units(self.pixel_size)
return ET.Element(
tag,
width=dimension,
height=dimension,
version=version,
**kwargs,
)
```

Вызов метода _svg с заданными параметрами

```python
from qrcode.image.svg import SvgFragmentImage
fragment = SvgFragmentImage()
tag = None
version = '1.1'
kwargs = {}
fragment._svg(tag, version, **kwargs)
```

**Смотрите также:**

def units(pixels, text = True) — Преобразует количество пикселей в миллиметры.

##### `new_image(**kwargs)`

Создаёт элемент SVG с заданными параметрами.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `object` — Элемент SVG.

**Примеры:**

Создаёт элемент SVG с заданными параметрами.

```python
return self._svg(**kwargs)
```

**Смотрите также:**

def _svg(tag = None, version = '1.1', **kwargs)

### `class SvgImage(SvgFragmentImage)`

Класс SvgImage предназначен для построения отдельного изображения SVG, представляющего QR-код.

**Назначение:**

Создаёт отдельное изображение QR-кода в формате SVG.

**Использование:**

Используйте метод _svg для настройки параметров SVG и _write для записи изображения в поток.

**Поля:**

- `background` (`str | None`) — —
- `drawer_aliases` (`qrcode.image.base.DrawerAliases`) — —

**Наследование:**

- `SvgFragmentImage`

#### Методы

##### `_svg(tag = 'svg', **kwargs)`

Возвращает объект SVG с настройками, переданными в качестве аргументов.

**Параметры:**

- `tag` (`string`) — Тег SVG, по умолчанию 'svg'
- `**kwargs` — —

**Возвращаемое значение:**

- `ET.Element` — Возвращает объект svg

**Примеры:**

Пример использования метода _svg

```python
svg = super()._svg(tag=tag, **kwargs)
svg.set("xmlns", self._SVG_namespace)
if self.background:
svg.append(
    ET.Element(
        "rect",
        fill=self.background,
        x="0",
        y="0",
        width="100%",
        height="100%",
    )
)
return svg
```

N/A

```N/A
N/A
```

##### `_write(stream)`

Записывает SVG изображение в указанный поток.

**Параметры:**

- `stream` (`N/A`) — поток для записи

**Примеры:**

Запись SVG изображения в поток

```python
ET.ElementTree(self._img).write(stream, encoding="UTF-8", xml_declaration=True)
```

### `class SvgPathFillImage(SvgPathImage)`

Класс SvgPathFillImage предназначен для создания SVG-изображений с заполнением фона белым цветом.

**Назначение:**

Класс SvgPathFillImage наследуется от SvgPathImage и заполняет фон белым цветом.

**Наследование:**

- `SvgPathImage`

### `class SvgPathImage(SvgImage)`

Класс SvgPathImage предназначен для создания SVG изображений с одним элементом <path>.

**Назначение:**

Конструктор SVG изображений с одним элементом <path> (удаляет пробелы между отдельными точками QR-кода).

**Использование:**

Инициализируйте объект класса SvgPathImage и используйте методы для настройки параметров и подготовки элемента path для SVG изображения QR кода.

**Поля:**

- `path` (`ET.Element | None`) — —
- `default_drawer_class` (`type[QRModuleDrawer]`) — —

**Наследование:**

- `SvgImage`

#### Методы

##### `__init__(*args, **kwargs)`

Инициализация объекта класса SvgPathImage

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация родительского класса

```python
super().__init__(*args, **kwargs)
```

##### `_svg(viewBox = None, **kwargs)`

Устанавливает значение параметра viewBox для SVG изображения и вызывает метод _svg родительского класса с обновлённым параметром viewBox.

**Параметры:**

- `viewBox` (`str`) — Область просмотра для SVG изображения
- `**kwargs` — —

**Возвращаемое значение:**

- `N/A` — Результат вызова метода _svg родительского класса

**Примеры:**

Установка значения viewBox, если оно не задано

```python
if viewBox is None:
 dimension = self.units(self.pixel_size, text=False)
 viewBox = f"0 0 {dimension} {dimension}"
 return super()._svg(viewBox=viewBox, **kwargs)
```

Вызов метода _svg родительского класса с обновлённым параметром viewBox

```python
return super()._svg(viewBox=viewBox, **kwargs)
```

##### `process()`

Метод process выполняет подготовку элемента path для SVG изображения QR кода.

**Примеры:**

Создание элемента path с объединёнными подпутями и стилями QR

```python
self.path = ET.Element(ET.QName("path"), d="".join(self._subpaths), **self.QR_PATH_STYLE)
```

**Смотрите также:**

qrcode.image.base, qrcode.compat.etree, qrcode.image.styles.moduledrawers.svg


---

[← qrcode](README.md) | [← К проекту](../README.md)
