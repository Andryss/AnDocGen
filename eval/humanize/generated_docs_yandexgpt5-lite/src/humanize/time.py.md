# Модуль `src/humanize/time.py`


Модуль содержит функции для преобразования дат, времени и временных интервалов в естественный, удобный для чтения человеком формат.

**Экспорт:**

- `naturaldate` (`function`) — Преобразует дату или datetime в естественный формат с добавлением года для дат более чем примерно пяти месяцев вперёд.
- `naturalday` (`function`) — Возвращает строку с представлением дня в естественном виде. Для дат завтрашнего, сегодняшнего или вчерашнего дня возвращает соответствующее представление. В противном случае возвращает строку, отформатированную согласно параметру format.
- `naturaldelta` (`function`) — Возвращает естественное представление временного интервала или количества секунд.
- `naturaltime` (`function`) — Возвращает естественное представление времени в подходящем разрешении.
- `precisedelta` (`function`) — Возвращает точное представление временной дельты или количества секунд в человекочитаемом формате.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class Unit(Enum)`

Класс Unit представляет собой перечисление (Enum) для работы с единицами времени.

**Назначение:**

Класс Unit является подклассом Enum и предназначен для работы с единицами измерения времени в контексте локализации.

**Использование:**

Используйте класс Unit для сравнения объектов Unit с другими объектами. Для этого можно применять метод __lt__.

**Наследование:**

- `Enum`

#### Методы

##### `__lt__(other: Any) -> Any`

Сравнивает объект Unit с другим объектом и возвращает результат сравнения.

**Параметры:**

- `other` (`Any`) — Сравниваемый объект

**Возвращаемое значение:**

- `Any` — Результат сравнения

**Примеры:**

Сравнение объекта Unit с другим объектом

```python
Unit.__lt__(other)
```

## Функции

### `def _convert_aware_datetime(value: dt.datetime | dt.timedelta | float | None) -> Any`

Преобразует aware datetime в naive datetime и пропускает любой другой тип.

**Параметры:**

- `value` (`dt.datetime | dt.timedelta | float | None`) — Преобразовать aware datetime в naive datetime и пропустить любой другой тип

**Возвращаемое значение:**

- `Any` — Любой тип

**Примеры:**

Преобразовать текущее aware datetime в naive datetime

```python
convert_aware_datetime(dt.datetime.now())
```

### `def _now() -> dt.datetime`

Возвращает текущее время в формате datetime.

**Возвращаемое значение:**

- `dt.datetime` — текущее время в формате datetime

**Примеры:**

Получить текущее время в формате datetime

```python
import datetime as dt
return dt.datetime.now()
```

### `def _rounding_by_fmt(format: str, value: float) -> float | int`

Округляет число согласно заданной строке формата в стиле printf.

**Параметры:**

- `format` (`str`) — Строка формата в стиле printf для округления числа
- `value` (`float`) — Число, которое нужно округлить

**Возвращаемое значение:**

- `float | int` — Число, округлённое согласно строке формата

**Примеры:**

Преобразование числа в целое с усечением дробной части

```python
_rounding_by_fmt('%d', 3.7)
```

Преобразование числа с округлением до двух знаков после запятой

```python
_rounding_by_fmt('%.2f', 3.789)
```

### `def _suitable_minimum_unit(min_unit: Unit, suppress: Iterable[Unit]) -> Unit`

Возвращает минимальную единицу времени, которая не подавлена, или, если все подавлены, вызывает исключение ValueError.

**Параметры:**

- `min_unit` (`Unit`) — Единица времени, для которой нужно найти подходящую минимальную единицу, не подавленную в списке suppress.
- `suppress` (`Iterable[Unit]`) — Список единиц времени, которые подавлены и не должны использоваться.

**Возвращаемое значение:**

- `Unit` — Единица времени, подходящая минимальная единица, не подавленная в списке suppress.

**Исключения:**

ValueError

**Граничные случаи:**

Если все переданные единицы времени подавлены, возникает исключение ValueError с сообщением о том, что минимальная единица подавлена и подходящая замена не найдена.

**Примеры:**

Если не подавлено, возвращается та же единица.

```python
_suitable_minimum_unit(Unit.HOURS, []).name
```

Если подавлено, находится единица больше исходной, которая не подавлена.

```python
_suitable_minimum_unit(Unit.HOURS, [Unit.HOURS]).name
```

Если несколько подавленных единиц, возвращается наибольшая подходящая единица.

```python
_suitable_minimum_unit(Unit.HOURS, [Unit.HOURS, Unit.DAYS]).name
```

### `def _suppress_lower_units(min_unit: Unit, suppress: Iterable[Unit]) -> set[Unit]`

Расширяет список подавленных единиц всеми единицами ниже минимальной единицы

**Параметры:**

- `min_unit` (`Unit`) — Расширить список подавленных единиц всеми единицами ниже минимальной единицы
- `suppress` (`Iterable[Unit]`) — Список единиц, которые нужно подавить

**Возвращаемое значение:**

- `set[Unit]` — Множество единиц, включая расширенный список подавленных единиц

**Примеры:**

Расширить список подавленных единиц всеми единицами ниже минимальной единицы

```python
from humanize.time import _suppress_lower_units, Unit
[x.name for x in sorted(_suppress_lower_units(Unit.SECONDS, [Unit.DAYS]))]
```

### `def naturalday(value: dt.date | dt.datetime, format: str = '%b %d') -> str`

Возвращает строку с представлением дня в естественном виде. Для дат завтрашнего, сегодняшнего или вчерашнего дня возвращает соответствующее представление. В противном случае возвращает строку, отформатированную согласно параметру format.

**Параметры:**

- `format` (`str`) — формат вывода даты
- `value` (`dt.date | dt.datetime`) — дата или время для преобразования

**Возвращаемое значение:**

- `str` — строка с представлением дня в естественном виде

**Примеры:**

Получить строку с форматом '%b %d' для текущей даты

```python
naturalday(dt.date.today(), '%b %d')
```

Получить строку с форматом '%b %d' для указанной даты

```python
naturalday(dt.date(2023, 10, 1), '%b %d')
```

Получить строку с форматом '%b %d' для текущей даты и времени

```python
naturalday(dt.datetime.now(), '%b %d')
```

Получить строку с форматом '%b %d' для указанной даты и времени

```python
naturalday(dt.datetime(2023, 10, 1, 12, 30), '%b %d')
```

Получить строку с форматом '%b %d' для даты, которая будет завтра

```python
naturalday(dt.datetime(2023, 10, 2, 12, 30), '%b %d')
```

### `def _abs_timedelta(delta: dt.timedelta) -> dt.timedelta`

Возвращает абсолютное значение для timedelta, всегда представляющее временной интервал.

**Параметры:**

- `delta` (`datetime.timedelta`) — Входное значение timedelta

**Возвращаемое значение:**

- `datetime.timedelta` — Абсолютное значение timedelta

**Примеры:**

Получить абсолютное значение для timedelta с отрицательным количеством дней

```python
from humanize.time import _abs_timedelta
from datetime import timedelta

