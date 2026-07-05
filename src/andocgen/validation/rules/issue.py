from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleIssue:
    code: str
    message: str
