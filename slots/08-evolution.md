# Slot 08 — Evolution

**How does the system improve over time?**

## What belongs here

Routines and checks that keep governance alive: exception review, audits, Librarian proposals, metrics.

**Not here:** One-off clean-ups without a routine.

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: evolution`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`instance-check` — a check of the instance that runs in its CI (and during setup).

## Verification

The check runs and passes today.

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `exception-watch` | [ADR-0014](../examples/acme/adr/ADR-0014-exception-watch.md) | Expired or invalid exceptions fail the instance CI; exceptions expiring within 30 days are warned |

## Caution

Evolution is also the Auditor and Librarian modes (Capabilities); this slot holds the *routines* that trigger them.
