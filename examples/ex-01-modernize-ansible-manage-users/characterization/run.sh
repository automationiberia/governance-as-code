#!/usr/bin/env bash
# Characterization of EX-01: run the original and the modernized role on the
# same starting state, twice, with a password change by the user in between,
# and record the resulting account state.
#   original   : ansible-core 2.15 inside the container (last version accepting `include`)
#   modernized : current controller through the podman connection
# Usage: ./run.sh   (needs podman; ANSIBLE_PLAYBOOK and collection path for the modernized run)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
EX="$(dirname "$HERE")"
IMAGE=registry.access.redhat.com/ubi9/ubi:latest
OUT="$HERE/results"
ANSIBLE_PLAYBOOK="${ANSIBLE_PLAYBOOK:-ansible-playbook}"
mkdir -p "$OUT"

changed_tasks() {  # list tasks that reported a change in a playbook log
  awk '/^TASK \[/{t=$0; sub(/^TASK \[/,"",t); sub(/\] \*+$/,"",t)} /^changed:/{print t}' "$1" | sort | uniq -c
}

simulate_password_change() {  # the user changes the password: last change = today
  podman exec "$1" sh -c 'chage -d "$(date +%F)" oracle'
}

# ---------- original ----------
podman rm -f -t 0 gac-char-orig >/dev/null 2>&1 || true
podman run -d --name gac-char-orig "$IMAGE" sleep infinity >/dev/null
podman exec gac-char-orig sh -c 'dnf -q -y install python3-pip >/dev/null && pip3 -q install "ansible-core==2.15.13" >/dev/null'
podman exec gac-char-orig mkdir -p /work/roles
podman cp "$EX/before/roles/manage-users" gac-char-orig:/work/roles/manage-users
for f in play-original.yml capture_state.py prepare.sh; do podman cp "$HERE/$f" gac-char-orig:/work/$f; done
podman exec gac-char-orig sh /work/prepare.sh
for run in 1 2; do
  [ "$run" = 2 ] && simulate_password_change gac-char-orig
  podman exec -e ANSIBLE_ROLES_PATH=/work/roles -e ANSIBLE_NOCOLOR=1 -w /work gac-char-orig \
    ansible-playbook play-original.yml > "$OUT/original-run$run.log" 2>&1 || echo "original run $run: FAILED (see log)"
  podman exec gac-char-orig python3 /work/capture_state.py > "$OUT/original-state$run.json"
  changed_tasks "$OUT/original-run$run.log" > "$OUT/original-changed$run.txt"
done
podman rm -f -t 0 gac-char-orig >/dev/null

# ---------- modernized ----------
podman rm -f -t 0 gac-char-new >/dev/null 2>&1 || true
podman run -d --name gac-char-new "$IMAGE" sleep infinity >/dev/null
for f in capture_state.py prepare.sh; do podman cp "$HERE/$f" gac-char-new:/tmp/$f; done
podman exec gac-char-new sh /tmp/prepare.sh
printf 'all:\n  hosts:\n    gac-char-new:\n      ansible_connection: containers.podman.podman\n      ansible_python_interpreter: /usr/bin/python3\n' > "$OUT/inventory.yml"
for run in 1 2; do
  [ "$run" = 2 ] && simulate_password_change gac-char-new
  ANSIBLE_ROLES_PATH="$EX/after/roles" ANSIBLE_NOCOLOR=1 ANSIBLE_DEPRECATION_WARNINGS=false \
    "$ANSIBLE_PLAYBOOK" -i "$OUT/inventory.yml" "$HERE/play-modernized.yml" > "$OUT/modernized-run$run.log" 2>&1 || echo "modernized run $run: FAILED (see log)"
  podman exec gac-char-new python3 /tmp/capture_state.py > "$OUT/modernized-state$run.json"
  changed_tasks "$OUT/modernized-run$run.log" > "$OUT/modernized-changed$run.txt"
done
podman rm -f -t 0 gac-char-new >/dev/null
rm -f "$OUT/inventory.yml"
echo "results in $OUT"
