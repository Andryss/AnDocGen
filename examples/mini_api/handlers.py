"""HTTP-like API handlers (simplified example)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .storage import InMemoryStorage, normalize_email


@dataclass
class ApiResponse:
    status: int
    body: dict[str, Any]


class UserHandler:
    """Handles user-related API operations."""

    def __init__(self, storage: InMemoryStorage) -> None:
        self._storage = storage

    def get_user(self, user_id: int) -> ApiResponse:
        user = self._storage.get(user_id)
        if user is None:
            return ApiResponse(status=404, body={"error": "not found"})
        return ApiResponse(status=200, body=user)

    def create_user(self, name: str, email: str) -> ApiResponse:
        email = normalize_email(email)
        user_id = self._storage.create({"name": name, "email": email})
        return ApiResponse(status=201, body={"id": user_id})
