"""Business logic for fixture library."""

from models import Item


class OrderService:
    """Coordinates order creation."""

    def create_order(self, customer: str) -> str:
        return customer.strip()

    def add_item(self, order_id: int, item: Item) -> int:
        return order_id + item.quantity
