# Reconstructed audit of the colorful-income Kilo UX session

**Status: RECONSTRUCTED.** This is not the transcript. Source of truth is `artifacts/sessions/ses_f4930aa1affeXv0fw5Syzn0Z8Y.json` (verbatim-redacted).

Session id: `ses_f4930aa1affeXv0fw5Syzn0Z8Y`  
Title: Using local embedding model in IDX  
Worktree: Agent Manager `colorful-income`  
Related live adapters: `%USERPROFILE%\.config\kilo\` and `%USERPROFILE%\.kilo\skills\screen-vision\`

## What the session actually mixed

IDX/Ollama embeddings, Kilo chat type, writing voice, vision capture, and CSS hot-reload. Only the last four become v1 modules. Embeddings stay out of this pack.

## What we built (current Kilo reference)

- Writing contract in global `AGENTS.md` / agent prompts: answer first, no forced TL;DR, real paragraphs, two modes.
- Prose tokens: 16px body, line-height 1.5, h1/h2/h3 22/18/16, `pre-wrap`.
- CSS hot-reload poller + 12s verify gate.
- Screen-vision skill, `/see`, and PNG property tests.

## What we reversed (superseded)

| Dead claim | Replaced by |
|---|---|
| Always-TL;DR | TL;DR only on long writeups |
| Body `0.875rem` | `16px` lock |
| Hide-all-reasoning | Preview while streaming; do not treat “hide forever” as the product rule |
| 3s CSS wait | 12s verify script |
| `assistant-message` as tool-row root | Tool rows are collapsible/tool slots |

## How to cite

Use content hashes in `artifacts/manifest.jsonl` and event `evidence_refs`. If this audit disagrees with the session JSON, the session JSON wins.
