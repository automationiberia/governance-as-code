# Slot 05 — Output

**How does the agent communicate?**

## What belongs here

Conversational style and artifact templates (audit report, success contract, PR body, ADR).

**Not here:** Rules about the content itself (Knowledge / rules).

## Admission criteria

Answer in the harness-adoption ADR (`type: harness-adoption`, `slot: output`):

| Question | Why it matters |
|----------|----------------|
| What does it touch: knowledge, actions, systems, data leaving the machine? | Data egress or model routing makes it a security decision |
| Project or user scope? | User-scope tools cannot be verified by the instance: `recommended` at most |
| How is it pinned (commit, release + checksum)? | No unpinned dependency enters L0 (GAC-0002) |
| What can it conflict with, and who wins? | Precedence must be explicit before adoption |
| How is it verified after install? | An adoption nobody can verify is documentation, not governance |
| How is it removed? | Every adoption must be reversible |

## Mechanism

`reference` for templates shipped with the modes; `lola-module` for style skills.

## Verification

Templates exist; style skills are installed.

## Reference adoption in acme

| Entry | ADR | What |
|-------|-----|------|
| `artifact-templates` | [ADR-0012](../examples/acme/adr/ADR-0012-output-style-and-templates.md) | Audit report, success contract, PR body, ADR templates |
| `i-have-adhd` | [ADR-0012](../examples/acme/adr/ADR-0012-output-style-and-templates.md) | Concise conversational style |

## Caution

Organization artifact templates always win over a conversational style (precedence P8): a report is complete even if the chat is terse.
