"""Data models for orders and items."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Item:
    """Single line item in an order."""

    sku: str
    title: str
    price: float
    quantity: int = 1


@dataclass
class Order:
    """Customer order aggregate."""

    order_id: int
    customer: str
    items: list[Item] = field(default_factory=list)

    def total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)
