# Design note — login_banner

> Short intake and design note for a new production role.

| | |
|---|---|
| **Need** | Every production Linux host shows the legally approved banner before and after login |
| **Requested by** | Security (compliance control: system use notification) |
| **Success criteria** | `/etc/motd`, `/etc/issue`, `/etc/issue.net` contain the approved text on all prod hosts; re-runs report no changes |
| **Repository classification** | prod (acme manifest) — low blast radius, no service restart |
| **Out of scope** | sshd `Banner` directive (separate change, it requires an sshd reload) |

## Design

- One role, `login_banner`, in the `acme.linux_baseline` collection (one function role per capability).
- One template, three destinations; each destination can be disabled.
- Destination paths and ownership are parameters, so the role is testable
  without root (Molecule scenario writes to a temporary directory).
- No handlers: the files are read at login time; nothing to restart.

## Governance applied

| Rule | Source | Effect on the design |
|------|--------|----------------------|
| R-DOC-001 | L1 ADR-0002 | `meta/argument_specs.yml` declares every variable |
| R-CODE-001 | L1 ADR-0001 | No loops in this role; nothing to apply |
| R-SEC-001 | L1 ADR-0003 | No credentials involved |
| R-CODE-002 | L1 ADR-0004 | No `command` / `shell` |
| R-TEST-001 | L1 ADR-0006 | Molecule scenario `integration_login_banner` with the `idempotence` step |
| CoP naming, check mode | L0 | `login_banner_` prefix; templates support check mode |
