# acme — reference governance instance

ACME is a fictitious organization. Its instance shows the minimum an
organization needs, following [docs/spec/08-instance.md](../../docs/spec/08-instance.md).

```text
acme/
├── manifest.yml                  # pinned bases, layers, promotion paths, slots, checker
├── AGENTS.pointer.md             # the pointer a team copies to AGENTS.md (method repo as submodule at governance/)
├── adr/                          # organization decisions (only the delta from L0)
├── rules/organization.yml        # rule registry — single source
├── exceptions/register.yml       # project exceptions (EXC-001)
└── gates/
    ├── ansible-lint.yml          # the checker configuration
    ├── ansible-lint-ignore.txt   # exceptions and baselines (none yet)
    └── rules/                    # organization lint rules (R-CODE-001 for roles at the repository root, R-DOC-001, R-COLL-001)
```

## Decisions

| ADR | Decision | Acts on L0 | Rule | Verifiability | Enforcement |
|-----|----------|------------|------|---------------|-------------|
| [ADR-0001](adr/ADR-0001-adopt-community-baseline.md) | Adopt CoP, ai-forge, aap-skills, ansible-lint `production`; loop vars `__<role>_` | add; tighten `lint:loop-var-prefix` | R-CODE-001 | mechanical | block |
| [ADR-0002](adr/ADR-0002-roles-declare-argument-specs.md) | Argument specs mandatory | tighten `cop:roles/argument-validation` | R-DOC-001 | mechanical | block |
| [ADR-0003](adr/ADR-0003-no-default-credentials.md) | No credentials in role defaults | add | R-SEC-001 (locked) | heuristic | advise |
| [ADR-0004](adr/ADR-0004-command-only-without-module.md) | `command`/`shell` only without a module | tighten lint rules | R-CODE-002 | heuristic | advise |
| [ADR-0005](adr/ADR-0005-forbid-community-general-in-production.md) | No `community.general` in production | add | R-COLL-001 (locked) | mechanical | block |
| [ADR-0006](adr/ADR-0006-production-roles-have-idempotency-test.md) | Production roles have an idempotency test | tighten `cop:roles/idempotency` | R-TEST-001 | heuristic | advise |
| [ADR-0007](adr/ADR-0007-test-platform.md) | Test platform: podman, UBI 9, no privilege escalation (Execution slot) | add (harness adoption) | — | — | — |
| [ADR-0008](adr/ADR-0008-knowledge-sources.md) … [ADR-0014](adr/ADR-0014-exception-watch.md) | One adoption per harness slot ([EX-04](../ex-04-harness-slots/README.md)) | add (harness adoption) | — | — | — |

Everything else follows the community baseline.

## Running the checker

From the root of a content repository that uses this instance:

```bash
ansible-lint -c <path-to>/acme/gates/ansible-lint.yml -i <path-to>/acme/gates/ansible-lint-ignore.txt
```

Note in [gates/ansible-lint.yml](gates/ansible-lint.yml): organization rules
must be listed in `enable_list`, because ansible-lint unloads every rule
outside the selected ansible-lint profile.

## Testing the organization rules

Organization lint rules are code and have fixtures (cases that must pass and
cases that must fail), run by [instance CI](.github/workflows/instance-ci.yml):

```bash
# Prerequisite: the tool environment from starter-kit/SETUP.md (ansible-lint, pytest)
pytest gates/rules/tests          # from this directory
```
