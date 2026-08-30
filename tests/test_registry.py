from __future__ import annotations

import pytest

from andocgen.registry import create_registered


class Demo:
    pass


def test_create_registered_instantiates_matching_entry() -> None:
    assert isinstance(create_registered({"demo": Demo}, "demo", "component"), Demo)


def test_create_registered_rejects_unknown_entry() -> None:
    with pytest.raises(ValueError, match="Unknown component implementation: missing"):
        create_registered({"demo": Demo}, "missing", "component")
