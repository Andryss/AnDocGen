"""Simple calculator module."""

from typing import Optional


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def divide(a: float, b: float) -> Optional[float]:
    if b == 0:
        return None
    return a / b


class Calculator:
    """Performs basic arithmetic operations."""

    def __init__(self, precision: int = 2) -> None:
        self.precision = precision

    def multiply(self, x: int, y: int) -> int:
        return x * y

    def format_result(self, value: float) -> str:
        return f"{value:.{self.precision}f}"
