"""HTTP-like handlers for fixture tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from storage import InMemoryStorage, normalize_email


@dataclass
class ApiResponse:
    status: int
    body: dict[str, Any]


class UserHandler:
    """Handles user-related API operations."""

    def __init__(self, storage: InMemoryStorage) -> None:
        self._storage = storage

    def create_user(self, name: str, email: str) -> ApiResponse:
        email = normalize_email(email)
        user_id = self._storage.create({"name": name, "email": email})
        return ApiResponse(status=201, body={"id": user_id})
