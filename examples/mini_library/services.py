"""Order business logic."""

from __future__ import annotations

from mini_library.config import Settings
from mini_library.exceptions import ValidationError
from mini_library.models import Item, Order
from mini_library.storage import InMemoryStorage
from mini_library.utils.formatting import format_price


class OrderService:
    """Coordinates order creation and pricing."""

    def __init__(self, storage: InMemoryStorage, settings: Settings | None = None) -> None:
        self._storage = storage
        self._settings = settings or Settings()

    def create_order(self, customer: str) -> Order:
        if not customer.strip():
            raise ValidationError("Customer name is required")
        return self._storage.create(customer.strip())

    def add_item(self, order_id: int, item: Item) -> Order:
        order = self._storage.get(order_id)
        if item.quantity < 1:
            raise ValidationError("Quantity must be positive")
        order.items.append(item)
        return order

    def quote_total(self, order_id: int) -> str:
        order = self._storage.get(order_id)
        subtotal = order.total()
        tax = subtotal * self._settings.tax_rate
        total = subtotal + tax
        return format_price(total, self._settings.currency)

    def summarize(self, order_id: int) -> dict[str, str | float]:
        order = self._storage.get(order_id)
        return {
            "customer": order.customer,
            "items": len(order.items),
            "subtotal": order.total(),
        }
