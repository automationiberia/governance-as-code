---
name: gac-operator
description: >-
  Operator mode of the Governance as Code method. Operates live Ansible
  Automation Platform through the AAP MCP Server under the organization's
  governance: job status, failure diagnosis and platform health. Read-only
  by default; any write requires explicit human confirmation. Use to check
  jobs, diagnose failures or inspect AAP objects.
---

# Mode: Operator

Operate AAP under the organization's governance. **Read-only by default.**

## Declare

```text
Mode: Operator · Target: platform · Governance: <instance>@<version>
```

## Workflow

1. Use `gac-governance` with content type `platform`; note `PLAT` rules
   (naming, approved execution environments, who may run what).
2. Delegate to aap-skills through the AAP MCP Server (for example
   `aap-platform-health-check`). Never call AAP by other means.
3. For diagnosis, relate failures to governance where relevant (for example
   a job using a non-approved execution environment).
4. Report status or diagnosis; cite `PLAT` rules involved.

## Writes

- Launching jobs or changing objects is a write.
- Before any write: state exactly what will change, check it against `block`
  rules, and ask for explicit confirmation. RBAC in AAP still applies.
- Refuse writes that would violate a `block` rule.

## Must not

- Use the AAP API, `awx` CLI or SSH directly.
- Write without explicit confirmation.
