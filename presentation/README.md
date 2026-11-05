# Presentation — Governance as Code

An animated, interactive walkthrough of the method for a technical and
executive audience, built with [FlowStory](https://github.com/noyitz/flowstory).

## Open it

Double-click **[flow.html](flow.html)**. It is a single self-contained file:
no server, no internet, works in any modern browser.

| Control | Use |
|---------|-----|
| Chapter selector (top right) | Ten chapters, 0 to 9 |
| ▶ Start / Reset | Play the selected chapter |
| Story list | Click a step to jump to it |
| Any box | Click for details and links to the real evidence |
| 1x | Playback speed |
| ☾ | Light / dark theme |

Direct links (also used for screenshots): `flow.html?flow=ex01&step=13`,
`flow.html?theme=light`.

## Contents

| File | Purpose |
|------|---------|
| [demo-script.md](demo-script.md) | Local demo: live part (deterministic) + saved evidence |
| [diagram.json](diagram.json) | **Source** of the presentation: map, chapters, details, side panel |
| [build.py](build.py) | Generates `flow.html` from `diagram.json` and the vendored engine |
| [validate.mjs](validate.mjs) | Validates `diagram.json` with FlowStory's own validator |
| [screenshots.sh](screenshots.sh) | One PNG per chapter ([screenshots/](screenshots/)) — layout review and fallback |
| [vendor/flowstory/](vendor/flowstory/VENDOR.md) | FlowStory engine and stylesheet, pinned to commit `9cac6a4` (Apache-2.0) |

## Change it

```bash
# edit diagram.json, then:
node validate.mjs        # FlowStory schema + every step points to an existing box
python3 build.py         # writes flow.html
./screenshots.sh         # optional: review every chapter's final picture
```

## Chapters

| # | Chapter | Shows |
|---|---------|-------|
| 0 | The problem | Generic community foundations; company rules nowhere; AI improvises |
| 1 | Community first, your rules on top | Layers: baseline, decisions, rules, repository map, exceptions, rule tests |
| 2 | The AI assistant and the trusted zone | Guidance in the assistant (incl. a guardrail on every edit), guarantee in the gates; plug-in points |
| 3 | How people use it | The four modes, set up once |
| 4 | Example: modernize a 2017 role | Audit → what it really does → contract → build → tests → pull request |
| 5 | Example: create a new collection — production vs lab | Two new collections; requirements decided by the repository map |
| 6 | Example: a new company rule | Impact → decision → tests first → rule → blocked draft → expiring exception |
| 7 | Example: plug tools into the harness | Adoption decision → setup "8/8" → guardrail live |
| 8 | We tested it with a fresh AI assistant | Two clean sessions: what they did, and how the method improved |
| 9 | What you get | Six takeaways |

The text on screen is in English, like the rest of the repository; the
narration can be in any language.
