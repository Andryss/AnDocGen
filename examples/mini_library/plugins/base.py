"""Plugin base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PluginBase(ABC):
    """Base class for export plugins."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.options = kwargs

    @abstractmethod
    def export(self, data: dict[str, Any]) -> str:
        """Serialize data to a string representation."""
