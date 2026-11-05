# EX-02 — Create collections with governance wired into the scaffold

**Use case:** UC-01 Create a collection · **Mode:** Builder ·
**Governance:** [acme](../acme/)

The Builder scaffolds collections through ai-forge (`ansible-creator`) and
**connects the organization's governance to what the scaffold generates**:
pointer, checker hook and CI gate. Two collections show that the
**repository classification** — decided in the instance manifest, not by
whoever asks for the work — determines which rules apply.

| | [`acme.lab_tools`](lab_tools/) | [`acme.linux_baseline`](linux_baseline/) |
|---|---|---|
| Role | `troubleshooting_packages` | `login_banner` |
| Classification (acme manifest) | **nonprod** | **prod** |

## What the classification changes

| Rule | `lab_tools` (nonprod) | `linux_baseline` (prod) |
|------|-----------------------|-------------------------|
| R-TEST-001 — idempotency test ([ADR-0006](../acme/adr/ADR-0006-production-roles-have-idempotency-test.md)) | does not apply | ✅ Molecule `integration_login_banner` with `idempotence` |
| R-COLL-001 — no `community.general` ([ADR-0005](../acme/adr/ADR-0005-forbid-community-general-in-production.md)) | does not apply | ✅ applies (no usage) |
| R-DOC-001 — argument specs | ✅ applies | ✅ applies |
| R-CODE-001 — loop variable prefix | ✅ applies | ✅ applies |
| ansible-lint `production` + CoP | ✅ | ✅ |
| CI gate `governance-checker` | ✅ | ✅ |

Each role has a success contract (GAC-0010):
[login_banner](linux_baseline/docs/contracts/login_banner.md) ·
[troubleshooting_packages](lab_tools/docs/contracts/troubleshooting_packages.md).
Writing the `login_banner` contract exposed three criteria the test did not
check (`/etc/issue` content, permissions, check mode); the test now covers
them, and one criterion — check mode on a first run — is marked not verified.

The design note and changelog fragment in `linux_baseline` are the Builder's
choice for a new production role; no acme rule requires them yet. If ACME
wants them, it adds `DOC` rules scoped to prod — the method imposes none.

`lab_tools` **failed the checker once** — its galaxy tags had none of the
required categories — and was fixed. Gates apply regardless of classification.

## How it was built

Builder delegated scaffolding to ai-forge `/ansible-scaffold-collection`,
which uses `ansible-creator` (26.10.0), then applied ACME governance on top:

1. `ansible-creator init collection acme.<name>` and `ansible-creator add resource role <role>`.
2. Removed sample content (ai-forge step 10): sample plugins, `run` role,
   sample EDA rulebook, sample integration target, and the `ansible.utils`
   dependency only the samples needed.
3. Wrote the role, argument specs and README; `meta/runtime.yml` →
   `requires_ansible: ">=2.16.0"`.
4. Wired governance into what ansible-creator generated:
   - `AGENTS.md`: kept ansible-creator's line, **appended** the governance
     pointer with the repository classification, and stated that the
     instance wins on conflict.
   - `.pre-commit-config.yaml`: added the acme checker hook.
   - `.github/workflows/governance-checker.yml`: added the acme CI gate.
5. Applied the process rules `gac-governance` returned: for `linux_baseline`
   (prod), R-TEST-001 → integration target plus Molecule scenario with
   `idempotence`. For `lab_tools` (nonprod), none.
6. Ran the checker until green, ran the Molecule scenario, and built both
   collections.

## Findings while building (fed back into the method)

| Finding | Consequence |
|---------|-------------|
| ansible-creator's CI runs ansible-lint with its own defaults, **not the organization's configuration** | Without the extra `governance-checker` job, acme rules would never run in CI. The Builder always adds the organization gate |
| ansible-creator writes an `AGENTS.md` that delegates to a **remote, unpinned** document (`refs/heads/main`) | An L0 instruction that can change silently. The pointer is appended and states precedence; pinning it is a candidate acme ADR |
| The acme rule R-DOC-001 flagged an ansible-test integration target as a role | Rule fixed to apply only under `roles/` (a gate bug found by real content) |
| `tempfile` in a test target breaks Molecule's idempotence step | Test targets write to a stable directory |

## Prerequisites, setup and teardown

**Prerequisites:** the one-time [setup](../../starter-kit/SETUP.md), run for
each collection (`--repo examples/ex-02-create-collection/lab_tools`, then
`.../linux_baseline`). The tool environment includes `ansible-creator` and
`molecule`.

**Setup** — Molecule resolves the role by its FQCN, so the collection must be
in a collections path:

```bash
mkdir -p /tmp/colls/ansible_collections/acme
ln -sfn "$PWD/linux_baseline" /tmp/colls/ansible_collections/acme/linux_baseline
```

**Teardown:**

```bash
rm /tmp/colls/ansible_collections/acme/linux_baseline        # the symlink
rm -r ~/.ansible/tmp/molecule.*.integration_login_banner     # Molecule state (destroy is a no-op)
rm -f */acme-*-1.0.0.tar.gz                                  # built artifacts
```

## Verify

```bash
# Checker — same command for both, from each collection root
cd lab_tools      && GAC_REPOSITORY=lab_tools      ansible-lint -c ../../acme/gates/ansible-lint.yml   # 0 findings
cd ../linux_baseline && GAC_REPOSITORY=linux_baseline ansible-lint -c ../../acme/gates/ansible-lint.yml   # 0 findings

# linux_baseline — R-TEST-001 idempotency test (after Setup)
cd extensions && ANSIBLE_COLLECTIONS_PATH=/tmp/colls molecule test -s integration_login_banner
# The scenario's destroy step is a no-op (ansible-creator pattern), so files
# persist in ~/.ansible/tmp/molecule.*.integration_login_banner between local
# runs; remove it to see the first converge report changes again.

# Both
ansible-galaxy collection build
```

Verified on 2026-11-04 with ansible-lint 26.10.1, ansible-core 2.22,
molecule 26.10.0: both checkers 0 findings; Molecule converge `changed=3`,
idempotence `changed=0`, check `changed=0`; both collections build.

## Do it yourself with your AI assistant

From an empty repository named `linux_baseline`, governed by acme and set up
once with [gac-setup.sh](../../starter-kit/SETUP.md):

```text
/build collection acme.linux_baseline with a role login_banner that manages /etc/motd, /etc/issue and /etc/issue.net
```

The Builder runs intake, resolves governance for `linux_baseline` (prod in
the manifest, so R-TEST-001 applies), scaffolds through ai-forge, wires the
governance into the scaffold, and stops with the checker and the Molecule
scenario green.
