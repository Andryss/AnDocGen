# Модуль `qrcode/image/styledpil.py`


Модуль StyledPilImage для работы с QR-кодами в формате PIL в проекте python-qrcode.

**Содержание:**

- [Классы](#классы)

## Классы

### `class StyledPilImage(qrcode.image.base.BaseImageWithDrawer)`

Класс StyledPilImage для построения стилизованных изображений с использованием библиотеки PIL. Поддерживает настройку модуля отрисовки и цветовой маски.

**Назначение:**

Класс StyledPilImage предназначен для создания стилизованных изображений QR-кодов в формате PIL, в основном PNG. Отличается от PilImage наличием module_drawer, color_mask и опционального изображения.

**Использование:**

Для использования класса StyledPilImage необходимо создать его экземпляр и настроить параметры, такие как module_drawer и color_mask. Изображение может быть задано путём или с помощью объекта Pillow Image. Для сохранения изображения используйте метод save().

**Поля:**

- `color_mask` (`QRColorMask`) — —

**Наследование:**

- `qrcode.image.base.BaseImageWithDrawer`

#### Методы

##### `__getattr__(name)`

Возвращает атрибут изображения, связанного с объектом StyledPilImage

**Параметры:**

- `name` (`str`) — Имя атрибута, для которого вызывается метод __getattr__

**Возвращаемое значение:**

- `object` — Возвращает значение атрибута изображения

**Примеры:**

Возвращает атрибут изображения, связанного с объектом StyledPilImage

```python
return getattr(self._img, name)
```

##### `draw_embedded_image()`

Встраивает изображение в объект StyledPilImage.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызвать метод для встраивания изображения

```python
StyledPilImage.draw_embedded_image()
```

##### `__init__(*args, **kwargs)`

Инициализация объекта StyledPilImage с использованием произвольных аргументов

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Примеры:**

Инициализация объекта StyledPilImage с использованием произвольных аргументов

```python
StyledPilImage.__init__(*args, **kwargs)
```

##### `init_new_image()`

Инициализация нового изображения в методе StyledPilImage.

**Примеры:**

Инициализация нового изображения

```python
super().init_new_image()
```

**Смотрите также:**

from PIL import Image; from qrcode.image.base import qrcode.image.base; from qrcode.image.styles.colormasks import QRColorMask, SolidFillColorMask; from qrcode.image.styles.moduledrawers.pil import SquareModuleDrawer

##### `drawrect(row, col)`

Метод для отрисовки прямоугольника на изображении.

**Параметры:**

- `row` (`int`) — Позиция строки для отрисовки прямоугольника
- `col` (`int`) — Позиция столбца для отрисовки прямоугольника

**Примеры:**

Вызов метода drawrect с указанием строки и столбца

```python
StyledPilImage.drawrect(row, col)
```

##### `new_image(**kwargs)`

Создаёт новое изображение с заданным режимом и цветом фона.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `Image` — Новое изображение с заданными параметрами

**Примеры:**

Создание нового изображения с заданными параметрами

```python
return Image.new(mode, (self.pixel_size, self.pixel_size), back_color)
```

##### `draw_embeded_image()`

Встраивает изображение в объект StyledPilImage.

**Возвращаемое значение:**

- `N/A` — Результат встраивания изображения

**Примеры:**

Встраивает изображение в объект StyledPilImage

```python
return self.draw_embedded_image()
```

**Смотрите также:**

def draw_embedded_image() — Встраивает изображение в объект StyledPilImage.

##### `process()`

Выполняет обработку изображения с применением маски и встраивает встроенное изображение, если оно есть.

**Примеры:**

Вызываются методы для обработки изображения

```python
self.color_mask.apply_mask(self._img)
if self.embedded_image:
    self.draw_embedded_image()
```

**Смотрите также:**

def draw_embedded_image() — Встраивает изображение в объект StyledPilImage.

##### `save(stream, format = None, **kwargs)`

Сохраняет изображение QR-кода в указанный поток в заданном формате.

**Параметры:**

- `format` (`str`) — формат сохранения изображения
- `stream` (`stream`) — поток для сохранения изображения
- `**kwargs` — —

**Примеры:**

Сохранение изображения QR-кода в файл

```python
import qrcode
img = qrcode.make('Some data here')
img.save('some_file.png')
```


---

[← qrcode](README.md) | [← К проекту](../README.md)
