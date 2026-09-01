# Модуль `src/cachetools/func.py`


Модуль предоставляет различные коллекции для мемоизации и декораторы, включая варианты декоратора функции @lru_cache из стандартной библиотеки Python.

**Экспорт:**

- `fifo_cache` (`function`) — Декоратор для обёртывания функции с кэшированием на основе алгоритма FIFO, сохраняющим до maxsize результатов.
- `lfu_cache` (`function`) — Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма Least Frequently Used (LFU)
- `lru_cache` (`function`) — Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма Least Recently Used (LRU)
- `rr_cache` (`function`) — Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма случайного замещения (RR)
- `ttl_cache` (`function`) — Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма LRU с временем жизни каждого элемента.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class _UnboundTTLCache(TTLCache)`

Класс _UnboundTTLCache представляет собой реализацию кэша с истекающим временем жизни элементов (TTL), не имеющего ограничения по максимальному размеру.

**Назначение:**

Класс _UnboundTTLCache является подклассом TTLCache и предназначен для реализации кэширования с истекающим временем жизни элементов (TTL).

**Использование:**

Инициализируйте объект _UnboundTTLCache с помощью метода __init__(ttl, timer), где ttl задаёт время жизни элементов в кэше, а timer отвечает за обновление времени жизни. Метод maxsize() возвращает значение None.

**Наследование:**

- `TTLCache`

#### Методы

##### `__init__(ttl, timer)`

Инициализирует объект TTLCache с заданными параметрами ttl и timer.

**Параметры:**

- `ttl` (`N/A`) — Параметр ttl используется для установки времени жизни элемента в кэше. Параметр timer используется для синхронизации кэша.
- `timer` (`N/A`) — Таймер для синхронизации кэша.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Инициализация TTLCache

```python
from cachetools import TTLCache
TTLCache.__init__(self, math.inf, ttl, timer)
```

##### `maxsize()`

Возвращает значение None.

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Возвращает None

```python
return None
```

## Функции

### `def _cache(cache, maxsize, typed)`

Функция _cache используется как декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше.

**Параметры:**

- `cache` (`N/A`) — Кэш, используемый для хранения результатов.
- `maxsize` (`N/A`) — Максимальный размер кэша.
- `typed` (`N/A`) — Флаг, указывающий на использование типизированного ключа.

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример использования функции _cache в качестве декоратора для функции func.

```python
def decorator(func):
    key = keys.typedkey if typed else keys.hashkey
    wrapper = cached(cache=cache, key=key, condition=Condition(), info=True)(func)
    wrapper.cache_parameters = lambda: {"maxsize": maxsize, "typed": typed}  # type: ignore
    return wrapper
return decorator
```

Импорт необходимых модулей для использования функции _cache.

```python
from . import cached
from . import keys
```

**Смотрите также:**

def cached(cache, key = keys.hashkey, lock = None, condition = None, info = False)

### `def fifo_cache(maxsize = 128, typed = False)`

Декоратор для обёртывания функции с кэшированием на основе алгоритма FIFO, сохраняющим до maxsize результатов.

**Параметры:**

- `maxsize` (`int`) — максимальное количество сохраняемых результатов
- `typed` (`bool`) — указывает, что кэширование должно учитывать типы данных

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Декоратор для функции с кэшированием на основе FIFO алгоритма

```python
from cachetools import fifo_cache
@fifo_cache(maxsize=128, typed=False)
def example_func(): pass
```

**Смотрите также:**

def _cache(cache, maxsize, typed)

### `def lfu_cache(maxsize = 128, typed = False)`

Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма Least Frequently Used (LFU)

**Параметры:**

- `maxsize` (`int`) — максимальное количество сохраняемых результатов
- `typed` (`bool`) — указывает, что ключи могут быть разных типов

**Примеры:**

Пример использования декоратора lfu_cache

```python
from cachetools import lfu_cache
@lfu_cache(maxsize=64, typed=True)
def example_func(arg):
    return arg
```

### `def rr_cache(maxsize = 128, choice = random.choice, typed = False)`

Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма случайного замещения (RR)

**Параметры:**

- `maxsize` (`int`) — максимальное количество сохраняемых результатов
- `choice` (`callable`) — функция для выбора элемента для удаления из кэша
- `typed` (`bool`) — указывает, что кэшируемые значения имеют определённый тип

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример использования декоратора rr_cache

```python
from cachetools import rr_cache
@rr_cache(maxsize=128, choice=random.choice, typed=False)
def some_func():
    pass
```

**Смотрите также:**

def _cache(cache, maxsize, typed)

### `def lru_cache(maxsize = 128, typed = False)`

Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма Least Recently Used (LRU)

**Параметры:**

- `maxsize` (`int`) — максимальное количество сохраняемых результатов
- `typed` (`bool`) — указывает, что ключи должны быть хэшируемыми объектами

**Примеры:**

Пример использования lru_cache для кэширования данных PEP

```python
from cachetools import lru_cache
@lru_cache(maxsize=32)
def get_pep(num):
    url = 'http://www.python.org/dev/peps/pep-%04d/' % num
    with urllib.request.urlopen(url) as s:
        return s.read()
```

Пример использования lru_cache для кэширования результатов вычисления чисел Фибоначчи

```python
from cachetools import lru_cache
@lru_cache(maxsize=128, typed=True)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

### `def ttl_cache(maxsize = 128, ttl = 600, timer = time.monotonic, typed = False)`

Декоратор для обёртывания функции с мемоизацией, сохраняющей результаты в кэше на основе алгоритма LRU с временем жизни каждого элемента.

**Параметры:**

- `maxsize` (`int`) — максимальное количество сохраняемых результатов на основе алгоритма LRU
- `ttl` (`int`) — время жизни каждого элемента в кэше в секундах
- `timer` (`callable`) — функция для получения текущего времени
- `typed` (`bool`) — указывает, что ключи в кэше должны быть типизированы

**Примеры:**

Кеширование данных о погоде с TTL в 10 минут

```python
from cachetools import TTLCache
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_weather(place):
    return owm.weather_at_place(place).get_weather()
```

Кеширование вычислений чисел Фибоначчи

```python
from cachetools import TTLCache
@cached(cache=TTLCache(maxsize=128, ttl=600))
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

**Смотрите также:**

def _cache(cache, maxsize, typed)


---

[← src](README.md) | [← К проекту](../README.md)
