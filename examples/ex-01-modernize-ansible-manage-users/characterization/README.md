# EX-01 — Characterization of the original role

> Validation experiment (phase 2): would freezing the original behavior
> **before** modernizing have surfaced earlier what we found during and after
> the build?

## Method

| | Original | Modernized |
|---|---|---|
| Runtime | ansible-core 2.15.13 inside a UBI 9 container (last version accepting `include`) | ansible-core 2.22 controller, podman connection, UBI 9 container |
| Starting state | [prepare.sh](prepare.sh): `oldgroup`, `olduser`, `orainfra` with a 30-day inactivity period | same |
| Scenario | [play-original.yml](play-original.yml) — default password behavior | [play-modernized.yml](play-modernized.yml) — variables mapped per the migration table |
| Runs | run 1 → user `oracle` changes its password → run 2 | same |
| Captured | [capture_state.py](capture_state.py): passwd, groups, shadow fields, whether the password equals the user name | same |

Reproduce: `./run.sh` (podman; set `ANSIBLE_PLAYBOOK` and `ANSIBLE_COLLECTIONS_PATH` for the modernized run). Raw output in [results/](results/).

## Results (2026-11-05)

| Aspect | Original | Modernized | Verdict |
|--------|----------|------------|---------|
| uid, gid, secondary groups, comment | as requested | as requested | ✅ preserved |
| Group creation and removal, user removal | done | done | ✅ preserved |
| Password of `oracle` equals the user name | **yes** (verified with crypt) | no | deviation — ADR-0003 |
| Password policy task | **fails**: `Unable to import chage due to invalid syntax` | applied | deviation — policy enforced for the first time |
| `orainfra` (existing user) inactivity period | stays 30 days | removed | deviation (consequence of the above) |
| `oracle` (new user) must change password at first login | no | yes | deviation (consequence of the above) |
| Run 2 after the user changed its password | no change (policy fails) | `changed=0`; not forced again | ✅ |

## What characterization found earlier — and what it did not

| Finding | How we found it in EX-01 | With characterization first |
|---------|--------------------------|-----------------------------|
| Password equals user name | Reading the code (Auditor, heuristic) | **Proven** on a running system before any change |
| The custom `chage` module does not import on Python 3; the policy never ran | **Not found** — the audit and the PR described what the code says, not what happens | **Found before building** — and it changes the decision: the modernized role introduces a policy that, in practice, does not exist today |
| Preserved behavior (accounts, groups) | Assumed | **Evidence** of equivalence |
| `append` without `groups` rejected by ansible-core | Idempotency test of the modernized role | **Not found**: ansible-core 2.15 still accepts it |
| Wrong shadow field index | Idempotency test of the modernized role | **Not found**: it is a defect of the new code |

## Conclusion

Characterization added value that nothing else in the method produced:

- It turned a code-reading assumption into evidence (password = user name).
- It **corrected a wrong claim** in the audit and the PR, and exposed the real
  behavior change for a human to decide **before** building.
- It gave objective evidence that everything else is preserved.

It does not replace testing the modernized content on the target runtime:
incompatibilities with newer ansible-core and defects in new code are still
found by the idempotency test.

Effort: one harness (four small files) and two disposable containers; about
two minutes per run.
