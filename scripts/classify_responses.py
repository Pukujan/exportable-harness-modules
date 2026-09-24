"""Label each assistant text as mini or chunked, plus chunk types. Not a good/bad score."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESS = ROOT / "artifacts" / "sessions"
CUT = 1789872252479


def chunk_type(text: str, index: int) -> str:
    head = text.strip()
    if "TL;DR" in head:
        return "summary"
    if head.startswith("#"):
        return "heading"
    if re.search(r"(?m)^(\s*[-*]|\s*\d+\.)\s+\S", head):
        return "list"
    if re.search(r"(?m)^\|.+\|", head):
        return "table"
    if "```" in head:
        return "fence"
    if re.search(r"(?i)(system prompt|directive you|instructions I'm|instructions I am)", head):
        return "echo"
    if re.search(r"(\bpx\b|\brem\b|font-size|[A-Za-z]:\\)", head):
        return "leak"
    if "**" in head:
        return "takeaway"
    if index == 0:
        return "answer"
    return "explain"


def classify(text: str) -> dict:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    if not blocks:
        return {"grain": "empty", "open": "empty", "chunks": []}
    first = blocks[0]
    first_line = first.split("\n", 1)[0].strip()
    if first_line.startswith("#"):
        open_ = "heading"
    elif "TL;DR" in first[:200]:
        open_ = "summary"
    elif re.match(r"(?i)^(i'll|i will|let me)\b", first_line):
        open_ = "throat"
    else:
        open_ = "sentence"
    return {
        "grain": "mini" if len(blocks) == 1 else "chunked",
        "open": open_,
        "chunks": [chunk_type(block, i) for i, block in enumerate(blocks)],
        "bold_in_first": "**" in first[:350],
    }


def main() -> None:
    rows = []
    for path in SESS.glob("ses_*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if (data.get("session") or {}).get("parent_id"):
            continue
        roles = {}
        for msg in data.get("messages", []):
            md = msg.get("data") if isinstance(msg.get("data"), dict) else {}
            roles[msg["id"]] = md.get("role")
        for part in data.get("parts", []):
            payload = part.get("data")
            if not isinstance(payload, dict) or payload.get("type") != "text":
                continue
            if roles.get(part.get("message_id")) != "assistant":
                continue
            text = (payload.get("text") or "").strip()
            if len(text) < 80:
                continue
            label = classify(text)
            label["session"] = path.stem
            label["ms"] = part.get("time_created") or 0
            label["side"] = "after" if label["ms"] >= CUT else "before"
            rows.append(label)
    counts: dict[str, int] = {}
    for row in rows:
        key = f"{row['side']}|{row['grain']}|{row['open']}"
        counts[key] = counts.get(key, 0) + 1
        for kind in row["chunks"]:
            ck = f"{row['side']}|chunk|{kind}"
            counts[ck] = counts.get(ck, 0) + 1
    out = {
        "n": len(rows),
        "cut": "2026-09-20 02:44:12 UTC",
        "counts": dict(sorted(counts.items())),
    }
    (SESS / "response-classes.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    (SESS / "response-classes.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )
    print("n", len(rows))
    for key, n in sorted(counts.items()):
        if "|chunk|" not in key:
            print(key, n)


if __name__ == "__main__":
    main()
