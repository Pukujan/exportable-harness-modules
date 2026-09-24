# Before and after, from the session bytes

This is a first score of the redacted Kilo sessions gathered on 2026-09-21. It is not W3C PROV. It is not a claim that later coding sessions became chat. The owner’s “this works” signal on 2026-09-21 is still the acceptance gold. These numbers say when the edits landed, and which habits moved.

Hashes for the gathered files are in `gather-manifest.json`. Files that were already in the tree were not overwritten.

## When the edits landed

All of these first hits are in `ses_f4930aa1affeXv0fw5Syzn0Z8Y` (colorful-income), UTC.

| When | What the bytes show |
| --- | --- |
| 2026-09-20 01:40 | “Write like a readable briefing” appears in a tool payload. |
| 2026-09-20 01:43 | Reasoning mentions `font-size: 14px`. |
| 2026-09-20 01:44 | The stylesheet marker `kilo-claude-md-start` is written. This is the first CSS patch. |
| 2026-09-20 02:32 | `0.875rem` appears. That is the type rule later killed. |
| 2026-09-20 02:38 | `font-size: 16px` appears. That is the lock that stayed. |
| 2026-09-20 02:44:12 | `write` of `%USERPROFILE%\.config\kilo\AGENTS.md`. This is the before/after line. |
| 2026-09-20 02:44:20 | `edit` of `%USERPROFILE%\.config\kilo\kilo.jsonc`. The sent agent prompt. Eight seconds later. | |

There is no separate before file. The before is the early part of that same session, plus older top-level sessions that started before 02:44 UTC.

## Taxonomy

Scored on assistant text parts longer than 80 characters. A paragraph means a blank line and at least three sentence marks in the first 900 characters. Crushed means no blank line and at most four non-empty lines. Tool-before-answer could not be scored. In this export, tool parts do not carry an earlier timestamp than the text part of the same message, so a zero there would be a lie.

| Code | Habit | What a point means |
| --- | --- | --- |
| S1 | Throat-clearing | Opens with “I'll”, “I will”, or “Let me”. |
| S2 | Forced TL;DR | `TL;DR` in the first 300 characters. |
| S3 | Crushed | No blank line, four lines or fewer. |
| S4 | Implementation dump | `px`, `rem`, `font-size`, or a markdown selector in the first 500 characters. |
| S5 | Real paragraph | Blank line plus three sentence marks. |

## Colorful-income, the clean split

| Window | Texts | S1 I'll | S2 TL;DR | S3 crushed | S4 px dump | S5 paragraph |
| --- | --- | --- | --- | --- | --- | --- |
| Before 01:40, no briefing phrase yet | 16 | 6.2% | 0.0% | 75.0% | 0.0% | 25.0% |
| 01:40–02:44, CSS experiments | 42 | 0.0% | 42.9% | 54.8% | 0.0% | 45.2% |
| After 02:44, agent prompt is in a tool payload | 22 | 0.0% | 31.8% | 45.5% | 9.1% | 54.5% |

**The middle window is the failed rule.** TL;DR was not the before. It spiked to 42.9% while the CSS was being tried, then fell, and was not gone yet inside that same session. Paragraphs rose from 25% to 54.5% after the agent prompt. Crushed replies fell from 75% to 45.5%. A px dump showed up only after the prompt, in 9.1% of those texts.

## All top-level sessions

Subagent replays (91 texts) are excluded. Split at the 02:44 agent-prompt hit.

| Pool | Texts | S1 I'll | S2 TL;DR | S3 crushed | S5 paragraph |
| --- | --- | --- | --- | --- | --- |
| Before the agent prompt | 359 | 9.5% | 5.3% | 60.7% | 39.0% |
| After the agent prompt | 565 | 3.2% | 1.4% | 63.5% | 36.5% |

**This pool does not prove the chat got skimmable.** Throat-clearing and TL;DR fell. Crushed replies did not. Later sessions are mostly code and replay work, and the writing contract says those stay short. A crushed rate that stays near 60% is expected there. It is not a before of the chat UX.

## What this can and cannot be used for

Use the colorful-income windows to say what changed on 2026-09-20. Use the later top-level drop in TL;DR and “I'll check” as a weak sign the prompt stayed loaded. Do not use the all-session crushed rate as a fail of the overlay. Do not treat this score as a match to Claude, and do not treat it as proof of the 16px window. Type still needs a screenshot.
