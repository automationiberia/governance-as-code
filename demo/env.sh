# The presenter's shell setup, done once before the demo, in the IDE terminal
# (bash or zsh). From workspaces/ansible-manage-users:   source ../../env.sh
# It only prepares tools; every demo command is literal.
if [ -n "${ZSH_VERSION:-}" ]; then
  eval '_gac_env_file="${(%):-%x}"'
else
  _gac_env_file="${BASH_SOURCE[0]}"
fi
DEMO_DIR="$(cd "$(dirname "$_gac_env_file")" && pwd)"
unset _gac_env_file
export DEMO_DIR

# The pinned tools (ansible-lint, molecule, lola...) prepared by: demo/reset.sh --machine
export PATH="$HOME/.cache/gac/venv/bin:$PATH"
export ANSIBLE_COLLECTIONS_PATH="$HOME/.cache/gac/collections"

if [ -n "${ZSH_VERSION:-}" ]; then
  PROMPT='%B%F{magenta}acme%f%b:%1~ %# '
else
  PS1='\[\e[1;35m\]acme\[\e[0m\]:\W\$ '
fi

[ -d "$DEMO_DIR/workspaces/ansible-manage-users" ] && cd "$DEMO_DIR/workspaces/ansible-manage-users"
if command -v ansible-lint >/dev/null && command -v lola >/dev/null; then
  echo "tools: ok"
else
  echo "tools: MISSING — run: $DEMO_DIR/reset.sh --machine"
fi
