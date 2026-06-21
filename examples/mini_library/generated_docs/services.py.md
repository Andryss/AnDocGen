# Модуль `services.py`


Модуль `services.py`, содержащий бизнес-логику для управления заказами.

**Содержание:**

- [Классы](#классы)

## Классы

### `class OrderService`

Класс для управления заказами с использованием хранилища и настроек.

#### Методы

##### `__init__(storage: InMemoryStorage, settings: Settings | None = None) -> None`

Инициализирует экземпляр класса OrderService с указанным хранилищем и настройками.

**Параметры:**

- `storage` (`InMemoryStorage`) — объект хранилища
- `settings` (`Settings | None`) — настройки (по умолчанию `None`)

**Примеры:**

```python
storage = InMemoryStorage()
service = OrderService(storage, settings=Settings())
```

##### `add_item(order_id: int, item: Item) -> Order`

Добавляет товар в заказ и возвращает обновленный заказ.

**Параметры:**

- `order_id` (`int`) — ID заказа
- `item` (`Item`) — добавляемый товар

**Возвращаемое значение:**

- `Order` — обновленный заказ

**Исключения:**

- `ValidationError` — если количество товара меньше 1

**Примеры:**

```python
order_service = OrderService(storage)
updated_order = order_service.add_item(123, Item(name="Book", quantity=5))
```

##### `create_order(customer: str) -> Order`

Создает заказ для указанного клиента.

**Параметры:**

- `customer` (`str`) — имя клиента, для которого создается заказ

**Возвращаемое значение:**

- `Order` — созданный заказ

**Исключения:**

- `ValidationError` — если имя клиента пустое или состоит только из пробелов

**Примеры:**

```python
# Создание заказа для клиента с именем "John Doe"
order = OrderService.create_order("John Doe")
```

##### `summarize(order_id: int) -> dict[str, str | float]`

Сводит информацию об заказе по его идентификатору.

**Параметры:**

- `order_id` (`int`) — идентификатор заказа

**Возвращаемое значение:**

- `dict[str, str | float]` — словарь с информацией о заказе: имя клиента, количество предметов и подитоговая стоимость

**Примеры:**

```python
order_service = OrderService()
result = order_service.summarize(123)
print(result)  # {'customer': 'John Doe', 'items': 5, 'subtotal': 99.99}
```

##### `quote_total(order_id: int) -> str`

Вычисляет общий счет для заказа и возвращает его строковое представление.

**Параметры:**

- `order_id` (`int`) — уникальный идентификатор заказа

**Возвращаемое значение:**

- `str` — общий счет заказа, отформатированный с учетом валюты

**Примеры:**

```python
service = OrderService(storage=InMemoryStorage(), settings=Settings())
total = service.quote_total(123)
print(total)  # Пример вывода: $10.50
```

**Смотрите также:**

- `format_price` — Форматирует сумму денег с символом валюты.


---

[← Индекс](README.md)
