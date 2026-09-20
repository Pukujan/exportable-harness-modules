---
name: screen-vision
description: Capture any desktop window or the full screen as a PNG and inspect it with vision. Use unprompted after visual/CSS/UI changes. After CSS patches, use the 12s verify script. Do not screenshot immediately after a CSS patch.
---

# Screen vision

Do not wait for the user to ask. Any visual change requires a capture.

## Steps

1. Run this module’s `scripts/screenshot.ps1` (or the harness equivalent).
2. The script prints one path.
3. `Read` that PNG path.
4. Judge from the image. If it is wrong, fix and capture again.

## CSS / hot-reload gate

Do not patch CSS and screenshot in the same breath.

After changing chat CSS, run **only** `scripts/verify-css.ps1` (or the harness equivalent). That script must wait **12 seconds**, then capture. Do not pass a shorter wait.

## Model

Use a vision-capable reader. Do not pretend a text-only model can see the screen.
