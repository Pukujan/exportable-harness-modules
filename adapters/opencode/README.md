# OpenCode copy adapter

This is a throwaway instruction surface. It is not a license to edit `~/.config/opencode/` or `~/.config/kilo/`.

OpenCode’s TUI is installed on this machine (`opencode`, default command). The scored check is headless `opencode run`, because an interactive TUI does not finish a reply this pack can read. CSS still does not transfer.

## What to send

Copy `adapters/tui/AGENTS.md` into a **new directory** as `AGENTS.md`. Point `opencode run --dir` at that directory. A file that stays in this repo and is not loaded does not count.

Do not paste `kilo-claude-markdown.css`, the hot-reload poller, or the 12-second webview script.

## Contamination

OpenCode also loads `~/.config/opencode/AGENTS.md`. That global file already contains a chat-first rule. A pass on this machine can be that file, not this pack. A clean copy test needs a config directory that is not the live one. This adapter does not create that isolation by itself, and it must not overwrite the live file to get it.

## Score the text

Same short ask as the VS Code gold:

- Did a question get an answer, or did tools start a long job?
- Does the reply start with the result, in paragraphs, without a px dump?

That score is a later text check. It is not the 2026-09-20 session export, and it cannot confirm 16px type.
