#!/usr/bin/env bash
# Plan B without AI: the same gates, run by hand. Deterministic, seconds each.
#   fallback/checker.sh legacy      # the 2017 role: dozens of findings
#   fallback/checker.sh modernized  # the modernized role (EX-01 after): 0
#   fallback/checker.sh guardrail   # what the assistant receives on a forbidden write
#   fallback/checker.sh collections # EX-02: prod and lab collections, both 0
set -uo pipefail
D="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "${GAC_REPO:-$D/..}" && pwd)"
export PATH="$HOME/.cache/gac/venv/bin:$PATH" ANSIBLE_COLLECTIONS_PATH="$HOME/.cache/gac/collections"
C="$REPO/examples/acme/gates/ansible-lint.yml"
show() { printf '\n\033[1;36m$ %s\033[0m\n' "$*"; }
lint() {  # $1 dir, $2 repository name
  ( cd "$1" && GAC_REPOSITORY="$2" ansible-lint -c "$C" -f pep8 --nocolor --offline 2>/dev/null ) \
    | grep -E '^[^ ].*:[0-9]+' > /tmp/gac-demo-lint.txt
  local n; n=$(wc -l < /tmp/gac-demo-lint.txt)
  grep -E 'R-[A-Z]+-[0-9]+' /tmp/gac-demo-lint.txt | head -5
  head -5 /tmp/gac-demo-lint.txt | grep -vE 'R-[A-Z]+-[0-9]+' | head -3
  printf '\033[1m→ %s finding(s)\033[0m\n' "$n"
}
case "${1:-}" in
  legacy)
    # Same layout as the live workspace (role + governance/ at the root), in a scratch copy
    T="$(mktemp -d /tmp/gac-fallback.XXXX)"
    cp -r "$REPO/examples/ex-01-modernize-ansible-manage-users/before/roles" "$T/"
    cp -r "$REPO/examples/acme" "$T/governance"; git -C "$T" init -q
    show "ansible-lint -c governance/gates/ansible-lint.yml   # the 2017 role"
    C="$T/governance/gates/ansible-lint.yml"; lint "$T" legacy-users
    rm -rf -- "$T" ;;
  modernized)
    show "ansible-lint -c governance/gates/ansible-lint.yml   # the modernized role"
    lint "$REPO/examples/ex-01-modernize-ansible-manage-users/after" ex-01-modernize-ansible-manage-users ;;
  guardrail)
    W="$REPO/examples/ex-04-harness-slots/demo-repo"
    show "cat roles/firewall/tasks/main.yml"; cat "$W/roles/firewall/tasks/main.yml"
    show "# the assistant writes that file → the hook runs"
    echo "{\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$W/roles/firewall/tasks/main.yml\"}}" \
      | CLAUDE_PROJECT_DIR="$W" python3 "$REPO/starter-kit/hooks/gac_checker_on_edit.py"
    printf '\033[1m→ exit %s (2 = shown to the assistant)\033[0m\n' "$?" ;;
  collections)
    show "ansible-lint   # acme.linux_baseline — production"
    lint "$REPO/examples/ex-02-create-collection/linux_baseline" linux_baseline
    show "ansible-lint   # acme.lab_tools — lab"
    lint "$REPO/examples/ex-02-create-collection/lab_tools" lab_tools ;;
  *) sed -n 2,7p "$0" ;;
esac
