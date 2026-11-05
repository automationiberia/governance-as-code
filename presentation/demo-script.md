# Demo script

Everything runs locally and offline-safe. No step depends on an AI assistant
answering live: the AI parts are shown from their real, saved outputs.

| Part | What the audience sees | Live or saved | Time |
|------|------------------------|---------------|------|
| A | A company rule blocking, an exception allowing, the exception expiring | **Live** — deterministic, seconds | 3 min |
| B | A 2017 role: before vs after, and what it really did | Saved evidence | 3 min |
| C | A fresh AI assistant auditing on its own | Saved output | 2 min |
| D | The guardrail: an AI-style edit checked on the spot | **Live** — deterministic, seconds | 2 min |

## Before the talk (once)

```bash
# One-time setup (tools in ~/.cache/gac/venv, collections in ~/.cache/gac/collections)
starter-kit/setup/gac-setup.sh --instance examples/acme \
  --repo examples/ex-03-forbid-community-general/repos/firewall_legacy
export PATH="$HOME/.cache/gac/venv/bin:$PATH"
export ANSIBLE_COLLECTIONS_PATH="$HOME/.cache/gac/collections"

# Dry run of part A (all three commands below must behave as described)
```

Open in tabs: `presentation/flow.html`, a terminal at the repository root,
and the files listed in parts B and C. If the browser fails, use
`presentation/screenshots/`.

## A — A company rule at work (live)

Narrative: "Security decided production must not use `community.general`.
Let's see the rule work."

```bash
cd examples/ex-03-forbid-community-general/repos

# 1. A production repository that complies → passes
(cd network_tuning && GAC_REPOSITORY=network_tuning ansible-lint -c ../../../acme/gates/ansible-lint.yml)

# 2. The first AI draft → blocked, 3 findings that cite the decision (ADR-0005)
(cd ../reports/builder-first-attempt && GAC_REPOSITORY=network_tuning ansible-lint -c ../../../acme/gates/ansible-lint.yml)

# 3. The legacy firewall repository → passes thanks to its exception (EXC-001, until 2027-03-31)
(cd firewall_legacy && GAC_REPOSITORY=firewall_legacy ansible-lint -c ../../../acme/gates/ansible-lint.yml)
```

Then show the exception expiring — on a scratch copy, never on the real register:

```bash
cp -r ../../acme /tmp/acme-demo
sed -i 's/expires: 2027-03-31/expires: 2026-01-01/' /tmp/acme-demo/exceptions/register.yml
(cd firewall_legacy && GAC_REPOSITORY=firewall_legacy ansible-lint -c /tmp/acme-demo/gates/ansible-lint.yml)   # blocked again
rm -r /tmp/acme-demo
```

Point out: the message names the rule, the decision and the way out
("…or request an exception").

**Fallback:** [EX-03 README, verification table](../examples/ex-03-forbid-community-general/README.md#verification-2026-11-04).

## B — Modernizing a 2017 role (saved evidence)

Show, in order:

1. [Audit report](../examples/ex-01-modernize-ansible-manage-users/reports/audit-before.md) — the summary: 60 findings, passwords equal user names.
2. [Characterization](../examples/ex-01-modernize-ansible-manage-users/characterization/README.md) — the table "Original vs Modernized": the password policy never ran.
3. [Success contract](../examples/ex-01-modernize-ansible-manage-users/reports/success-contract.md) — what stays, what changes, approved.
4. [Pull request](../examples/ex-01-modernize-ansible-manage-users/reports/pr-body.md) — rules applied with their sources, migration table.

Optional live (≈1 min, needs podman): the idempotency test in
[EX-01 Verify](../examples/ex-01-modernize-ansible-manage-users/README.md#4-verify).

## C — A fresh AI assistant (saved output)

Show [the clean `/audit` output](../docs/validation/dogfooding-2026-11-05/audit-output.md):
the mode declared, the six company rules found on its own, every finding with
its source, the plan, and the question to the human before building. Then the
[lessons](../docs/validation/dogfooding-2026-11-05/README.md#lessons-for-the-method).

## D — The guardrail (live)

Narrative: "When the AI edits a file, the governance checks it at once — this
is exactly what the assistant receives."

```bash
cd examples/ex-04-harness-slots/demo-repo
cat roles/firewall/tasks/main.yml          # the task an AI might write
echo "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$PWD/roles/firewall/tasks/main.yml\"}}" \
  | CLAUDE_PROJECT_DIR=$PWD python3 ../../../starter-kit/hooks/gac_checker_on_edit.py
echo "exit=$?"                             # 2 = shown to the AI; ~7 seconds
```

Point out: the message names the rule and the decision; the repository is not
classified, so it is treated as production (deny by default). Then show what a
real fresh session did with it:
[EX-04 live session](../examples/ex-04-harness-slots/evidence/live-session.md),
and the [setup output](../examples/ex-04-harness-slots/evidence/setup-output.txt)
ending in *Slots active: 8/8*.

## After the talk

Nothing to clean: part A uses a scratch copy that the script removes.
