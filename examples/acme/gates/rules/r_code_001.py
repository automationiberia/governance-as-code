"""ACME R-CODE-001 (ADR-0001): role loop variables are named __<role>_*.

Inside roles/<name>/, ansible-lint's own loop-var-prefix enforces it (enabled in
gates/ansible-lint.yml). A role repository has the role at its root (a Galaxy
role, a fork of one): there is no role directory, so loop-var-prefix stays
silent. This rule covers that case only.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml
from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable
    from ansiblelint.utils import Task


def root_role_name(root: Path) -> str | None:
    """Role name of a repository whose root is a role, else None.

    galaxy_info.role_name if set; otherwise the repository name without the
    ansible-role- / ansible- prefix, with dashes as underscores (Galaxy's rule).
    """
    if not (root / "tasks").is_dir():
        return None
    meta = next((m for m in (root / "meta" / "main.yml", root / "meta" / "main.yaml") if m.is_file()), None)
    if meta is None:
        return None
    try:
        data = yaml.safe_load(meta.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        data = {}
    name = str((data.get("galaxy_info") or {}).get("role_name") or "")
    if not name:
        name = re.sub(r"^ansible-(role-)?", "", root.name)
    return name.split(".")[-1].replace("-", "_")


class RootRoleLoopVarPrefixRule(AnsibleLintRule):
    """Loop variables of a role at the repository root use the __<role>_ prefix."""

    id = "R-CODE-001"
    description = (
        "ACME ADR-0001: role loop variables are named __<role>_* "
        "(roles at the repository root; roles/<name>/ is covered by loop-var-prefix)."
    )
    severity = "MEDIUM"
    tags = ["acme", "idiom"]
    version_changed = "0.1.0"

    def matchtask(self, task: Task, file: Lintable | None = None) -> bool | str | list[MatchError]:
        if file is None:
            return False
        path = Path(str(file.path))
        if path.is_absolute():
            try:
                path = path.resolve().relative_to(Path.cwd().resolve())
            except ValueError:
                return False
        if not path.parts or path.parts[0] not in ("tasks", "handlers"):
            return False
        role = root_role_name(Path.cwd())
        if role is None:
            return False
        raw: dict[str, Any] = task.raw_task if hasattr(task, "raw_task") else dict(task)
        if "loop" not in raw and not any(str(key).startswith("with_") for key in raw):
            return False
        prefix = f"__{role}_"
        loop_var = (raw.get("loop_control") or {}).get("loop_var")
        if not loop_var:
            return f"Loop has no loop_control.loop_var; use the prefix '{prefix}' (ACME ADR-0001)."
        if not str(loop_var).startswith(prefix):
            return f"Loop variable '{loop_var}' does not start with '{prefix}' (ACME ADR-0001)."
        return False
