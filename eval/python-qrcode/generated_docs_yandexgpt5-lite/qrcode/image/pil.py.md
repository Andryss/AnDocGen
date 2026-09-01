# Модуль `qrcode/image/pil.py`


Модуль для работы с изображениями в формате PIL в целях генерации QR-кодов.

**Содержание:**

- [Классы](#классы)

## Классы

### `class PilImage(qrcode.image.base.BaseImage)`

Класс для работы с изображениями в формате PIL, используемый для генерации QR-кодов.

**Назначение:**

Класс для создания изображений QR-кодов в формате PIL, по умолчанию используется формат PNG.

**Использование:**

Создайте экземпляр класса PilImage и используйте методы для создания и сохранения изображений. Для более детального контроля используйте класс QRCode.

**Наследование:**

- `qrcode.image.base.BaseImage`

#### Методы

##### `drawrect(row, col)`

Отрисовывает прямоугольник на изображении в заданной позиции.

**Параметры:**

- `row` (`int`) — координата по вертикали для отрисовки прямоугольника
- `col` (`int`) — координата по горизонтали для отрисовки прямоугольника

**Примеры:**

Вызвать метод drawrect с параметрами row и col

```python
PilImage.drawrect(row, col)
```

##### `__getattr__(name)`

Возвращает атрибут изображения PIL, используя метод getattr

**Параметры:**

- `name` (`str`) — Имя атрибута, который нужно получить

**Возвращаемое значение:**

- `object` — Значение атрибута изображения PIL

**Примеры:**

Возвращает атрибут изображения PIL

```python
return getattr(self._img, name)
```

Пример использования класса qrcode для создания QR-кода

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

##### `new_image(**kwargs)`

Создаёт новое изображение с заданными параметрами цвета фона и заполнения.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `Image` — изображение PIL

**Исключения:**

ImportError

**Примеры:**

Создание QR-кода с помощью функции make

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

Создание QR-кода с использованием класса QRCode

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

##### `save(stream, format = None, **kwargs)`

Сохраняет изображение в указанный поток в заданном формате.

**Параметры:**

- `format` (`str`) — Формат файла для сохранения изображения
- `stream` (`stream`) — Поток для сохранения изображения
- `**kwargs` — —

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Сохранение изображения QR-кода в файл

```python
import qrcode
img = qrcode.make('Some data here')
img.save('some_file.png')
```


---

[← qrcode](README.md) | [← К проекту](../README.md)
