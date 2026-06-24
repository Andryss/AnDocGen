"""Domain models for fixture library."""


class Item:
    """Order line item."""

    def __init__(self, name: str, quantity: int = 1) -> None:
        self.name = name
        self.quantity = quantity
