"""In-memory order storage."""

from __future__ import annotations

from mini_library.exceptions import NotFoundError
from mini_library.models import Order


class InMemoryStorage:
    """Stores orders in a process-local dictionary."""

    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next_id = 1

    def create(self, customer: str) -> Order:
        order = Order(order_id=self._next_id, customer=customer)
        self._orders[self._next_id] = order
        self._next_id += 1
        return order

    def get(self, order_id: int) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            raise NotFoundError(f"Order {order_id} not found")
        return order

    def list_ids(self) -> list[int]:
        return sorted(self._orders.keys())
