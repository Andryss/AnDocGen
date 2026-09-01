# Модуль `qrcode/image/styles/moduledrawers/__init__.py`


Модуль для ленивого импорта рисовальщиков PIL с предупреждением об устаревании. Импорт рисовальщиков PIL из этого модуля разрешён для обеспечения обратной совместимости, но будет вызывать DeprecationWarning. Модуль будет удалён в версии 9.0.

**Содержание:**

- [Функции](#функции)

## Функции

### `def __getattr__(name)`

Ленивый импорт с предупреждением об устаревании для рисовальщиков PIL

**Параметры:**

- `name` (`str`) — Имя атрибута, для которого вызывается метод __getattr__

**Возвращаемое значение:**

- `object` — Возвращает атрибут из модуля pil, если имя атрибута есть в списке pil_drawers, иначе вызывает AttributeError

**Исключения:**

AttributeError

**Примеры:**

Импорт и возврат рисовальщика из модуля pil

```python
from . import pil # noqa: PLC0415
return getattr(pil, name)
```

Обработка атрибутов модуля

```python
if name in pil_drawers:
 if PIL_AVAILABLE:
 warnings.warn(f"Importing '{name}' directly from this module is deprecated."...)
 from . import pil # noqa: PLC0415
 return getattr(pil, name)
# For any other attribute, raise AttributeError
raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```


---

[← qrcode](README.md) | [← К проекту](../README.md)
