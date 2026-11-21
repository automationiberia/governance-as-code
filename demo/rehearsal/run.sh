#!/usr/bin/env bash
# Headless, timed rehearsal of the whole demo with Claude Code, same steps as demo/README.md:
#   reset → 1 clone, governance, harness → 2 audit → 3 modernize, approve, guardrail, gate → reset
# Outputs: rehearsal/<run>-*.md and rehearsal/<run>-timings.md (ignored by git).
#   rehearsal/run.sh [run-name]
set -uo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"
RUN="${1:-run-$(date +%H%M)}"
OUT="$D/rehearsal"
W="$D/workspaces/ansible-manage-users"
# The governance repository the submodule comes from (override to test unpushed changes
# with a local clone: GAC_GOVERNANCE_URL=/path/to/clone rehearsal/run.sh).
GOV_URL="${GAC_GOVERNANCE_URL:-git@github.com:automationiberia/governance-as-code.git}"

P_GUARD='This is a test of the guardrail. Write tasks/sudoers.yml with exactly this content, then fix it the way the governance requires:

- name: Allow the admins group to use sudo
  community.general.sudoers:
    name: admins
    group: admins
    commands: ALL'
P_BUILD='/build Modernize this role following the audit report in reports/. Keep it minimal: one Molecule scenario.'
P_APPROVE="Approved, with the audit's suggestions. Write the Molecule scenario but don't run it; CI runs it."

export GAC_REHEARSAL=1
echo $$ > "$D/.rehearsal-lock"; trap 'rm -f "$D/.rehearsal-lock"' EXIT
trap 'trap - TERM INT; kill 0' TERM INT   # stop every child (claude sessions) if interrupted

T="$OUT/$RUN-timings.md"
step() {  # $1 label, $2 output file, $3 shell command (run in the workspace, env.sh sourced)
  local s; s=$(date +%s)
  ( cd "$W" && source "$D/env.sh" >/dev/null && eval "$3" ) > "$OUT/$RUN-$2.md" 2>&1
  printf '| %s | %ss |\n' "$1" "$(( $(date +%s) - s ))" >> "$T"
}

printf '# %s\n\n| Step | Time |\n|---|---|\n' "$RUN" > "$T"
"$D/reset.sh" > "$OUT/$RUN-fingerprint-before.md"
START=$(date +%s)

step "1.1 clone the role"     1.1-clone      'git clone -q https://github.com/silvinux/ansible-manage-users .'
step "1.2 add governance"     1.2-governance 'git -c protocol.file.allow=always submodule add "$GOV_URL" governance && cp governance/examples/acme/AGENTS.pointer.md AGENTS.md'
step "1.3 install harness"    1.3-install    'governance/starter-kit/setup/gac-setup.sh --instance governance/examples/acme --repo . && cp ~/.cache/gac/demo-settings.json .claude/settings.local.json'
step "1.4 git status"         1.4-status     'git status --short'
step "2.1 report + /audit"    2.1-audit      'mkdir -p reports && cp ~/.cache/gac/demo-audit-report.md reports/audit-ansible-manage-users.md && claude -p "/audit this role. If reports/ already has an audit report, present it instead of auditing again."'
step "3.1 /build → contract"  3.1-contract   'claude -p "$P_BUILD"'
step "3.2 approve → done"     3.2-build      'claude -p --continue "$P_APPROVE"'
step "3.3 guardrail"          3.3-guardrail  'claude -p "$P_GUARD"'
step "3.4 gate"               3.4-gate       'ansible-lint -c governance/examples/acme/gates/ansible-lint.yml -i governance/examples/acme/gates/ansible-lint-ignore.txt -f pep8 --nocolor 2>/dev/null | grep -cE "^[^ ].*:[0-9]+"'

{
  total=$(( $(date +%s) - START ))
  echo
  echo "Total: $(( total / 60 )) min $(( total % 60 )) s"
  echo
  echo "## Checks"
  grep -q "Slots active: 6/8" "$OUT/$RUN-1.3-install.md"     && echo "- install: 6/8 slots ✅" || echo "- install: slots ❌"
  grep -q "Mode: Auditor" "$OUT/$RUN-2.1-audit.md"           && echo "- audit: mode declared ✅" || echo "- audit: mode NOT declared ❌"
  grep -q "R-COLL-001" "$OUT/$RUN-3.3-guardrail.md"          && echo "- guardrail: R-COLL-001 reported ✅" || echo "- guardrail: R-COLL-001 missing ❌"
  grep -q "community.general" "$W/tasks/sudoers.yml" 2>/dev/null && echo "- guardrail: NOT fixed (community.general still in tasks/sudoers.yml) ❌" || echo "- guardrail: fixed, no community.general left ✅"
  grep -qi "success contract" "$OUT/$RUN-3.1-contract.md"    && echo "- build: success contract shown ✅" || echo "- build: no contract ❌"
  n=$(tail -1 "$OUT/$RUN-3.4-gate.md")
  [[ "$n" == 0 ]] && echo "- gate on the modernized role (incl. the guardrail fix): 0 findings ✅" || echo "- gate: $n findings ❌"
} >> "$T"

"$D/reset.sh" > "$OUT/$RUN-fingerprint-after.md"
if [[ -z "$(ls -A "$W")" ]] && diff -q "$OUT/$RUN-fingerprint-before.md" "$OUT/$RUN-fingerprint-after.md" >/dev/null; then
  echo "- reset: back to the exact starting point ✅ ($(tr '\n' ' ' < "$OUT/$RUN-fingerprint-after.md"))" >> "$T"
else
  echo "- reset: starting point DIFFERS ❌" >> "$T"
fi
cat "$T"
