# Slot 07 — Execution

**Where does the agent run, and with which credentials?**

## What belongs here

Workspaces, sandboxes and the test platform for disposable hosts.

**Not here:** Production credentials in the agent's environment.

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: execution`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`test-platform` — the runtime and image declared in `manifest.yml` → `test_platform`.

## Verification

The runtime is available and the image is present (pulled if needed).

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `test-platform` | [ADR-0007](../examples/acme/adr/ADR-0007-test-platform.md) | podman + UBI 9 (init variant for systemd), no privilege escalation |

## Caution

If the platform is missing, tests are reported as "written, not run" — never as passing (GAC-0010).
