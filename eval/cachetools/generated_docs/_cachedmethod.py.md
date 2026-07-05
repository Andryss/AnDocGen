# Модуль `_cachedmethod.py`


Модуль с инструментами для создания и управления кэшированными методами.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class _DeprecatedDescriptorBase(_DescriptorBase)`

Класс базового дескриптора, поддерживающий устаревшее использование декоратора `@classmethod`.

**Наследование:**

- `_DescriptorBase`

#### Методы

##### `__init__(wrapper, cache_clear)`

Инициализирует экземпляр `_DeprecatedDescriptorBase`.

**Параметры:**

- `wrapper` — —
- `cache_clear` — —

##### `__call__(*args, **kwargs)`

Вызывает обертку, предупреждая о устаревшем использовании декоратора `@cachedmethod`.

**Параметры:**

- `*args` — позиционные аргументы, передаваемые wrapped method
- `**kwargs` — именованные аргументы, передаваемые wrapped method

**Примеры:**

```python
# Пример использования недоступен, так как метод является устаревшим.
```

**Смотрите также:**

- `_warn_classmethod` — Предупреждает о устаревшем использовании декоратора `@cachedmethod`.

##### `cache_clear(objtype)`

Удаляет все закэшированные значения для указанного типа объекта.

**Параметры:**

- `objtype` — —

**Возвращаемое значение:**

`None`

**Побочные эффекты:**

Изменяет состояние объекта, удаляя все закэшированные значения.

**Примеры:**

```python
class MyClass:
    @cachedmethod
    def my_method(self):
        return some_expensive_operation()

# Создаем экземпляр класса и вызываем метод
obj = MyClass()
obj.my_method()  # Значение закэшируется

# Очищаем кэш для типа объекта
MyClass.cache_clear(obj)
```

**Смотрите также:**

- `@cachedmethod`

### `class _DescriptorBase`

Базовый класс дескриптора, реализующий базовый протокол дескрипторов.

N/A

#### Методы

##### `__init__(deprecated = False)`

Инициализирует экземпляр `_DescriptorBase`.

**Параметры:**

- `deprecated` (`bool`) — устаревший параметр

##### `__set_name__(owner, name)`

Устанавливает имя для декорированного метода и проверяет, чтобы не могло быть присвоено одно и то же упакованное методо двум различным именам.

**Параметры:**

- `owner` (`type`) — тип класса, содержащего декорированный метод
- `name` (`str`) — имя атрибута, которому будет присвоен декорированный метод

**Исключения:**

- `TypeError` — если одно и то же упакованное методо пытается быть присвоено двум различным именам

**Примеры:**

```python
class MyClass:
    @cachedmethod
    def my_method(self):
        pass
```

##### `__get__(obj, objtype = None)`

Возвращает обертку для объекта, которая кэширует значение свойства.

**Параметры:**

- `obj` (`object`) — объект, на который применяется дескриптор
- `objtype` (`type, optional`) — тип объекта (по умолчанию `None`)

**Возвращаемое значение:**

- `_CachedMethodWrapper` — обертка для объекта с кэшированным свойством

**Исключения:**

- `TypeError` — если не удалось установить слот для кэширования свойства или если дескриптор вызывается без предварительного вызова `__set_name__`

**Граничные случаи:**

- Если `obj` равно `None`, возвращает саму обертку без изменений, чтобы поддерживать интроспекцию на уровне класса
- Если объект не имеет словаря атрибутов (`__dict__`) или его словарь не поддерживает присваивание элементов, выбрасывается ошибка

**Примеры:**

```python
class MyClass:
    @cachedmethod
    def my_property(self):
        return some_expensive_operation()

obj = MyClass()
result = obj.my_property  # Обертка кэширует результат my_property
```

**Смотрите также:**

- `_warn_instance_dict` — Функция для выдачи предупреждений

### `class _WrapperBase`

Базовый класс для обёрток, предоставляющий стандартные реализации для свойств.

#### Методы

##### `cache()`

Вызывает закэшированный метод объекта.

**Возвращаемое значение:**

- `any` — результат вызова закэшированного метода

##### `__call__(*args, **kwargs)`

N/A

**Параметры:**

- `*args` — —
- `**kwargs` — —

##### `cache_condition()`

Выполняет условие кэширования, возвращая результат его выполнения.

**Возвращаемое значение:**

- `bool` — результат выполнения условия кэширования

**Примеры:**

```python
class MyClass:
    def __init__(self, cond):
        self._obj = self
        self.__cond = weakref(ref(cond))

