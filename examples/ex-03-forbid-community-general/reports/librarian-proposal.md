# Librarian proposal — forbid community.general in production

```text
Mode: Librarian · Target: governance · Governance: acme@2026.11
```

**Need** (raised by Security, 2026-11-04): production automation must only use
collections covered by a support agreement. `community.general` is a large
community collection without that coverage, and teams keep adding it as a
dependency for one or two modules.

## 1. Check L0 first

| Source | Covers it? |
|--------|------------|
| CoP good practices | No — no guidance on which collections are allowed |
| ansible-lint (any profile) | No — no rule restricts collections |
| ai-forge | No |

→ A new organization rule is justified (`add`), not a `tighten`.

## 2. ADR draft

`ADR-0005 — Forbid community.general in production content` ·
type `security-policy` · status **proposed** · approvers: automation-lead,
security · locked: yes (owner: security).

Decision (delta only): no module, plugin, filter, lookup, dependency or
execution environment content from `community.general` in repositories on
the **prod** promotion path. Alternatives: `ansible.builtin`, `ansible.posix`,
certified collections. Exceptions only through the register, approved by the
rule owner, with expiry.

## 3. Rule draft

| Field | Value |
|-------|-------|
| id | `R-COLL-001` |
| verifiability | mechanical — custom lint rule [r_coll_001.py](../../acme/gates/rules/r_coll_001.py) |
| scope | content: playbook, role, collection, ee · promotion path: prod |
| enforcement | block |
| locked | true · owner: security |

The rule reads scope and exceptions from the instance:

- **Promotion path** from `manifest.yml`. Unclassified repositories are treated
  as **prod** (deny by default): forgetting to register a production repository
  must not switch the rule off.
- **Exceptions** from `exceptions/register.yml`, honoring repository, items,
  paths, approval and expiry. (The ansible-lint ignore file cannot express
  expiry and is shared across repositories.)

## 4. Manifest change

```diff
 promotion_paths:
   prod:
     repositories:
       - ex-01-modernize-ansible-manage-users
       - linux_baseline
+      - firewall_legacy
+      - network_tuning
+  nonprod:
+    repositories:
+      - lab_tools
+      - lab_sandbox
```

`nonprod` becomes explicit because of deny by default.

## 5. Impact (checker with the draft rule, 2026-11-04)

| Repository | Path | Uses community.general | Result |
|------------|------|------------------------|--------|
| ex-01 `manage_users` | prod | no | pass |
| `linux_baseline` | prod | no | pass |
| `network_tuning` | prod | no | pass |
| `lab_tools` | nonprod | no | pass |
| `lab_sandbox` | nonprod | yes (`timezone`) | pass — out of scope |
| **`firewall_legacy`** | prod | **yes** (`ufw` ×2, dependency) | **3 findings** |

Controls:

- `lab_sandbox` checked as an unclassified repository → 2 findings (deny by default works).
- A Builder draft for `network_tuning` using `community.general.ufw` and the
  `community.general.json_query` filter → 3 findings (filters and dependencies
  are detected, not only modules).

## 6. Recommendation

- Enter directly in **block**: only one repository is affected, so a warn
  period and baseline add nothing.
- `firewall_legacy` cannot comply today (legacy Ubuntu hosts, `ufw` has no
  supported alternative until their migration). It should request an
  exception — draft below, to be approved by the rule owner.

## 7. Exception draft (for firewall_legacy)

| Field | Value |
|-------|-------|
| id | `EXC-001` |
| rule | `R-COLL-001` |
| scope | repository `firewall_legacy` · items `community.general.ufw`, `community.general` (dependency) |
| justification | Legacy Ubuntu 20.04 hosts use ufw; they are retired in the Q1 2027 migration |
| expires | 2027-03-31 |
| approved_by | *(pending — rule owner: security)* |

**Everything above is a proposal.** Status changes and approvals are made by
the approvers, not by the Librarian.
