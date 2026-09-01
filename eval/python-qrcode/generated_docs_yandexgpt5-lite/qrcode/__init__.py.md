# Модуль `qrcode/__init__.py`


Модуль python-qrcode для генерации QR-кодов. Содержит функции для создания QR-кодов и примеры их использования.

**Экспорт:**

- `ERROR_CORRECT_H` — —
- `ERROR_CORRECT_L` — —
- `ERROR_CORRECT_M` — —
- `ERROR_CORRECT_Q` — —
- `QRCode` — —
- `image` — —
- `make` — —
- `run_example` (`function`) — Создаёт пример QR-кода и отображает его

**Содержание:**

- [Функции](#функции)

## Функции

### `def run_example(data = 'http://www.lincolnloop.com', *args, **kwargs)`

Создаёт пример QR-кода и отображает его.

**Параметры:**

- `data` (`str`) — Данные для кодирования в QR-код
- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `N/A` — N/A

**Побочные эффекты:**

Отображение QR-кода

**Примеры:**

Создание QR-кода с использованием класса QRCode и его отображение

```python
import qrcode
qr = qrcode.QRCode()
qr.add_data('Some data')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
```

Создание QR-кода с использованием функции make

```python
import qrcode
img = qrcode.make('Some data here')
type(img)  # qrcode.image.pil.PilImage
img.save("some_file.png")
```

**Смотрите также:**

from qrcode import image
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q
from qrcode.main import QRCode, make


---

[← qrcode](README.md) | [← К проекту](../README.md)