def my_condition():
    return True

wrapper = _WrapperBase(my_condition)
result = wrapper.cache_condition()  # Возвращает True
```

##### `cache_clear()`

Не реализован метод очистки кэша.

##### `cache_key()`

Возвращает ключ для кэширования.

**Возвращаемое значение:**

- `str` — ключ для кэширования

**Примеры:**

```python
class MyClass:
    def __init__(self, key):
        self._key = key

    cache_key = _WrapperBase.cache_key.__get__(MyClass())

# Использование
obj = MyClass('example_key')
print(obj.cache_key())  # Выведет: example_key
```

##### `cache_lock()`

Возвращает блокировку для кэширования.

**Возвращаемое значение:**

- `function` — функция-блокировка

**Примеры:**

```python
lock = _WrapperBase.cache_lock()
```

##### `__init__(obj, method, cache, key, lock = None, cond = None)`

Инициализирует экземпляр `_WrapperBase`, сохраняя ссылку на объект, метод и дополнительные параметры.

**Параметры:**

- `obj` (`object`) — объект, к которому применяется метод
- `method` (`callable`) — метод, который будет закэширован
- `cache` (`Mapping`) — словарь для хранения результатов вызова метода
- `key` (`Callable`) — функция, генерирующая ключ для кеша
- `lock` (`Lock, optional`) — объект блокировки для синхронизации доступа
- `cond` (`Condition, optional`) — объект условия для синхронизации доступа

**Побочные эффекты:**

Устанавливает атрибуты `_obj`, `__cache`, `__key`, `__lock` и `__cond`.

**Примеры:**

```python
# Пример использования не предоставлен
```

**Смотрите также:**

- `_warn_classmethod` — Предупреждает о устаревшем использовании декоратора `@cachedmethod` для классовых методов.

## Функции

### `def _condition(method, cache, key, lock, cond)`

Функция `_condition` создает декоратор для кэширования методов с условием. Декоратор проверяет наличие ключа в словаре `pending`, ожидает выполнения условия и кэширует результат при необходимости.

**Параметры:**

- `method` (`callable`) — метод, который нужно обернуть
- `cache` (`callable`) — функция для создания или получения кэша
- `key` (`callable`) — функция для генерации ключа кэша
- `lock` (`callable`) — функция для создания или получения блокировки
- `cond` (`callable`) — функция для создания или получения условного объекта

**Побочные эффекты:**

Функция изменяет состояние глобального словаря `pending`, удаляя и добавляя ключи. Также блокирует и разблокирует объекты с использованием функций `lock` и `cond`.

**Примеры:**

```python
from threading import Lock, Condition

def my_method(self, arg):
    return arg * 2

cache = lambda self: {}
key = lambda self, arg: arg
lock = lambda self: Lock()
cond = lambda self: Condition()

conditioned_method = _condition(my_method, cache, key, lock, cond)

class MyClass:
    my_method = conditioned_method(MyClass.my_method)

obj = MyClass()
print(obj.my_method(3))  # Вывод: 6
```

### `def _condition_info(method, cache, key, lock, cond, info)`

Создает и возвращает дескриптор, который управляет кэшированием методов с условием.

**Параметры:**

- `method` — —
- `cache` — —
- `key` — —
- `lock` — —
- `cond` — —
- `info` — —

**Возвращаемое значение:**

- `_DescriptorBase.Wrapper` — обработчик для метода с условием

**Примеры:**

```python
descriptor = _condition_info(some_method, cache, key, lock, cond, info)
```

### `def _locked(method, cache, key, lock)`

Метод-декоратор для кэширования методов с блокировкой.

**Параметры:**

- `method` — —
- `cache` — —
- `key` — —
- `lock` — —

**Возвращаемое значение:**

- `Descriptor` — объект-дескриптор, который можно использовать для декорирования методов

**Примеры:**

```python
@_locked(cache=my_cache, key=key_func, lock=lock_obj)
def my_method(self, *args, **kwargs):
    # Мой метод с кэшированием и блокировкой
```

### `def _locked_info(method, cache, key, lock, info)`

Создает и возвращает дескриптор для закрытой информации с использованием метода.

**Параметры:**

- `method` (`callable`) — метод, для которого создается дескриптор
- `cache` (`Mapping`) — словарь для кэширования результатов метода
- `key` (`Callable`) — функция для создания ключей в кэше
- `lock` (`Lock`) — объект блокировки для обеспечения безопасности многопоточного доступа
- `info` (`Callable`) — функция для получения информации о кэшировании

**Возвращаемое значение:**

- `Descriptor` — созданный дескриптор

**Примеры:**

```python
# Пример использования _locked_info
class MyClass:
    @classmethod
    def my_method(cls, a, b):
        return a + b

