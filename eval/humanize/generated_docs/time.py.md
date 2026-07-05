# Модуль `time.py`


Модуль для создания "человеческого" представления времени и даты.

**Экспорт:**

- `naturaldate` — —
- `naturalday` — —
- `naturaldelta` — —
- `naturaltime` — —
- `precisedelta` — —

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class Unit(Enum)`

Класс для представления единиц измерения времени.

N/A

N/A

N/A

**Наследование:**

- `Enum`

#### Методы

##### `__lt__(other: Any) -> Any`

Сравнивает два объекта `Unit` и возвращает результат сравнения.

**Параметры:**

- `other` (`Any`) — другой объект для сравнения

**Возвращаемое значение:**

- `Any` — результат сравнения

## Функции

### `def _convert_aware_datetime(value: dt.datetime | dt.timedelta | float | None) -> Any`

Преобразует сознательное время (aware datetime) в несознательное время (naive datetime) и передает любые другие типы данных.

**Параметры:**

- `value` (`dt.datetime | dt.timedelta | float | None`) — значение, которое нужно преобразовать

**Возвращаемое значение:**

- `Any` — преобразованное значение или исходное значение в зависимости от его типа

**Примеры:**

```python
import datetime as dt

# Пример использования функции
aware_dt = dt.datetime.now(dt.timezone.utc)
naive_dt = _convert_aware_datetime(aware_dt)  # Преобразование сознательного времени в несознательное
print(naive_dt)

other_value = None
result = _convert_aware_datetime(other_value)  # Прямое передача значения без изменений
print(result)
```

### `def _now() -> dt.datetime`

Возвращает текущее время.

**Возвращаемое значение:**

- `datetime.datetime` — текущее время

**Примеры:**

```python
current_time = _now()
print(current_time)
```

### `def _rounding_by_fmt(format: str, value: float) -> float | int`

Округляет число в зависимости от строки формата, предоставленной.

Строка формата — это устаревший стиль строкового форматирования printf.

Если используется формат, который обрезает значение, например, "%d" или "%i", возвращаемое значение будет типа `int`.

Если используется формат, который округляет значение, например, "%.2f" или даже "%.0f", мы вернем число типа `float`.

**Параметры:**

- `format` (`str`) — строка формата
- `value` (`float`) — число для округления

**Возвращаемое значение:**

- `float | int` — округленное значение в зависимости от формата

**Примеры:**

```python
# Примеры использования функции _rounding_by_fmt
result1 = _rounding_by_fmt("%d", 3.7)  # result1 будет 3 (int)
result2 = _rounding_by_fmt("%.2f", 3.7)  # result2 будет 3.7 (float)
```

### `def _suitable_minimum_unit(min_unit: Unit, suppress: Iterable[Unit]) -> Unit`

Возвращает минимальный допустимый единицу времени, который не подавлен.

Если единица времени не подавлена, возвращается та же самая единица:

>>> from humanize.time import _suitable_minimum_unit, Unit
>>> _suitable_minimum_unit(Unit.HOURS, []).name
'HOURS'

Но если единица времени подавлена, ищется следующая за исходной единицей время, которая не подавлена:

>>> _suitable_minimum_unit(Unit.HOURS, [Unit.HOURS]).name
'DAYS'

>>> _suitable_minimum_unit(Unit.HOURS, [Unit.HOURS, Unit.DAYS]).name
'MONTHS'

**Параметры:**

- `min_unit` (`Unit`) — минимальная единица времени
- `suppress` (`Iterable[Unit]`) — список подавленных единиц времени

**Возвращаемое значение:**

- `Unit` — минимальная допустимая единица времени, которая не подавлена

**Исключения:**

- `ValueError` — если минимальная единица времени подавлена и нет подходящего замены

**Примеры:**

```python
>>> from humanize.time import _suitable_minimum_unit, Unit
>>> _suitable_minimum_unit(Unit.HOURS, []).name
'HOURS'
>>> _suitable_minimum_unit(Unit.HOURS, [Unit.HOURS]).name
'DAYS'
>>> _suitable_minimum_unit(Unit.HOURS, [Unit.HOURS, Unit.DAYS]).name
'MONTHS'
```

### `def _suppress_lower_units(min_unit: Unit, suppress: Iterable[Unit]) -> set[Unit]`

Расширяет набор подавляемых единиц измерения (если они есть) всеми единицами, меньшими минимальной единицы.

**Параметры:**

- `min_unit` (`Unit`) — минимальная единица измерения
- `suppress` (`Iterable[Unit]`) — список подавляемых единиц измерения

**Возвращаемое значение:**

- `set[Unit]` — расширенный набор подавляемых единиц измерения

**Примеры:**

```python
from humanize.time import _suppress_lower_units, Unit

