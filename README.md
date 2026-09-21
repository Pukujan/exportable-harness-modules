# Exportable harness modules

Start at `PRESERVE.md`. That is the pack.

The owner’s signal (2026-09-21) is the gold: VS Code Kilo was unusable on every model, and after five UX behaviors landed it was usable. Those behaviors are what this repo keeps. A future Kilo config or an OpenCode TUI should copy them. Do not strip the live VS Code install to test a before.

The five behaviors: turn routing, visible chat type, the output prompt that is actually sent, Claude-like paragraph shape, and screenshot-before-claim plus CSS hot reload. Routing and writing transfer to a TUI. CSS and hot reload do not. `kilo run` has no stylesheet.

This repository is also a portable knowledge pack. Another agent should be able to implement the text half from the SPECs. It is **not** a zip of Kilo’s `webview.js`. Kilo files under `adapters/kilo/` are a reference implementation, including `adapters/kilo/known-good/` copied from the working overlay.

FOSSIL can answer what we tried, what we reversed, and which files are the current Kilo reference — **cited to ingested session bytes**, not a reconstructed story.

## Not this pack

- ChatGPT/Claude transcript mining (separate plan)
- IDX / Ollama embedding setup
- Claiming Kilo equals ChatGPT or Claude

## Layout

```text
pack/manifest.json          # pack_id, write_targets, fossil schemas
artifacts/                  # redacted session export, hashes, reconstructed audit
events/                     # durable claim + supersession snapshot
modules/
  turn-routing/             # chat vs research vs code vs long run
  writing-contract/         # SPEC + AGENTS fragment + good/bad transcripts
  prose-type/               # tokens + properties + Kilo CSS adapter
  css-hot-reload/           # recipe + 12s gate + Kilo poller/watcher
  screen-vision/            # SPEC + skill + screenshot.ps1 + tests
checkers/                   # portable property tests (no Kilo UI)
```

## How to implement an adapter

Not the current job. Checkers already pass. A new agent should read `AGENTS.md` and `HANDOFF.md` and wait.

When the owner later asks for a new harness:

1. Read the module `SPEC.md`. Those properties are the contract.
2. Run `python checkers/run_all.py`. It should pass on this repo today.
3. Implement your harness adapter until the portable tests pass.
4. Do **not** copy Kilo selectors unless you are maintaining the Kilo adapter.
5. Keep writing rules and type tokens separate. Claude feels better because of **writing**, then **type**, not 2,000 CSS variables.

## Run the checkers

```text
python checkers/run_all.py
```

No Kilo window is required. Live screenshot capture is optional and is not part of the default suite.

## Evidence rules

- `artifacts/sessions/` is **verbatim-redacted** session export (secrets stripped).
- `artifacts/reconstructed/` is labeled reconstruction. Do not promote it to verbatim evidence.
- Claims in `events/` start as `proposed`. Supersession of killed ideas is recorded. Agents do not self-promote to current-best without the property tests.
