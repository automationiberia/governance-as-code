#!/usr/bin/env python3
"""ACME exception watch — Evolution slot (ADR-0014).

Reviews the exception register:
- expired exceptions        -> exit 1 (remove or renew them through the Librarian)
- missing expiry/approval   -> exit 1 (invalid entries)
- expiring within N days    -> warning, exit 0

Run by the instance CI. Usage:
  exception_watch.py [--register PATH] [--today YYYY-MM-DD] [--warn-days N]
"""

from __future__ import annotations

import argparse
import datetime
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULT_REGISTER = Path(__file__).resolve().parents[2] / "exceptions" / "register.yml"


@dataclass
class Review:
    expired: list[str] = field(default_factory=list)
    expiring: list[str] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)


def review(register: list[dict], today: datetime.date, warn_days: int) -> Review:
    result = Review()
    for exc in register or []:
        exc_id = exc.get("id", "<no id>")
        expires = exc.get("expires")
        if not isinstance(expires, datetime.date) or not exc.get("approved_by"):
            result.invalid.append(exc_id)
            continue
        if expires < today:
            result.expired.append(exc_id)
        elif (expires - today).days <= warn_days:
            result.expiring.append(exc_id)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--today", type=datetime.date.fromisoformat, default=datetime.date.today())
    parser.add_argument("--warn-days", type=int, default=30)
    args = parser.parse_args()

    register = yaml.safe_load(args.register.read_text(encoding="utf-8")) or []
    result = review(register, args.today, args.warn_days)
    for exc_id in result.invalid:
        print(f"INVALID  {exc_id}: missing expiry date or approval")
    for exc_id in result.expired:
        print(f"EXPIRED  {exc_id}: remove it or renew it through the Librarian")
    for exc_id in result.expiring:
        print(f"WARNING  {exc_id}: expires within {args.warn_days} days")
    total = len(register)
    print(f"{total} exception(s) reviewed on {args.today}: "
          f"{len(result.expired)} expired, {len(result.invalid)} invalid, {len(result.expiring)} expiring soon")
    return 1 if result.expired or result.invalid else 0


if __name__ == "__main__":
    sys.exit(main())
