"""Guard the installer scorer and the 50-ask corpus. No live config."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from installer.corpus import asks  # noqa: E402
from installer.score import score_reply  # noqa: E402

C01 = (
    "Why are we always trying to do a TL;DR? Is that built into the product? "
    "Answer only. Do not edit files."
)
K01 = (
    "The paragraph gaps are too large. "
    "Say what you would change, in a short reply. Do not edit files."
)
CHAT_END = "Answer only. Do not edit files."
CODE_END = "Say what you would change, in a short reply. Do not edit files."

CHAT_PASS = (
    "A short question does not need a summary block. **Answer first.**\n"
    "\n"
    "The second paragraph keeps the reply chunked, not mini."
)
CHAT_TLDR = (
    "Printing TL;DR is the miss. **This is bold.**\n"
    "\n"
    "The second paragraph keeps the reply from being a single chunk."
)


def _check(ok: bool, label: str) -> int:
    if ok:
        print(f"PASS {label}")
        return 0
    print(f"FAIL {label}")
    return 1


def _stage_line() -> tuple[int, str]:
    stage = ROOT / "installer" / "stage.py"
    if not stage.is_file():
        return 0, "SKIP stage not present"
    try:
        from installer import stage as stage_mod
    except Exception as exc:
        return 1, (
            "FAIL is_live cannot be imported from installer.stage "
            f"({type(exc).__name__}: {exc})"
        )
    is_live = getattr(stage_mod, "is_live", None)
    if not callable(is_live):
        return 1, "FAIL is_live cannot be imported from installer.stage"
    return 0, "PASS is_live importable from installer.stage"


def run() -> int:
    fails = 0
    items = asks()
    chat = [item for item in items if item.get("kind") == "chat"]
    code = [item for item in items if item.get("kind") == "code"]
    by_id = {item.get("id"): item for item in items}
    expected_ids = {f"c{i:02d}" for i in range(1, 26)} | {f"k{i:02d}" for i in range(1, 26)}

    fails += _check(len(items) == 50, "asks() length is 50")
    fails += _check(len(chat) == 25 and len(code) == 25, "25 chat and 25 code")
    fails += _check(
        set(by_id) == expected_ids and len(by_id) == 50,
        "ids are c01-c25 and k01-k25",
    )
    fails += _check(
        by_id.get("c01", {}).get("text") == C01 and by_id.get("c01", {}).get("kind") == "chat",
        "c01 matches the frozen chat ask",
    )
    fails += _check(
        by_id.get("k01", {}).get("text") == K01 and by_id.get("k01", {}).get("kind") == "code",
        "k01 matches the frozen code ask",
    )
    bad_chat = [
        item.get("id")
        for item in chat
        if not str(item.get("text", "")).endswith(CHAT_END)
    ]
    bad_code = [
        item.get("id")
        for item in code
        if not str(item.get("text", "")).endswith(CODE_END)
    ]
    fails += _check(not bad_chat, "chat asks end with the answer-only suffix")
    fails += _check(not bad_code, "code asks end with the short-reply suffix")

    good_chat = score_reply("chat", CHAT_PASS)
    fails += _check(
        good_chat.get("pass") is True and good_chat.get("fails") == [],
        "chat two-paragraph reply with bold passes",
    )
    bad_chat_score = score_reply("chat", CHAT_TLDR)
    fails += _check(
        bad_chat_score.get("pass") is False,
        "chat reply that prints TL;DR fails",
    )
    good_code = score_reply("code", "I would use a single line break.\n")
    fails += _check(
        good_code.get("pass") is True and good_code.get("fails") == [],
        "code single line break passes",
    )
    bad_code_score = score_reply("code", "## TL;DR\n\nshrink it")
    fails += _check(
        bad_code_score.get("pass") is False,
        "code summary heading fails",
    )

    stage_fails, stage_line = _stage_line()
    print(stage_line)
    fails += stage_fails
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
