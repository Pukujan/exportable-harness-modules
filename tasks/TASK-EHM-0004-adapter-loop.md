# TASK-EHM-0004 — Frozen adapter loop

<!-- continuity:task {"acceptance":["this file is the frozen plan before any new harness run","chat pass is chunked, open sentence, bold in the first chunk, no summary chunk, no throat","code pass is a short answer-first reply","live Kilo, Grok, and OpenCode configs are not edited","each iteration changes one sent prompt and records the class of the reply","a miss is not called a pass"],"depends_on":["EHM-0003"],"goal":"Iterate each throwaway adapter until the frozen asks match the response classes. Do not auto-advance past a miss.","id":"EHM-0004","next_action":"Stop. Do not start a new goal. Do not edit live configs.","owner":"kilo session in exportable-harness-modules","priority":"P0","protocol_version":"0.1.0-draft","schema":"project-continuity.task.v1","status":"completed","why":"Grok and OpenCode each have a recorded pass on the chat ask and the code ask. The loop stops. It does not start a new goal."} -->

- Status: completed
- Owner: kilo session in exportable-harness-modules
- Priority: P0
- Depends on: EHM-0003

## Frozen

This task is the frozen plan. Do not add a new success rule during a run. Do not treat a response label as permission to start the next goal.

There is no metamorphic goal switcher. Classification labels replies. It does not move the task.

## Goal

Iterate each throwaway adapter until the frozen asks match the response classes. Stop on a miss. Record the class. Change one prompt rule. Run again.

## Pass rules

Chat pass, all of these:

- Grain is chunked.
- Open is sentence.
- The first chunk contains bold.
- No summary chunk.
- Open is not throat.
- No tool start.

Code pass:

- First sentence states the result.
- Short is allowed. Mini is allowed.
- No summary heading.

Out of this loop: 16px type, and a screenshot before a visual claim. Text cannot prove those.

## Models

- Grok: grok-4.7, streaming.
- OpenCode and Pi: yolo-auto/qwen3.8-flash, streaming.
- Do not edit `~/.config/kilo/`, `~/.grok/config.toml`, or `~/.config/opencode/`.

## Allowed files

- this task
- `checkpoints/CURRENT.md`
- `adapters/pi/SYSTEM.md`
- `adapters/grok/chat-profile.md`
- `adapters/opencode/throwaway/**`
- `artifacts/sessions/captures/**`
- `artifacts/sessions/harness-score.md`

## Acceptance criteria

- [x] this file is the frozen plan before any new harness run
- [x] chat pass is chunked, open sentence, bold in the first chunk, no summary chunk, no throat
- [x] code pass is a short answer-first reply
- [x] live Kilo, Grok, and OpenCode configs are not edited
- [x] each iteration changes one sent prompt and records the class of the reply
- [x] a miss is not called a pass

## Checkpoint log

### 2026-09-22 01:25 UTC — kilo

Completed:
- Plan frozen in this file before the new runs.
- Pi chat now passes the frozen class rules. Pi code ask passes the short result-first rule.
- Grok chat was rerun. It is a miss.

Evidence:
- Pi chat: chunked, sentence open, bold in the first chunk, no summary label, no throat. Capture `pi-chat-2026-09-22-d.txt`.
- Pi code: first sentence states the margin change. Short. No summary heading.
- Grok grok-4.7 streaming: bold in the first chunk and a blank line, but the second chunk prints the summary label. Not a pass.

Decisions:
- Do not call the Grok reply a pass.
- Do not auto-advance to OpenCode.
- One rule change next: Grok profile forbids the label in any chunk.

Blocked/uncertain:
- none.

Next:
- Change the Grok profile so no chunk may contain the summary label, then rerun only the chat ask.

### 2026-09-22 01:40 UTC — kilo

Completed:
- One profile sentence now forbids the summary label in any chunk and any spelling. Nothing else was changed before the run.
- Grok chat ask, streamed, grok-4.7. Miss. Not a pass.

Evidence:
- Capture `artifacts/sessions/captures/grok-chat-2026-09-22.txt`.
- Stream model `grok-4.7-build`. Session `01a0c6be-6d68-7273-a54c-0ab210cc6c0a`. `end_turn`, one turn, no tool call.
- Class: chunked, sentence open, no summary label, no throat, no tools. Bold is in the third chunk, not the first.
- Ran from a throwaway temp directory with `--agent` on the throwaway profile. Live configs were not edited.

Decisions:
- Do not call this a pass. This is the second recorded Grok chat miss. The first was the label in a later chunk.
- One rule change after the capture: the takeaway bold must sit in the first chunk.
- One rerun remains before the third-miss stop.

Blocked/uncertain:
- none.

Next:
- Rerun only the Grok chat ask.

### 2026-09-22 01:50 UTC — kilo

Completed:
- One rule after the prior miss: the takeaway bold must sit in the first chunk.
- Grok chat ask, streamed, grok-4.7. Pass.

Evidence:
- Capture `artifacts/sessions/captures/grok-chat-2026-09-22-b.txt`.
- Stream model `grok-4.7-build`. Session `01a0c6bf-f98c-7323-a1f4-72353e1a6f1d`. `end_turn`, one turn, no tool call.
- Class: chunked, sentence open, bold in the first chunk, no summary label in any reply chunk, no throat, no tools.
- The hidden thought named the label. That stream is not a reply chunk.
- Live configs were not edited.

