"""ACME R-COLL-001 (ADR-0005): community.general is forbidden in production content.

Scope and exceptions are read from the instance (single source, GAC-0004):
- promotion path: manifest.yml `promotion_paths` (unclassified repositories are
  treated as prod — deny by default);
- exceptions: exceptions/register.yml (repository, items, expiry date).

The repository name is taken from the GAC_REPOSITORY environment variable (set
it in CI), or else the name of the directory ansible-lint runs from.
"""

from __future__ import annotations

import datetime
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml
from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable

RULE_ID = "R-COLL-001"
FORBIDDEN = "community.general"
INSTANCE_ROOT = Path(__file__).resolve().parents[2]
# In dependency files the collection name alone is a use; elsewhere only a
# fully qualified name (community.general.<plugin>) is.
DEPENDENCY_PATTERN = re.compile(r"\bcommunity\.general(\.[a-z0-9_]+)?\b")
FQCN_PATTERN = re.compile(r"\bcommunity\.general\.[a-z0-9_]+\b")
DEPENDENCY_FILES = {"requirements.yml", "requirements.yaml", "galaxy.yml", "galaxy.yaml",
                    "execution-environment.yml", "execution-environment.yaml"}
NAME_LINE = re.compile(r"^-?\s*name\s*:")


@lru_cache(maxsize=1)
def _load(relative: str) -> Any:
    path = INSTANCE_ROOT / relative
    if not path.is_file():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def repository_name() -> str:
    return os.environ.get("GAC_REPOSITORY") or Path.cwd().name


def applies_to(repo: str, manifest: dict | None = None) -> bool:
    """True when the repository is prod or unclassified (deny by default)."""
    manifest = _load("manifest.yml") if manifest is None else manifest
    paths = (manifest or {}).get("promotion_paths", {})
    nonprod = (paths.get("nonprod") or {}).get("repositories") or []
    prod = (paths.get("prod") or {}).get("repositories") or []
    if repo in prod:
        return True
    return repo not in nonprod


def is_excepted(
    repo: str,
    item: str,
    rel_path: str,
    today: datetime.date | None = None,
    register: list | None = None,
) -> str | None:
    """Return the exception id that covers this finding, if any and not expired."""
    today = today or datetime.date.today()
    register = _load("exceptions/register.yml") if register is None else register
    for exc in register or []:
        if exc.get("rule") != RULE_ID:
            continue
        scope = exc.get("scope") or {}
        if scope.get("repository") != repo:
            continue
        expires = exc.get("expires")
        if not isinstance(expires, datetime.date) or expires < today:
            continue
        if not exc.get("approved_by"):
            continue
        items = scope.get("items") or []
        paths = scope.get("paths") or []
        if items and item not in items:
            continue
        if paths and not any(Path(rel_path).match(p) for p in paths):
            continue
        return exc.get("id")
    return None


class CommunityGeneralForbiddenRule(AnsibleLintRule):
    """community.general must not be used in production content."""

    id = RULE_ID
    description = (
        "ACME ADR-0005: community.general (modules, plugins, filters, lookups, "
        "dependencies, execution environments) is forbidden in production "
        "content. Use ansible.builtin, ansible.posix or certified collections."
    )
    severity = "HIGH"
    tags = ["acme", "security", "dependencies"]
    version_changed = "0.1.0"

    def matchlines(self, file: Lintable) -> list[MatchError]:
        repo = repository_name()
        if not applies_to(repo):
            return []
        results: list[MatchError] = []
        rel_path = str(file.path)
        is_dependency_file = Path(rel_path).name in DEPENDENCY_FILES
        pattern = DEPENDENCY_PATTERN if is_dependency_file else FQCN_PATTERN
        for lineno, line in enumerate(str(file.content).splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue
            # Task and play names are prose: mentioning the collection is not using it.
            if not is_dependency_file and NAME_LINE.match(stripped):
                continue
            for match in pattern.finditer(line):
                item = match.group(0)
                if is_excepted(repo, item, rel_path):
                    continue
                results.append(
                    self.create_matcherror(
                        message=(
                            f"'{item}' is forbidden in production content "
                            f"(ACME ADR-0005, repository '{repo}'). "
                            "Use ansible.builtin, ansible.posix or certified collections, "
                            "or request an exception."
                        ),
                        lineno=lineno,
                        filename=file,
                    )
                )
        return results
