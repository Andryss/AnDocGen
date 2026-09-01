# Модуль `src/cachetools/_cachedmethod.py`


Модуль содержит вспомогательные функции для декорирования методов с помощью кэширования и базовые классы для дескрипторов.

**Содержание:**

- [Классы](#классы)
- [Функции](#функции)

## Классы

### `class _DeprecatedDescriptorBase(_DescriptorBase)`

Класс _DeprecatedDescriptorBase является базовым классом дескриптора, который поддерживает устаревшее использование @classmethod.

**Назначение:**

Базовый класс дескриптора, поддерживающий устаревшее использование @classmethod.

**Наследование:**

- `_DescriptorBase`

#### Методы

##### `__init__(wrapper, cache_clear)`

Инициализирует объект _DeprecatedDescriptorBase с указанием унаследованного параметра deprecated=True и заданными wrapper и cache_clear.

**Параметры:**

- `wrapper` (`N/A`) — обозначает, что объект унаследован от другого класса с параметром deprecated=True
- `cache_clear` (`N/A`) — функция для очистки кэша

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Инициализация объекта _DeprecatedDescriptorBase

```python
super().__init__(deprecated=True)
self.__wrapper = wrapper
self.__cache_clear = cache_clear
```

##### `__call__(*args, **kwargs)`

Вызывает метод self.__wrapper с переданными аргументами и выводит предупреждение об устаревании использования @cachedmethod для декорирования методов класса.

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Возвращаемое значение:**

- `N/A` — Возвращает результат вызова метода self.__wrapper с переданными аргументами.

**Примеры:**

Вызывается метод __call__ с произвольными аргументами.

```python
def __call__(*args, **kwargs)
```

**Смотрите также:**

def _warn_classmethod(stacklevel) — Выводит предупреждение о том, что использование @cachedmethod для декорирования методов класса устарело

##### `cache_clear(objtype)`

Очищает кэш для указанного типа объекта.

**Параметры:**

- `objtype` (`N/A`) — Тип объекта, для которого нужно очистить кэш

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Вызов метода для очистки кэша с указанием типа объекта

```python
_DeprecatedDescriptorBase.cache_clear(objtype)
```

**Смотрите также:**

_warn_classmethod(stacklevel)

### `class _DescriptorBase`

Класс _DescriptorBase предназначен для использования в качестве базового класса для дескрипторов, реализующих основной протокол дескриптора.

**Назначение:**

Базовый класс дескриптора, реализующий основной протокол дескриптора.

**Использование:**

Инициализируйте объект _DescriptorBase с помощью метода __init__, установите имя атрибута для дескриптора с помощью метода __set_name__ и используйте метод __get__ для получения обёртки для объекта.

#### Методы

##### `__init__(deprecated = False)`

Инициализирует объект _DescriptorBase, устанавливая значения атрибутов __attrname и __deprecated

**Параметры:**

- `deprecated` (`bool`) — Указывает, является ли объект устаревшим

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример использования декоратора для ускорения вычисления чисел Фибоначчи

```python
from cachetools import cached, LRUCache, TTLCache
@cached(cache={})
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

Пример использования LRUCache для кэширования данных о Python Enhancement Proposals

```python
from cachetools import cached, LRUCache
@cached(cache=LRUCache(maxsize=32))
def get_pep(num):
    url = 'http://www.python.org/dev/peps/pep-%04d/' % num
    with urllib.request.urlopen(url) as s:
        return s.read()
```

Пример использования TTLCache для кэширования данных о погоде

```python
from cachetools import cached, TTLCache
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_weather(place):
    return owm.weather_at_place(place).get_weather()
```

##### `__set_name__(owner, name)`

Устанавливает имя атрибута для дескриптора в соответствии с именем атрибута владельца и проверяет на возможность присвоения одного и того же @cachedmethod двум разным именам.

**Параметры:**

- `owner` (`N/A`) — Устанавливает имя атрибута для дескриптора в соответствии с именем атрибута владельца
- `name` (`N/A`) — Имя атрибута, которое будет связано с дескриптором

**Исключения:**

TypeError: Cannot assign the same @cachedmethod to two different names (...).

**Примеры:**

Пример вызова метода __set_name__

```python
def __set_name__(owner, name)
```

##### `__get__(obj, objtype = None)`

Возвращает обёртку для объекта, заменяя дескриптор экземпляром обёртки в словаре экземпляра при необходимости.

**Параметры:**

- `obj` (`object`) — Объект, для которого вызывается метод
- `objtype` (`object`) — Тип объекта, для которого вызывается метод

**Возвращаемое значение:**

- `object` — Обёртка для объекта

**Исключения:**

TypeError

**Граничные случаи:**

Если объект не указан, возвращается сам обёртка без изменений. Если атрибут уже был заменён другим потоком, используется изначальная обёртка. Если объект не имеет атрибута __dict__, возникает ошибка AttributeError. Если атрибут __dict__ не поддерживает присваивание элементов, возникает ошибка TypeError.

**Примеры:**

Создание обёртки для объекта

```python
wrapper = self.Wrapper(obj)
```

Замена дескриптора экземпляром обёртки в словаре экземпляра

```python
obj.__dict__.setdefault(self.__attrname, wrapper)
```

**Смотрите также:**

_warn_instance_dict(msg, stacklevel)

### `class _WrapperBase`

Класс _WrapperBase является базовым и предоставляет стандартные реализации для свойств.

**Назначение:**

Базовый класс-обёртка, предоставляющий реализации по умолчанию для свойств.

**Использование:**

Инициализируйте объект _WrapperBase с помощью метода __init__ и используйте соответствующие методы для работы с кэшем.

#### Методы

##### `__call__(*args, **kwargs)`

Метод NotImplementedError, так как не реализована логика

**Параметры:**

- `*args` — —
- `**kwargs` — —

**Исключения:**

NotImplementedError

**Примеры:**

Вызов метода __call__

```python
raise NotImplementedError()  # pragma: no cover
```

##### `cache_clear()`

Метод cache_clear не реализован и вызывает NotImplementedError.

**Исключения:**

NotImplementedError

**Примеры:**

Вызов метода cache_clear

```python
raise NotImplementedError()
```

##### `cache()`

Возвращает результат вызова метода __cache с аргументом _obj.

**Возвращаемое значение:**

- `N/A` — Результат вызова метода __cache с аргументом _obj

**Примеры:**

Вызов метода cache

```python
return self.__cache(self._obj)
```

##### `cache_condition()`

Возвращает результат вызова метода __cond с аргументом _obj.

**Возвращаемое значение:**

- `N/A` — результат вызова метода __cond с аргументом _obj

**Примеры:**

Возвращает результат вызова метода __cond с аргументом _obj

```python
return self.__cond(self._obj)
```

##### `cache_key()`

Возвращает значение ключа кэша.

**Возвращаемое значение:**

- `N/A` — Значение ключа кэша.

**Примеры:**

Возвращает значение ключа кэша.

```python
return self.__key # self._obj passed via functools.partial
```

##### `cache_lock()`

Блокирует объект для синхронизации доступа к кэшу.

**Возвращаемое значение:**

- `N/A` — Возвращает результат блокировки объекта

**Примеры:**

Вызывается метод для блокировки объекта

```python
return self.__lock(self._obj)
```

##### `__init__(obj, method, cache, key, lock = None, cond = None)`

Инициализирует объект WrapperBase

**Параметры:**

- `lock` (`object`) — lock используется для блокировки кэша, если None, то блокировка не используется
- `cond` (`object`) — cond используется для условия, при котором обновляется кэш, если None, то условие не используется
- `method` (`object`) — метод, который будет декорирован
- `obj` (`object`) — объект, к которому применяется метод
- `cache` (`object`) — кэш для хранения результатов
- `key` (`object`) — функция для генерации ключа кэша

**Примеры:**

Инициализация объекта WrapperBase

```python
def __init__(obj, method, cache, key, lock = None, cond = None)
```

**Смотрите также:**

def _warn_classmethod(stacklevel)

## Функции

### `def _condition(method, cache, key, lock, cond)`

N/A

**Параметры:**

- `method` (`N/A`) — Используется в контексте метода для управления кешированием
- `cache` (`N/A`) — Объект кеша
- `key` (`N/A`) — Ключ для кеширования
- `lock` (`N/A`) — Блокировка для синхронизации доступа к кешу
- `cond` (`N/A`) — Условие для ожидания освобождения ключа

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример вызова функции _condition с необходимыми аргументами

```python
def _condition(method, cache, key, lock, cond): ...
```

### `def _condition_info(method, cache, key, lock, cond, info)`

N/A

**Параметры:**

- `method` (`N/A`) — метод, связанный с кешем
- `cache` (`N/A`) — кеш
- `key` (`N/A`) — ключ
- `lock` (`N/A`) — блокировка
- `cond` (`N/A`) — условие
- `info` (`N/A`) — информация о кеше

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

N/A

```N/A
N/A
```

### `def _locked(method, cache, key, lock)`

N/A

**Параметры:**

- `method` (`N/A`) — Метод, который будет обернут для кэширования
- `cache` (`N/A`) — Кэш для хранения значений
- `key` (`N/A`) — Ключ для доступа к кэшу
- `lock` (`N/A`) — Блокировка для синхронизации доступа к кэшу

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример вызова функции _locked с необходимыми аргументами

```python
def _locked(method, cache, key, lock): ...
```

### `def _none(_)`

Возвращает None.

**Параметры:**

- `_` (`N/A`) — N/A

**Возвращаемое значение:**

- `None` — None

**Примеры:**

Возвращает None

```python
return None
```

### `def _locked_info(method, cache, key, lock, info)`

N/A

**Параметры:**

- `method` (`N/A`) — метод, связанный с кэшем
- `cache` (`N/A`) — кэш
- `key` (`N/A`) — ключ
- `lock` (`N/A`) — блокировка
- `info` (`N/A`) — информация о кэше

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

N/A

```N/A
N/A
```

### `def _unlocked(method, cache, key)`

N/A

**Параметры:**

- `method` (`function`) — Функция, которая будет вызываться при доступе к свойству или методу
- `cache` (`object`) — Кэш, используемый для хранения результатов
- `key` (`function`) — Ключ, используемый для идентификации результата в кэше

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

Пример вызова функции _unlocked

```python
def _unlocked(method, cache, key):
    # body of the function
    pass
```

### `def _unlocked_info(method, cache, key, info)`

N/A

**Параметры:**

- `info` (`N/A`) — информация о кеше, попаданиях и промахах
- `key` (`N/A`) — ключ для кеширования
- `method` (`N/A`) — метод для кеширования
- `cache` (`N/A`) — объект кеша

**Возвращаемое значение:**

- `N/A` — N/A

**Примеры:**

N/A

```python
_unlocked_info(method, cache, key, info)
```

### `def _warn_classmethod(stacklevel)`

Выводит предупреждение о том, что использование @cachedmethod для декорирования методов класса устарело

**Параметры:**

- `stacklevel` (`int`) — Уровень стека, на котором выводится предупреждение

**Примеры:**

Вывести предупреждение о том, что использование @cachedmethod для декорирования методов класса устарело

```python
warnings.warn("decorating class methods with @cachedmethod is deprecated", DeprecationWarning, stacklevel=stacklevel)
```

### `def _warn_instance_dict(msg, stacklevel)`

Выводит предупреждение с использованием модуля warnings

**Параметры:**

- `msg` (`str`) — Сообщение для вывода предупреждения
- `stacklevel` (`int`) — Уровень стека для вывода предупреждения

**Побочные эффекты:**

Выводит предупреждение

**Примеры:**

Вывести предупреждение с указанием уровня стека

```python
warnings.warn(msg, DeprecationWarning, stacklevel=stacklevel)
```

### `def _wrapper(method, cache, key, lock = None, cond = None, info = None)`

Обертывает метод в кэшированный, используя заданный кэш, ключ и другие параметры для управления кэшированием.

**Параметры:**

- `method` (`function`) — Метод, который будет обернут в кэшированный
- `cache` (`N/A`) — Кэш, используемый для хранения результатов
- `key` (`N/A`) — Ключ, используемый для идентификации кэшированных результатов
- `lock` (`N/A`) — Блокировка для синхронизации доступа к кэшу
- `cond` (`N/A`) — Условие для кэширования результата
- `info` (`N/A`) — Дополнительная информация для кэширования

**Возвращаемое значение:**

- `function` — Обернутый метод с кэшированием

**Примеры:**

Пример вызова функции _wrapper с указанием всех параметров

```python
def _wrapper(method, cache, key, lock = None, cond = None, info = None)
```


---

[← src](README.md) | [← К проекту](../README.md)