delta = timedelta(days=-1)
result = _abs_timedelta(delta)
print(result)
```

**Смотрите также:**

def _now() -> dt.datetime — Возвращает текущее время в формате datetime.

### `def _quotient_and_remainder(value: float, divisor: float, unit: Unit, minimum_unit: Unit, suppress: Iterable[Unit], format: str) -> tuple[float, float]`

Делит значение на делитель, возвращая частное и остаток. Если unit совпадает с minimum_unit, частное будет округлено согласно строке формата и остаток будет равен нулю. Если unit находится в списке suppress, частное будет равно нулю, а остаток будет равен исходному значению. В других случаях возвращается частное и остаток как это делает divmod.

**Параметры:**

- `value` (`float`) — Делимое число.
- `divisor` (`float`) — Делитель.
- `unit` (`Unit`) — Единица измерения для результата.
- `minimum_unit` (`Unit`) — Минимальная единица измерения для результата.
- `suppress` (`Iterable[Unit]`) — Список единиц измерения, которые нужно подавить.
- `format` (`str`) — Строка формата для округления результата.

**Возвращаемое значение:**

- `tuple[float, float]` — Кортеж из двух чисел: частное и остаток.

**Примеры:**

Если unit совпадает с minimum_unit, частное будет округлено согласно строке формата и остаток будет равен нулю.

```python
_quotient_and_remainder(36, 24, Unit.DAYS, Unit.DAYS, [], "%0.2f")
```

Если unit находится в списке suppress, частное будет равно нулю, а остаток будет равен исходному значению.

```python
_quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [Unit.DAYS], "%0.2f")
```

В других случаях возвращается частное и остаток как это делает divmod.

```python
_quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [], "%0.2f")
```

**Смотрите также:**

def _rounding_by_fmt(format: str, value: float) -> float | int — Округляет число согласно заданной строке формата в стиле printf.

### `def _date_and_delta(value: Any) -> tuple[Any, Any]`

Преобразует значение в дату и timedelta, представляющую, как давно это было. Если это невозможно, возвращает (None, value).

**Параметры:**

- `value` (`Any`) — Преобразует значение в дату и timedelta, представляющую, как давно это было. Если это невозможно, возвращает (None, value).

**Возвращаемое значение:**

- `tuple[Any, Any]` — дата и timedelta, представляющая, как давно это было, или (None, value), если преобразование невозможно

**Примеры:**

Преобразовать текущее время в дату и timedelta.

```python
date, delta = _date_and_delta(dt.datetime.now())
```

Преобразовать timedelta в дату и timedelta.

```python
date, delta = _date_and_delta(dt.timedelta(seconds=10))
```

Преобразовать число в дату и timedelta.

```python
date, delta = _date_and_delta(5)
```

**Смотрите также:**

def _abs_timedelta(delta: dt.timedelta) -> dt.timedelta — Возвращает абсолютное значение для timedelta, всегда представляющее временной интервал. def _now() -> dt.datetime — Возвращает текущее время в формате datetime.

### `def naturaldate(value: dt.date | dt.datetime) -> str`

Преобразует дату или datetime в естественный формат с добавлением года для дат более чем примерно пяти месяцев вперёд.

**Параметры:**

- `value` (`dt.date | dt.datetime`) — Преобразовать дату или datetime в естественный формат с добавлением года для дат более чем примерно пяти месяцев вперёд

**Возвращаемое значение:**

- `str` — Строковое представление даты в естественном формате

**Примеры:**

Преобразовать дату в естественный формат

```python
naturaldate(dt.date(2020, 1, 1))
```

Преобразовать datetime в естественный формат

```python
naturaldate(dt.datetime(2020, 1, 1, 12, 0, 0))
```

**Смотрите также:**

def _abs_timedelta(delta: dt.timedelta) -> dt.timedelta — Возвращает абсолютное значение для timedelta, всегда представляющее временной интервал. def naturalday(value: dt.date | dt.datetime, format: str = '%b %d') -> str — Возвращает строку с представлением дня в естественном виде.

### `def naturaldelta(value: dt.timedelta | float, months: bool = True, minimum_unit: str = 'seconds') -> str`

Возвращает естественное представление временного интервала или количества секунд.

**Параметры:**

- `months` (`bool`) — Если `True`, то используется количество месяцев (на основе 30,5 дней) для приблизительного подсчёта между годами.
- `minimum_unit` (`str`) — Наименьшая единица времени, которая может быть использована.
- `value` (`dt.timedelta | float | int`) — Временной интервал, который нужно представить в естественном виде (может быть datetime.timedelta, int или float).

**Возвращаемое значение:**

- `str` — Естественное представление временного интервала, если `value` не является datetime.timedelta или не может быть преобразовано в int, возвращается `value` без изменений.

**Исключения:**

OverflowError: If `value` is too large to convert to datetime.timedelta.

**Примеры:**

Сравнение двух временных меток в локальном часовом поясе.

```python
>>> import datetime as dt
>>> from dateutil.tz import gettz
>>> berlin = gettz("Europe/Berlin")
>>> now = dt.datetime.now(tz=berlin)
>>> later = now + dt.timedelta(minutes=30)
>>> assert naturaldelta(later - now) == "30 minutes"
True
```

N/A

```N/A
N/A
```

**Смотрите также:**

def _ngettext(message: str, plural: str, num: int) -> str — Возвращает перевод с учётом числа, используя множественное число, если это необходимо.
def intcomma(value: NumberOrString, ndigits: int | None = None) -> str — Преобразует целое число или число с плавающей точкой в строку с запятыми каждые три цифры.

### `def naturaltime(value: dt.datetime | dt.timedelta | float, future: bool = False, months: bool = True, minimum_unit: str = 'seconds', when: dt.datetime | None = None) -> str`

Возвращает естественное представление времени в подходящем разрешении.

**Параметры:**

- `future` (`bool`) — Игнорируется для datetime и timedelta, где время всегда определяется на основе текущего времени. Для целых чисел и чисел с плавающей точкой возвращаемое значение будет по умолчанию в прошедшем времени, если future не равно True
- `months` (`bool`) — Если True, то для определения разницы между годами будет использоваться количество месяцев (на основе 30,5 дней)
- `minimum_unit` (`str`) — Наименьшая единица, которая может быть использована
- `when` (`dt.datetime`) — Точка во времени относительно которой интерпретируется значение. По умолчанию текущее время в локальном часовом поясе
- `value` (`dt.datetime | dt.timedelta | float`) — Значение datetime, timedelta или число секунд

**Возвращаемое значение:**

- `str` — Естественное представление ввода в подходящем разрешении

**Примеры:**

Получить представление временного интервала в один день назад

```python
naturaltime(dt.datetime.now() - dt.timedelta(days=1))
```

Получить представление временного интервала в один миллион секунд в будущем

```python
naturaltime(1000000, future=True)
```

**Смотрите также:**

def _convert_aware_datetime(value: dt.datetime | dt.timedelta | float | None) -> Any — Преобразует aware datetime в naive datetime и пропускает любой другой тип.

### `def precisedelta(value: dt.timedelta | float | None, minimum_unit: str = 'seconds', suppress: Iterable[str] = (), format: str = '%0.2f') -> str`

Возвращает точное представление временной дельты или количества секунд в человекочитаемом формате.

**Параметры:**

- `value` (`dt.timedelta | float | None`) — Значение, которое нужно преобразовать в человекочитаемый формат. Может быть timedelta, float или None.
- `minimum_unit` (`str`) — Минимальная единица времени для представления. Возможные значения: 'seconds', 'microseconds' и т.д.
- `suppress` (`Iterable[str]`) — Список единиц времени, которые нужно подавить.
- `format` (`str`) — Формат представления дробной части числа.

**Возвращаемое значение:**

- `str` — Строковое представление временной дельты или числа секунд.

**Примеры:**

Получить представление временной дельты.

```python
precisedelta(dt.timedelta(seconds=3633, days=2, microseconds=123000))
```

Получить представление временной дельты с точностью до четырёх знаков после запятой.

```python
precisedelta(delta, format='%0.4f')
```

Получить представление временной дельты с точностью до микросекунд.

```python
precisedelta(delta, minimum_unit='microseconds')
```

Получить представление временной дельты без дней.

```python
precisedelta(delta, suppress=['days'])
```

Получить представление временной дельты в минутах, игнорируя секунды и меньшие единицы.

```python
precisedelta(delta, suppress=['seconds', 'milliseconds', 'microseconds'])
```

Получить представление временной дельты в минутах, даже если она меньше минуты.

```python
precisedelta(delta, minimum_unit='minutes')
```


---

[← src](README.md) | [← К проекту](../README.md)
