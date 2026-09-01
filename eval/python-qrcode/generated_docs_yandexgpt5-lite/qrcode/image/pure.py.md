# Модуль `qrcode/image/pure.py`


Модуль python-qrcode представляет собой генератор QR-кодов на чистом Python. Он использует библиотеку pypng для создания PNG-файлов и может отображать QR-коды непосредственно в консоли. Для более широких возможностей по работе с изображениями требуется установка зависимости pil, которая устанавливает pillow.

**Содержание:**

- [Классы](#классы)

## Классы

### `class PyPNGImage(BaseImage)`

Класс PyPNGImage предназначен для построения изображений QR-кодов с использованием библиотеки pypng.

**Назначение:**

Класс для создания изображений QR-кодов в формате PNG.

**Использование:**

Создайте экземпляр класса PyPNGImage и используйте методы new_image, drawrect, save, rows_iter и border_rows_iter для работы с изображением QR-кода.

**Наследование:**

- `BaseImage`

#### Методы

##### `border_rows_iter()`

Итерирует строки границы для QR-кода.

**Примеры:**

Итерировать строки границы

```python
border_rows_iter()
```

##### `drawrect(row, col)`

Метод для отрисовки прямоугольника.

**Параметры:**

- `row` (`int`) — координата строки для отрисовки прямоугольника
- `col` (`int`) — координата столбца для отрисовки прямоугольника

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

N/A

```python
PyPNGImage.drawrect(row, col)
```

N/A

```N/A
N/A
```

##### `new_image(**kwargs)`

Создаёт новое изображение с заданными параметрами.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `PngWriter` — Экземпляр класса PngWriter

**Исключения:**

ImportError: PyPNG library not installed.

**Примеры:**

Создание нового изображения с заданными параметрами

```python
return PngWriter(self.pixel_size, self.pixel_size, greyscale=True, bitdepth=1)
```

##### `rows_iter()`

Итерирует строки QR-кода, включая строки границы.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример использования метода rows_iter()

```python
yield from self.border_rows_iter()
border_col = [1] * (self.box_size * self.border)
for module_row in self.modules:
    row = (
border_col
    + list(
        chain.from_iterable(
            ([not point] * self.box_size) for point in module_row
        )
    ) + border_col
)
for _ in range(self.box_size):
yield row
yield from self.border_rows_iter()
```

Пример вызова border_rows_iter()

```python
yield from self.border_rows_iter()
```

**Смотрите также:**

border_rows_iter()

##### `save(stream, kind = None)`

Сохраняет изображение QR-кода в указанный файл или поток.

**Параметры:**

- `stream` (`str or file`) — Тип файла, в который будет сохранено изображение. Может быть строкой, представляющей путь к файлу, или файловым объектом.
- `kind` (`None`) — Тип сохраняемого изображения. N/A

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример использования метода save() для сохранения изображения QR-кода в файл

```python
import qrcode
qr = qrcode.QRCode()
qr.add_data('Some data')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("some_file.png")
```

Пример использования метода save() для сохранения изображения QR-кода в файл

```python
import qrcode
img = qrcode.make('Some data here')
img.save("some_file.png")
```


---

[← qrcode](README.md) | [← К проекту](../README.md)
