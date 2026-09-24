# TUI adapter

OpenCode’s TUI, `kilo run`, and any terminal agent can take two of the five preserved behaviors. They cannot take the webview ones.

## Paste this

`adapters/tui/AGENTS.md` is both fragments in one file. Put that file in the agent instructions that are actually sent. A file that sits in this repo and is not loaded does not count.

OpenCode: `adapters/opencode/README.md`. Grok Build CLI: `adapters/grok/README.md`. Neither may edit the live Kilo config. The global OpenCode instruction file already has its own chat-first rule, so a pass on this machine can be that file rather than this pack.

## Do not paste these

- `kilo-claude-markdown.css` — selectors target the VS Code webview. A terminal will ignore them.
- The hot-reload poller — it fetches a stylesheet into `document`. There is no document.
- The 12-second CSS verify script — there is no webview to patch.

## What “working” means on a TUI

Same short ask as the VS Code gold, then read the text:

- Did a question get an answer, or did tools start a long job?
- Does the reply start with the result, in paragraphs, without a px dump?

If the product also opens a desktop window, screenshot that window and read the PNG. Score that picture for skim. Do not score it against 16px webview type unless that window renders markdown with a stylesheet you control.

## What “working” means on VS Code Kilo

The live window is already the gold. Do not uninstall its CSS or blank `~/.config/kilo/AGENTS.md` to get a before. Apply this pack only to a copy.
