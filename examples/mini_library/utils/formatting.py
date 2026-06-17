"""Formatting helpers."""

from __future__ import annotations


def format_price(amount: float, currency: str = "USD") -> str:
    """Format monetary amount with currency symbol."""
    return f"{currency} {amount:.2f}"


def format_items(*labels: str, separator: str = ", ") -> str:
    """Join variable number of item labels."""
    return separator.join(labels)
