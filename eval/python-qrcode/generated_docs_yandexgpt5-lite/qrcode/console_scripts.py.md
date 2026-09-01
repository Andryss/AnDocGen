# Модуль `qrcode/console_scripts.py`


Модуль для работы с QR-кодами, включая конвертацию данных в QR-код через командную строку и функции для работы с изображениями QR-кодов.

**Содержание:**

- [Функции](#функции)

## Функции

### `def commas(items: Iterable[str], joiner = 'or') -> str`

Объединяет элементы итерируемого объекта items с помощью joiner и возвращает строку.

**Параметры:**

- `joiner` (`str`) — элемент, которым нужно объединить элементы списка
- `items` (`Iterable[str]`) — итерируемый объект, содержащий элементы для объединения

**Возвращаемое значение:**

- `str` — строка, содержащая объединённые элементы списка

**Примеры:**

Объединить элементы списка с помощью joiner 'or'.

```python
commas(['a', 'b', 'c'])
```

Объединить элементы списка с помощью joiner 'or', если список содержит более одного элемента.

```python
commas(['a', 'b'])
```

### `def get_factory(module: str) -> type[BaseImage]`

Возвращает фабрику изображений для указанного модуля.

**Параметры:**

- `module` (`str`) — строка, представляющая полный путь к модулю на Python

**Возвращаемое значение:**

- `type[BaseImage]` — возвращает объект типа type[BaseImage]

**Исключения:**

ValueError: The image factory is not a full python path

**Примеры:**

Получить фабрику изображений для модуля qrcode

```python
get_factory('qrcode')
```

### `def get_drawer_help() -> str`

Возвращает строку с информацией о доступных фабриках изображений и их алиасах.

**Возвращаемое значение:**

- `str` — строка с информацией о доступных фабриках изображений и их алиасах

**Примеры:**

Получить справку по доступным фабрикам изображений

```python
get_drawer_help()
```

**Смотрите также:**

def commas(items: Iterable[str], joiner = 'or') -> str; def get_factory(module: str) -> type[BaseImage]

### `def main(args = None)`

Функция main обрабатывает аргументы командной строки и создаёт QR-код.

**Параметры:**

- `args` (`list`) — Список аргументов для функции, по умолчанию равен sys.argv[1:]

**Примеры:**

Вызов функции main без аргументов

```python
qrcode.main()
```

Вызов функции main с аргументами из sys.argv

```python
qrcode.main(sys.argv[1:])
```

**Смотрите также:**

def commas(items: Iterable[str], joiner = 'or') -> str, def get_drawer_help() -> str, def get_factory(module: str) -> type[BaseImage]


---

[← qrcode](README.md) | [← К проекту](../README.md)
