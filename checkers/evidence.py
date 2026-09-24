"""Evidence-honesty properties. No UI required."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run() -> int:
    fails = 0
    evidence = (ROOT / "pack" / "evidence.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    tui = (ROOT / "adapters" / "tui" / "AGENTS.md").read_text(encoding="utf-8")
    opencode = (ROOT / "adapters" / "opencode" / "README.md").read_text(encoding="utf-8")
    grok = (ROOT / "adapters" / "grok" / "README.md").read_text(encoding="utf-8")

    checks = [
        (evidence, "Copy test", "E1 names the copy test"),
        (evidence, "Path test", "E1 names the path test"),
        (evidence, "This is not W3C PROV", "E5 refuses a PROV relabel"),
        (evidence, "2026-09-20", "E4 names the export date"),
        (evidence, "2026-09-21", "E4 names the gold-signal date"),
        (evidence, "session_diff", "E3 names the stored diff"),
        (tui, "Chat.", "TUI paste includes routing"),
        (tui, "start with the answer", "TUI paste includes answer-first"),
    ]
    for text, needle, label in checks:
        if needle in text:
            print(f"PASS {label}")
        else:
            print(f"FAIL {label}")
            fails += 1

    if "FOSSIL can answer what we tried" in readme:
        print("FAIL README still claims FOSSIL can answer the whole history")
        fails += 1
    else:
        print("PASS README does not overclaim the history")

    for name, text in (("opencode", opencode), ("grok", grok)):
        if "~/.config/kilo/" in text and "Do not" in text:
            print(f"PASS {name} adapter forbids the live Kilo config")
        else:
            print(f"FAIL {name} adapter missing live-config refusal")
            fails += 1

    return fails
