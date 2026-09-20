---
name: screen-vision
description: Capture any desktop window or the full screen as a PNG and inspect it with vision. Use unprompted after visual/CSS/UI changes. After CSS patches, use verify-css.ps1 (12s gate). Do not screenshot immediately after a CSS patch.
---

# Screen vision

Do not wait for the user to ask. Any visual change requires a capture.

## Steps

1. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\pujan\.kilo\skills\screen-vision\scripts\screenshot.ps1" -Target all
```

2. The script prints one path, default `C:\Users\pujan\AppData\Local\Temp\kilo\vision\latest.png`.
3. `Read` that PNG path.
4. Judge from the image. If it is wrong, fix and capture again.

## Targets

Any window on this PC is allowed.

- `-Target all` — every monitor (default)
- `-Target screen` — primary monitor
- `-Target vscode` — VS Code window
- `-Target window -Window "Chrome"` — first visible window whose title contains that text
- `-List` — print process + window titles, then pick one

## CSS / hot-reload gate

Do not patch CSS and screenshot in the same breath. The Kilo webview poller needs time.

After changing `kilo-claude-markdown.css`, run **only** this:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\pujan\.kilo\skills\screen-vision\scripts\verify-css.ps1"
```

That script patches, waits **12 seconds**, then captures VS Code. Do not pass a shorter wait. Do not use `Start-Sleep 2` or `Start-Sleep 3` and then screenshot.

Plain screenshots (no CSS patch) stay immediate:

```powershell
...screenshot.ps1 -Target vscode
```

## Model

Use a vision model. Grok 4.6 can Read PNGs. If the current model cannot, use the `vision` agent (`xai/grok-4.6`).
