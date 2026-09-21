# Turn routing

## Goal

The agent picks the phase from the message in front of it. A question is not a long job. A frozen `/goal` plus an explicit go is not a chat.

## Properties

- **R1 Chat.** Status, why, and what-is-stopping questions get a full answer. Look if needed. Do not start a long task.
- **R2 Go-ahead.** “Let’s do it” without `/goal` and an explicit go is still chat. Explain, then wait.
- **R3 No-stop.** After `/goal` is set, the plan is frozen, and the owner says go, do not idle and do not ask for another continue.
- **R4 Research stays research.** A look burst is not permission to edit.
- **R5 Code stays code.** Implementation does not get a UX rewrite. Talk-to-user text does not get crushed into a patch log.
- **R6 Default personality loses.** A product line that says “accomplish the task, do not chat” does not override R1–R3.

## Not in scope

- Tool-name histograms
- SWE-bench or a public coding exam
- CSS, fonts, or terminal themes

## Adapter job

Paste `AGENTS.fragment.md` into the harness instruction surface so it is sent on every turn. A TUI can do this. A webview is not required.

## Provenance

Owner-taught 2026-09-20 after a status question was treated as a long job. Preserved 2026-09-21 because the owner named this routing as one of the behaviors worth keeping. Not a corpus count.
