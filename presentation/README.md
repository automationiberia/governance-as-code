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
| Side panel · Commands | Terminal (`[TERM]`) and chat (`[CHAT]`) prompts for the live parts |
| 1x | Playback speed |
| ☾ | Light / dark theme |

Direct links (also used for screenshots): `flow.html?flow=ex01&step=1`,
`flow.html?flow=ex03&step=1`, `flow.html?theme=light`.

## Contents

| File | Purpose |
|------|---------|
| [demo-script.md](demo-script.md) | Talk script: live deterministic parts + saved evidence |
| [diagram.json](diagram.json) | **Source** of the presentation: map, chapters, details, side panel |
| [build.py](build.py) | Generates `flow.html` from `diagram.json` and the vendored engine |
| [validate.mjs](validate.mjs) | Validates `diagram.json` with FlowStory's own validator |
| [screenshots.sh](screenshots.sh) | One PNG per chapter ([screenshots/](screenshots/)) — layout review and fallback |
| [vendor/flowstory/](vendor/flowstory/VENDOR.md) | FlowStory engine and stylesheet, pinned to commit `9cac6a4` (Apache-2.0) |

Worked examples live under **[../examples/](../examples/)**. Optional hands-on
AI walkthrough: **[../demo/README.md](../demo/README.md)**.

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
| 4 | Live demo — modernize a 2017 role | Follows [demo/README.md](../demo/README.md): clone → submodule → harness 6/8 → `/audit` → `/build` → guardrail → ansible-lint |
| 5 | **EX-02** — Create a collection | Prod vs lab from the repository map (R-TEST-001) |
| 6 | **EX-03** — A new company rule | Librarian → ADR-0005 → R-COLL-001 → block → exception |
| 7 | **EX-04** — Plug tools into the harness | Slots 8/8 · guardrail live · Evolution |
| 8 | Validation — Fresh AI assistant | Dogfooding: audit, build, lessons |
| 9 | What you get | Six takeaways |

Each **EX-0N** chapter starts with a Story line prefixed `EX-0N · …` so the
section boundary is obvious in the step list. Longer agent runs insert
**Waiting · …** beats so you can narrate what the assistant is doing in
real time without skipping the original example steps.

The text on screen is in English, like the rest of the repository; the
narration can be in any language.
