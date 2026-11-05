# 10 — Evolution

> Status: draft v0.1

Governance that does not evolve becomes shelfware. The Librarian mode and a
few recurring routines keep it alive.

## Routines

| Routine | Cadence | Trigger | Output |
|---------|---------|---------|--------|
| Upstream review | Per release of a base, at least quarterly | New CoP / ai-forge / aap-skills version | Librarian impact report; evolution ADR to bump the pin |
| Exception review | Monthly | Exceptions expiring, renewed more than twice | Renew, close, or ADR revision proposal |
| Finding review | Monthly | Findings recurring across repositories without a rule | Candidate rules (Librarian) |
| Baseline burn-down | Per rule | `block_from` approaching | Remaining debt per repository |
| Slot review | Quarterly | New tools requested or available | Harness-adoption ADR drafts |

## Upgrading a community base

```text
 new upstream ref ──▶ Librarian: diff + affected L1 items ──▶ Auditor dry-run on sample repos
        ──▶ evolution ADR (proposed) ──▶ approval ──▶ bump pin in manifest ──▶ regenerate channels
```

Because L1 is only a delta, the review is limited to L1 items that act on the
changed upstream topics.

## Metrics

| Metric | Shows |
|--------|-------|
| `block` violations per repository over time | Compliance trend |
| Repositories with CI gate in `block` | Coverage |
| Open exceptions, age, renewals | Where rules do not fit reality |
| Time from ADR `proposed` to `block` | Governance throughput |
| Rules by verifiability | How much depends on review vs gates |

## Evolving the method

Changes to the method itself (slots, modes, precedence) are GAC ADRs in this
repository, versioned with the starter kit.
