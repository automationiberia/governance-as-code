# Templates

Templates live **inside the skills that use them**, so they travel with the
skill when Lola installs it. An instance may override any of them under
`<instance>/templates/`.

| Template | Artifact | Used by |
|----------|----------|---------|
| [adr.md](../starter-kit/gac-modes/module/skills/gac-librarian/templates/adr.md) | Organization (or domain) ADR | Librarian |
| [rule.yml](../starter-kit/gac-modes/module/skills/gac-librarian/templates/rule.yml) | Rule registry entry | Librarian |
| [exception.yml](../starter-kit/gac-modes/module/skills/gac-librarian/templates/exception.yml) | Exception register entry | Librarian |
| [instance-manifest.yml](../starter-kit/gac-modes/module/skills/gac-librarian/templates/instance-manifest.yml) | Bases, layers, slot adoptions, checker | Librarian |
| [audit-report.md](../starter-kit/gac-modes/module/skills/gac-auditor/templates/audit-report.md) | Auditor output | Auditor |
| [success-contract.md](../starter-kit/gac-modes/module/skills/gac-builder/templates/success-contract.md) | What counts as success, approved before building | Builder |
| [pr-body.md](../starter-kit/gac-modes/module/skills/gac-builder/templates/pr-body.md) | Pull request description with governance section | Builder |

Identifiers:

| Artifact | Format | Example |
|----------|--------|---------|
| Method ADR | `GAC-NNNN` | `GAC-0004` |
| Organization ADR | `ADR-NNNN` | `ADR-0012` |
| Rule | `R-<AREA>-NNN` | `R-COLL-001` |
| Exception | `EXC-NNN` | `EXC-031` |
