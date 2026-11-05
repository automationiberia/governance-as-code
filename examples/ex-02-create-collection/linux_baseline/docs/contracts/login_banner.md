# Success contract — role `login_banner`

> Written after the fact: GAC-0010 postdates this example. Writing it exposed
> three criteria the test did not check — `/etc/issue` content, file
> permissions and check mode — and the test was extended before marking them.

| | |
|---|---|
| **Kind** | new content |
| **Repository** | `linux_baseline` · classification: prod |
| **Governance** | acme@2026.11 |
| **Status** | approved by Security (requester) and the automation lead (approval simulated in this example) |

## Acceptance criteria

| # | Given | When | Then | Result |
|---|-------|------|------|--------|
| A1 | A host without the banner | The role runs with a banner text | `motd` and `issue` contain the text, preceded by an `ansible_managed` comment | ✅ met (Molecule asserts) |
| A2 | `login_banner_issue_net_enabled: false` | The role runs | `issue.net` is not created | ✅ met |
| A3 | Default permissions | The role runs | Files have mode `0644` | ✅ met (added to the test) |
| A4 | State after A1 | The role runs again | No changes reported | ✅ met (Molecule `idempotence`) |
| A5 | State after A1 | The role runs in check mode | No changes reported, no failure | ✅ met (Molecule `check`, added) |
| A6 | A host without the banner | The role runs in check mode (first run) | Reports the changes it would make, no failure | ⚠️ not verified — the test reads files that would not exist |

## Verification

| | |
|---|---|
| Process rules that apply | R-TEST-001 (prod repository) |
| How | Molecule scenario `integration_login_banner`: converge, idempotence, check — exit 0 |
| Test platform | Delegated to localhost with a temporary directory (the role's paths are parameters); no container needed |
| Out of scope | sshd `Banner` directive (needs an sshd reload; separate change) |
