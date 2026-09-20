# Writing contract

## Goal

Human-facing answers should read like a careful briefing: start with the answer, then explain. Source code and diffs stay correctness-first.

## Properties

- **W1 Answer first.** The first sentence states the result. Do not open with throat-clearing or a heading on a tiny task.
- **W2 No forced TL;DR.** `## TL;DR` is allowed only on long writeups (research, handoffs, multi-part decisions). Ordinary chat replies must not start with it.
- **W3 Real paragraphs.** At least one paragraph has three or more sentences, or a paragraph that occupies more than two lines. Do not crush the reply into 1–4 dense lines. Do not break every 2–3 lines.
- **W4 No implementation dump.** Unless the user asked to edit a file, do not dump `px`, `rem`, `jsonc`, CSS selectors, class names, or tool traces.
- **W5 Two modes.** Talk-to-user text optimizes for skim. Code/tests/diffs optimize for correctness.
- **W6 Notice, then why.** Explain what the user will notice, then why it matters.

## Not in scope

- Restyling source files, linters, or diffs for UX
- Cloning another product’s chrome, serif, or artifact cards

## Adapter job

Copy `AGENTS.fragment.md` (or equivalent) into the harness instruction surface. Do not implement this with CSS.
