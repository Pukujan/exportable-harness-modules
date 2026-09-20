# Screen vision

## Goal

Give the agent a way to look at a window or the desktop by capturing a PNG and reading it. Do not claim the UI is correct without that image.

## Properties

- **P1 Path:** a successful run prints one existing absolute file path.
- **P2 PNG:** the file starts with bytes `89 50 4E 47 0D 0A 1A 0A`.
- **P3 Size:** the file is larger than 8 KB.
- **P4 Dimensions:** width and height are at least 100 px.
- **P5 Stable output:** default output path is `%LOCALAPPDATA%\Temp\kilo\vision\latest.png` on the Kilo adapter (other harnesses may substitute an equivalent).
- **P6 Fallback:** if a named window cannot be found, capture the full virtual desktop instead of failing empty.
- **P7 List:** a list mode prints visible window titles without writing a PNG.
- **P8 CSS gate:** verify-css waits at least 12 seconds after patching before it captures.
- **P9 Desktop width:** a desktop/VS Code capture is at least 1200 px wide (cropped leftovers fail).

## Not in scope

- Click / type computer-use loops
- Auto-routing to a different model
- Always-on screen watching

## Adapter job

1. Capture.
2. Read the PNG with a vision-capable reader.
3. Judge from pixels. Fix and recapture if wrong.
