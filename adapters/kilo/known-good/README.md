# Known-good Kilo overlay

These files are a snapshot of the overlay that the owner said made VS Code Kilo usable (2026-09-21). They are the copy source. They are not a license to overwrite the live config.

- `AGENTS.md` — instructions loaded every turn (routing + writing + screenshot policy).
- `agent-prompt.txt` — the string set on `build`, `code`, `plan`, and `general` so the product’s terse default does not win.

The webview CSS snapshot lives at `modules/prose-type/adapters/kilo/kilo-claude-markdown.css`.

Live paths this was copied from, not to be edited by an experiment:

- `%USERPROFILE%\.config\kilo\AGENTS.md`
- `%USERPROFILE%\.config\kilo\kilo.jsonc` agent prompts
- `%USERPROFILE%\.config\kilo\kilo-claude-markdown.css`
