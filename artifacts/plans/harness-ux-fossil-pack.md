# HISTORICAL — do not execute

This plan is done as far as this repo is concerned. The GitHub repo is not empty. Do not ingest fossil-core from here. Do not search other folders for the task. Current instructions: `AGENTS.md`, then `HANDOFF.md`, then `PRESERVE.md`.

# Fossil this Kilo UX session + exportable harness modules

Separate from `.kilo/plans/chatgpt-harness-export.md` (ChatGPT/Claude work-mode habits). This plan is **this colorful-income Kilo thread**: embeddings, chat CSS, writing voice, vision, hot-reload — turned into durable FOSSIL evidence and a pack other agents can rebuild from.

## Where this session lives

Not in the hades git tree.

| What | Where |
|---|---|
| Kilo session | Agent Manager worktree `colorful-income`; session started as “Using local embedding model in IDX” (`ses_f4930aa1affeXv0fw5Syzn0Z8Y` and related `session_share` / `session_diff` JSON under `C:\Users\pujan\.local\share\kilo\storage\`) |
| Live adapters | `C:\Users\pujan\.config\kilo\` (CSS, AGENTS.md, kilo.jsonc, patch/hot-reload/watcher) and `C:\Users\pujan\.kilo\skills\screen-vision\` |
| Target pack repo | https://github.com/Pukujan/exportable-harness-modules (**empty**) |
| Durable ingest | https://github.com/Pukujan/fossil-core (`research-ingestion` skill, `/ingest`, MCP `fossil.propose` / `fossil.commit`) |

There is no skill literally named `fossil-ingest`. Use **research-ingestion** + reviewed `/ingest` / propose-then-commit. Preserve **source bytes first**; do not treat this chat’s summaries as verbatim evidence.

## Split of duties

**fossil-core:** immutable session export, content hashes, claims with lifecycle (`PROPOSED` → evidenced → **SUPERSEDED** when we reversed ourselves). Agents propose; gates commit.

**exportable-harness-modules:** the **portable knowledge pack** + module SPECs, red tests, goldens, Kilo reference adapters. Other harnesses **build** from properties; they do not need Kilo’s `webview.js`.

Do not put IDX/Ollama or the ChatGPT observe-before-code pack in this repo’s v1 modules.

## Phase 1 — Capture the session as evidence

1. Export the Kilo session JSON (and this audit) into the pack as **raw artifacts**. Label reconstructions (the deep audit) as reconstructed, not as the transcript.
2. Strip secrets (`auth.json`, `KILO_SERVER_PASSWORD`, tokens).
3. Ingest into a local FOSSIL node / reviewed `/ingest` with pack write scoped to the new pack id.
4. Record **supersession events** for claims we later killed (examples: always-TL;DR, 0.875rem, hide-all-reasoning, 3s CSS wait, `assistant-message` as tool-row root).

## Phase 2 — Pack layout in `exportable-harness-modules`

```text
pack/manifest.json          # pack_id, write_targets, fossil schemas
artifacts/                  # session export, screenshots, hashes
events/                     # or generate via fossil-core then snapshot
modules/
  writing-contract/         # SPEC + AGENTS fragment + good/bad transcripts
  prose-type/               # tokens + properties + Kilo CSS adapter
  css-hot-reload/           # recipe + 12s gate + Kilo poller/watcher
  screen-vision/            # SPEC + skill + screenshot.ps1 + tests
README.md                   # how an agent implements an adapter from SPEC
```

Each module: **SPEC (properties)** → **red tests** → **golden pass/fail** (shots + sample replies) → **optional Kilo adapter** → **“how we failed”**.

## Phase 3 — Checkers future agents must be able to run

Portable (no Kilo UI):

- Writing: sample reply must start with the answer, no forced TL;DR, paragraphs longer than two lines, no px/jsonc dump unless asked.
- Vision: PNG magic, min size, width ≥ 1200 for a desktop capture, 12s wait in CSS-verify script.
- Tokens: 16px body, line-height 1.5, h1/h2/h3 22/18/16, `pre-wrap`.

Kilo-only checkers stay under `adapters/kilo/`.

## Phase 4 — What we will not do here

- ChatGPT/Claude transcript mining (other plan).
- Claiming Kilo = ChatGPT.
- Shipping only patched `dist/webview.js` as “the module.”
- Promoting chat claims to `CURRENT_BEST` without the property tests.

## Success

Another agent, given only this repo + SPEC, can implement OpenCode/Pi/Kilo adapters and fail/pass the red tests. FOSSIL can answer: what we tried, what we reversed, and which files are the current Kilo reference — **cited to the ingested session bytes**, not a reconstructed story.
