# gac-modes

Lola module with the Governance as Code modes.

| Skill | Mode |
|-------|------|
| `gac-governance` | Shared: resolves effective governance for a task |
| `gac-auditor` | Auditor (`/audit`) |
| `gac-builder` | Builder (`/build`) |
| `gac-librarian` | Librarian (`/librarian`) |
| `gac-operator` | Operator (`/operate`) |

## Install

Use the one-time setup ([../SETUP.md](../SETUP.md)): it installs this module
together with the community modules pinned by the governance instance, in your
assistant's format. Then add the pointer
([../AGENTS.pointer.md](../AGENTS.pointer.md)) to the repository's `AGENTS.md`.

Manual install of this module only:

```bash
lola mod add <method-checkout>/starter-kit/gac-modes --name gac-modes
lola install gac-modes -a claude-code
```