result = _suppress_lower_units(Unit.SECONDS, [Unit.DAYS])
print([x.name for x in sorted(result)])
# Output: ['MICROSECONDS', 'MILLISECONDS', 'DAYS']
```

### `def naturalday(value: dt.date | dt.datetime, format: str = '%b %d') -> str`

Возвращает "человеческое" представление даты, которое может быть "сегодня", "воскресенье" или "12 марта".

**Параметры:**

- `value` (`dt.date | dt.datetime`) — дата или дата и время для обработки
- `format` (`str, optional`) — строка формата для представления даты, если она не является сегодняшней, вчерашней или завтрашней; по умолчанию '%b %d'

**Возвращаемое значение:**

- `str` — "человеческое" представление даты или строковое представление в формате `format`

**Граничные случаи:**

- Если значение не является объектом даты или временной метки, функция вернет его строковое представление.
- Если значение находится вне допустимого диапазона дат (например, слишком большое число), функция вернет его строковое представление.

**Примеры:**

```python
from datetime import date, datetime

print(naturalday(date(2023, 1, 1)))  # N/A — зависит от текущей даты
print(naturalday(datetime.now()))     # Напечатает "today"
print(naturalday(datetime(2023, 1, 2)))  # Напечатает "tomorrow"
print(naturalday(datetime(2023, 1, 0)))  # Напечатает "yesterday"
print(naturalday(date(2024, 2, 29)))  # Напечатает строковое представление даты
```

### `def _abs_timedelta(delta: dt.timedelta) -> dt.timedelta`

Возвращает абсолютное значение для timedelta, всегда представляющее собой промежуток времени.

**Параметры:**

- `delta` (`datetime.timedelta`) — вводные временные интервалы.

**Возвращаемое значение:**

- `datetime.timedelta` — абсолютный временной интервал.

**Примеры:**

```python
abs_delta = _abs_timedelta(dt.timedelta(days=-1))  # Возвращает timedelta(days=1)
```

**Смотрите также:**

- `def _now() -> dt.datetime` — Возвращает текущее время.

### `def _quotient_and_remainder(value: float, divisor: float, unit: Unit, minimum_unit: Unit, suppress: Iterable[Unit], format: str) -> tuple[float, float]`

Разделяет значение на частное и остаток, возвращая их.

Если указанный единица измерения (`unit`) совпадает с минимальной единицей измерения (`minimum_unit`), то частное будет округлением значения делителя согласно строке формата, а остаток — нулем. Это связано с тем, что если единица измерения является единицей для частного, мы не можем представить остаток, так как он потребовал бы единицы меньшего размера.

Если указанный единица измерения входит в список подавленных единиц измерений (`suppress`), то частное будет равно нулю, а остаток — исходному значению. Это связано с тем, что если мы не можем использовать указанную единицу измерения, мы должны прибегнуть к использованию меньшей единицы измерения.

В остальных случаях возвращаются частное и остаток так, как это делает функция `divmod`.

**Параметры:**

- `value` (`float`) — исходное значение для разделения
- `divisor` (`float`) — делитель
- `unit` (`Unit`) — единица измерения
- `minimum_unit` (`Unit`) — минимальная единица измерения
- `suppress` (`Iterable[Unit]`) — список подавленных единиц измерений
- `format` (`str`) — строка формата для округления частного

**Возвращаемое значение:**

- `tuple[float, float]` — кортеж, содержащий частное и остаток

**Граничные случаи:**

- Если `unit == minimum_unit`, то частное будет отформатировано согласно строке формата, а остаток будет нулем.
- Если `unit in suppress`, то частное будет нулем, а остаток — исходным значением.

**Примеры:**

```python
from humanize.time import _quotient_and_remainder, Unit
# Пример, когда unit равен minimum_unit
print(_quotient_and_remainder(36, 24, Unit.DAYS, Unit.DAYS, [], "%0.2f"))  # (1.5, 0)
# Пример, когда unit в suppress
print(_quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [Unit.DAYS], "%0.2f"))  # (0, 36)
# Пример, когда используется divmod
print(_quotient_and_remainder(36, 24, Unit.DAYS, Unit.HOURS, [], "%0.2f"))  # (1, 12)
```

**Смотрите также:**

- `def _rounding_by_fmt(format: str, value: float) -> float | int` — Округляет число в зависимости от строки формата, предоставленной.

### `def _date_and_delta(value: Any) -> tuple[Any, Any]`

Функция `_date_and_delta` принимает значение и возвращает кортеж, содержащий дату и разницу во времени (timedelta), которая представляет, как давно это значение было. Если невозможно преобразовать значение в дату и timedelta, функция возвращает `(None, value)`.

**Параметры:**

- `value` (`Any`) — Значение, которое необходимо преобразовать в дату и разницу во времени.

**Возвращаемое значение:**

- `tuple[Any, Any]` — Кортеж, содержащий дату и разницу во времени. Если не удалось преобразовать значение, возвращается `(None, value)`.

**Граничные случаи:**

1. Если входное значение является экземпляром `datetime.datetime`, функция вернет текущее время как дату и разницу во времени как timedelta.
2. Если входное значение является экземпляром `datetime.timedelta`, функция вернет дату, вычисленную на основе текущего времени минус timedelta, и само timedelta.
3. Если входное значение не может быть преобразовано в дату или timedelta, функция вернет `(None, value)`.

**Примеры:**

```python
from time import _date_and_delta

