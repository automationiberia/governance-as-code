# Method ADRs

Decisions about **the method itself**. They are identified as `GAC-NNNN`.

This directory never contains organization rules. Organization decisions
(`ADR-NNNN`) live in each organization's instance — see
[adr.md](../starter-kit/gac-modes/module/skills/gac-librarian/templates/adr.md).

| ADR | Title | Status |
|-----|-------|--------|
| [GAC-0001](GAC-0001-separate-authority-from-enforcement.md) | Separate authority from enforcement | accepted |
| [GAC-0002](GAC-0002-consume-bases-never-fork.md) | Consume community bases, never fork them | accepted |
| [GAC-0003](GAC-0003-organization-layer-is-a-delta.md) | The organization layer is a delta | accepted |
| [GAC-0004](GAC-0004-single-source-for-rules.md) | A single source for every rule | accepted |
| [GAC-0005](GAC-0005-harness-slots.md) | Extend the harness through slots | accepted |
| [GAC-0006](GAC-0006-gates-are-the-guarantee.md) | Gates are the guarantee; the AI channel is guidance | accepted |
| [GAC-0007](GAC-0007-modes-are-common-orchestrators.md) | Modes are common orchestrators; organization governance is data | accepted |
| [GAC-0008](GAC-0008-modes-and-targets.md) | Separate modes from targets; add Operator, read-only first | accepted |
| [GAC-0009](GAC-0009-no-work-profiles.md) | No work profiles: process requirements are organization rules scoped by repository classification | accepted |
| [GAC-0010](GAC-0010-define-success-before-acting.md) | Define success before acting | accepted |

New method ADRs use the same template as organization ADRs, with the `GAC-`
prefix and `layer: method`.
