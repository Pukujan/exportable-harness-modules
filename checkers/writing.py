"""Portable writing-contract properties. No Kilo UI required."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDENS = ROOT / "modules" / "writing-contract" / "goldens"
FRAGMENT = ROOT / "modules" / "writing-contract" / "AGENTS.fragment.md"

IMPL_DUMP = re.compile(
    r"(font-size\s*:|kilo\.jsonc|data-component=|\[data-component)",
    re.I,
)


def paragraphs(text: str) -> list[str]:
    chunks = re.split(r"\n\s*\n", text.strip())
    return [c.strip() for c in chunks if c.strip()]


def sentence_count(text: str) -> int:
    return len([s for s in re.split(r"[.!?]+", text) if s.strip()])


def first_sentence(text: str) -> str:
    stripped = text.strip()
    match = re.match(r".+?[.!?]", stripped, re.S)
    if match:
        return match.group(0).strip()
    return stripped.splitlines()[0].strip() if stripped else ""


def visual_lines(text: str, width: int = 78) -> int:
    total = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        total += max(1, (len(stripped) + width - 1) // width)
    return total


def check_good(text: str) -> list[str]:
    fails: list[str] = []
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return ["W1 empty"]
    if lines[0].startswith("#"):
        fails.append("W1 opens with a heading")
    if re.search(r"^##\s*TL;DR\s*$", text, re.I | re.M):
        fails.append("W2 forced TL;DR")
    paras = paragraphs(text)
    long_para = any(sentence_count(p) >= 3 or visual_lines(p) > 2 for p in paras)
    if visual_lines(text) <= 4:
        fails.append("W3 crushed into 1-4 dense lines")
    elif not long_para:
        fails.append("W3 no real paragraph")
    if IMPL_DUMP.search(text):
        fails.append("W4 implementation dump")
    if sentence_count(first_sentence(text)) == 0:
        fails.append("W1 missing first sentence")
    return fails


def check_bad_should_fail(name: str, text: str, expected: str) -> str | None:
    fails = check_good(text)
    if expected not in " ".join(fails) and not any(expected in f for f in fails):
        return f"{name} expected fail containing {expected!r}, got {fails}"
    return None


def run() -> int:
    fails = 0

    fragment = FRAGMENT.read_text(encoding="utf-8")
    for needle, prop in [
        ("Never crush user-facing answers into 1–4 dense lines", "R10"),
        ("Talk to the user", "R11"),
        ("Change code", "R11"),
        ("Documents and PRs", "R12"),
        ("Do not open every reply with TL;DR", "W2"),
    ]:
        if needle not in fragment:
            print(f"FAIL {prop} missing {needle!r} in AGENTS.fragment.md")
            fails += 1
        else:
            print(f"PASS {prop} {needle}")

    good = (GOLDENS / "good-chat.md").read_text(encoding="utf-8")
    good_fails = check_good(good)
    if good_fails:
        print(f"FAIL W-good {good_fails}")
        fails += 1
    else:
        print("PASS W-good sample starts with the answer, no TL;DR, real paragraphs")

    cases = [
        ("bad-tldr.md", "W2"),
        ("bad-crushed.md", "W3"),
        ("bad-px-dump.md", "W4"),
    ]
    for filename, expected in cases:
        text = (GOLDENS / filename).read_text(encoding="utf-8")
        err = check_bad_should_fail(filename, text, expected)
        if err:
            print(f"FAIL {err}")
            fails += 1
        else:
            print(f"PASS {filename} is rejected for {expected}")

    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
