# EX-01 — Modernize `ansible-manage-users`

**Use case:** UC-04 Modernize a role · **Modes:** Auditor → Builder ·
**Repository:** prod · **Governance:** [acme](../acme/)

A 2017 role ([silvinux/ansible-manage-users](https://github.com/silvinux/ansible-manage-users))
that no longer loads on supported ansible-core, sets each user's password to
its user name, and ships an unmaintained custom module — modernized under
ACME governance.

## Layout

```text
ex-01-modernize-ansible-manage-users/
├── AGENTS.md                 # pointer to the acme governance instance
├── before/roles/manage-users # original role, unmodified (see before/NOTICE.md)
├── after/
│   ├── ansible.cfg
│   ├── roles/manage_users    # modernized role
│   └── tests/                # idempotency test (podman container)
├── characterization/         # original vs modernized on the same starting state
└── reports/
    ├── checker-before.txt    # raw checker output on the original
    ├── audit-before.md       # Auditor output
    ├── success-contract.md   # what must stay the same + approved deviations (GAC-0010)
    └── pr-body.md            # Builder output
```

## Result

| | Before | After |
|---|---|---|
| Loads on ansible-core ≥ 2.16 | ❌ (`include` removed) | ✅ |
| Checker findings (acme, ansible-lint profile `production`) | 60 (+11 hidden) | **0** |
| Organization rules violated | R-CODE-001, R-DOC-001, R-SEC-001, R-CODE-002, R-TEST-001 | none |
| Default password | user name | none — required from a vault |
| Custom module | `library/chage` (2016) | removed |
| Password policy | ❌ never applied: the custom module fails on Python 3 ([characterization](characterization/README.md)) | ✅ applied, idempotent (`changed=0`) |
| Check mode | unknown | ✅ `changed=0` |

## Do it yourself with your AI assistant

### 1. Prepare

**Prerequisites:** the one-time [setup](../../starter-kit/SETUP.md) for this
directory, and podman for step 4.

```bash
# From the method checkout: modes + acme's pinned ai-forge modules, for your assistant
starter-kit/setup/gac-setup.sh \
  --instance examples/acme \
  --repo examples/ex-01-modernize-ansible-manage-users \
  --assistant claude-code
export PATH="$HOME/.cache/gac/venv/bin:$PATH"
export ANSIBLE_COLLECTIONS_PATH="$HOME/.cache/gac/collections"
```

Open `examples/ex-01-modernize-ansible-manage-users/` in your assistant. Its
[AGENTS.md](AGENTS.md) points to the acme instance.

### 2. Audit

```text
/audit before/roles/manage-users
```

The Auditor declares itself, resolves acme governance (4 rules apply to a
role in prod), runs the checker, adds the CoP review and the heuristic
organization rules, and writes a report like
[reports/audit-before.md](reports/audit-before.md) with a remediation plan.

What to look for in the report:

- Every finding cites its source: `L0 lint`, `L0 cop:`, or `L1 ADR-000N`.
- The invalid role name **hides** 11 findings; the Auditor says so.
- Two findings are not lint problems at all: guessable passwords (R-SEC-001,
  heuristic) and an unmaintained custom module (R-CODE-002). Running the
  original ([characterization](characterization/README.md)) showed that the
  module does not even load on Python 3 — something reading the code missed.

### 3. Build

```text
/build fix findings in reports/audit-before.md into after/roles/manage_users
```

The Builder resolves governance for the repository (prod, so R-TEST-001
applies), rewrites the role through ai-forge skills, and loops on the
checker until no `block` findings remain. It then writes the idempotency
test R-TEST-001 asks for, runs it twice, and drafts a PR
like [reports/pr-body.md](reports/pr-body.md), including the migration table
and the behavior changes a human must approve.

### 4. Verify

```bash
cd after
ansible-lint -c ../../acme/gates/ansible-lint.yml        # 0 findings

podman run -d --name gac-ex01 registry.access.redhat.com/ubi9/ubi sleep infinity
podman exec gac-ex01 sh -c 'groupadd oldgroup && useradd olduser'
ansible-playbook -i tests/inventory.yml tests/test.yml   # run 1: changes
ansible-playbook -i tests/inventory.yml tests/test.yml   # run 2: changed=0
ansible-playbook -i tests/inventory.yml tests/test.yml --check

# Characterization of the original (optional, ~2 min, needs Internet in the container)
../characterization/run.sh
```

**Teardown:**

```bash
podman rm -f gac-ex01                                    # test container
# characterization/run.sh removes its own containers
```

## What this example shows about the method

| Method principle | Where it shows |
|------------------|----------------|
| Bases consumed, not forked ([GAC-0002](../../adr/GAC-0002-consume-bases-never-fork.md)) | L0 findings come from unmodified ansible-lint and CoP |
| L1 is only a delta ([GAC-0003](../../adr/GAC-0003-organization-layer-is-a-delta.md)) | acme has 4 rules; two of them *tighten* L0 (`loop-var-prefix`, CoP argument validation) |
| Single source for rules ([GAC-0004](../../adr/GAC-0004-single-source-for-rules.md)) | `R-DOC-001` is the registry id, the lint rule id and the id in the report |
| Gates are the guarantee ([GAC-0006](../../adr/GAC-0006-gates-are-the-guarantee.md)) | Same checker command for the agent, pre-commit and CI |
| Heuristic rules are explicit | R-SEC-001 and R-CODE-002 are judged by the Auditor and approved in the PR, not faked as lint rules |
| Tests catch what lint cannot | `append` without `groups` and a wrong shadow field index were found only by running the role |

## How this example was produced

The Auditor and Builder steps were executed by an AI assistant following the
`gac-auditor` and `gac-builder` skills, with the checker and tests run for
real (ansible-lint 26.10.1, ansible-core 2.22, UBI 9 container). Two defects
in the first Builder output were caught by the idempotency test and fixed
before the checker and test passed.
