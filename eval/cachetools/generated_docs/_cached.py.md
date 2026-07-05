# Модуль `_cached.py`


Модуль с декораторами для работы с кэшем и условными операциями.

**Содержание:**

- [Функции](#функции)

## Функции

### `def _condition(func, cache, key, lock, cond)`

Функция `_condition` используется для кэширования результатов функции `func`, применяя условие на основе ключа, созданного с помощью функции `key`. Если значение уже находится в кэше или выполнение функции `func` невозможно из-за ошибки `ValueError`, функция вернётся без обновления кэша.

**Параметры:**

- `func` (`callable`) — функция, чьи результаты необходимо кэшировать.
- `cache` (`dict`) — словарь для хранения кэшированных значений.
- `key` (`callable`) — функция, возвращающая ключ для кэша на основе аргументов вызова.
- `lock` (`threading.Lock`) — объект блокировки для обеспечения безопасности доступа к кэшу и условной переменной.
- `cond` (`threading.Condition`) — условная переменная для управления блокировкой.

**Побочные эффекты:**

Функция изменяет содержимое словаря `cache` и уведомляет другие потоки об изменениях через объект `cond`.

**Примеры:**

```python
from threading import Lock, Condition

def cached_func(a, b):
    return a + b

key = lambda a, b: (a, b)
cache = {}
lock = Lock()
cond = Condition()

conditioned_func = _condition(cached_func, cache, key, lock, cond)

print(conditioned_func(1, 2))  # Вычисляет и кэширует
print(conditioned_func(1, 2))  # Возвращает из кэша

def error_func():
    raise ValueError("Too large")

error_key = lambda: "error"
error_cache = {}
error_lock = Lock()
error_cond = Condition()

conditioned_error_func = _condition(error_func, error_cache, error_key, error_lock, error_cond)

try:
    print(conditioned_error_func())
except ValueError as e:
    print(e)  # Выводит "Too large"
```

### `def _condition_info(func, cache, key, lock, cond, info)`

Функция `_condition_info` оборачивает другую функцию `func`, добавляя кэширование с условием и предоставлением информации о кэше.

**Параметры:**

- `func` (`Callable`) — исходная функция, которую нужно обернуть.
- `cache` (`Mapping`) — словарь для хранения результатов выполнения функции.
- `key` (`Callable`) — функция, которая генерирует ключ для кэша на основе аргументов.
- `lock` (`Lock`) — объект блокировки для обеспечения потокобезопасности при доступе к кэшу и переменным состояния.
- `cond` (`Condition`) — условие для синхронизации потоков, когда ключ уже в процессе обработки.
- `info` (`Callable`) — функция, которая возвращает информацию о кэше.

**Побочные эффекты:**

Функция изменяет состояние `cache`, `hits` и `misses`. Также блокирует доступ к этим ресурсам через объекты `lock` и `cond`.

**Примеры:**

```python
from threading import Lock, Condition

def my_func(x):
    return x * x

cache = {}
key = lambda x: x
lock = Lock()
cond = Condition(lock)
info = lambda hits, misses: f"Hits: {hits}, Misses: {misses}"

wrapper = _condition_info(my_func, cache, key, lock, cond, info)

print(wrapper(5))  # 25 (miss)
print(wrapper(5))  # 25 (hit)
```

### `def _locked(func, cache, key, lock)`

Функция `_locked` используется для создания оболочки, которая обеспечивает синхронизацию доступа к кэшу с использованием блокировки.

**Параметры:**

- `func` (`callable`) — функция, чьи результаты будут закэшированы
- `cache` (`dict`) — словарь для хранения результирующих значений
- `key` (`callable`) — функция для генерации ключей кэша
- `lock` (`threading.Lock`) — блокировка для обеспечения синхронизации

**Побочные эффекты:**

Изменяет объекты `cache` и `lock`.

**Примеры:**

```python
def compute_expensive_operation(a, b):
    # Эмулирует затратную операцию
    import time
    time.sleep(1)
    return a + b

@_locked(compute_expensive_operation, {}, lambda a, b: f"{a}_{b}", threading.Lock())
def get_cached_result(a, b):
    return compute_expensive_operation(a, b)

result = get_cached_result(3, 4)  # Выполнится операция
result = get_cached_result(3, 4)  # Будет взято из кэша
```

### `def _locked_info(func, cache, key, lock, info)`

Функция `_locked_info` оборачивает другую функцию `func`, чтобы обеспечить безопасный доступ к кэшированному результату с использованием блокировки.

**Параметры:**

- `func` (`callable`) — функция, результат которой будет кэшироваться
- `cache` (`dict`) — словарь для хранения кэшированных значений
- `key` (`Callable[[*args, **kwargs], Any]`) — функция, возвращающая ключ для кэша на основе аргументов
- `lock` (`Lock`) — объект блокировки, обеспечивающий потокобезопасность при доступе к кэшу и информации о кэше
- `info` — —

**Побочные эффекты:**

- Изменяет значение переменных `hits` и `misses`, отслеживающих количество обращений в кэш
- Обновляет или удаляет значения в словаре `cache`

**Примеры:**

```python
from threading import Lock
from functools import lru_cache

def my_func(x, y):
    return x + y

cache = {}
key = lambda x, y: (x, y)
lock = Lock()
info = lambda hits, misses: f"Hits: {hits}, Misses: {misses}"

locked_info = _locked_info(my_func, cache, key, lock, info)

# Использование обернутой функции
result = locked_info(3, 4)  # Hits: 1, Misses: 0
result = locked_info(3, 4)  # Hits: 2, Misses: 0
```

### `def _uncached(func)`

Функция `_uncached` создает обертку для другой функции `func`, которая не кэшируется.

**Параметры:**

- `func` (`callable`) — оборачиваемая функция

**Возвращаемое значение:**

- `wrapper` — обертка, которая выполняет вызов `func` без кэширования и имеет метод `cache_clear`, который ничего не делает

**Примеры:**

```python
def add(a, b):
    return a + b

uncached_add = _uncached(add)
print(uncached_add(1, 2))  # Вывод: 3
```

### `def _uncached_info(func, info)`

Функция `_uncached_info` оборачивает другую функцию и добавляет к ней информацию о количестве промахов в кэше.

**Параметры:**

- `func` (`function`) — функция, которую нужно обернуть
- `info` (`function`) — функция, которая возвращает информацию о кэше

**Возвращаемое значение:**

- `function` — новая функция с добавленной информацией о количестве промахов и методами для очистки кэша и получения информации

**Побочные эффекты:**

Функция изменяет значение переменной `misses`, отслеживающей количество промахов в кэше.

**Примеры:**

```python
def my_function():
    return 42

info = lambda hits, misses: (hits, misses)
uncached_func = _uncached_info(my_function, info)

print(uncached_func())  # Выводит (0, 1)
print(uncached_func.cache_info())  # Выводит (0, 1)
uncached_func.cache_clear()
print(uncached_func.cache_info())  # Выводит (0, 0)
```

### `def _unlocked(func, cache, key)`

Функция-обертка, которая добавляет кэширование к другой функции.

**Параметры:**

- `func` (`callable`) — целевая функция для которой нужно добавить кэширование.
- `cache` (`dict`) — словарь, используемый для хранения результатов вызова функции.
- `key` (`callable`) — функция, генерирующая ключ для кэша на основе аргументов функции.

**Возвращаемое значение:**

- `callable` — возвращает обертку вокруг целевой функции с добавленным кэшированием.

**Примеры:**

```python
def my_function(x, y):
    return x + y

cache = {}
my_cached_function = _unlocked(my_function, cache, lambda x, y: (x, y))
print(my_cached_function(1, 2))  # Вычисляется и кэшируется результат
print(my_cached_function(1, 2))  # Используется кэшированный результат
```

### `def _unlocked_info(func, cache, key, info)`

Функция `_unlocked_info` оборачивает другую функцию `func`, добавляя кэширование с подсчетом количества попаданий и промахов.

**Параметры:**

- `func` (`callable`) — оборачиваемая функция
- `cache` (`dict`) — словарь для хранения результата вызова `func`
- `key` (`callable`) — функция, которая генерирует ключ для кэша
- `info` (`callable`) — функция, возвращающая информацию о кэше (количество попаданий и промахов)

**Возвращаемое значение:**

- `callable` — обертка вокруг `func`, добавляющая кэширование и подсчеты

**Побочные эффекты:**

Функция не имеет побочных эффектов.

**Примеры:**

```python
def my_func(x):
    return x * 2

cache = {}
key = lambda x: x
info = lambda h, m: f"Hits: {h}, Misses: {m}"

wrapper = _unlocked_info(my_func, cache, key, info)

print(wrapper(1))  # Промах, вычисление и кэширование
print(wrapper(1))  # Попадание, возврат из кэша
print(wrapper.cache_info())  # Выводит "Hits: 1, Misses: 1"
```

### `def _wrapper(func, cache, key, lock = None, cond = None, info = None)`

Функция `_wrapper` используется для создания оболочки вокруг другой функции `func`, которая выполняет различные типы кэширования в зависимости от параметров.

**Параметры:**

- `func` (`function`) — оборачиваемая функция.
- `cache` (`dict`) — словарь, используемый для хранения результатов вызова `func`.
- `key` (`callable`) — функция, которая генерирует ключ для кэша на основе аргументов и ключевых слов.
- `lock` (`threading.Lock, optional`) — блокировка, используется для синхронизации доступа к кэшу.
- `cond` (`threading.Condition, optional`) — условие, используется для управления доступом к кэшу в многопоточной среде.
- `info` (`bool, optional`) — флаг, определяющий, следует ли добавлять информацию о состоянии кэша.

**Возвращаемое значение:**

- `function` — оболочка вокруг `func` с примененным кэшированием.

**Примеры:**

```python
# Пример использования без параметра info
@_wrapper(func=my_function, cache={})
def my_cached_function(*args, **kwargs):
    pass

# Пример использования с параметром info
@_wrapper(func=my_function, cache={}, key=make_key, lock=lock, cond=condition, info=True)
def my_cached_function_with_info(*args, **kwargs):
    pass
```

**Смотрите также:**

- `_condition`
- `_condition_info`
- `_locked`
- `_locked_info`
- `_uncached`
- `_uncached_info`
- `_unlocked`
- `_unlocked_info`


---

[← Индекс](README.md)
