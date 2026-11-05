---
description: Audit Ansible content or AAP state against the organization's governance (Auditor mode)
argument-hint: "<path | PR | platform scope>"
---

Use the `gac-auditor` skill to audit `$ARGUMENTS`.

1. Resolve effective governance with the `gac-governance` skill.
2. Run the checker, the community review and the organization heuristics.
3. Produce the audit report and a remediation plan for the Builder.

Do not modify the audited content. The audit report is the only file you
write (default: `reports/audit-<scope>-<date>.md`).
