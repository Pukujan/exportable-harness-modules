"""Fifty stable asks. Twenty-five chat, twenty-five code. No randomness."""

from __future__ import annotations

CHAT_SUFFIX = "Answer only. Do not edit files."
CODE_SUFFIX = "Say what you would change, in a short reply. Do not edit files."

CHAT_STEMS = (
    "Why are we always trying to do a TL;DR? Is that built into the product?",
    "What is the difference between a copy test and a path test?",
    "Why should a question get an answer before a long job starts?",
    "Can a terminal confirm that chat prose is about 16px?",
    "What should a person notice when turn routing is working?",
    "Why must an experiment avoid the live Kilo config?",
    "When is a screenshot required before a visual claim?",
    "What is the difference between a chat turn and a code turn?",
    "Why is a summary label a bad open on a short reply?",
    "What should happen after /goal and an explicit go?",
    "Why are the export date and the gold-signal date different days?",
    "Can a CLI reply prove the webview stylesheet is correct?",
    "Why is a proposed FOSSIL receipt not W3C PROV?",
    "Why should the first sentence be the answer itself?",
    "What does paragraph shape change for someone skimming?",
    "Why can a bare TUI not copy hot reload?",
    "What goes wrong if a missing session is rebuilt from memory?",
    "When should an agent ask for a go-ahead instead of starting?",
    "Why may a code reply be one sentence with no bold?",
    "What does it mean that a copy test is not a history?",
    "Why must a later export be redacted before it is stored?",
    "What stays out of scope once the five behaviors are preserved?",
    "Is the stored session diff a history of the stylesheet?",
    "Why wait twelve seconds after a CSS edit before capture?",
    "What is the risk of citing an audit when the session JSON disagrees?",
)

CODE_STEMS = (
    "The paragraph gaps are too large.",
    "Headings in chat are the same size as the body.",
    "Code blocks run off the right edge.",
    "The reply opens with a heading instead of the answer.",
    "A one-line question still gets a summary block on top.",
    "The model starts tools when the user only asked a question.",
    "Chat prose is too small to skim.",
    "The first line promises to look it up instead of stating the result.",
    "A list is crushed onto one dense line.",
    "The reply dumps file paths the user did not ask to edit.",
    "The opening paragraph has no bold takeaway.",
    "A long job starts before anyone says go.",
    "A CSS-only edit still forces a full window reload.",
    "A visual claim is made without reading the screenshot.",
    "A code reply is padded out when one sentence is enough.",
    "The output prompt tells the model to write a telegram.",
    "A status question is treated as a standing goal.",
    "The terminal paste includes webview rules it cannot apply.",
    "The evidence text treats the export as the gold-day transcript.",
    "The checker runner never calls the install guard.",
    "Paragraphs break every two lines even when the idea continues.",
    "The reply leads with pixel sizes instead of what a person will notice.",
    "A research question is answered with a code edit.",
    "A later chunk still contains a summary label.",
    "Throwaway notes name the live config as the install target.",
)


def asks() -> list[dict]:
    items: list[dict] = []
    for index, stem in enumerate(CHAT_STEMS, start=1):
        items.append(
            {
                "id": f"c{index:02d}",
                "kind": "chat",
                "text": f"{stem} {CHAT_SUFFIX}",
            }
        )
    for index, stem in enumerate(CODE_STEMS, start=1):
        items.append(
            {
                "id": f"k{index:02d}",
                "kind": "code",
                "text": f"{stem} {CODE_SUFFIX}",
            }
        )
    return items
