# Good and bad, from the bytes we actually scored

This is not a finished atomic catalog of all five UX behaviors. The session gather was scored for sentence shape. It was not coded turn by turn into a good set and a bad set for routing, type, the sent prompt, paragraph shape, and screenshot-before-claim.

## What was analyzed

Assistant text longer than 80 characters, split at 2026-09-20 02:44:12 UTC, then split again into chat asks and code asks. Codes are in `taxonomy.md`. Rates are in `structure-score.json` and `chat-code-score.json`.

## What was not analyzed

Visible type. No transcript row can prove 16px. That needs a screenshot.

Look-then-claim. The 12-second wait and the PNG read are not in these text scores.

A full routing label on every user turn. We classified asks as chat or code with a verb list. We did not mark each turn as research, clarify, or long-run.

So the five behaviors are not yet a granulated gold set. Three of them have text evidence. Two do not.

## Atomic pairs the bytes do support

| Id | Good | Bad | Where it showed |
| --- | --- | --- | --- |
| A1 | First sentence is the answer | Opens with I'll, I will, or Let me | I'll fell from 9.5% to 3.2% on top-level text after the cut |
| A2 | Bold takeaway inside the first paragraph | Bold only at the end, or no bold | Colorful-income chat: 41.9% before, 58.8% after |
| A3 | A blank line between paragraphs on a chat answer | A crushed block on a chat answer | Colorful-income chat blank line 45.2% to 52.9% |
| A4 | No summary heading | A TL;DR heading, including a joke label | Spiked to 42.9% during the CSS hour, then fell. Not dead at the cut |
| A5 | Code reply stays short and states the result | A code reply that opens as a document | Code crushed stayed near 70%. That is allowed |
| A6 | A status question gets text, not a tool start | Tools run before the answer on a why | Seen on the first OpenCode paste test. Not measurable from part timestamps |

Chat gold is A1, A2, A3, A4, A6. Code gold is A5. Do not average them.

## Adapter rule this implies

Each harness needs its own sent prompt. A shared file that is not loaded does not count. The Pi miss was A2: the bold sat in the last paragraph. The next Pi prompt has to put the bold in the first paragraph.