Decisions:
- Grok chat harness stops on this pass. Do not rerun it.
- Next harness is the Grok code ask, once.

Blocked/uncertain:
- none.

Next:
- Run the Grok code ask once. Score it. Same miss rule.

### 2026-09-22 01:55 UTC — kilo

Completed:
- Grok code ask, streamed, grok-4.7. Pass on the first try.

Evidence:
- Capture `artifacts/sessions/captures/grok-code-2026-09-22.txt`.
- Stream model `grok-4.7-build`. Session `01a0c6c1-565b-79f1-ad75-579bac32691b`. `end_turn`, one turn, no tool call.
- First sentence states the spacing change. Short. No summary heading.
- Live configs were not edited.

Decisions:
- Grok code harness stops on this pass. Do not rerun it.
- Next harness is OpenCode chat, once. Do not edit the global OpenCode file.

Blocked/uncertain:
- none.

Next:
- Run only the OpenCode chat ask.

### 2026-09-22 02:00 UTC — kilo

Completed:
- OpenCode chat ask, streamed, yolo-auto/qwen3.8-flash. Miss. Not a pass.

Evidence:
- Capture `artifacts/sessions/captures/opencode-chat-2026-09-22.txt`.
- Session `ses_f393d4b14ffeomcODZ47U5QOCI`. `stop`, no tool call.
- Class: chunked, bold in the first chunk, no throat, no tools. Both chunks contain the summary label, so the open is a summary, not a sentence.
- The reply cites the global OpenCode instruction file and the throwaway file. The global file may have loaded. It was not edited.

Decisions:
- Do not call this a pass. This is the first recorded OpenCode chat miss.
- One rule change: no chunk may contain the summary label in any spelling.
- Do not edit `~/.config/opencode/`.

Blocked/uncertain:
- none.

Next:
- Rerun only the OpenCode chat ask.

### 2026-09-22 02:05 UTC — kilo

Completed:
- OpenCode chat ask, streamed, after the label-ban sentence. Miss. Not a pass.

Evidence:
- Capture `artifacts/sessions/captures/opencode-chat-2026-09-22-b.txt`.
- Session `ses_f393c4eb6ffe0kzp8WHShzxhYc`. `stop`, no tool call.
- Class: chunked, sentence open, bold in the first chunk, no throat, no tools. The third chunk prints the summary label.
- The reply cites the global OpenCode file and this repo's instruction file. The global file may have loaded. It was not edited.

Decisions:
- Do not call this a pass. This is the second recorded OpenCode chat miss.
- One rule change: name the forbidden spellings, including a denial.
- One rerun remains before the third-miss stop.

Blocked/uncertain:
- none.

Next:
- Rerun only the OpenCode chat ask.

### 2026-09-22 02:10 UTC — kilo

Completed:
- OpenCode chat ask, streamed, after naming the forbidden spellings. Pass.

Evidence:
- Capture `artifacts/sessions/captures/opencode-chat-2026-09-22-c.txt`.
- Session `ses_f393b5c4effeMwOUwI3JCBtakr`. `stop`, no tool call.
- Class: chunked, sentence open, bold in the first chunk, no summary label, no throat, no tools.
- The global OpenCode file may still have loaded. It was not edited. This reply does not cite that path, so this is not a clean pack-only proof.

Decisions:
- OpenCode chat harness stops on this pass. Do not rerun it.
- Next harness is the OpenCode code ask, once.

Blocked/uncertain:
- none.

Next:
- Run the OpenCode code ask once.

### 2026-09-22 02:15 UTC — kilo

Completed:
- OpenCode code ask, streamed, yolo-auto/qwen3.8-flash. Miss. Not a pass.

Evidence:
- Capture `artifacts/sessions/captures/opencode-code-2026-09-22.txt`.
- Session `ses_f393a3229ffefzbPxfqbndW7mL`. Step finished `tool-calls`. No reply text.
- `grep` and `glob` started and were auto-rejected. No first sentence stated a change.
- The global OpenCode file may still have loaded. It was not edited. No file was edited.

Decisions:
- Do not call this a pass. This is the first recorded OpenCode code miss.
- One rule change: do not run tools on a code ask.
- Do not edit `~/.config/opencode/`.

Blocked/uncertain:
- none.

Next:
- Rerun only the OpenCode code ask.

### 2026-09-22 02:20 UTC — kilo

Completed:
- OpenCode code ask, streamed, after forbidding tools. Pass.
- Acceptance lines in `GOAL.md` are ready to check. No new goal.

Evidence:
- Capture `artifacts/sessions/captures/opencode-code-2026-09-22-b.txt`.
- Session `ses_f39391603ffeHuFtp3KiP5PVf1`. `stop`, no tool call.
- First sentence states the spacing change. Short. No summary heading.
- The global OpenCode file may still have loaded. It was not edited. This is not a clean pack-only proof.
- A path is named. That is not a code fail under the frozen rules.

Decisions:
- OpenCode code harness stops on this pass. Do not rerun it.
- Grok chat, Grok code, OpenCode chat, and OpenCode code each have a recorded pass.
- Stop. Do not start a new goal.

Blocked/uncertain:
- none.

Next:
- Check the acceptance lines. Stop.
