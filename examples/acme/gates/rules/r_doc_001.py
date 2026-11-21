"""ACME R-DOC-001 (ADR-0002): roles declare their interface in argument specs."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable


class RoleArgumentSpecsRule(AnsibleLintRule):
    """Roles must declare their entry point variables in meta/argument_specs.yml."""

    id = "R-DOC-001"
    description = (
        "ACME ADR-0002: every role declares its entry point variables in "
        "meta/argument_specs.yml (or argument_specs in meta/main.yml)."
    )
    severity = "HIGH"
    tags = ["acme", "documentation"]
    version_changed = "0.1.0"

    def matchdir(self, file: Lintable) -> list[MatchError]:
        # Evaluated on the role directory, not on tasks/main.yml: ansible-lint
        # skips every other rule on a file with a syntax error, which would hide
        # this one exactly on the roles that most need it.
        if file.kind != "role":
            return []
        role_dir = Path(str(file.path))
        # Only roles under roles/. Excludes, for example, ansible-test
        # integration targets (tests/integration/targets/<t>).
        if role_dir.parent.name != "roles":
            return []
        return self._check(role_dir, role_dir.name, file)

    def matchyaml(self, file: Lintable) -> list[MatchError]:
        # A role repository (a Galaxy role, a fork of one) has the role at its
        # root: ansible-lint sees no role directory, only meta/main.yml.
        path = Path(str(file.path))
        if path.name not in ("main.yml", "main.yaml") or path.parent.name != "meta":
            return []
        role_dir = path.parent.parent
        if role_dir.resolve() != Path.cwd().resolve() or not (role_dir / "tasks").is_dir():
            return []
        return self._check(role_dir, Path.cwd().name, file)

    def _check(self, role_dir: Path, name: str, file: Lintable) -> list[MatchError]:
        meta = role_dir / "meta"
        if (meta / "argument_specs.yml").is_file() or (meta / "argument_specs.yaml").is_file():
            return []
        for main in (meta / "main.yml", meta / "main.yaml"):
            if main.is_file() and "argument_specs:" in main.read_text(encoding="utf-8"):
                return []
        return [
            self.create_matcherror(
                message=f"Role '{name}' has no meta/argument_specs.yml (ACME ADR-0002).",
                filename=file,
                lineno=1,
            )
        ]
