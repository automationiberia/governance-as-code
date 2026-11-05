# Success contract — <what is built or changed>

| | |
|---|---|
| **Kind** | modernize \| new content \| bug fix |
| **Repository** | <name> · classification: <promotion path>[, criticality: <value>] |
| **Governance** | <instance>@<version> |
| **Status** | not approved \| approved by <name/role> on YYYY-MM-DD |

<!-- Keep only the section for this kind of work. -->

## Modernize — what must stay the same

Current behavior, from the audit report or characterized now. State how it was
obtained: **observed** (the original was run) or **described** (read from the
code, to be confirmed by a human).

| # | Behavior | Obtained | Check after the change |
|---|----------|----------|------------------------|
| B1 | <e.g. creates the listed groups with their gid> | observed | <same resulting state> |

### Proposed deviations — need approval

| # | Today | After | Why (rule, finding) | Approved |
|---|-------|-------|---------------------|----------|
| D1 | <e.g. password defaults to the user name> | <required input, no default> | R-SEC-001 | yes / no |

## New content — acceptance criteria

| # | Given | When | Then |
|---|-------|------|------|
| A1 | <starting state> | <the content runs with these inputs> | <observable result> |
| A2 | <state after A1> | <it runs again> | <no changes reported> |

## Bug fix — reproduction

| | |
|---|---|
| Starting state | <...> |
| Steps | <...> |
| Wrong result today | <...> |
| Expected result | <...> |

## Verification

| | |
|---|---|
| Process rules that apply | <e.g. R-TEST-001> or none |
| How each item is checked | <automated test on the test platform \| run with assertions \| syntax check> |
| Test platform | <from manifest.yml → test_platform> |
| Out of scope | <...> |
