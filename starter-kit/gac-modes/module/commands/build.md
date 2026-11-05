---
description: Create or modernize Ansible content under the organization's governance (Builder mode)
argument-hint: "<what to build | 'fix findings in <audit report>'>"
---

Use the `gac-builder` skill for: `$ARGUMENTS`.

1. Run intake: what, why, target repository.
2. Resolve effective governance with the `gac-governance` skill.
3. Build through ai-forge skills, then loop on the checker until no `block`
   findings remain.
4. Summarize changes and the rules applied. Do not commit unless asked.
