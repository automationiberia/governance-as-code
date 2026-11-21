#!/usr/bin/env bash
# Leave the demo at its real starting point: an empty folder, workspaces/ansible-manage-users,
# where the IDE is opened. Everything else happens live: the team clones the role
# (github.com/silvinux/ansible-manage-users) and adds the governance as a submodule
# (github.com/automationiberia/governance-as-code).
#
#   ./reset.sh             # before every rehearsal — with no IDE or terminal inside workspaces/
#   ./reset.sh --machine   # once per laptop: warm ~/.cache/gac (tools, collections, pinned
#                          # bases, test image) so the live setup takes seconds, offline
set -euo pipefail

DEMO="$(cd "$(dirname "$0")" && pwd)"
METHOD="$(cd "$DEMO/.." && pwd)"
[[ "$(basename "$DEMO")" == "demo" && -f "$METHOD/examples/acme/manifest.yml" ]] \
  || { echo "refusing: $DEMO is not governance-as-code/demo" >&2; exit 1; }

# Refuse while a headless rehearsal is using the workspace (rehearsal/run.sh).
if [[ -z "${GAC_REHEARSAL:-}" && -f "$DEMO/.rehearsal-lock" ]] && kill -0 "$(cat "$DEMO/.rehearsal-lock")" 2>/dev/null; then
  echo "a rehearsal is running on the workspace (pid $(cat "$DEMO/.rehearsal-lock")); wait for it to finish" >&2; exit 1
fi

# Fixed identity and dates: every reset produces the same commit hashes.
export GIT_AUTHOR_NAME=demo GIT_AUTHOR_EMAIL=demo@example.com
export GIT_COMMITTER_NAME=demo GIT_COMMITTER_EMAIL=demo@example.com
export GIT_AUTHOR_DATE="2026-01-01T00:00:00Z" GIT_COMMITTER_DATE="2026-01-01T00:00:00Z"

if [[ "${1:-}" == "--machine" ]]; then
  scratch="$DEMO/.machine-scratch"
  rm -rf -- "$scratch"; mkdir -p "$scratch"; git -C "$scratch" init -q
  cp -r "$METHOD/examples/acme" "$scratch/governance"
  # Full setup, recommended slots included, so every pinned base and binary is cached.
  "$METHOD/starter-kit/setup/gac-setup.sh" --instance "$scratch/governance" --repo "$scratch" --with-recommended \
    | grep -E "^Slots active|failed|ERROR" || true
  rm -rf -- "$scratch"
  echo "machine ready: $(du -sh "$HOME/.cache/gac" | cut -f1) in ~/.cache/gac"
  exit 0
fi

rm -rf -- "$DEMO/workspaces" "$DEMO/remotes"
mkdir -p "$DEMO/workspaces"

# The folder the IDE opens; step 1.1 clones the role into it.
mkdir -p "$DEMO/workspaces/ansible-manage-users"

# Demo-only settings for the AI chat (copied in step 1.2): the pre-approved commands of
# permissions.json, plus the pinned tools on PATH — the IDE chat does not inherit the
# terminal environment.
python3 - "$DEMO/permissions.json" "$DEMO/workspaces/demo-settings.json" <<'EOF'
import json, os, sys
settings = json.load(open(sys.argv[1]))
home = os.path.expanduser("~")
settings["env"] = {
    "PATH": f"{home}/.cache/gac/venv/bin:/usr/local/bin:/usr/bin:/bin",
    "ANSIBLE_COLLECTIONS_PATH": f"{home}/.cache/gac/collections",
}
json.dump(settings, open(sys.argv[2], "w"), indent=2)
EOF

echo "ready: workspaces/ansible-manage-users (empty) · workspaces/demo-settings.json"