# Пример 1: Входное значение является datetime.datetime
result = _date_and_delta(datetime.datetime(2023, 1, 1))
print(result)  # Output: (datetime.datetime(2023, 1, 1), timedelta(0))

# Пример 2: Входное значение является datetime.timedelta
result = _date_and_delta(datetime.timedelta(days=1))
print(result)  # Output: (datetime.datetime(2022, 12, 31), datetime.timedelta(days=1))

# Пример 3: Входное значение не может быть преобразовано в дату или timedelta
result = _date_and_delta("invalid_value")
print(result)  # Output: (None, "invalid_value")
```

**Смотрите также:**

- `def _abs_timedelta(delta: dt.timedelta) -> dt.timedelta` — Возвращает абсолютное значение для timedelta, всегда представляющее собой промежуток времени.
- `def _now() -> dt.datetime` — Возвращает текущее время.

### `def naturaldate(value: dt.date | dt.datetime) -> str`

Возвращает "человеческое" представление даты с учетом года для дат, находящихся более чем через пять месяцев от текущего.

**Параметры:**

- `value` (`dt.date | dt.datetime`) — Дата или дата и время

**Возвращаемое значение:**

- `str` — Человеческое представление даты

**Примеры:**

```python
print(naturaldate(dt.date(2023, 10, 1)))  # Пример с датой в текущем году
print(naturaldate(dt.date(2024, 5, 1)))   # Пример с датой через пять месяцев
```

**Смотрите также:**

- `_abs_timedelta`
- `naturalday`

### `def naturaldelta(value: dt.timedelta | float, months: bool = True, minimum_unit: str = 'seconds') -> str`

Возвращает естественное представление timedelta или количества секунд.

Эта функция похожа на `naturaltime`, но не добавляет временные прилагательные к результату.

Таймдефляйт будет округлен до ближайшей единицы, которая имеет смысл.

**Параметры:**

- `value` (`datetime.timedelta | float`) — timedelta или количество секунд.
- `months` (`bool`) — Если `True`, то будет использовано количество месяцев (на основе 30.5 дней) для нечеткости между годами.
- `minimum_unit` (`str`) — Наиболее низкая единица, которая может быть использована.

**Возвращаемое значение:**

- `str` — естественное представление прошедшего времени или само значение `value`, если это не timedelta или не может быть преобразовано в int (не может быть float из-за 'inf' или 'nan').

**Исключения:**

- `OverflowError`: Если `value` слишком большой, чтобы быть преобразованным в datetime.timedelta.

**Примеры:**

```pycon
>>> import datetime as dt
>>> from dateutil.tz import gettz

