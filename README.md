# Exportable harness modules

Start at `PRESERVE.md`. That is the pack.

The owner’s signal (2026-09-21) is the gold: VS Code Kilo was unusable on every model, and after five UX behaviors landed it was usable. Those behaviors are what this repo keeps. A future Kilo config or an OpenCode TUI should copy them. Do not strip the live VS Code install to test a before.

The five behaviors: turn routing, visible chat type, the output prompt that is actually sent, Claude-like paragraph shape, and screenshot-before-claim plus CSS hot reload. Routing and writing transfer to a TUI. CSS and hot reload do not. `kilo run` has no stylesheet.

This repository is also a portable knowledge pack. Another agent should be able to implement the text half from the SPECs. It is **not** a zip of Kilo’s `webview.js`. Kilo files under `adapters/kilo/` are a reference implementation, including `adapters/kilo/known-good/` copied from the working overlay.

Two tests are different. Read `pack/evidence.md` before citing history. A **copy test** (known-good files, or `adapters/tui/AGENTS.md` on a throwaway config, plus `python checkers/run_all.py`) can be run today. A **path test** cannot. The 2026-09-20 export is a redacted session plus a proposed FOSSIL receipt. It is not W3C PROV, not an ordered diff of the live config, and not the 2026-09-21 transcript.

## Not this pack

- ChatGPT/Claude transcript mining (separate plan)
- IDX / Ollama embedding setup
- Claiming Kilo equals ChatGPT or Claude

## Layout

```text
pack/manifest.json          # pack_id, write_targets, fossil schemas
pack/evidence.md            # copy test vs path test; what may be cited
artifacts/                  # redacted session export, hashes, reconstructed audit
events/                     # proposed claim + supersession snapshot, not accepted
modules/
  turn-routing/             # chat vs research vs code vs long run
  writing-contract/         # SPEC + AGENTS fragment + good/bad transcripts
  prose-type/               # tokens + properties + Kilo CSS adapter
  css-hot-reload/           # recipe + 12s gate + Kilo poller/watcher
  screen-vision/            # SPEC + skill + screenshot.ps1 + tests
checkers/                   # portable property tests (no Kilo UI)
adapters/tui/AGENTS.md      # routing + writing paste for a throwaway TUI
adapters/opencode/          # OpenCode copy notes; do not edit the live config
adapters/grok/              # Grok Build CLI copy notes; pass --rules
```

## Say install

Point the agent at this repo and say install. If that agent loads this file or `AGENTS.md`, it runs `python install.py install`. That stages a bundle under `dist/install` and refuses the live Kilo, Grok, and OpenCode configs. The receipt in that bundle is the one line that points their harness at the staged files. A file that stays in this repo and is not loaded does nothing.

## How to implement an adapter

Building a new harness from scratch is not the current job. Checkers already pass. The text-half copy test is `adapters/tui/AGENTS.md` on a throwaway directory, scored by `adapters/opencode/README.md` or `adapters/grok/README.md`. Do not point that test at the live Kilo config.

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

The contract is `pack/evidence.md`. Short form:

- `artifacts/sessions/` is a **verbatim-redacted** export from 2026-09-20. Secrets stripped. Cite those bytes for what was said that day.
- `artifacts/reconstructed/` is labeled reconstruction. Do not promote it to verbatim evidence.
- `artifacts/kilo-storage/session_diff/` adds three plan files. It is not the live config trail.
- Claims in `events/` are `proposed`. Accepted count is zero. The receipt is non-authoritative. This is not W3C PROV.
- Do not cite the 2026-09-20 export as the 2026-09-21 “this works” session.
