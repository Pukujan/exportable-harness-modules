"""Score assistant text structure before and after the 2026-09-20 prompt write."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SESS = ROOT / "artifacts" / "sessions"
PRIMARY = "ses_f4930aa1affeXv0fw5Syzn0Z8Y"
KEYS = (
    "heading_open",
    "tldr_open",
    "ill_open",
    "bold_lead",
    "blank",
    "list",
    "table",
    "fence",
    "pathish",
    "px",
)


def iso(ms: int | None) -> str | None:
    if not ms:
        return None
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def file_of(payload: dict) -> str:
    state = payload.get("state") or {}
    inp = state.get("input") if isinstance(state, dict) else {}
    if not isinstance(inp, dict):
        return ""
    return str(inp.get("filePath") or inp.get("path") or "")


def shape(text: str) -> dict:
    head = text.strip()[:400]
    first = head.split("\n", 1)[0]
    return {
        "heading_open": first.startswith("#"),
        "tldr_open": "TL;DR" in head[:200],
        "ill_open": bool(re.match(r"(?i)^(i'll|i will|let me)\b", first)),
        "bold_lead": "**" in text[:350],
        "blank": "\n\n" in text,
        "list": bool(re.search(r"(?m)^(\s*[-*]|\s*\d+\.)\s+\S", text)),
        "table": bool(re.search(r"(?m)^\|.+\|", text)),
        "fence": "```" in text,
        "pathish": bool(re.search(r"[A-Za-z]:\\", text[:800])) or "`" in text[:400],
        "px": bool(re.search(r"(\bpx\b|\brem\b|font-size)", text[:500])),
    }


def load_rows() -> tuple[list[dict], int, int]:
    rows: list[dict] = []
    agents_ms = None
    jsonc_ms = None
    for path in SESS.glob("ses_*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        session = data.get("session") or {}
        parent = bool(session.get("parent_id"))
        roles: dict[str, str] = {}
        times: dict[str, int] = {}
        for msg in data.get("messages", []):
            md = msg.get("data") if isinstance(msg.get("data"), dict) else {}
            roles[msg["id"]] = md.get("role") or ""
            times[msg["id"]] = msg.get("time_created") or 0
        by: dict[str, list] = {}
        for part in data.get("parts", []):
            by.setdefault(part.get("message_id"), []).append(part)
            if path.stem != PRIMARY:
                continue
            payload = part.get("data")
            if not isinstance(payload, dict) or payload.get("type") != "tool":
                continue
            blob = json.dumps(payload, ensure_ascii=False)
            if "Never crush user-facing answers" not in blob:
                continue
            dest = file_of(payload)
            t = part.get("time_created") or 0
            if dest.endswith("AGENTS.md") and payload.get("tool") == "write":
                agents_ms = t if agents_ms is None else min(agents_ms, t)
            if dest.endswith("kilo.jsonc") and (jsonc_ms is None or t < jsonc_ms):
                jsonc_ms = t
        for mid, parts in by.items():
            if roles.get(mid) != "assistant":
                continue
            for part in parts:
                payload = part.get("data")
                if not isinstance(payload, dict) or payload.get("type") != "text":
                    continue
                text = (payload.get("text") or "").strip()
                if len(text) < 80:
                    continue
                row = shape(text)
                row["ms"] = part.get("time_created") or times.get(mid) or 0
                row["parent"] = parent
                row["session"] = path.stem
                row["title"] = session.get("title") or ""
                row["created"] = session.get("time_created") or 0
                rows.append(row)
    if agents_ms is None or jsonc_ms is None:
        raise SystemExit(f"missing cut agents={agents_ms} jsonc={jsonc_ms}")
    return rows, agents_ms, jsonc_ms


def rate(subset: list[dict]) -> dict:
    n = len(subset)
    out = {"n": n}
    for key in KEYS:
        out[key] = round(100 * sum(1 for row in subset if row[key]) / n, 1) if n else 0
    return out


def main() -> None:
    rows, agents_ms, jsonc_ms = load_rows()
    top = [row for row in rows if not row["parent"]]
    ci = [row for row in rows if row["session"] == PRIMARY]
    report = {
        "cut": {
            "agents_md_write": {"when": iso(agents_ms), "ms": agents_ms, "path": r"C:\Users\pujan\.config\kilo\AGENTS.md"},
            "kilo_jsonc_edit": {"when": iso(jsonc_ms), "ms": jsonc_ms, "path": r"C:\Users\pujan\.config\kilo\kilo.jsonc"},
            "note": "The instruction file and the sent agent prompt were written eight seconds apart. That pair is the cut.",
        },
        "colorful_income": {
            "before_write": rate([r for r in ci if r["ms"] < agents_ms]),
            "after_write": rate([r for r in ci if r["ms"] >= agents_ms]),
        },
        "top_level": {
            "before_write": rate([r for r in top if r["ms"] < agents_ms]),
            "after_write": rate([r for r in top if r["ms"] >= agents_ms]),
        },
    }
    scopes: dict[str, list] = {"before": [], "after": [], "spans": []}
    seen: dict[str, dict] = {}
    for row in rows:
        info = seen.setdefault(
            row["session"],
            {"title": row["title"], "created": row["created"], "parent": row["parent"], "min": row["ms"], "max": row["ms"], "n": 0},
        )
        info["min"] = min(info["min"], row["ms"])
        info["max"] = max(info["max"], row["ms"])
        info["n"] += 1
    for sid, info in seen.items():
        if info["max"] < agents_ms:
            bucket = "before"
        elif info["min"] >= agents_ms:
            bucket = "after"
        else:
            bucket = "spans"
        scopes[bucket].append({"id": sid, **info, "created_iso": iso(info["created"])})
    report["scopes"] = {k: sorted(v, key=lambda item: item["created"]) for k, v in scopes.items()}
    out = SESS / "structure-score.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("agents", iso(agents_ms))
    print("jsonc", iso(jsonc_ms))
    print("ci", report["colorful_income"])
    print("top", report["top_level"])
    print("scope", {k: len(v) for k, v in scopes.items()})


if __name__ == "__main__":
    main()
