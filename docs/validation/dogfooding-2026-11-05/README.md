# Dogfooding — clean AI assistant sessions (2026-11-05)

**Question:** do the modes work from the installed skills alone, in a fresh
assistant session with no other context?

## Setup

| | |
|---|---|
| Repository | A copy of EX-01 laid out like a real content repository: `roles/manage-users` (original), `governance/` (acme instance), `AGENTS.md` pointer |
| Installation | [`gac-setup.sh`](../../../starter-kit/setup/gac-setup.sh): 5 ai-forge modules pinned to the acme manifest commit + `gac-modes`, for Claude Code (11 commands, 37 skills) |
| Assistant | Claude Code 2.1.312, headless (`claude -p`), fresh session |
| Permissions | Auditor: read, ansible-lint, copy, write report. Builder: read/write/edit, ansible-lint, ansible-playbook, `git mv`/`git rm`. No podman, no `rm` |

## `/audit roles/manage-users`

Output: [audit-output.md](audit-output.md).

| Expected from the method | Result |
|--------------------------|--------|
| Declares the mode | ✅ |
| Resolves governance: 6 acme rules, classification **prod** read from the manifest, EXC-001 discarded (other repository) | ✅ |
| Every finding cites rule and source layer | ✅ 22 findings |
| Notes findings hidden by the invalid role name | ✅ |
| Remediation plan and asks for approval before building | ✅ |
| Found what the first manual audit missed | ✅ Python 2 `chage` module (by reading the code), plaintext passwords in examples and in loop output, unsalted hash with `update_password: always`, stale README |

**Method defects it exposed (fixed):**

| Defect | Fix |
|--------|-----|
| With the instance inside the repository (`governance/`, the recommended layout), the checker linted the instance's rule fixtures → 21 findings; the gate could never pass | acme `exclude_paths: [governance/]`; documented in the starter-kit spec |
| R-DOC-001 did not fire when `tasks/main.yml` had a syntax error (ansible-lint skips other rules on that file) | Rule moved to the role directory (`matchdir`); written test-first: new fixture red → fix → green |
| `/audit` command said "do not modify any file" while the skill says "save the report" → the agent did not save it | Command and skill aligned: the report is the only file the Auditor writes |

## `/build` (modernize, with the architect's decisions in the prompt)

Output: [build-output.md](build-output.md) · PR draft: [build-pr-body.md](build-pr-body.md).

| Expected from the method | Result |
|--------------------------|--------|
| Declares the mode, resolves governance, applies process rules (R-TEST-001 for prod) | ✅ |
| Checker loop to green | ✅ 66 findings → 0 (verified independently) |
| Rules applied listed with their sources; heuristic rules handled explicitly | ✅ |
| Behavior changes listed for review; asks the architect on security-relevant ones | ✅ 19 listed, 2 flagged for decision |
| Writes the idempotency test (R-TEST-001) | ✅ Molecule scenario with `idempotence` and `verify` |

**Independent verification of the Builder's role** (podman, molecule-plugins):

| Run (podman + `molecule-plugins[podman]`, now in the tool environment) | Result |
|-----|--------|
| Its Molecule scenario as written | ❌ container exits (`/sbin/init` on an image without systemd) |
| After fixing the start command | ❌ `become: true` but the image has no `sudo` |
| With both environment fixes (role untouched) | ✅ converge `changed=5`, **idempotence `changed=0`**, verify passed |

The role works and is idempotent. The test scenario — written but not run,
because podman was not allowed in the session — had two environment defects.

## Lessons for the method

1. **The skills alone are enough** for a fresh assistant to follow the method
   end to end, including asking for human decisions.
2. **Running the content in the real layout finds method defects** that the
   examples did not: the instance inside the repository, a fragile rule, a
   command/skill contradiction.
3. **Tests must run where they are written.** The Builder needs an execution
   environment for tests (Execution slot). The instance should declare the
   test platform (image, init, privileges, `become`) so generated scenarios
   match it.
4. **Unattended sessions need permissions that match how agents run
   commands**: compound shell commands and `VAR=value cmd` prefixes do not
   match simple allowlist patterns.
