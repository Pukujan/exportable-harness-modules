# Output-structure taxonomy

Scored on assistant text longer than 80 characters. The cut is not the first CSS patch. The cut is the minute the writing instruction was written into the files Kilo actually loads.

## Exact cut

Both writes are in `ses_f4930aa1affeXv0fw5Syzn0Z8Y`, UTC, 2026-09-20.

| Time | Tool | File |
| --- | --- | --- |
| 02:44:12 | write | `%USERPROFILE%\.config\kilo\AGENTS.md` |
| 02:44:20 | edit | `%USERPROFILE%\.config\kilo\kilo.jsonc` |

Eight seconds apart. The first file is loaded every turn. The second is the agent prompt, so the terse default does not win. **02:44:12 is the before/after line.** Text at or after that timestamp is after. Text before it is before.

Earlier the same night, and not this cut: the stylesheet marker at 01:44, `0.875rem` at 02:32, and `font-size: 16px` at 02:38. Those change type. They do not change the sentence shape.

## Codes

| Code | What you see | How it is counted |
| --- | --- | --- |
| O1 | Opens on a heading | First line starts with `#` |
| O2 | Opens on TL;DR | `TL;DR` in the first 200 characters |
| O3 | Opens on a promise to look | First line starts with I'll, I will, or Let me |
| O4 | Bold in the lead | `**` in the first 350 characters |
| B1 | Paragraph rhythm | A blank line in the reply |
| B2 | A list | A line that is a bullet or a number |
| B3 | A table | A markdown table row |
| L1 | A path in the lead | A drive letter, or a backtick, in the first 400–800 characters |
| L2 | A type dump | `px`, `rem`, or `font-size` in the first 500 characters |
| L3 | A code fence | A fenced block anywhere in the reply |

O1–O3 are opening moves. O4 and B1 are the skim. B2–B3 are scan devices. L1–L3 are leaks of implementation into the chat voice.

## Scope

| Scope | Sessions | Rule |
| --- | --- | --- |
| Before | 12 | Every scored assistant text in the session is before 02:44:12 |
| Spans | 1 | Colorful-income. Split its texts on 02:44:12. Do not call the whole session before or after. |
| After | 42 | Every scored assistant text is at or after 02:44:12. Includes later Hades and harness-on-steroids chats. Those are after the prompt existed. They are not a chat-UX sample. |

Child sessions are in those counts. The rate tables below drop children, because a replay subagent is not the chat voice.

## What moved

Colorful-income only, split on the 02:44:12 write.

| Code | Before the write (58 texts) | After the write (22 texts) |
| --- | --- | --- |
| O1 heading open | 32.8% | 22.7% |
| O2 TL;DR open | 31.0% | 31.8% |
| O3 I'll open | 1.7% | 0.0% |
| O4 bold lead | 37.9% | 63.6% |
| B1 blank line | 39.7% | 54.5% |
| B2 list | 36.2% | 27.3% |
| B3 table | 12.1% | 18.2% |
| L1 pathish | 37.9% | 27.3% |
| L2 px / rem | 0.0% | 9.1% |

**Inside that session, the write did not kill TL;DR.** It raised the bold lead and the blank line, and it stopped the “I'll look” opening. The TL;DR spike belongs to the hour before this cut, while CSS was being tried. That hour is still before 02:44:12, so it sits in the before column. That is why before already shows 31% TL;DR.

All top-level sessions, same cut.

| Code | Before (359) | After (565) |
| --- | --- | --- |
| O1 heading open | 5.3% | 1.1% |
| O2 TL;DR open | 5.3% | 1.4% |
| O3 I'll open | 9.5% | 3.2% |
| O4 bold lead | 37.3% | 43.5% |
| B1 blank line | 39.3% | 36.5% |
| L1 pathish | 51.0% | 46.2% |

**The durable move across sessions is the opening, not the paragraph rate.** Headings, TL;DR, and “I'll look” all fall. Blank lines do not rise, because most later sessions are code. A flat paragraph rate there is not a before of the chat.

Machine-readable rates are in `structure-score.json`. This score does not prove 16px type, and it is not a Claude match.
