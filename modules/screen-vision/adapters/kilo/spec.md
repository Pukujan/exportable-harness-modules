# Screen vision spec

## Goal

Give the Kilo agent a way to look at any window or the full desktop by capturing a PNG and reading it with the existing image-capable `Read` tool.

## Not in scope

- Click / type computer-use loops
- Auto-routing to a different model
- Always-on screen watching

## Properties

- **P1 Path:** a successful run prints one existing absolute file path.
- **P2 PNG:** the file starts with bytes `89 50 4E 47 0D 0A 1A 0A`.
- **P3 Size:** the file is larger than 8 KB.
- **P4 Dimensions:** width and height are at least 100 px.
- **P5 Stable output:** default output path is `%LOCALAPPDATA%\Temp\kilo\vision\latest.png`.
- **P6 Fallback:** if a named window cannot be found, capture the full virtual desktop instead of failing empty.
- **P7 List:** `-List` prints visible window titles without writing a PNG.
- **P8 CSS gate:** `verify-css.ps1` waits at least 12 seconds after patching before it captures. Agents must not screenshot immediately after a CSS patch.

## Agent contract

1. Run `scripts/screenshot.ps1`.
2. `Read` the printed PNG path.
3. Describe what is on screen. Do not claim you can see the UI without that image.
