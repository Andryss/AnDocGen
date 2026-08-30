from __future__ import annotations

from andocgen.config_values import config_bool, config_int, config_str


def test_config_value_helpers_preserve_explicit_values() -> None:
    assert config_str("ru", "en") == "ru"
    assert config_int(3, 1) == 3
    assert config_bool(False, True) is False


def test_config_value_helpers_apply_defaults_for_missing_values() -> None:
    assert config_str(None, "ru") == "ru"
    assert config_str("", "ru") == "ru"
    assert config_int(None, 1) == 1
    assert config_bool(None, True) is True
