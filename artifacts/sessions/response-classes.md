# Response classes

Good versus bad is a verdict on top of this. It is not the classification. Every assistant text is a response. A response is either mini or chunked. Each blank-line block inside it is a chunk. A chunk has one type.

This does not yet label visible type or the screenshot rule. Those are not in the text.

## Grain

| Grain | Rule |
| --- | --- |
| Mini | One block. No blank line. |
| Chunked | Two or more blocks, split on a blank line. |

## How the response opens

| Open | Rule |
| --- | --- |
| heading | First line starts with `#` |
| summary | The first block contains the summary label `TL;DR` |
| throat | First line starts with I'll, I will, or Let me |
| sentence | Anything else |

A response can carry more than one of these only if a later chunk differs. The open code is the first block only.

## Chunk types

Checked in this order. First match wins.

| Chunk | What it is |
| --- | --- |
| summary | Contains the summary label |
| heading | Starts with `#` |
| list | A bullet or a numbered line |
| table | A markdown table row |
| fence | A fenced block |
| echo | Quotes the instruction it was given, or says it is reading the prompt |
| leak | `px`, `rem`, `font-size`, or a drive letter |
| takeaway | Contains bold |
| answer | The first block, and it is a sentence |
| explain | Any other prose |

## Worked examples

The first Pi capture is chunked. Open is sentence. Chunks are answer, explain, takeaway. The takeaway is last, so the bold is not in the lead. The summary label appears inside the takeaway chunk.

The second Pi capture is mini. Open is sentence. One chunk, type answer, and that chunk also contains the summary label and an echo of the prompt. No takeaway chunk. No blank line.

A Kilo reply that opens `# …` then `## TL;DR` then bullets is chunked. Open is heading. Chunks are heading, summary, list.

## Verdict, separate from class

Chat gold is a chunked response, open sentence, first chunk type answer, a takeaway in that first chunk, no summary chunk, no throat. Code gold is a mini or a short chunked response whose first chunk is answer. A crushed mini on a code ask is not a fail. A mini on a chat ask is a miss of paragraph rhythm, even if the sentence is right.

The machine pass that labels each stored assistant text is `scripts/classify_responses.py`. One row per text is in `response-classes.jsonl`. Counts are in `response-classes.json`.

## Counts, top-level texts, split on the cut

924 texts. Children excluded.

| Side | Grain | Open | n |
| --- | --- | --- | --- |
| Before | Mini | Sentence | 184 |
| Before | Mini | Throat | 34 |
| Before | Chunked | Sentence | 122 |
| Before | Chunked | Heading | 19 |
| After | Mini | Sentence | 340 |
| After | Mini | Throat | 18 |
| After | Chunked | Sentence | 199 |
| After | Chunked | Heading | 6 |
| After | Chunked | Summary | 1 |
| After | Mini | Summary | 1 |

Throat openings fell. Heading documents fell. Mini sentence replies rose, which is right for code and wrong for a chat answer that needed a blank line. That is a class change, not a good-or-bad stamp.
