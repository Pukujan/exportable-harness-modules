"""Build the instruction text that a product actually sends.

Reads adapters/tui/AGENTS.md and appends the three proved rules when that
file does not already contain them. Does not edit the source file.
"""

from __future__ import annotations

from pathlib import Path

PROVED_RULES = (
    "In the first chunk, wrap the takeaway in **bold**.",
    "No chunk may print TL;DR, TLDR, or any other spelling of that label, even to deny it.",
    "Do not run tools on a why, a status question, or a code ask that says not to edit files.",
)

_TUI_REL = Path("adapters") / "tui" / "AGENTS.md"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _norm(text: str) -> str:
    return " ".join(text.split()).casefold()


def rule_present(text: str, rule: str) -> bool:
    """True only when this exact rule sentence is already in the text."""
    return _norm(rule) in _norm(text)


def missing_rules(text: str) -> list[str]:
    return [rule for rule in PROVED_RULES if not rule_present(text, rule)]


def append_rules(text: str) -> str:
    """Append proved rules that are not already present. Source files stay untouched."""
    missing = missing_rules(text)
    if not missing:
        return text if text.endswith("\n") else text + "\n"
    if text and not text.endswith("\n"):
        text += "\n"
    lines = [
        "",
        "# Proved rules",
        "",
        "Apply these even if an earlier line disagrees.",
        "",
    ]
    lines.extend(f"- {rule}" for rule in missing)
    lines.append("")
    return text + "\n".join(lines)


def pack_prompt() -> str:
    """Instruction text built from the TUI copy source plus any missing proved rules."""
    source = repo_root() / _TUI_REL
    text = source.read_text(encoding="utf-8")
    return append_rules(text)
