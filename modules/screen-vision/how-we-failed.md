# How we failed (vision)

| Killed claim | Why it failed | Current property |
|---|---|---|
| “It looks right” from CSS text | The 0.875rem pass compiled and still rendered ~11px. | Capture then Read |
| Cropped leftover PNGs | Old shots were far under 1200 px wide and were not the live window. | **P9** width ≥ 1200 |
| Immediate screenshot after patch | Hot-reload had not applied. | **P8** / css-hot-reload **H1** |
