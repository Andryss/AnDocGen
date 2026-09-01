# Модуль `src/cachetools/_cached.py`


Модуль предоставляет различные инструменты для кэширования, включая варианты декоратора функции @lru_cache из стандартной библиотеки Python.

**Содержание:**

- [Функции](#функции)

## Функции

### `def _condition(func, cache, key, lock, cond)`

Создаёт обёртку для функции с кэшированием, используя заданный кэш и условия.

**Параметры:**

- `func` (`function`) — Функция, которая будет обёрнута в кэш.
- `cache` (`cache`) — Кэш, используемый для хранения результатов.
- `key` (`function`) — Функция для получения ключа для кэша.
- `lock` (`lock`) — Блокировка для синхронизации доступа к кэшу.
- `cond` (`condition`) — Условие для ожидания освобождения ключа в кэше.

**Возвращаемое значение:**

- `function` — Обёрнутая функция с кэшированием.

**Примеры:**

Пример вызова функции _condition с необходимыми аргументами.

```python
def _condition(func, cache, key, lock, cond): ...
```

### `def _condition_info(func, cache, key, lock, cond, info)`

Функция _condition_info используется для управления кэшированием и обработки условий при доступе к кэшу.

**Параметры:**

- `func` (`function`) — Параметр функции, используемый в кэшировании
- `cache` (`object`) — Кэш для хранения результатов
- `key` (`function`) — Ключ для идентификации кэшированных данных
- `lock` (`object`) — Блокировка для синхронизации доступа к кэшу
- `cond` (`object`) — Условие для ожидания освобождения ключа
- `info` (`object`) — Информация о количестве попаданий и промахов

**Примеры:**

Пример вызова функции _condition_info

```python
def _condition_info(func, cache, key, lock, cond, info)
```

### `def _locked(func, cache, key, lock)`

Создает обертку для функции с кэшированием, используя заданный кэш и механизм блокировки.

**Параметры:**

- `func` (`function`) — Функция, которая будет обернута для кэширования
- `cache` (`cache`) — Кэш для хранения значений
- `key` (`function`) — Ключ для получения значения из кэша
- `lock` (`lock`) — Блокировка для обеспечения потокобезопасности

**Возвращаемое значение:**

- `function` — Обернутая функция с кэшированием

**Примеры:**

Пример использования функции _locked

```python
def wrapper(*args, **kwargs): k = key(*args, **kwargs) with lock: try: return cache[k] except KeyError: pass # key not found v = func(*args, **kwargs) with lock: try: # In case of a race condition, i.e. if another thread # stored a value for this key while we were calling # func(), prefer the cached value. return cache.setdefault(k, v) except ValueError: return v # value too large
```

### `def _locked_info(func, cache, key, lock, info)`

Создаёт обёртку для функции с кэшированием, используя заданный кэш, ключ, блокировку и функцию для получения информации о кэше.

**Параметры:**

- `func` (`function`) — Функция, которая будет обернута для кэширования
- `cache` (`cache`) — Кэш, используемый для хранения результатов
- `key` (`function`) — Функция для генерации ключа кэша
- `lock` (`lock`) — Блокировка для синхронизации доступа к кэшу
- `info` (`function`) — Функция для получения информации о кэше

**Возвращаемое значение:**

- `wrapper` — N/A

**Примеры:**

Пример вызова функции _locked_info

```python
def _locked_info(func, cache, key, lock, info)
```

### `def _uncached(func)`

Создаёт обёртку для функции, удаляя кэширование.

**Параметры:**

- `func` (`function`) — Функция, которую нужно обернуть для удаления кэширования

**Возвращаемое значение:**

- `function` — Обернутая функция без кэширования

**Примеры:**

Пример использования функции _uncached

```python
def wrapper(*args, **kwargs):
 return func(*args, **kwargs)

wrapper.cache_clear = lambda: None
return wrapper
```

### `def _uncached_info(func, info)`

Создаёт обёртку для функции с дополнительной логикой для работы с кэшем.

**Параметры:**

- `func` (`function`) — Функция, которую нужно обернуть для работы с кэшем
- `info` (`function`) — Информация о промахах кэша

**Возвращаемое значение:**

- `function` — Обернутая функция с дополнительной логикой для работы с кэшем

**Примеры:**

Пример использования функции _uncached_info

```python
def _uncached_info(func, info):
 miss = 0

 def wrapper(*args, **kwargs):
 nonlocal miss
 miss += 1
 return func(*args, **kwargs)

 def cache_clear():
 nonlocal miss
 miss = 0

 wrapper.cache_clear = cache_clear
 wrapper.cache_info = lambda: info(0, miss)
 return wrapper
```

### `def _unlocked(func, cache, key)`

Создаёт кэширующую обёртку для функции func, которая будет использовать кэш cache и ключ key для хранения результатов работы функции.

**Параметры:**

- `func` (`function`) — Функция, которую нужно обернуть в кэширующую обёртку
- `cache` (`cache`) — Кэш, в котором будет храниться результат работы функции
- `key` (`function`) — Ключ, по которому будет храниться результат работы функции в кэше

**Возвращаемое значение:**

- `function` — Кэширующая обёртка для функции func

**Примеры:**

Пример использования функции _unlocked

```python
def wrapper(*args, **kwargs): k = key(*args, **kwargs) try: return cache[k] except KeyError: pass # key not found v = func(*args, **kwargs) try: cache[k] = v except ValueError: pass # value too large return v wrapper.cache_clear = lambda: cache.clear() return wrapper
```

### `def _unlocked_info(func, cache, key, info)`

Создаёт обёртку для функции с кэшированием

**Параметры:**

- `func` (`function`) — Функция, которую нужно кэшировать
- `cache` (`cache`) — Кэш, используемый для хранения результатов
- `key` (`function`) — Функция для получения ключа кэша
- `info` (`function`) — Функция для получения информации о кэше

**Возвращаемое значение:**

- `wrapper` — N/A

**Примеры:**

Пример использования функции _unlocked_info

```python
def _unlocked_info(func, cache, key, info):
    hits = misses = 0

    def wrapper(*args, **kwargs):
        nonlocal hits, misses
        k = key(*args, **kwargs)
        try:
            result = cache[k]
            hits += 1
            return result
        except KeyError:
            misses += 1
        v = func(*args, **kwargs)
        try:
            cache[k] = v
        except ValueError:
            pass  # value too large
        return v

    def cache_clear():
        nonlocal hits, misses
        cache.clear()
        hits = misses = 0

    def cache_info():
        return info(hits, misses)

    wrapper.cache_clear = cache_clear
    wrapper.cache_info = cache_info
    return wrapper
```

Примеры использования различных кэширующих инструментов из модуля cachetools

```python
from cachetools import cached, LRUCache, TTLCache

# speed up calculating Fibonacci numbers with dynamic programming
@cached(cache={})
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

# cache least recently used Python Enhancement Proposals
@cached(cache=LRUCache(maxsize=32))
def get_pep(num):
    url = 'http://www.python.org/dev/peps/pep-%04d/' % num
    with urllib.request.urlopen(url) as s:
        return s.read()

# cache weather data for no longer than ten minutes
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_weather(place):
    return owm.weather_at_place(place).get_weather()
```

Пример вызова функции _unlocked_info

```python
def _unlocked_info(func, cache, key, info):
    # реализация функции _unlocked_info
```

### `def _wrapper(func, cache, key, lock = None, cond = None, info = None)`

Создаёт обёртку для функции с кэшированием, используя заданный кэш, ключ, блокировку и условия.

**Параметры:**

- `info` (`any`) — дополнительная информация для обёртки
- `lock` (`any`) — механизм блокировки для работы с кэшем
- `cond` (`any`) — условие для работы с кэшем
- `cache` (`any`) — кэш для хранения результатов работы функции
- `func` (`any`) — функция, для которой создаётся обёртка
- `key` (`any`) — ключ для доступа к кэшу

**Возвращаемое значение:**

- `function` — обёртка для функции с кэшированием

**Примеры:**

Пример вызова функции _wrapper с различными параметрами.

```python
from functools import functools
def _wrapper(func, cache, key, lock=None, cond=None, info=None):
    # implementation
    return functools.update_wrapper(wrapper, func)
```

**Смотрите также:**

def _condition(func, cache, key, lock, cond), def _condition_info(func, cache, key, lock, cond, info), def _locked(func, cache, key, lock), def _locked_info(func, cache, key, lock, info), def _uncached(func), def _uncached_info(func, info), def _unlocked(func, cache, key), def _unlocked_info(func, cache, key, info)


---

[← src](README.md) | [← К проекту](../README.md)
