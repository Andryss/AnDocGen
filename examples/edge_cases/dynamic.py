"""Edge cases for documentation generation testing."""

from typing import Any, Callable


def dynamic_dispatch(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Call arbitrary callable with dynamic arguments."""
    return fn(*args, **kwargs)


class MetaFactory(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        namespace["created_by"] = "MetaFactory"
        return super().__new__(mcs, name, bases, namespace)


class DynamicModel(metaclass=MetaFactory):
    def __init__(self, **data: Any) -> None:
        self.__dict__.update(data)
