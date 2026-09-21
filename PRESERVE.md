# What to preserve

Owner signal, 2026-09-21: Kilo in VS Code was unusable on every model. After the behaviors below landed, the same product was usable, and the owner said it was working extremely well. That observation is the acceptance gold for this pack. It outranks a string checker.

Do not strip the live VS Code install to recreate a before. The live window is the after. Copy from this repo onto a **new** config or a TUI. Never overwrite `~/.config/kilo/` or the installed extension `dist/` to run an experiment.

## The five behaviors

| # | Behavior | What the person notices | Transfers to a TUI? |
| --- | --- | --- | --- |
| 1 | Turn routing | A question gets an answer. Research stays research. Code stays code. A long job starts only after `/goal` and an explicit go, then it does not stall. | Yes. Prompt only. |
| 2 | Visible type | Chat prose is large enough to skim. Headings step up. Code wraps. | No. This is a webview stylesheet. A terminal has no `[data-component=markdown]`. |
| 3 | Output prompt | The model is told to write a briefing, not a telegram, and that instruction is actually sent. | Yes. Paste into the agent prompt. |
| 4 | Paragraph shape | Answer first. Real paragraphs. Bold the takeaway. No forced TL;DR on a short reply. No px / path dump unless they asked to edit a file. | Yes. Same prompt. |
| 5 | Look, then claim | CSS and “does it look right” work is not done until a screenshot is read. CSS edits wait 12 seconds, then capture. Hot reload avoids a window reload for CSS-only edits. | Only if that product has a window. `kilo run` and a bare TUI have no CSS to hot-reload. |

## Where the known-good text lives

- Turn routing: `modules/turn-routing/AGENTS.fragment.md`
- Writing and paragraph shape: `modules/writing-contract/AGENTS.fragment.md`
- Exact file that is working in VS Code today: `adapters/kilo/known-good/AGENTS.md`
- Prompt string sent on `build` / `code` / `plan` / `general`: `adapters/kilo/known-good/agent-prompt.txt`
- Webview CSS: `modules/prose-type/adapters/kilo/kilo-claude-markdown.css`
- Hot reload and 12s gate: `modules/css-hot-reload/`
- Screenshot policy: `modules/screen-vision/`

## How to apply without risking the gold window

**Kilo, new machine or throwaway config.** Copy the known-good instruction file and the agent prompt into that config. Copy the CSS only if that Kilo has a webview. Do not point the experiment at the config that already works.

**OpenCode TUI, or any terminal agent.** Paste turn routing and the writing fragment into that agent’s instructions. Skip the CSS, the poller, and the 12s webview gate. Score the text: did it answer, did it jump, is the paragraph skimmable. If a desktop window is open, screenshot that window. Do not pretend the terminal rendered 16px prose.

**CLI `kilo run`.** Text only. It can confirm routing and writing. It cannot confirm CSS.

## What this pack is not

It is not a claim that these sentences were counted out of ChatGPT transcripts. Turn routing was owner-taught after a jump, then written down because it worked. The type rules were fit to how Claude chat *looks* (about 16px prose, heading steps, wrapping code), not a saved Claude message. The owner’s “this is usable” is the result. A later vision compare may sit beside that signal. It does not replace it.
