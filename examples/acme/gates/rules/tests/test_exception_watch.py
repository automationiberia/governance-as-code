"""Tests for the exception watch (Evolution slot, ADR-0014).

Expired exceptions fail the instance CI (they must be removed or renewed through
the Librarian); exceptions expiring soon produce a warning. Dates are injected.
"""

from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = HERE.parents[1] / "checks"
sys.path.insert(0, str(CHECKS))
import exception_watch  # noqa: E402  pylint: disable=wrong-import-position

TODAY = datetime.date(2026, 11, 5)


def exc(id_: str, expires: datetime.date | None, approved_by: str | None = "security") -> dict:
    return {"id": id_, "rule": "R-X-001", "scope": {"repository": "r"}, "approved_by": approved_by, "expires": expires}


def test_valid_exception_is_ok() -> None:
    result = exception_watch.review([exc("EXC-1", datetime.date(2027, 3, 31))], TODAY, warn_days=30)
    assert result.expired == [] and result.expiring == [] and result.invalid == []


def test_expired_exception_is_reported() -> None:
    result = exception_watch.review([exc("EXC-1", datetime.date(2026, 11, 4))], TODAY, warn_days=30)
    assert result.expired == ["EXC-1"]


def test_expiring_today_is_still_valid_but_warned() -> None:
    result = exception_watch.review([exc("EXC-1", TODAY)], TODAY, warn_days=30)
    assert result.expired == [] and result.expiring == ["EXC-1"]


def test_expiring_within_window_is_warned() -> None:
    result = exception_watch.review([exc("EXC-1", datetime.date(2026, 12, 1))], TODAY, warn_days=30)
    assert result.expiring == ["EXC-1"]


def test_missing_expiry_or_approval_is_invalid() -> None:
    result = exception_watch.review(
        [exc("EXC-1", None), exc("EXC-2", datetime.date(2027, 1, 1), approved_by=None)], TODAY, warn_days=30
    )
    assert result.invalid == ["EXC-1", "EXC-2"]


def test_command_line_on_the_real_register_passes() -> None:
    """The acme register (EXC-001 until 2027-03-31) is healthy today."""
    proc = subprocess.run(
        [sys.executable, str(CHECKS / "exception_watch.py"), "--today", "2026-11-05"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_command_line_fails_when_an_exception_has_expired() -> None:
    proc = subprocess.run(
        [sys.executable, str(CHECKS / "exception_watch.py"), "--today", "2027-04-01"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "EXC-001" in proc.stdout
