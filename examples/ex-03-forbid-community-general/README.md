# EX-03 — `community.general` forbidden in production

**Use cases:** UC-08 Add an organization rule · UC-09 Request a project
exception · **Modes:** Librarian, Builder · **Governance:** [acme](../acme/)

The full life of an organization rule: a need becomes an ADR, the ADR becomes
one registry entry and one lint rule, the AI agent and the gates apply it,
and a project that cannot comply gets a scoped, expiring exception.

```text
 Security need ──▶ Librarian ──▶ ADR-0005 (proposed) ──▶ approval ──▶ ADR-0005 (accepted)
                     │ impact analysis                                   │
                     │ 1 of 6 repos affected                             ▼
                     ▼                                         R-COLL-001 (registry)
               EXC-001 draft ──▶ rule owner approves ──▶ register   │
                                                                     ├─▶ Builder (gac-governance hint)
                                                                     ├─▶ pre-commit / CI (lint rule)
                                                                     └─▶ expiry enforced by the rule
```

## Layout

```text
ex-03-forbid-community-general/
├── repos/
│   ├── firewall_legacy/      # prod — uses community.general.ufw → EXC-001
│   ├── network_tuning/       # prod — built by the Builder, compliant
│   └── lab_sandbox/          # nonprod — uses community.general, out of scope
└── reports/
    ├── librarian-proposal.md         # ADR + rule + manifest drafts, impact analysis
    ├── builder-first-attempt/        # Builder draft before the checker loop
    ├── success-contract-network_tuning.md  # acceptance criteria (GAC-0010)
    └── builder-first-attempt-checker.txt
```

Instance changes in [acme](../acme/): [ADR-0005](../acme/adr/ADR-0005-forbid-community-general-in-production.md),
`R-COLL-001` in the [registry](../acme/rules/organization.yml), the lint rule
[r_coll_001.py](../acme/gates/rules/r_coll_001.py), repository classification
in the [manifest](../acme/manifest.yml), and `EXC-001` in the
[exception register](../acme/exceptions/register.yml).

## Prerequisites, setup and teardown

**Prerequisites:** the one-time [setup](../../starter-kit/SETUP.md) for the
repository you work in (`--repo examples/ex-03-forbid-community-general/repos/<repo>`).
No containers are needed; this example only runs the checker.

**Setup:** set the repository identity the CI platform would provide, and
make the pinned collections available so ansible-lint does not download them:

```bash
export GAC_REPOSITORY=<repo>                       # firewall_legacy, network_tuning, lab_sandbox
export ANSIBLE_COLLECTIONS_PATH="$HOME/.cache/gac/collections"
```

**Teardown:** none (the checker writes only an `.ansible/` cache, ignored by Git).

## Step by step

### 1. Librarian — from need to proposal

```text
/librarian rule "production automation must not depend on community.general"
```

The Librarian checks L0 first (CoP, ansible-lint and ai-forge say nothing
about allowed collections, so a new rule is justified), drafts ADR-0005 and
`R-COLL-001`, drafts the lint rule, proposes the manifest classification, and
**measures impact** with the draft rule on a scratch copy of the instance:

| Repository | Path | Result |
|------------|------|--------|
| ex-01 `manage_users`, `linux_baseline`, `network_tuning`, `lab_tools` | prod / nonprod | pass |
| `lab_sandbox` | nonprod | pass — uses `community.general`, out of scope |
| `firewall_legacy` | prod | **3 findings** |

One repository affected → the proposal enters directly in `block`, and
drafts an exception for `firewall_legacy`. See
[reports/librarian-proposal.md](reports/librarian-proposal.md).

### 2. Approval — humans

automation-lead and security accept ADR-0005; security, as owner of the
locked rule, approves EXC-001 (expires 2027-03-31). *Approval is simulated in
this example.*

### 3. Builder — the rule reaches the agent

```text
/build playbook to allow HTTPS in the firewall and tune network sysctl on production nodes, in network_tuning
```

`gac-governance` returns, among others:

```text
R-COLL-001 (ADR-0005, L1, block, mechanical): Do not use community.general in production
           repositories. Use ansible.builtin, ansible.posix or certified collections.
```

The [first draft](reports/builder-first-attempt/) still used
`community.general.ufw` and the `community.general.json_query` filter; the
checker blocked it with 3 findings
([output](reports/builder-first-attempt-checker.txt)). The final
[playbook](repos/network_tuning/playbooks/type_linux_network_tuning.yml) uses
`ansible.posix.firewalld` (the hosts run RHEL) and built-in filters.

### 4. Gates — the rule and its exception

The lint rule reads its context from the instance, not from each repository:

| Context | Source | Behavior |
|---------|--------|----------|
| Is this repository prod? | `manifest.yml` `promotion_paths` | Unlisted → treated as prod (deny by default) |
| Is there a valid exception? | `exceptions/register.yml` | Repository, items, paths, approval and expiry enforced |
| Which repository is this? | `GAC_REPOSITORY`, set by the CI platform | — |

## Verification (2026-11-04)

| Case | Expected | Result |
|------|----------|--------|
| `firewall_legacy` with EXC-001 valid | pass | ✅ 0 findings |
| `network_tuning` (Builder final) | pass | ✅ 0 findings |
| `lab_sandbox` (nonprod) | pass | ✅ 0 findings |
| `lab_sandbox` checked as an unclassified repository | block | ✅ 2 findings |
| Builder first draft | block | ✅ 3 findings (modules, filter, dependency) |
| EXC-001 expired yesterday | block | ✅ 3 findings |
| EXC-001 without approval | block | ✅ 3 findings |
| A module outside EXC-001 items | block | ✅ 1 finding |

```bash
cd repos/firewall_legacy
GAC_REPOSITORY=firewall_legacy ansible-lint -c ../../../acme/gates/ansible-lint.yml   # 0 findings (EXC-001)
cd ../network_tuning
GAC_REPOSITORY=network_tuning ansible-lint -c ../../../acme/gates/ansible-lint.yml    # 0 findings
cd ../lab_sandbox
GAC_REPOSITORY=lab_sandbox ansible-lint -c ../../../acme/gates/ansible-lint.yml       # 0 findings (nonprod)
GAC_REPOSITORY=unregistered ansible-lint -c ../../../acme/gates/ansible-lint.yml      # 2 findings (deny by default)
```

## What this example taught the method

| Finding | Change |
|---------|--------|
| The ansible-lint ignore file cannot expire and is shared by every repository | Organization rules read the exception register directly; the ignore file is kept for built-in rules only |
| "Not listed = nonprod" fails open | Deny by default: unlisted repositories are prod for prod-scoped rules; `nonprod` is explicit in the manifest |
| Repository identity decides scope, so it is a bypass vector | `GAC_REPOSITORY` comes from the CI platform; non-bypassable gates need organization-level enforcement on the platform |
| A dependency-level ban must catch more than modules | One detector for tasks, filters, lookups, `requirements.yml`, `galaxy.yml` and EE files |
