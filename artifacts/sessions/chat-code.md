# Chat asks and code asks are not one score

The plan for this split is `tasks/TASK-EHM-0002-chat-code-split.md`. The cut is still 2026-09-20 02:44:12 UTC. Children are excluded. A user ask is chat if it is a why, what, how, or a question, and it does not ask to implement, fix, edit, or patch. A code ask is one of those verbs. The two are not averaged.

## Colorful-income, the session that contains the cut

| Ask | When | n | TL;DR | I'll | Bold lead | Blank line | Crushed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chat | Before | 31 | 38.7% | 0.0% | 41.9% | 45.2% | 54.8% |
| Chat | After | 17 | 23.5% | 0.0% | 58.8% | 52.9% | 47.1% |
| Code | Before | 23 | 17.4% | 4.3% | 30.4% | 30.4% | 69.6% |
| Code | After | 3 | 66.7% | 0.0% | 66.7% | 33.3% | 66.7% |

**Chat is the move.** After the write, bold leads rise and TL;DR falls, and “I'll” stays at zero. Code stays crushed. The after-code cell is three texts. Do not treat 66.7% TL;DR there as a law.

## All top-level sessions

| Ask | When | n | TL;DR | I'll | Bold lead | Blank line | Crushed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chat | Before | 211 | 6.2% | 6.6% | 47.9% | 50.2% | 49.8% |
| Chat | After | 361 | 1.4% | 2.8% | 39.3% | 38.8% | 61.2% |
| Code | Before | 51 | 7.8% | 7.8% | 27.5% | 25.5% | 74.5% |
| Code | After | 59 | 3.4% | 6.8% | 28.8% | 28.8% | 71.2% |

**Do not use the all-session chat row as the success picture.** TL;DR and “I'll” fall. Bold leads and blank lines do not, because many later “questions” are still engineering asks in other repos. Success for chat is the colorful-income chat row. Success for code is staying short: crushed near 70% is not a fail.

Rates are in `chat-code-score.json`.
