"""In-memory key-value storage."""

from __future__ import annotations

from typing import Any


def normalize_email(email: str) -> str:
    """Normalize email for storage."""
    return email.strip().lower()


class InMemoryStorage:
    """Simple in-memory storage for demo purposes."""

    def __init__(self) -> None:
        self._data: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def get(self, item_id: int) -> dict[str, Any] | None:
        return self._data.get(item_id)

    def create(self, payload: dict[str, Any]) -> int:
        item_id = self._next_id
        self._next_id += 1
        self._data[item_id] = payload
        return item_id
