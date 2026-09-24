"""Split assistant replies by the user ask in front of them. Chat is not averaged with code."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESS = ROOT / "artifacts" / "sessions"
CUT = 1789872252479  # 2026-09-20 02:44:12 UTC AGENTS.md write
CHAT = re.compile(
    r"(?i)\b(why|what(?:'s| is)|how did|how do|explain|status|stopping|think|tell me)\b|\?"
)
CODE = re.compile(
    r"(?i)\b(implement|fix|add|edit|patch|refactor|write the|build|test|create the|change the)\b"
)


def shape(text: str) -> dict:
    head = text.strip()[:400]
    first = head.split("\n", 1)[0]
    return {
        "tldr_open": "TL;DR" in head[:200],
        "ill_open": bool(re.match(r"(?i)^(i'll|i will|let me)\b", first)),
        "bold_lead": "**" in text[:350],
        "blank": "\n\n" in text,
        "crushed": ("\n\n" not in text) and len([ln for ln in text.splitlines() if ln.strip()]) <= 4,
    }


def kind(user: str) -> str:
    code = bool(CODE.search(user))
    chat = bool(CHAT.search(user))
    if code and not chat:
        return "code"
    if chat and not code:
        return "chat"
    if code and chat:
        return "code" if re.search(r"(?i)\b(implement|fix|edit|patch|add)\b", user) else "chat"
    return "other"


def pairs() -> list[dict]:
    rows = []
    for path in SESS.glob("ses_*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if (data.get("session") or {}).get("parent_id"):
            continue
        ordered = []
        for msg in data.get("messages", []):
            md = msg.get("data") if isinstance(msg.get("data"), dict) else {}
            ordered.append((msg.get("time_created") or 0, md.get("role"), msg["id"]))
        ordered.sort()
        texts: dict[str, str] = {}
        times: dict[str, int] = {}
        for part in data.get("parts", []):
            payload = part.get("data")
            if not isinstance(payload, dict) or payload.get("type") != "text":
                continue
            text = (payload.get("text") or "").strip()
            if len(text) < 40:
                continue
            mid = part.get("message_id")
            prev = texts.get(mid, "")
            if len(text) > len(prev):
                texts[mid] = text
                times[mid] = part.get("time_created") or 0
        last_user = ""
        for _t, role, mid in ordered:
            if role == "user" and mid in texts:
                last_user = texts[mid]
            elif role == "assistant" and mid in texts and last_user:
                reply = texts[mid]
                if len(reply) < 80:
                    continue
                row = shape(reply)
                row["kind"] = kind(last_user)
                row["ms"] = times.get(mid) or 0
                row["ask"] = last_user[:240].replace("\n", " ")
                row["reply"] = reply[:400].replace("\n", " / ")
                row["session"] = path.stem
                rows.append(row)
    return rows


def rate(subset: list[dict]) -> dict:
    n = len(subset)
    keys = ("tldr_open", "ill_open", "bold_lead", "blank", "crushed")
    out = {"n": n}
    for key in keys:
        out[key] = round(100 * sum(1 for row in subset if row[key]) / n, 1) if n else 0
    return out


def main() -> None:
    rows = pairs()
    report = {}
    for scope, pred in (
        ("before", lambda row: row["ms"] < CUT),
        ("after", lambda row: row["ms"] >= CUT),
    ):
        report[scope] = {}
        for label in ("chat", "code", "other"):
            report[scope][label] = rate([row for row in rows if pred(row) and row["kind"] == label])
    out = SESS / "chat-code-score.json"
    out.write_text(json.dumps({"cut_ms": CUT, "rates": report, "examples": {
        "chat_after": [row for row in rows if row["ms"] >= CUT and row["kind"] == "chat"][:4],
        "code_after": [row for row in rows if row["ms"] >= CUT and row["kind"] == "code"][:4],
    }}, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
