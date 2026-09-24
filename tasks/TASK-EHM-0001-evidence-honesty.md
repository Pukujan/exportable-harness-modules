# TASK-EHM-0001 — Evidence honesty and throwaway copy test

<!-- continuity:task {"acceptance":["pack/evidence.md states copy test is not a path test and is not W3C PROV","README HANDOFF PRESERVE source-policy and artifacts note match that limit","five behavior SPECs are not rewritten","throwaway adapters do not write ~/.config/kilo or the live OpenCode config","a headless text check is attempted on grok and opencode, or the exact failure is recorded","continuity validate passes"],"depends_on":[],"goal":"Write the evidence limit and score a throwaway text copy without touching the live Kilo install.","id":"EHM-0001","next_action":"No further EHM-0001 work. Do not export the 2026-09-21 session unless the owner asks.","owner":"kilo session in exportable-harness-modules","priority":"P0","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"completed","why":"The pack can reapply the end state. It cannot replay the config history. The docs were saying those were the same test."} -->

- Status: completed
- Owner: kilo session in exportable-harness-modules
- Priority: P0
- Depends on: none

## Goal

Write the evidence limit and score a throwaway text copy without touching the live Kilo install.

## Why

The pack can reapply the end state. It cannot replay the config history. The docs were saying those were the same test.

## Allowed files

- `pack/evidence.md`
- `pack/source-policy.md`
- `README.md`
- `HANDOFF.md`
- `PRESERVE.md`
- `AGENTS.md`
- `PROJECT.md`
- `kilo.jsonc`
- `artifacts/README.md`
- `adapters/tui/**`
- `adapters/opencode/**`
- `adapters/grok/**`
- `checkers/evidence.py`
- `checkers/run_all.py`
- `.continuity/**`
- `checkpoints/CURRENT.md`
- `tasks/TASK-EHM-0001-evidence-honesty.md`

Do not edit `~/.config/kilo/`, the installed extension `dist/`, or `~/.config/opencode/`.

## Acceptance criteria

- [x] `pack/evidence.md` states a copy test is not a path test and is not W3C PROV
- [x] README, HANDOFF, PRESERVE, source policy, and the artifacts note match that limit
- [x] the five behavior SPECs are not rewritten
- [x] throwaway adapters do not write the live Kilo or OpenCode config
- [x] a headless text check is attempted on grok and opencode, or the exact failure is recorded
- [x] continuity validate passes

## Checkpoint log

### 2026-09-21 22:45 UTC — kilo

Completed:
- Evidence spec and the honesty edits are in the tree.
- Throwaway paste file and OpenCode / Grok notes are in the tree. Live configs were not written.
- Headless copy test was run. Routing did not pass.

Evidence:
- `python checkers/run_all.py` -> ALL PORTABLE CHECKERS PASSED
- `python -m continuity validate --root D:\claude\exportable-harness-modules` -> VALID
- `grok -p` in a temp dir, rules from `adapters/tui/AGENTS.md`, `--max-turns 2 --permission-mode plan` -> system prompt contained the paste; first visible sentence was “I'll check…” and then tool calls. No final answer before the turn cap. Routing fail.
- `opencode run --dir` that temp dir, `--pure`, model `qwen3.8-27b` -> shell tools ran, including a listing of `~/.config/opencode`, then a short answer that no export was running. Routing fail. Writing of the final sentence was a paragraph, not a telegram. Global OpenCode instructions were also loaded, so this is not a clean pack-only test.

Decisions:
- Do not call this a reproducible pass.
- Do not launch the interactive TUI. Both CLIs are installed. A TUI would not finish a reply this pack can score, and it cannot confirm CSS.
- Do not backfill the 2026-09-21 session or relabel the receipt as W3C PROV.

Blocked/uncertain:
- none for the doc pass. The copy test failed routing on both CLIs. That is a result, not a blocker.

Next:
- No further EHM-0001 work. Do not export the 2026-09-21 session unless the owner asks.

## Handoff

Read PROJECT → CURRENT → this task → `pack/evidence.md`. Checkpoint before stopping.
