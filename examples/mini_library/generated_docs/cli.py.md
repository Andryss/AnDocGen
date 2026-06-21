# Модуль `cli.py`


Команда-строка для мини-библиотеки с базовыми операциями.

**Содержание:**

- [Функции](#функции)

## Функции

### `def build_parser() -> argparse.ArgumentParser`

Создает и настраивает объект `argparse.ArgumentParser` для командной строки.

**Возвращаемое значение:**

- `argparse.ArgumentParser` — настроенный парсер командной строки

**Примеры:**

```python
parser = build_parser()
args = parser.parse_args(["John Doe"])
print(args.customer)  # Output: John Doe
print(args.sku)       # Output: SKU-1
print(args.price)     # Output: 9.99
```

### `def main(args: list[str] | None = None) -> int`

Запускает демонстрационный поток заказов и выводит оцененную сумму.

**Параметры:**

- `args` (`list[str] | None`) — аргументы командной строки для парсера (по умолчанию `None`)

**Возвращаемое значение:**

- `int` — код завершения программы (всегда 0)

**Побочные эффекты:**

- Создает и обрабатывает заказ
- Выводит в консоль оцененную сумму заказа

**Примеры:**

```python
main(["--customer", "John Doe", "--sku", "SKU123", "--price", "10.99"])
```


---

[← Индекс](README.md)
