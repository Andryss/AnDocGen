# Модуль `image/pure.py`


Модуль для работы с изображениями, используя библиотеку PyPNG.

**Содержание:**

- [Классы](#классы)

## Классы

### `class PyPNGImage(BaseImage)`

Класс для создания изображений в формате PNG.

**Наследование:**

- `BaseImage` (`qrcode.image.base`) — базовый класс для изображений QR кода

#### Методы

##### `border_rows_iter()`

Генерирует итератор для строк границ изображения.

**Возвращаемое значение:**

- `Iterator[List[int]]` — генератор строк границ, заполненных значением 1

**Примеры:**

```python
img = PyPNGImage(width=10, border=2)
for row in img.border_rows_iter():
    print(row)
```

##### `drawrect(row, col)`

N/A

**Параметры:**

- `row` (`int`) — строка
- `col` (`int`) — столбец

##### `new_image(**kwargs)`

Создает новый изображение с использованием библиотеки PyPNG.

**Параметры:**

- `**kwargs` — —

**Возвращаемое значение:**

- `PngWriter` — объект нового изображения

**Исключения:**

- `ImportError` — если библиотека PyPNG не установлена

**Примеры:**

```python
img = PyPNGImage.new_image()
```

##### `rows_iter()`

Итератор по строкам изображения PNG, добавляющий границы вокруг модулей.

**Возвращаемое значение:**

- `generator` — генератор строк изображения

**Примеры:**

```python
# Пример использования
image = PyPNGImage()
for row in image.rows_iter():
    print(row)
```

##### `save(stream, kind = None)`

Сохраняет изображение в указанный поток.

**Параметры:**

- `stream` (`str`) — путь к файлу или объект, который поддерживает запись байтов
- `kind` (`NoneType, optional`) — тип изображения (не используется)

**Побочные эффекты:**

Записывает изображение в поток.

**Примеры:**

```python
from image.pure import PyPNGImage
img = PyPNGImage()
img.save("output.png")
```


---

[← image](README.md) | [← К проекту](../README.md)
