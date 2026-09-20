"""Portable prose-type properties. Checks tokens.json and optional CSS adapter."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "modules" / "prose-type" / "tokens.json"
CSS = ROOT / "modules" / "prose-type" / "adapters" / "kilo" / "kilo-claude-markdown.css"


def run() -> int:
    fails = 0
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    expected = {
        "body_font_size": "16px",
        "line_height": "1.5",
        "h1_font_size": "22px",
        "h2_font_size": "18px",
        "h3_font_size": "16px",
        "code_white_space": "pre-wrap",
    }
    for key, value in expected.items():
        if tokens.get(key) != value:
            print(f"FAIL T-{key} {tokens.get(key)!r} != {value!r}")
            fails += 1
        else:
            print(f"PASS T-{key} {value}")

    if not CSS.is_file():
        print("FAIL T-adapter missing Kilo CSS adapter")
        return fails + 1

    text = CSS.read_text(encoding="utf-8")
    checks = [
        (r'\[data-component="markdown"\]\s*\{[^}]*font-size:\s*16px', "T1 16px body"),
        (r'\[data-component="markdown"\]\s*\{[^}]*line-height:\s*1\.5\b', "T2 line-height 1.5"),
        (r"h1 \{ font-size: 22px; \}", "T3 h1 22px"),
        (r"h2 \{ font-size: 18px; \}", "T3 h2 18px"),
        (r"h3 \{ font-size: 16px; \}", "T3 h3 16px"),
        (r"white-space:\s*pre-wrap", "T4 pre-wrap"),
    ]
    for pattern, label in checks:
        if re.search(pattern, text):
            print(f"PASS {label}")
        else:
            print(f"FAIL {label}")
            fails += 1

    if re.search(r"font-size:\s*0\.875rem", text):
        print("FAIL T1 still uses 0.875rem")
        fails += 1
    else:
        print("PASS T1 no 0.875rem body")

    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
