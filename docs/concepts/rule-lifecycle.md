# Rule lifecycle — from a need to an enforced rule

An organization rule always starts as a decision and ends as something a gate
can check (or, when that is impossible, something a process guarantees).

```text
 Need ──▶ ADR ──────────────────────────────▶ Rule ─────────────────────▶ Channels ──▶ Verification
          proposed → in-review → accepted     registry entry              AI harness    warn → block
                         └─▶ rejected         (single source)             pre-commit
                                                                          CI, EE, AAP
          superseded / deprecated ◀── a later ADR
```

## 1. Need

Someone identifies a gap: a convention the community does not cover, a
security policy, a recurring review comment, an upstream change.

Anyone may raise a need, including an AI agent in **Librarian** mode. The
agent drafts; it never approves.

## 2. ADR

The need becomes an organization ADR (see [adr.md](../../starter-kit/gac-modes/module/skills/gac-librarian/templates/adr.md)).

| State | Meaning |
|-------|---------|
| `proposed` | Drafted, open for discussion |
| `in-review` | Assigned to its approvers |
| `accepted` | Approved; the decision is now binding |
| `rejected` | Not adopted; kept for the record |
| `superseded` | Replaced by a later ADR |
| `deprecated` | No longer applies, not replaced |

Approvers depend on the decision type:

| Type | Minimum approvers |
|------|-------------------|
| `coding-standard` | Automation lead + representative of affected teams |
| `security-policy` | Automation lead + Security |
| `lifecycle-policy` | Automation lead + Operations |
| `harness-adoption` | Automation lead (+ Security if data leaves the environment) |
| `exception-policy` | Owner of the affected locked rule |
| `evolution` | Automation lead |

An ADR is **not** binding until it is `accepted`.

## 3. Rule

Each accepted ADR produces one or more **rule registry entries**
(see [rule.yml](../../starter-kit/gac-modes/module/skills/gac-librarian/templates/rule.yml)). The registry is the only
thing channels read ([GAC-0004](../../adr/GAC-0004-single-source-for-rules.md)).

Every rule declares how it can be verified:

| Verifiability | Example | Guaranteed by |
|---------------|---------|---------------|
| `mechanical` | Collection denylist, variable naming | A gate that blocks |
| `heuristic` | "One role per capability" | Auditor review + human review in the PR |
| `process` | "Changes to `criticality: high` repositories need CAB approval" | Required approvers, PR checklist, intake template |

## 4. Channels

Channels derive their configuration from the registry. Nobody writes a rule
into a channel by hand.

| Channel | Role |
|---------|------|
| AI harness (mode skills, pointer, hooks) | Guides the agent before and while it works |
| pre-commit | Early local feedback |
| CI | Blocks merges |
| EE build / Hub publish | Blocks artifacts |
| AAP runtime | Final safety net (approved EEs, RBAC) |

## 5. Verification

New rules start in `warn` and move to `block` on a date stated in the rule.
During `warn`, the Auditor measures existing violations and records a
**baseline**: new content must comply; existing debt is tracked and burned
down instead of blocking everyone on day one.

| Enforcement | Effect |
|-------------|--------|
| `advise` | AI guidance only (typical for heuristic rules) |
| `warn` | Reported by gates, does not block |
| `block` | Gates fail |

## Exceptions

When a project cannot comply, it requests an exception
(see [exception.yml](../../starter-kit/gac-modes/module/skills/gac-librarian/templates/exception.yml)): scope, owner,
justification, expiry. Gates honor it only within its scope and only until it
expires. Exceptions that keep being renewed are a signal for the Librarian to
propose revisiting the ADR.
