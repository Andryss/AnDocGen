"""Application settings."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    """Runtime configuration."""

    currency: str = "USD"
    tax_rate: float = 0.07
    debug: bool = False
