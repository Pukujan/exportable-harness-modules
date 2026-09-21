"""Turn-routing properties. No UI required."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = ROOT / "modules" / "turn-routing" / "AGENTS.fragment.md"
SPEC = ROOT / "modules" / "turn-routing" / "SPEC.md"
PRESERVE = ROOT / "PRESERVE.md"
TUI = ROOT / "adapters" / "tui" / "README.md"


def run() -> int:
    fails = 0
    text = FRAGMENT.read_text(encoding="utf-8")
    spec = SPEC.read_text(encoding="utf-8")
    preserve = PRESERVE.read_text(encoding="utf-8")
    tui = TUI.read_text(encoding="utf-8")

    checks = [
        ("G1", "Chat.", "fragment names the chat phase"),
        ("G2", "/goal", "fragment names /goal"),
        ("G3", "seek go-ahead", "fragment requires go-ahead"),
        ("G4", "still chat", "let's-do-it without go stays chat"),
    ]
    for code, needle, label in checks:
        if needle in text:
            print(f"PASS {code} {label}")
        else:
            print(f"FAIL {code} {label}")
            fails += 1

    if "Owner-taught" in spec:
        print("PASS G5 provenance is owner-taught, not a fake corpus count")
    else:
        print("FAIL G5 missing provenance")
        fails += 1

    if "Do not strip the live VS Code install" in preserve:
        print("PASS G6 preserve doc forbids stripping the gold window")
    else:
        print("FAIL G6 gold window not protected")
        fails += 1

    if "kilo-claude-markdown.css" in tui and "Do not paste" in tui:
        print("PASS G7 TUI adapter refuses webview CSS")
    else:
        print("FAIL G7 TUI adapter missing CSS refusal")
        fails += 1

    return fails
