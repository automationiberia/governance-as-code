---
name: gac-governance
description: >-
  Resolves the effective governance (organization rules, exceptions,
  repository classification and checker) that applies to an Ansible task, following the
  Governance as Code method. Used by the gac-auditor, gac-builder,
  gac-librarian and gac-operator skills before they act. Use when you need to
  know which rules apply to a repository, role, playbook, collection or AAP
  object.
---

# Governance as Code — resolve effective governance

Organization rules are **data** in a governance instance. This skill turns
that data into the short list of rules that apply to the current task.

## 1. Locate the instance

1. Read the `Governance as Code` section of the repository's `AGENTS.md`. It
   gives the instance path (for example `governance/`) and version.
2. If there is no such section, ask the user where the governance instance
   is. If the user says there is none, continue with **L0 only** and state
   it clearly in every output.

## 2. Read the manifest

From `<instance>/manifest.yml` take:

| Field | Use |
|-------|-----|
| `instance`, `method_version` | Declare them in your output |
| `bases` | Pinned L0 sources and enabled ai-forge modules |
| `layers` | Where ADRs, rules and exceptions live |
| `promotion_paths` | Repository classification: does the repository reach production? |
| `classification` | Optional objective attributes per repository (for example `criticality`) |
| `gates.checker` | How to run the checker |
| `test_platform` | How disposable test hosts are created (image, start command, privileges, `become`) |

## 3. Determine the scope

| Dimension | How to decide |
|-----------|---------------|
| Content type | `role`, `playbook`, `collection`, `plugin`, `ee`, or `platform` for AAP objects |
| Promotion path | Listed under `promotion_paths.prod` → `prod`; listed under `promotion_paths.nonprod` → `nonprod`; **not listed → treat as `prod`** (deny by default) and suggest classifying it |
| Domain | Only if the manifest declares domains and the repository belongs to one |
| Other attributes | From the manifest `classification`, for example `criticality` |
| Repository | Current repository name (used to match exceptions) |

## 4. Select rules

Read every file under the rules location (and the domain's, if any). Keep a
rule when **all** of these hold:

- `scope.content` contains the content type, or is `[all]`.
- `scope.promotion_path` contains the promotion path, or is `[all]`.
- Any other attribute in `scope` (e.g. `criticality`) matches the
  repository's classification.
- Its `adr` exists and has `status: accepted`. If not, do not apply the rule
  and report the inconsistency.

Read the exceptions location. Keep an exception when its `scope.repository`
matches and `expires` is today or later. Expired exceptions do not apply;
mention them.

## 5. Present the effective governance

Keep it short. Use this exact shape:

```text
Governance: <instance>@<version> · method <method_version> · scope: <content> / <promotion path>
L0: CoP good practices + ansible-lint profile <profile> apply where L1 is silent
L1/L2 rules:
  <id> (<adr>, <layer>, <enforcement>, <verifiability>): <ai_hint>
  ...
Exceptions: <EXC-id rule scope expires> | none
Checker: ansible-lint -c <instance>/<config> [-i <instance>/<ignore_file>]   (run from the content root, no paths)
Test platform: <runtime> · <default image> · become <true|false>
```

Open an ADR only when you need its reasoning (for example to explain a
finding or to judge a heuristic rule).

## 6. Process rules come from the classification

Tests, documentation, reviewers and change approvals are ordinary rules in
the areas `TEST`, `DOC` and `PROC`. Select them exactly like any other rule:
by content type and by the repository classification (promotion path and any
attribute in the manifest `classification`, e.g. `criticality: [high]`).

- The classification is read from the manifest. Never ask the requester to
  choose it, and never infer it from the request.
- If a rule's scope uses an attribute the repository does not have in the
  manifest, the rule does not apply; mention the missing classification.
- When no process rules apply, say so: the method imposes none by itself.

## Rules for every mode

- Never invent a rule. Every rule you apply or report has an id and a source:
  an L1/L2 registry id, `lint:<rule>`, or `cop:<section>`.
- Never edit L0 (CoP, ai-forge, aap-skills).
- Artifacts (audit report, success contract, PR body, ADR) always follow their
  templates in full, whatever conversational style skill is installed (Output
  slot precedence: templates win).
- When governance blocks the task, stop and propose an exception or an ADR
  (gac-librarian); do not work around it.
