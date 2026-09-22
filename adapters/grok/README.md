# Grok Build CLI copy adapter

`grok` 1.0.40 is the Grok Build TUI. It does not auto-load this repo’s `AGENTS.md` (`grok inspect` reported no project instructions). `--rules` only appends, and that lost. The throwaway profile that replaces the prompt is `adapters/grok/chat-profile.md`. Pass it with `--agent` and the file path. `--agent-profile` is not a flag on `grok -p`. Do not install it into `~/.grok/`.

Do not write `~/.grok/config.toml`. Do not write `~/.config/kilo/`.

## Headless check

From a throwaway directory, not this repo and not the live config:

```text
grok -p "<short status question>" --rules <contents of adapters/tui/AGENTS.md> --max-turns 2 --no-subagents --permission-mode plan
```

`--rules` appends. It does not replace Grok’s own prompt. If the reply is still a telegram, the paste did not win. That is a real result, not a reason to edit the live Kilo window.

`--system-prompt-override` replaces the prompt instead. Use it only when the question is whether this exact text was sent, and say so in the score note.

## Interactive TUI

`grok` with no `-p` opens the TUI. Do not start it against the live Kilo config. A TUI session is not proof of CSS. Score the finished text the same way as `grok -p`: did a question get an answer, in paragraphs, without a px dump.

## What this cannot prove

A CLI reply is not W3C PROV, not the 2026-09-20 session, and not a diff of the live stylesheet.
