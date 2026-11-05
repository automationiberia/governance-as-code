#!/usr/bin/env bash
# Regenerate one PNG per chapter (its final step) from flow.html, with headless Chrome.
# Useful to review the layout and as a fallback if the browser fails during the talk.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CHROME="${CHROME:-google-chrome}"
mkdir -p "$HERE/screenshots"
rm -f "$HERE"/screenshots/*.png
python3 - "$HERE/diagram.json" <<'PY' | while read -r idx key steps; do
import json, sys
d = json.load(open(sys.argv[1]))
for i, key in enumerate(d["flowOrder"]):
    print(i, key, len(d["flows"][key]["steps"]))
PY
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 \
    --virtual-time-budget=8000 --screenshot="$HERE/screenshots/$(printf '%02d' "$idx")-$key.png" \
    "file://$HERE/flow.html?flow=$key&step=$steps" 2>/dev/null
  echo "screenshots/$(printf '%02d' "$idx")-$key.png"
done
