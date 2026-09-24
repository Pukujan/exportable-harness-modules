# Goal

Follow this file until every line under Acceptance is checked. Do not invent a next project. Do not edit the live Kilo config, the live Grok config, or the live OpenCode config. Do not stack shell commands. One harness run, then record, then the next step.

There is no automatic goal switcher. This file is the frozen plan. A reply label does not start a new goal.

## Already done

Do not redo these.

- Evidence honesty, session gather, and the cut at 2026-09-20 02:44:12 UTC.
- Response classes: mini or chunked, opening, chunk type. 924 texts labeled.
- Pi chat passes the chat rules below. Capture: `artifacts/sessions/captures/pi-chat-2026-09-22-d.txt`.
- Pi code ask passes the code rules below.

## Pass rules

Chat, all of them:

- Chunked, not mini.
- Opens with a sentence, not a heading, not I'll, not a summary label.
- The first chunk contains bold.
- No chunk contains TL;DR or TLDR in any spelling.
- No tool start.

Code:

- The first sentence states the result.
- Short is allowed.
- No summary heading.

Out of scope: 16px type, a screenshot claim, a W3C PROV graph, a new export of the live session, and installing any throwaway profile into a live config.

## Models

- Grok: `grok-4.7`, streaming JSON, profile `adapters/grok/chat-profile.md`.
- OpenCode: `yolo-auto/qwen3.8-flash`, `--format json`, directory `adapters/opencode/throwaway`.
- Pi: `yolo-auto/qwen3.8-flash`, throwaway `PI_CODING_AGENT_DIR` at `adapters/pi`. Do not rerun Pi unless a later edit regresses it.

## Steps

1. Edit `adapters/grok/chat-profile.md` so no chunk may contain the summary label in any spelling. Do not change anything else.
2. Run only the chat ask, streamed, on grok-4.7. Capture the reply under `artifacts/sessions/captures/`. Score it. A miss is not a pass. If it misses, change one rule and run that ask again. Stop that harness when it passes or after three misses, and record the third miss.
3. When Grok chat passes, run the code ask once. Score it. Same miss rule.
4. Then OpenCode, same two asks, same rules, flash model, streaming. The global OpenCode file may still load. Say so in the score. Do not edit that file to stop it.
5. After each run, append a checkpoint to `tasks/TASK-EHM-0004-adapter-loop.md` and update `checkpoints/CURRENT.md`.
6. When Grok and OpenCode have a recorded pass or a third miss on each ask, check the acceptance lines and stop. Do not start a new goal.

## Asks

Chat: Why are we always trying to do a TL;DR? Is that built into the product? Answer only. Do not edit files.

Code: The paragraph gaps are too large. Say what you would change, in a short reply. Do not edit files.

## Acceptance

- [x] Grok chat is a pass, or three misses are recorded
- [x] Grok code is a pass, or three misses are recorded
- [x] OpenCode chat is a pass, or three misses are recorded
- [x] OpenCode code is a pass, or three misses are recorded
- [x] Each reply is captured
- [x] Live configs were not edited
- [x] This file was not replaced with a new plan mid-run
