from __future__ import annotations

import sys

from andocgen.reporting.implementations.console_progress import (
    ConsoleProgressReporter,
    _format_progress_line,
)
from andocgen.reporting.implementations.null_progress import NullProgressReporter
from andocgen.reporting.progress_format import (
    compute_progress_eta,
    format_duration,
    format_duration_fixed,
)


def test_format_duration_seconds() -> None:
    assert format_duration(12.3) == "12s"


def test_format_duration_minutes() -> None:
    assert format_duration(90) == "1m 30s"


def test_format_duration_fixed_width() -> None:
    assert format_duration_fixed(5) == "    5s"
    assert format_duration_fixed(90) == "1m 30s"
    assert len(format_duration_fixed(5)) == len(format_duration_fixed(90))


def test_progress_line_fixed_columns() -> None:
    line_a = _format_progress_line(1, 40, "cli.py::build_parser", True, 6.0, 234)
    line_b = _format_progress_line(16, 40, "utils/formatting.py::format_items", True, 5.1, 122)
    assert len(line_a) == len(line_b)
    assert "workers=" not in line_a
    assert "ETA" in line_a
    assert "s/ent" in line_a


def test_eta_extrapolates_from_wall_clock() -> None:
    # 8 entities done in 40s wall-clock (parallel); each req ~15s individually.
    avg, eta = compute_progress_eta(elapsed_sec=40.0, current=8, total=16)
    assert avg == 5.0
    assert eta == 40.0
    per_request_avg = 15.0
    wrong_eta = per_request_avg * (16 - 8)
    assert eta < wrong_eta


def test_null_progress_is_silent(capsys) -> None:
    reporter = NullProgressReporter()
    reporter.on_stage("hidden")
    reporter.on_llm_progress(1, 10, "mod::fn", 100.0, True)
    assert capsys.readouterr().out == ""


def test_console_progress_non_tty(capsys) -> None:
    reporter = ConsoleProgressReporter()
    reporter.on_stage("Generating 5 entities...")
    reporter.on_llm_progress(1, 5, "a.py::foo", 500.0, True)
    out = capsys.readouterr().out
    assert "Generating 5 entities..." in out
    assert "[1/5]" in out
    assert "a.py::foo" in out
    assert "workers=" not in out


def test_console_progress_fail_clears_previous_line(monkeypatch, capsys) -> None:
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    reporter = ConsoleProgressReporter()
    reporter.on_llm_progress(1, 3, "a.py::ok", 100.0, True)
    reporter.on_llm_progress(2, 3, "b.py::fail", 100.0, False)
    out = capsys.readouterr().out
    assert out.count("FAIL") == 1
    assert not any("a.py::ok" in line and "b.py::fail" in line for line in out.splitlines())
    fail_lines = [line for line in out.splitlines() if "b.py::fail" in line]
    assert len(fail_lines) == 1
    assert "FAIL" in fail_lines[0]
