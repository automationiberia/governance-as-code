#!/usr/bin/env bash
# Governance as Code — set up a content repository for an AI assistant.
#
# 1. Creates/updates a Python virtualenv with the pinned tools (checker, tests, Lola).
# 2. Applies and verifies the instance's harness slots (gac_setup.py): community
#    and method modules, MCP servers, hooks, test platform, instance checks —
#    every entry pinned and traced to an ADR in the instance manifest.
#
# Usage:
#   gac-setup.sh --instance <governance-instance-dir> --repo <content-repo-dir>
#                [--assistant claude-code] [--scope project|user]
#                [--with-recommended] [--venv <dir>] [--no-tools]
set -euo pipefail

METHOD_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CACHE="${GAC_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/gac}"
VENV="$CACHE/venv"
TOOLS=1
ARGS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --venv) VENV="$2"; shift 2 ;;
    --no-tools) TOOLS=0; shift ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

if [ "$TOOLS" = 1 ]; then
  printf '==> Python tools in %s\n' "$VENV"
  [ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -r "$METHOD_ROOT/starter-kit/environment/requirements.txt"
  # Scope the collections path during install: otherwise ansible-galaxy skips
  # collections already present in other default paths, which are not on the
  # ANSIBLE_COLLECTIONS_PATH used afterwards.
  ANSIBLE_COLLECTIONS_PATH="$CACHE/collections" "$VENV/bin/ansible-galaxy" collection install \
    -r "$METHOD_ROOT/starter-kit/environment/requirements.yml" -p "$CACHE/collections" \
    | grep -E "installed successfully|already installed|ERROR" || true
fi

status=0
"$VENV/bin/python" "$METHOD_ROOT/starter-kit/setup/gac_setup.py" --cache "$CACHE" "${ARGS[@]}" || status=$?

cat <<EOF

Before working, in your shell:
  export PATH="$VENV/bin:\$PATH"
  export ANSIBLE_COLLECTIONS_PATH="$CACHE/collections"
EOF
exit $status
