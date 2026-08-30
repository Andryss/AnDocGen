from __future__ import annotations


def config_str(value: object, default: str = "") -> str:
    return str(value) if value not in (None, "") else default


def config_int(value: int | None, default: int) -> int:
    return value if value is not None else default


def config_bool(value: bool | None, default: bool) -> bool:
    return value if value is not None else default
