# Vendored: FlowStory

| | |
|---|---|
| Source | https://github.com/noyitz/flowstory |
| Commit | `9cac6a417f9d` (2026-05-11) |
| Files | `dist/flowstory.min.js`, `templates/style.css`, `LICENSE` — unmodified |
| License | Apache-2.0 (see [LICENSE](LICENSE)) |

Pinned and local so the presentation works offline and does not change if the
upstream site changes. `../build.py` inlines these files into `flow.html` and
replaces, in the generated output only, the inspector's HTTP labels
("Request", "Headers", "Body"…) with presentation labels. These files stay
unmodified.
