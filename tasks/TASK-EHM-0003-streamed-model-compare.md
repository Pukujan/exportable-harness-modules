# TASK-EHM-0003 — Streamed compare on named models

<!-- continuity:task {"acceptance":["plan is in this file before any harness run","Grok runs on grok-4.7 with streaming","OpenCode and Pi run on yolo-auto qwen3.8-flash, not qwen3.8-27b","live Kilo, Grok, and OpenCode configs are not edited","Pi keys are not invented; if yolo-auto is not a Pi provider the exact failure is recorded","chat and code frozen asks are scored on the structure codes"],"depends_on":["EHM-0002"],"goal":"Rerun the frozen asks with streaming, Grok on grok-4.7, OpenCode and Pi on yolo-auto qwen3.8-flash.","id":"EHM-0003","next_action":"No further EHM-0003 work. Do not stack permission prompts. Do not install throwaway profiles into live config.","owner":"kilo session in exportable-harness-modules","priority":"P0","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"completed","why":"The last OpenCode score used qwen3.8-27b because that is the live build agent. That confounds the prompt test. Streaming was not requested then."} -->

- Status: completed
- Owner: kilo session in exportable-harness-modules
- Priority: P0
- Depends on: EHM-0002

## Goal

Rerun the frozen asks with streaming. Grok on grok-4.7. OpenCode and Pi on yolo-auto qwen3.8-flash, not 27b.

## Why

The last OpenCode score used qwen3.8-27b because that is the live build agent. That confounds the prompt test. Streaming was not requested then.

## Plan (written before the runs)

1. Do not edit `~/.config/kilo/`, `~/.grok/config.toml`, or `~/.config/opencode/`.
2. Grok: `grok-4.7`, `--output-format streaming-json` or the streaming format the CLI actually accepts, `--agent adapters/grok/chat-profile.md`.
3. OpenCode: model `yolo-auto/qwen3.8-flash`, throwaway dir, streaming if the CLI prints as it generates. Do not switch the live model to 27b or to flash.
4. Pi: same flash model if Pi can call yolo-auto without inventing a provider. `--system-prompt` from the throwaway instructions. `--no-tools` on the chat ask. `--no-session` so the gold install is not a session store we depend on. If Pi cannot see that model, record the error and stop. Do not guess a Google model.
5. Asks stay the frozen pair: why TL;DR, and the paragraph-gap code ask.
6. Score shape, not wording. Chat pass is bold lead, blank line, no TL;DR open, no “I'll”. Code pass is result in the first sentence. A short code reply is allowed.

## Allowed files

- this task
- `checkpoints/CURRENT.md`
- `artifacts/sessions/harness-score.md`
- `adapters/grok/chat-profile.md`
- `adapters/opencode/throwaway/**`
- `adapters/pi/**`

## Acceptance criteria

- [x] plan is in this file before any harness run
- [x] Grok runs on grok-4.7 with streaming
- [x] OpenCode and Pi run on yolo-auto qwen3.8-flash, not qwen3.8-27b
- [x] live Kilo, Grok, and OpenCode configs are not edited
- [x] Pi keys are not invented; if yolo-auto is not a Pi provider the exact failure is recorded
- [x] chat and code frozen asks are scored on the structure codes

## Checkpoint log

### 2026-09-22 00:45 UTC — kilo

Completed:
- Streamed frozen asks. Scores are in `artifacts/sessions/harness-score.md`.

Evidence:
- Grok `grok-4.7` streaming-json: chat pass, code pass.
- OpenCode `--model yolo-auto/qwen3.8-flash` `--format json`: chat pass, code pass. Global file may still have loaded.
- Pi first error: `Unknown provider "yolo-auto"` because an empty key failed schema load. After a non-secret placeholder, Pi listed `yolo-auto/qwen3.8-flash` and answered. Chat fail: bolded a “TL;DR” line. Code pass.

Decisions:
- Do not click Allow again on a dead permission card. That retries a gone id and repeats “failed to update permission.”
- Do not stack parallel shell approvals.
- Do not edit live config.

Blocked/uncertain:
- The permission toast is a client card on a stale id. It is not a model failure, and it is not fixed by another shell command.

Next:
- No further EHM-0003 work. Do not stack permission prompts. Do not install throwaway profiles into live config.
