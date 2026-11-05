# Precedence — resolving layers into effective governance

Precedence orders **sources of authority** only. Skills, hooks, linters and
CI are **channels** that consume the result; they never take part in
precedence ([GAC-0001](../../adr/GAC-0001-separate-authority-from-enforcement.md)).

```text
  Sources of authority                     Channels (consume, never decide)
  ────────────────────                     ────────────────────────────────
  L3 Project   (exceptions)                AI harness: skills, hooks, MCP
  L2 Domain                     resolve    pre-commit
  L1 Organization        ───────────────▶  CI
  L0 Community                             EE build, Hub publish
                         effective         AAP runtime controls
                         governance
```

## Resolution rules

| # | Rule |
|---|------|
| P1 | A higher layer overrides a lower layer on the same topic. |
| P2 | If no higher layer addresses a topic, the lower layer applies. |
| P3 | A rule marked **locked** at L1 cannot be relaxed by L2 or L3. Only its L1 owner can grant an exception. |
| P4 | L3 never creates rules; it only holds exceptions. |
| P5 | Every exception has a scope, an owner, a justification and an expiry date. An expired exception no longer applies. |
| P6 | L0 versions are pinned. Upgrading an L0 base is an L1 decision. |
| P7 | Tools adopted into any slot follow the same rules as rules: they enter through an ADR in the owning layer. |
| P8 | When an Output style conflicts with an organization artifact template, the template wins. |

## Override actions

A higher layer may act on a lower-layer item in exactly these ways:

| Action | Meaning | Example |
|--------|---------|---------|
| `add` | Introduce something the lower layer does not cover | Forbid a collection |
| `replace` | Substitute a lower-layer rule with another | Different variable prefix convention |
| `tighten` | Keep the rule, make it stricter | `warn` → `block` |
| `disable` | Turn off a lower-layer rule or capability, with justification | Disable a skill not used by the organization |
| `except` | L3 only: a scoped, temporary exception | One module in one repository until a date |

Every action references the ADR (or exception record) that justifies it.

## Example

```text
  L0  CoP: role variables prefixed with the role name            (rule)
  L1  ADR-0001 tighten: role loop variables use the __<role>_ prefix (tighten)
  L1  ADR-0005 add: community.general forbidden in production     (add, locked)
  L3  EXC-001 except: community.general.ufw in firewall_legacy    (except, expires 2027-03-31)
  ─────────────────────────────────────────────────────────────────
  Effective for firewall_legacy:
    - __<role>_ loop variable prefix             (from L1, ADR-0001)
    - community.general forbidden, except ufw    (L1 ADR-0005 + L3 EXC-001)
    - everything else CoP says                   (from L0)
```
