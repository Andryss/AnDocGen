# Модуль `__init__.py`


Основной модуль пакета для форматирования чисел и дат в более читаемый вид.

**Экспорт:**

- `__version__` (`str`) — версия пакета.
- `activate` (`Callable[[Optional[str]], None]`) — активация локализации.
- `apnumber` (`Callable[[int], str]`) — преобразование числа в словесное представление для использования в числительных.
- `clamp` (`Callable[[float, float, float], float]`) — ограничение значения между заданными границами.
- `deactivate` (`Callable[[], None]`) — деактивация локализации.
- `decimal_separator` (`str`) — символ десятичного разделителя.
- `fractional` (`Callable[[float, Optional[int]], str]`) — преобразование дробной части числа в словесное представление.
- `intcomma` (`Callable[[Union[int, float], bool, int], str]`) — добавление запятых для тысяч и десятиков.
- `intword` (`Callable[[Union[int, float]], str]`) — преобразование числа в более читаемый формат с использованием единиц измерения.
- `metric` (`Callable[[float], str]`) — преобразование числа в строку с метрическими единицами.
- `natural_list` (`Callable[[Sequence[Any]], str]`) — преобразование списка в строку с последовательностью слов, используя соединитель "и".
- `naturaldate` (`Callable[[Union[datetime.date, datetime.datetime], bool], str]`) — преобразование даты или времени в более читаемый формат.
- `naturalday` (`Callable[[Union[datetime.date, datetime.datetime]], str]`) — преобразование дня в словесное представление.
- `naturaldelta` (`Callable[[Union[timedelta, int, float], bool, Optional[str]], str]`) — преобразование временного интервала в более читаемый формат.
- `naturalsize` (`Callable[[int, str, int], str]`) — преобразование размера файла в более читаемый формат с использованием единиц измерения.
- `naturaltime` (`Callable[[Union[int, float]], str]`) — преобразование времени в словесное представление.
- `ordinal` (`Callable[[int], str]`) — преобразование числа в порядковое слово.
- `precisedelta` (`Callable[[timedelta, int], str]`) — преобразование временного интервала с точностью до заданного количества единиц времени.
- `scientific` (`Callable[[float], str]`) — преобразование числа в научный формат.
- `thousands_separator` (`str`) — символ разделителя тысяч.


---

[← Индекс](README.md)