cache = {}
lock = threading.Lock()
info_func = lambda cache, hits, misses: (hits, misses)
locked_info = _locked_info(MyClass.my_method, cache, lambda self, a, b: f"{a}_{b}", lock, info_func)

my_class_instance = MyClass()
result = locked_info(my_class_instance, 10, 20)  # result = 30
info = locked_info.cache_info()  # info = (1, 0)
```

### `def _unlocked(method, cache, key)`

Функция `_unlocked` используется для создания декоратора, который оборачивает метод в кэширование. Она проверяет наличие ключа в кэше и, если он отсутствует, вычисляет значение метода, сохраняет его в кэше и возвращает.

**Параметры:**

- `method` (`callable`) — метод, который нужно обернуть в кэширование
- `cache` (`callable`) — функция, создающая или возвращающая кэш
- `key` (`callable`) — функция, генерирующая ключ для кэша

**Побочные эффекты:**

Нет явных побочных эффектов.

**Примеры:**

```python
class Example:
    def __init__(self):
        self._cache = {}

    @staticmethod
    def cache(obj):
        return obj._cache

    @staticmethod
    def key(obj, *args, **kwargs):
        return args

    @_unlocked(method='some_method', cache=cache, key=key)
    def some_method(self, a, b):
        return a + b

example = Example()
result = example.some_method(1, 2)  # Результат будет вычислен и сохранен в кэше
```

### `def _unlocked_info(method, cache, key, info)`

Функция `_unlocked_info` возвращает экземпляр дескриптора `Descriptor`, который оборачивает метод и управляет кэшированием вызовов.

**Параметры:**

- `method` — —
- `cache` — —
- `key` — —
- `info` — —

**Возвращаемое значение:**

- `Descriptor` — экземпляр дескриптора, оборачивающего метод и обрабатывающий кэширование вызовов

**Примеры:**

```python
# Пример использования не требуется, так как функция возвращает объект дескриптора
```

### `def _warn_classmethod(stacklevel)`

Предупреждает о устаревшем использовании декоратора `@cachedmethod` для классовых методов.

**Параметры:**

- `stacklevel` (`int`) — уровень стека, откуда будет вызываться предупреждение

**Примеры:**

```python
class MyClass:
    @staticmethod
    def my_method():
        pass

# Usage of _warn_classmethod will issue a deprecation warning when called
_warn_classmethod(stacklevel=2)
```

### `def _none(_)`

Возвращает `None`.

**Параметры:**

- `_` — —

**Возвращаемое значение:**

- `None` — всегда возвращает `None`

**Примеры:**

```python
result = _none()
print(result)  # Выведет: None
```

### `def _warn_instance_dict(msg, stacklevel)`

Выдает предупреждение с сообщением и уровнем стека.

**Параметры:**

- `msg` (`str`) — сообщение предупреждения
- `stacklevel` (`int`) — уровень стека для предупреждения

**Примеры:**

```python
_warn_instance_dict("This method is deprecated", 2)
```

### `def _wrapper(method, cache, key, lock = None, cond = None, info = None)`

Создает декоратор для кэширования методов с учетом условий, блокировок и информации.

**Параметры:**

- `method` (`function`) — метод для кэширования
- `cache` (`dict`) — словарь для хранения результата кэширования
- `key` (`str`) — ключ для доступа к кэшу
- `lock` (`Lock`) — блокировка для синхронизации многопоточного доступа (если используется)
- `cond` (`Condition`) — условие ожидания для блокировки (если используется)
- `info` (`any, опционально`) — дополнительная информация для кэширования

**Возвращаемое значение:**

- `function` — декоратор, который управляет кэшированием метода

**Примеры:**

```python
def example_method(self):
    return "result"

cache = {}
key = "example_key"
lock = threading.Lock()
condition = threading.Condition()

wrapped_method = _wrapper(example_method, cache, key, lock, condition)
result = wrapped_method(None)  # Результат будет кэширован
```

**Смотрите также:**

- `def _condition(method, cache, key, lock, cond)`
- `def _condition_info(method, cache, key, lock, cond, info)`
- `def _locked(method, cache, key, lock)`
- `def _locked_info(method, cache, key, lock, info)`
- `def _unlocked(method, cache, key)`
- `def _unlocked_info(method, cache, key, info)`


---

[← Индекс](README.md)