>>> berlin = gettz("Europe/Berlin")
>>> now = dt.datetime.now(tz=berlin)
>>> later = now + dt.timedelta(minutes=30)

>>> assert naturaldelta(later - now) == "30 minutes"
True
```

**Смотрите также:**

- `_ngettext(message: str, plural: str, num: int) -> str`
- `intcomma(value: NumberOrString, ndigits: int | None = None) -> str`

### `def naturaltime(value: dt.datetime | dt.timedelta | float, future: bool = False, months: bool = True, minimum_unit: str = 'seconds', when: dt.datetime | None = None) -> str`

Возвращает естественное представление времени с учетом текущего момента и заданных параметров.

Эта функция похожа на Django's `naturaltime` filter, но не добавляет временные прилагательные к результату.

**Параметры:**

- `value` (`datetime.datetime | datetime.timedelta | float`) — Временная метка в виде `datetime`, `timedelta` или количества секунд.
- `future` (`bool, опционально`) — Не используется для `datetime` и `timedelta`. Для целых чисел и浮тинг-поинтов по умолчанию возвращаемое значение будет прошедшем временной периодом, за исключением случаев, когда `future=True`.
- `months` (`bool, опционально`) — Если `True`, то количество месяцев (на основании 30.5 дней) используется для оценки различий между годами.
- `minimum_unit` (`str, опционально`) — Наименьшая единица измерения, которая может быть использована.
- `when` (`datetime.datetime, опционально`) — Момент времени относительно которого интерпретируется `_value`. По умолчанию используется текущее время в местном часовом поясе.

**Возвращаемое значение:**

- `str` — Естественное представление времени с учетом заданных параметров и текущего момента.

**Примеры:**

```python
print(naturaltime(datetime.datetime(2023, 10, 1)))  # Output: "октябрь"
print(naturaltime(datetime.timedelta(days=5)))       # Output: "5 days ago"
print(naturaltime(3600))                          # Output: "an hour ago"
```

### `def precisedelta(value: dt.timedelta | float | None, minimum_unit: str = 'seconds', suppress: Iterable[str] = (), format: str = '%0.2f') -> str`

Возвращает точное представление timedelta или числа секунд.

**Параметры:**

- `value` (`dt.timedelta | float | None`) — значение, которое нужно преобразовать в точный формат времени
- `minimum_unit` (`str`) — минимальная единица измерения для отображения (по умолчанию 'seconds')
- `suppress` (`Iterable[str]`) — список подавляемых единиц измерений
- `format` (`str`) — строка формата для представления дробной части времени

**Возвращаемое значение:**

- `str` — точное представление времени в виде строки

**Примеры:**

```pycon
>>> import datetime as dt
>>> from humanize.time import precisedelta

>>> delta = dt.timedelta(seconds=3633, days=2, microseconds=123000)
>>> precisedelta(delta)
'2 days, 1 hour and 33.12 seconds'

>>> precisedelta(delta, format="%0.4f")
'2 days, 1 hour and 33.1230 seconds'

>>> precisedelta(delta, minimum_unit="microseconds")
'2 days, 1 hour, 33 seconds and 123 milliseconds'

>>> precisedelta(delta, suppress=['days'])
'49 hours and 33.12 seconds'
```


---

[← Индекс](README.md)
