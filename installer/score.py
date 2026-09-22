"""Score a chat or code reply. No network and no live config."""

from __future__ import annotations

import re

# TL;DR / TLDR, any case, optional semicolon, spaces allowed between letters.
_LABEL_RE = re.compile(r"t\s*l\s*;?\s*d\s*r", re.IGNORECASE)
_LABEL_ONLY_RE = re.compile(r"tl;?dr", re.IGNORECASE)
_THROAT_RE = re.compile(r"^(?:i'll|i will|let me)\b", re.IGNORECASE)
_APOSTROPHES = str.maketrans(
    {
        "\u2019": "'",
        "\u2018": "'",
        "\u02bc": "'",
    }
)


def chunks(text: str) -> list[str]:
    """Split on blank lines. Leading and trailing blank lines are dropped."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    parts = re.split(r"\n\s*\n", normalized)
    return [part.strip() for part in parts if part.strip()]


def _first_line(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for line in normalized.split("\n"):
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _throat(line: str) -> bool:
    return _THROAT_RE.match(line.translate(_APOSTROPHES)) is not None


def _label_only(chunk: str) -> bool:
    compact = re.sub(r"\s+", "", chunk.strip())
    return _LABEL_ONLY_RE.fullmatch(compact) is not None


def _has_label(text: str) -> bool:
    return _LABEL_RE.search(text) is not None


def _opens_with_label(text: str) -> bool:
    return _LABEL_RE.match(text.lstrip()) is not None


def _summary_heading(text: str) -> bool:
    if _opens_with_label(text):
        return True
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for line in normalized.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") and _has_label(stripped):
            return True
    return False


def _chat_fails(text: str, tools_started: bool) -> list[str]:
    fails: list[str] = []
    parts = chunks(text)
    line = _first_line(text)
    if len(parts) < 2:
        fails.append("mini")
    if line.startswith("#"):
        fails.append("heading")
    if line and _throat(line):
        fails.append("throat")
    if parts and _label_only(parts[0]):
        fails.append("summary-open")
    if not parts or "**" not in parts[0]:
        fails.append("bold-not-in-first")
    if any(_has_label(part) for part in parts):
        fails.append("summary-label")
    if tools_started:
        fails.append("tool-start")
    return fails


def _code_fails(text: str, tools_started: bool) -> list[str]:
    fails: list[str] = []
    line = _first_line(text)
    if not text or not text.strip():
        fails.append("empty")
    if line.startswith("#"):
        fails.append("heading")
    if line and _throat(line):
        fails.append("throat")
    if text.strip() and _summary_heading(text):
        fails.append("summary-heading")
    if tools_started:
        fails.append("tool-start")
    return fails


def score_reply(kind: str, text: str, tools_started: bool = False) -> dict:
    if kind == "chat":
        fails = _chat_fails(text, tools_started)
    elif kind == "code":
        fails = _code_fails(text, tools_started)
    else:
        fails = ["unknown-kind"]
    return {"pass": fails == [], "fails": fails}
