# 04 — Human roles

> Status: draft v0.1

Humans define requirements, rules and limits, and approve results. AI agents
execute within those limits.

## Roles

| Role | Responsibility |
|------|----------------|
| **Architect** | Defines direction, red lines and blueprints; final approval on governance |
| **Automation lead** | Owns the instance; approves most ADRs and repository classification changes |
| **Rule owner** | Owns one or more locked rules; grants exceptions to them |
| **Security** | Approves security policies and anything that sends data out or changes models |
| **Operations** | Approves lifecycle and platform policies |
| **Project owner** | Requests exceptions; accountable for the project's compliance |
| **Developer** | Builds content, manually or with AI modes |
| **AI agent** | Runs modes; drafts and proposes; never approves |

## RACI

R = responsible · A = accountable/approves · C = consulted · I = informed

| Activity | Architect | Automation lead | Rule owner | Security | Operations | Project owner | Developer | AI agent |
|----------|-----------|-----------------|------------|----------|------------|---------------|-----------|----------|
| Coding-standard ADR | C | A | C | — | — | I | C | R (draft) |
| Security-policy ADR | C | A | C | A | — | I | I | R (draft) |
| Lifecycle-policy ADR | C | A | — | — | A | I | I | R (draft) |
| Harness-adoption ADR | C | A | — | C (A if data leaves) | — | I | C | R (draft) |
| Lock a rule (red line) | A | R | R | C | C | I | I | — |
| Exception to a locked rule | I | I | A | C | — | R | C | R (draft) |
| Exception to an unlocked rule | — | A | — | — | — | R | C | R (draft) |
| Upgrade a community base | I | A | C | C | — | I | I | R (impact report) |
| Classify a repository (promotion path, `criticality`) | I | A | — | C | C | C | I | R (draft) |
| Merge content | — | I | — | — | — | A | R | R |
| Merge content — extra approvals from `PROC` rules (e.g. a repository classified `criticality: high`) | I | A | — | C | C | A | R | R |
| Write to live AAP | — | I | — | — | A | A | R | R (with confirmation) |
| Change the method (GAC ADR) | A | R | — | C | C | — | — | R (draft) |

Extra approvals are not defined by the method: they come from the
organization's `PROC` rules, scoped by repository classification
([GAC-0009](../../adr/GAC-0009-no-work-profiles.md)). An organization may map
these roles to its own titles in its instance manifest.
