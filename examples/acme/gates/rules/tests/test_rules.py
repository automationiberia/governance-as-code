"""Tests for ACME organization lint rules.

Each rule has fixtures that must pass and fixtures that must fail. They come
from the examples in the rule's ADR and from bugs found in real content.

Black-box tests run ansible-lint exactly as the gates do (same configuration)
on minimal fixture repositories. Exception and expiry logic is unit-tested
with injected registers and dates, so no environment variable can point the
rule at a different register.

Run: pytest examples/acme/gates/rules/tests
"""

from __future__ import annotations

import datetime
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CONFIG = HERE.parents[1] / "ansible-lint.yml"
FIXTURES = HERE / "fixtures"

sys.path.insert(0, str(HERE.parent))
import r_coll_001  # noqa: E402  pylint: disable=wrong-import-position


def lint(case: str, repository: str) -> list[str]:
    """Run the checker on a copy of a fixture, as a Git repository like real
    content repositories; return its finding lines."""
    env = dict(os.environ, GAC_REPOSITORY=repository)
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / case
        shutil.copytree(FIXTURES / case, repo)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        proc = subprocess.run(
            [sys.executable, "-m", "ansiblelint", "-c", str(CONFIG), "--offline", "-f", "pep8", "--nocolor"],
            cwd=repo,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    return proc.stdout.splitlines()


def hits(lines: list[str], rule_id: str) -> list[str]:
    return [line for line in lines if f": {rule_id}:" in line]


# --------------------------------------------------------------------------
# R-DOC-001 (ADR-0002) — roles declare argument specs
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("case", "expected"),
    [
        ("doc_role_with_argument_specs", 0),
        ("doc_role_with_specs_in_meta_main", 0),
        ("doc_role_without_argument_specs", 1),
        # Regression (dogfooding): a syntax error in tasks/main.yml must not hide the rule.
        ("doc_role_with_broken_tasks", 1),
        # Regression: an ansible-test integration target is not a role (EX-02).
        ("doc_integration_target_is_not_a_role", 0),
    ],
)
def test_r_doc_001(case: str, expected: int) -> None:
    assert len(hits(lint(case, "lab_tools"), "R-DOC-001")) == expected


# --------------------------------------------------------------------------
# R-COLL-001 (ADR-0005) — no community.general in production
# --------------------------------------------------------------------------
PROD, NONPROD, UNCLASSIFIED = "linux_baseline", "lab_tools", "unregistered_repository"


@pytest.mark.parametrize(
    ("case", "repository", "expected"),
    [
        ("coll_module_in_role", PROD, 1),
        ("coll_filter_in_role", PROD, 1),
        ("coll_dependency_in_requirements", PROD, 1),
        ("coll_dependency_in_galaxy", PROD, 1),
        ("coll_ee_definition", PROD, 1),
        ("coll_comment_only", PROD, 0),
        # Regression: task names are prose; mentioning the collection is not using it.
        ("coll_name_mentions_only", PROD, 0),
        ("coll_module_in_role", NONPROD, 0),
        ("coll_module_in_role", UNCLASSIFIED, 1),  # deny by default
        # Real EXC-001 in the acme register (firewall_legacy, ufw + dependency)
        ("coll_exception_covers_items", "firewall_legacy", 0),
        ("coll_exception_item_outside", "firewall_legacy", 1),
        ("coll_exception_covers_items", "network_tuning", 2),  # exception is per repository
    ],
)
def test_r_coll_001(case: str, repository: str, expected: int) -> None:
    assert len(hits(lint(case, repository), "R-COLL-001")) == expected


TODAY = datetime.date(2026, 11, 5)


def exception(**overrides: object) -> dict:
    exc = {
        "id": "EXC-T",
        "rule": "R-COLL-001",
        "scope": {"repository": "repo_a", "paths": [], "items": ["community.general.ufw"]},
        "approved_by": "security",
        "expires": datetime.date(2027, 3, 31),
    }
    exc.update(overrides)
    return exc


@pytest.mark.parametrize(
    ("exc", "repository", "item", "path", "expected"),
    [
        (exception(), "repo_a", "community.general.ufw", "roles/x/tasks/main.yml", "EXC-T"),
        (exception(expires=TODAY), "repo_a", "community.general.ufw", "a.yml", "EXC-T"),  # last valid day
        (exception(expires=TODAY - datetime.timedelta(days=1)), "repo_a", "community.general.ufw", "a.yml", None),
        (exception(approved_by=None), "repo_a", "community.general.ufw", "a.yml", None),
        (exception(), "repo_b", "community.general.ufw", "a.yml", None),
        (exception(), "repo_a", "community.general.timezone", "a.yml", None),
        (exception(rule="R-OTHER-001"), "repo_a", "community.general.ufw", "a.yml", None),
        (
            exception(scope={"repository": "repo_a", "paths": ["playbooks/*.yml"], "items": []}),
            "repo_a",
            "community.general.ufw",
            "roles/x/tasks/main.yml",
            None,
        ),
        (
            exception(scope={"repository": "repo_a", "paths": ["playbooks/*.yml"], "items": []}),
            "repo_a",
            "community.general.ufw",
            "playbooks/fw.yml",
            "EXC-T",
        ),
    ],
)
def test_r_coll_001_exceptions(exc: dict, repository: str, item: str, path: str, expected: str | None) -> None:
    assert r_coll_001.is_excepted(repository, item, path, today=TODAY, register=[exc]) == expected


@pytest.mark.parametrize(
    ("repository", "expected"),
    [("prod_repo", True), ("lab_repo", False), ("never_classified", True)],
)
def test_r_coll_001_scope(repository: str, expected: bool) -> None:
    manifest = {
        "promotion_paths": {
            "prod": {"repositories": ["prod_repo"]},
            "nonprod": {"repositories": ["lab_repo"]},
        }
    }
    assert r_coll_001.applies_to(repository, manifest=manifest) is expected
