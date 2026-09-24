# TASK-EHM-0002 — Split chat from code, then score a throwaway compare

<!-- continuity:task {"acceptance":["the plan is written in this task before analysis files are added","assistant texts are scored separately for chat asks and code asks","a frozen ask list exists, with one after-cut Kilo reply per ask as a reference sample not a string to copy","a throwaway Grok profile and a throwaway OpenCode config replace the winning prompt and do not edit live config","those headless replies are scored on the structure codes, or the exact failure is recorded","Pi is not invented","the ontology names the existing codes and cites session bytes, and is not labeled W3C PROV"],"depends_on":["EHM-0001"],"goal":"Remove the code-versus-chat confound, freeze the asks, and score throwaway Grok and OpenCode profiles against the structure codes.","id":"EHM-0002","next_action":"No further EHM-0002 work. Do not install the throwaway profiles into live config.","owner":"kilo session in exportable-harness-modules","priority":"P0","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"completed","why":"Averaging all sessions hides the chat move. A harness compare before that split repeats the paste failure."} -->

- Status: completed
- Owner: kilo session in exportable-harness-modules
- Priority: P0
- Depends on: EHM-0001

## Goal

Remove the code-versus-chat confound, freeze the asks, and score throwaway Grok and OpenCode profiles against the structure codes.

## Why

Averaging all sessions hides the chat move. A harness compare before that split repeats the paste failure.

## Plan (written before the analysis)

Do this in order. Do not skip to a harness.

1. Split scored assistant texts by the user ask in front of them. Chat asks are status, why, what-is-stopping, and explain. Code asks are implement, fix, edit, or test. Do not average the two.
2. Success for chat is the colorful-income move after 2026-09-20 02:44:12 UTC: a bold lead, a blank line, no “I'll look” opening, no forced TL;DR. Success for code stays short. A crushed code reply is not a fail.
3. Freeze a few asks of each kind from the session bytes. For each ask, keep one after-cut Kilo reply as a reference sample. It is not a sentence another model must copy. Do not start a new live Kilo chat to get that sample, and do not edit `~/.config/kilo/`.
4. Only after that split exists, write a throwaway Grok agent profile and a throwaway OpenCode config. Each must replace the prompt that actually wins, and a status question must not be allowed to open tools. Do not write `~/.grok/config.toml` or `~/.config/opencode/`.
5. Run those headless, on a throwaway directory. Score the replies on the structure codes. Record a failure as a failure.
6. Pi still has no instruction surface. Do not invent keys for it.
7. The ontology is names for the codes already in `artifacts/sessions/taxonomy.md`, cited to session bytes. It is not W3C PROV.

## Allowed files

- `tasks/TASK-EHM-0002-chat-code-split.md`
- `checkpoints/CURRENT.md`
- `artifacts/sessions/chat-code.md`
- `artifacts/sessions/frozen-asks.md`
- `artifacts/sessions/ontology.md`
- `adapters/grok/**`
- `adapters/opencode/**`
- `scripts/score_structure.py`

Do not edit `~/.config/kilo/`, the installed extension, `~/.grok/config.toml`, or `~/.config/opencode/`.

## Acceptance criteria

- [x] the plan is written in this task before analysis files are added
- [x] assistant texts are scored separately for chat asks and code asks
- [x] a frozen ask list exists, with one after-cut Kilo reply per ask as a reference sample not a string to copy
- [x] a throwaway Grok profile and a throwaway OpenCode config replace the winning prompt and do not edit live config
- [x] those headless replies are scored on the structure codes, or the exact failure is recorded
- [x] Pi is not invented
- [x] the ontology names the existing codes and cites session bytes, and is not labeled W3C PROV

## Checkpoint log

### 2026-09-22 00:20 UTC — kilo

Completed:
- Plan written in this task and in GitHub issue 1 before the analysis files.
- Chat and code scored separately. Frozen asks, ontology, throwaway profiles, and harness scores are in the tree.

Evidence:
- Colorful-income chat after the cut: bold lead 58.8%, blank line 52.9%, TL;DR 23.5%, I'll 0%. Code stayed crushed.
- Grok `--agent adapters/grok/chat-profile.md`: chat pass, code pass, no tools.
- OpenCode on the throwaway dir: answer-first and bold, no tool start, blank line not visible. Global config may still have loaded.

Decisions:
- Do not average chat and code.
- Do not install these profiles into live config.
- Pi stays unconfigured.

Blocked/uncertain:
- none.

Next:
- No further EHM-0002 work. Do not install the throwaway profiles into live config.

## Handoff

Read PROJECT → CURRENT → this task → `artifacts/sessions/taxonomy.md`. The cut stays 2026-09-20 02:44:12 UTC.
