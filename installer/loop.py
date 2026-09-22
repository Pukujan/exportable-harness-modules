"""Controlled on/off runner. Plans by default. Does not edit live configs or staged profiles.

`python -m installer.loop` writes a plan only. It does not spawn grok or opencode.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

__all__ = [
    "extract_grok_text",
    "extract_opencode_text",
    "score_pair",
    "summarize",
    "top_miss",
    "overlay_rule",
    "grok_commands",
    "opencode_commands",
    "run_controlled",
]

_ARM_TIMEOUT = 180
_LABEL_RE = re.compile(r"t\s*l\s*;?\s*d\s*r", re.IGNORECASE)
_LABEL_ONLY_RE = re.compile(r"tl;?dr", re.IGNORECASE)
_THROAT_RE = re.compile(r"^(?:i'll|i will|let me)\b", re.IGNORECASE)
_APOSTROPHES = str.maketrans({"\u2019": "'", "\u2018": "'", "\u02bc": "'"})
_OVERLAY = {
    "mini": "Write at least two paragraphs separated by a blank line.",
    "heading": "Do not open with a heading.",
    "throat": "Do not open with I'll, I will, or Let me.",
    "summary-open": "Do not open with TL;DR, TLDR, or any other spelling of that label.",
    "bold-not-in-first": "In the first chunk, wrap the takeaway in **bold**.",
    "summary-label": "No chunk may print TL;DR, TLDR, or any other spelling of that label, even to deny it.",
    "tool-start": "Do not run tools on a why, a status question, or a code ask that says not to edit files.",
    "empty": "The first sentence must state a non-empty result.",
    "summary-heading": "Do not open with a summary heading or a heading that contains TL;DR or TLDR in any spelling.",
}
_TOOL_TYPES = {"tool_use", "tool", "tool_call", "tool_call_update"}


def extract_grok_text(stream: str) -> tuple[str, bool]:
    """Concatenate type==text data fields. Ignore type==thought. Flag tool_use or a tool call."""
    pieces: list[str] = []
    tools = False

    def consume(obj: object, in_thought: bool) -> None:
        nonlocal tools
        if isinstance(obj, list):
            for item in obj:
                consume(item, in_thought)
            return
        if not isinstance(obj, dict):
            return
        typ = obj.get("type")
        update = obj.get("sessionUpdate")
        thought = in_thought or typ in ("thought", "thinking") or update == "agent_thought_chunk"
        if typ in _TOOL_TYPES or update in ("tool_call", "tool_call_update") or _has_tool_call(obj):
            tools = True
        if not thought and typ == "text":
            data = obj.get("data")
            if isinstance(data, str):
                pieces.append(data)
            elif isinstance(obj.get("text"), str):
                pieces.append(obj["text"])
        elif not thought and update == "agent_message_chunk":
            content = obj.get("content")
            if isinstance(content, str):
                pieces.append(content)
            elif isinstance(content, dict) and content.get("type") != "text" and isinstance(content.get("text"), str):
                pieces.append(content["text"])
        for key, value in obj.items():
            if not thought and typ == "text" and key in ("data", "text") and isinstance(value, str):
                continue
            consume(value, thought)

    for obj in _iter_json(stream):
        consume(obj, False)
    return "".join(pieces), tools


def extract_opencode_text(stream: str) -> tuple[str, bool]:
    """Read JSON lines. Text is part.text where type==text. Flag a tool_use event."""
    buffers: dict[str, str] = {}
    order: list[str] = []
    anon = 0
    tools = False
    for line in stream.splitlines():
        raw = line.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        if _opencode_tool(obj):
            tools = True
        part = _opencode_part(obj)
        event_type = obj.get("type")
        part_type = part.get("type") if isinstance(part, dict) else None
        if event_type != "text" and part_type != "text":
            continue
        piece = part.get("text") if isinstance(part, dict) else None
        if not isinstance(piece, str):
            continue
        part_id = part.get("id") if isinstance(part, dict) else None
        if not isinstance(part_id, str) or not part_id:
            anon += 1
            part_id = f"#{anon}"
            buffers[part_id] = piece
            order.append(part_id)
            continue
        if part_id not in buffers:
            order.append(part_id)
            buffers[part_id] = piece
            continue
        prev = buffers[part_id]
        if piece.startswith(prev):
            buffers[part_id] = piece
        elif not prev.endswith(piece) and not prev.startswith(piece):
            buffers[part_id] = prev + piece
    return "".join(buffers[key] for key in order), tools


def score_pair(
    kind: str,
    on_text: str,
    off_text: str,
    on_tools: bool = False,
    off_tools: bool = False,
) -> dict:
    """Score both arms. on_wins means the pack arm passed and the control arm failed."""
    on_pass, on_fails = _score_one(kind, on_text, on_tools)
    off_pass, off_fails = _score_one(kind, off_text, off_tools)
    return {
        "on_pass": on_pass,
        "off_pass": off_pass,
        "on_fails": on_fails,
        "off_fails": off_fails,
        "on_wins": on_pass and not off_pass,
    }


def summarize(rows: list[dict]) -> dict:
    """Count pair outcomes. A tie is both passing or both failing."""
    pairs = _as_pairs(rows)
    on_pass = sum(1 for row in pairs if row["on_pass"])
    off_pass = sum(1 for row in pairs if row["off_pass"])
    on_wins = sum(1 for row in pairs if row["on_pass"] and not row["off_pass"])
    off_wins = sum(1 for row in pairs if row["off_pass"] and not row["on_pass"])
    ties = sum(1 for row in pairs if row["on_pass"] == row["off_pass"])
    return {
        "n": len(pairs),
        "on_pass": on_pass,
        "off_pass": off_pass,
        "on_wins": on_wins,
        "off_wins": off_wins,
        "ties": ties,
    }


def top_miss(rows: list[dict], arm: str = "on") -> str | None:
    """Most common fail string on that arm, or None."""
    counts: Counter[str] = Counter()
    key = f"{arm}_fails"
    for row in rows:
        if key in row:
            fails = row.get(key) or []
        elif row.get("arm") == arm:
            fails = row.get("fails") or []
        else:
            continue
        for fail in fails:
            counts[str(fail)] += 1
    if not counts:
        return None
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ranked[0][0]


def overlay_rule(miss: str) -> str:
    """One sentence to append to the pack prompt. Does not edit a profile."""
    if miss in _OVERLAY:
        return _OVERLAY[miss]
    return f"Do not do {miss}."


def grok_commands(ask: str, on_profile: Path, off_profile: Path) -> tuple[list[str], list[str]]:
    """On and off argv. --agent is the staged profile, never ~/.grok."""
    return (_grok_argv(ask, on_profile), _grok_argv(ask, off_profile))


def opencode_commands(ask: str, on_dir: Path, off_dir: Path) -> tuple[list[str], list[str]]:
    """On and off argv. --dir is a staged or temp directory, never the live OpenCode config."""
    return (_opencode_argv(ask, on_dir), _opencode_argv(ask, off_dir))


def run_controlled(
    dest: Path,
    out_dir: Path,
    n: int = 50,
    product: str = "grok",
    execute: bool = False,
    start: int = 0,
) -> dict:
    """Plan n on/off asks, or run them when execute is True.

    execute=False writes out_dir/plan.json and does not spawn a model.
    start skips that many asks so parallel shards do not repeat the same ids.
    A crash resume skips ask ids that already have both arms in pairs.jsonl.
    A new prompt round needs a new out_dir, or those ids will be skipped.
    """
    if n < 0 or start < 0:
        raise ValueError("n and start must be >= 0")
    product = product.strip().lower()
    if product not in ("grok", "opencode"):
        raise ValueError(f"unsupported product {product!r}; expected grok or opencode")
    dest = Path(dest)
    out_dir = Path(out_dir)
    _refuse_live(dest, "dest")
    _refuse_live(out_dir, "out_dir")
    asks = _load_asks()[start : start + n]
    on_target, off_target = _targets(dest, product)
    _refuse_agent(on_target)
    if product == "grok":
        _refuse_agent(off_target)
    else:
        _refuse_live(on_target, "opencode dir")

    if not execute:
        plan_path = out_dir / "plan.json"
        _write_json(plan_path, _plan(dest, product, n, asks, on_target, off_target))
        return {"executed": False, "n": n, "plan": str(plan_path)}

    _require_binary(product)
    if product == "grok":
        for path in (on_target, off_target):
            if not path.is_file():
                raise FileNotFoundError(
                    f"staged profile missing: {path}. The installer has not landed, or dest is wrong."
                )
    elif not (on_target / "AGENTS.md").is_file():
        raise FileNotFoundError(
            f"staged OpenCode instructions missing: {on_target / 'AGENTS.md'}. The installer has not landed."
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = out_dir / "pairs.jsonl"
    done = _completed_ids(_read_jsonl(jsonl_path), product)
    workdir = Path(tempfile.mkdtemp(prefix="ehm-loop-"))
    _refuse_repo_workdir(workdir)
    off_dir = _opencode_off_dir() if product == "opencode" else None
    try:
        for ask in asks:
            ask_id = str(ask["id"])
            if ask_id in done:
                continue
            kind = str(ask["kind"])
            text = str(ask["text"])
            if product == "grok":
                off_argv = _grok_argv(text, off_target)
                on_argv = _grok_argv(text, on_target)
            else:
                assert off_dir is not None
                off_argv = _opencode_argv(text, off_dir)
                on_argv = _opencode_argv(text, on_target)
            off_text, off_tools, off_meta = _spawn(product, off_argv, workdir)
            on_text, on_tools, on_meta = _spawn(product, on_argv, workdir)
            scored = score_pair(kind, on_text, off_text, on_tools, off_tools)
            _append_jsonl(
                jsonl_path,
                _arm_row(ask_id, kind, "off", product, off_text, off_tools, scored["off_pass"], scored["off_fails"], off_meta),
            )
            _append_jsonl(
                jsonl_path,
                _arm_row(ask_id, kind, "on", product, on_text, on_tools, scored["on_pass"], scored["on_fails"], on_meta),
            )
    finally:
        if off_dir is not None:
            shutil.rmtree(off_dir, ignore_errors=True)
        shutil.rmtree(workdir, ignore_errors=True)

    paired = _pairs_from_jsonl(_read_jsonl(jsonl_path), asks, product)
    summary = summarize(paired)
    summary_path = out_dir / "summary.json"
    _write_json(summary_path, summary)
    overlay_path = out_dir / "overlay.md"
    wrote_overlay = False
    if summary["on_pass"] <= summary["off_pass"]:
        miss = top_miss(paired, "on")
        sentence = overlay_rule(miss) if miss else "Do not treat a tie with the control arm as a win."
        overlay_path.write_text(sentence + "\n", encoding="utf-8")
        wrote_overlay = True
    elif overlay_path.exists():
        overlay_path.unlink()
    return {
        "executed": True,
        "n": n,
        "pairs": str(jsonl_path),
        "summary": str(summary_path),
        "on_pass": summary["on_pass"],
        "off_pass": summary["off_pass"],
        "overlay": str(overlay_path) if wrote_overlay else None,
    }


def _plan(
    dest: Path,
    product: str,
    n: int,
    asks: list[dict],
    on_target: Path,
    off_target: Path,
) -> dict:
    if product == "grok":
        on_command, off_command = grok_commands("{ask}", on_target, off_target)
        off_note = "Off arm uses the staged control profile. Do not install it live."
    else:
        on_command = _opencode_argv("{ask}", on_target)
        off_command = [
            "opencode",
            "run",
            "--dir",
            "{off_dir}",
            "--model",
            "yolo-auto/qwen3.8-flash",
            "--format",
            "json",
            "{ask}",
        ]
        off_note = (
            "Off arm is a temp dir created only when execute=True. "
            "Its AGENTS.md is only 'Answer the user.' The staged on profile is not edited. "
            "The global OpenCode file may still load and must not be edited."
        )
    return {
        "executed": False,
        "spawned": False,
        "n": n,
        "product": product,
        "dest": str(dest),
        "ids": [str(ask["id"]) for ask in asks],
        "asks": [
            {"id": str(ask["id"]), "kind": str(ask["kind"]), "text": str(ask["text"])}
            for ask in asks
        ],
        "on_profile": str(on_target),
        "off_profile": str(off_target) if product == "grok" else "{off_dir}",
        "on_command": on_command,
        "off_command": off_command,
        "off_note": off_note,
    }


def _targets(dest: Path, product: str) -> tuple[Path, Path]:
    root = dest.expanduser().resolve()
    if product == "grok":
        return root / "grok" / "chat-profile.md", root / "grok" / "off-profile.md"
    return root / "opencode", root / "opencode-off"


def _load_asks() -> list[dict]:
    try:
        from installer.corpus import asks
    except ImportError as exc:
        raise RuntimeError(
            "corpus worker has not landed: installer.corpus.asks() could not be imported"
        ) from exc
    loaded = asks()
    if not isinstance(loaded, list):
        raise RuntimeError("installer.corpus.asks() did not return a list")
    return loaded


def _score_one(kind: str, text: str, tools: bool) -> tuple[bool, list[str]]:
    try:
        from installer.score import score_reply
    except ImportError:
        score_reply = _fallback_score_reply
    try:
        raw = score_reply(kind, text, tools_started=tools)
    except TypeError:
        raw = score_reply(kind, text, tools)
    return _unpack_score(raw)


def _unpack_score(raw: object) -> tuple[bool, list[str]]:
    if isinstance(raw, dict):
        fails = [str(item) for item in (raw.get("fails") or [])]
        if "pass" in raw:
            return bool(raw["pass"]), fails
        return fails == [], fails
    if isinstance(raw, tuple) and len(raw) == 2:
        return bool(raw[0]), [str(item) for item in raw[1]]
    raise TypeError("score_reply must return {pass, fails}")


def _fallback_score_reply(kind: str, text: str, tools_started: bool = False) -> dict:
    if kind == "chat":
        fails = _fallback_chat(text, tools_started)
    elif kind == "code":
        fails = _fallback_code(text, tools_started)
    else:
        fails = ["unknown-kind"]
    return {"pass": fails == [], "fails": fails}


def _fallback_chunks(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    return [part.strip() for part in re.split(r"\n\s*\n", normalized) if part.strip()]


def _fallback_first_line(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for line in normalized.split("\n"):
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _fallback_chat(text: str, tools_started: bool) -> list[str]:
    fails: list[str] = []
    parts = _fallback_chunks(text)
    line = _fallback_first_line(text)
    if len(parts) < 2:
        fails.append("mini")
    if line.startswith("#"):
        fails.append("heading")
    if line and _THROAT_RE.match(line.translate(_APOSTROPHES)):
        fails.append("throat")
    if parts and _LABEL_ONLY_RE.fullmatch(re.sub(r"\s+", "", parts[0].strip())):
        fails.append("summary-open")
    if not parts or "**" not in parts[0]:
        fails.append("bold-not-in-first")
    if any(_LABEL_RE.search(part) for part in parts):
        fails.append("summary-label")
    if tools_started:
        fails.append("tool-start")
    return fails


def _fallback_code(text: str, tools_started: bool) -> list[str]:
    fails: list[str] = []
    line = _fallback_first_line(text)
    if not text or not text.strip():
        fails.append("empty")
    if line.startswith("#"):
        fails.append("heading")
    if line and _THROAT_RE.match(line.translate(_APOSTROPHES)):
        fails.append("throat")
    if text.strip() and _fallback_summary_heading(text):
        fails.append("summary-heading")
    if tools_started:
        fails.append("tool-start")
    return fails


def _fallback_summary_heading(text: str) -> bool:
    if _LABEL_RE.match(text.lstrip()):
        return True
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    for line in normalized.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") and _LABEL_RE.search(stripped):
            return True
    return False


def _grok_argv(ask: str, profile: Path) -> list[str]:
    _refuse_agent(profile)
    return [
        "grok",
        "-p",
        ask,
        "--model",
        "grok-4.7",
        "--output-format",
        "streaming-json",
        "--agent",
        str(profile),
        "--max-turns",
        "2",
        "--no-subagents",
        "--permission-mode",
        "plan",
    ]


def _opencode_argv(ask: str, directory: Path | str) -> list[str]:
    if not isinstance(directory, str):
        _refuse_live(directory, "opencode dir")
    elif directory != "{off_dir}":
        _refuse_live(Path(directory), "opencode dir")
    folder = directory if isinstance(directory, str) else str(directory)
    return [
        "opencode",
        "run",
        "--dir",
        folder,
        "--model",
        "yolo-auto/qwen3.8-flash",
        "--format",
        "json",
        ask,
    ]


def _spawn(product: str, argv: list[str], cwd: Path) -> tuple[str, bool, dict]:
    _refuse_repo_workdir(cwd)
    _refuse_live(cwd, "workdir")
    command = _resolve_argv(argv)
    meta: dict = {"returncode": None, "error": ""}
    try:
        proc = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=_ARM_TIMEOUT,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        meta["error"] = "timeout"
        meta["returncode"] = 124
        stdout = exc.stdout or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        text, tools = _extract(product, stdout)
        return text, tools, meta
    except OSError as exc:
        meta["error"] = str(exc)
        meta["returncode"] = 127
        return "", False, meta
    meta["returncode"] = proc.returncode
    if proc.returncode != 0:
        meta["error"] = (proc.stderr or "")[-2000:]
    text, tools = _extract(product, proc.stdout or "")
    return text, tools, meta


def _extract(product: str, stream: str) -> tuple[str, bool]:
    if product == "grok":
        return extract_grok_text(stream)
    return extract_opencode_text(stream)


def _resolve_argv(argv: list[str]) -> list[str]:
    name = argv[0]
    found = shutil.which(name)
    if os.name == "nt":
        exe = shutil.which(f"{name}.exe")
        cmd = shutil.which(f"{name}.cmd")
        if exe:
            found = exe
        elif cmd:
            found = cmd
        elif found and found.lower().endswith(".ps1"):
            sibling = Path(found).with_suffix(".cmd")
            if sibling.is_file():
                found = str(sibling)
    if not found:
        return argv
    path = Path(found)
    if os.name == "nt" and path.suffix.lower() in {".cmd", ".bat"}:
        return ["cmd", "/c", subprocess.list2cmdline([str(path), *argv[1:]])]
    return [str(path), *argv[1:]]


def _arm_row(
    ask_id: str,
    kind: str,
    arm: str,
    product: str,
    text: str,
    tools: bool,
    passed: bool,
    fails: list[str],
    meta: dict,
) -> dict:
    return {
        "id": ask_id,
        "kind": kind,
        "arm": arm,
        "product": product,
        "text": text,
        "tools_started": tools,
        "pass": passed,
        "fails": fails,
        "returncode": meta.get("returncode"),
        "error": meta.get("error") or "",
    }


def _append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _completed_ids(rows: list[dict], product: str) -> set[str]:
    arms: dict[str, set[str]] = {}
    for row in rows:
        if row.get("product") not in (None, product):
            continue
        ask_id = row.get("id")
        arm = row.get("arm")
        if not isinstance(ask_id, str) or arm not in ("on", "off"):
            continue
        arms.setdefault(ask_id, set()).add(arm)
    return {ask_id for ask_id, seen in arms.items() if "on" in seen and "off" in seen}


def _pairs_from_jsonl(rows: list[dict], asks: list[dict], product: str) -> list[dict]:
    latest: dict[tuple[str, str], dict] = {}
    for row in rows:
        if row.get("product") not in (None, product):
            continue
        ask_id = row.get("id")
        arm = row.get("arm")
        if isinstance(ask_id, str) and arm in ("on", "off"):
            latest[(ask_id, arm)] = row
    paired = []
    for ask in asks:
        ask_id = str(ask["id"])
        on = latest.get((ask_id, "on"))
        off = latest.get((ask_id, "off"))
        if not on or not off:
            continue
        on_pass = bool(on.get("pass"))
        off_pass = bool(off.get("pass"))
        paired.append(
            {
                "id": ask_id,
                "kind": str(ask.get("kind") or on.get("kind") or ""),
                "on_pass": on_pass,
                "off_pass": off_pass,
                "on_fails": list(on.get("fails") or []),
                "off_fails": list(off.get("fails") or []),
                "on_wins": on_pass and not off_pass,
            }
        )
    return paired


def _as_pairs(rows: list[dict]) -> list[dict]:
    if rows and all("on_pass" in row or "off_pass" in row for row in rows):
        return [
            {
                "on_pass": bool(row.get("on_pass")),
                "off_pass": bool(row.get("off_pass")),
                "on_fails": list(row.get("on_fails") or []),
                "off_fails": list(row.get("off_fails") or []),
            }
            for row in rows
        ]
    latest: dict[tuple[str, str], dict] = {}
    order: list[str] = []
    for index, row in enumerate(rows):
        ask_id = str(row.get("id") or index)
        arm = row.get("arm")
        if arm not in ("on", "off"):
            continue
        if ask_id not in order:
            order.append(ask_id)
        latest[(ask_id, arm)] = row
    paired = []
    for ask_id in order:
        on = latest.get((ask_id, "on"))
        off = latest.get((ask_id, "off"))
        if not on or not off:
            continue
        on_pass = bool(on.get("pass"))
        off_pass = bool(off.get("pass"))
        paired.append(
            {
                "on_pass": on_pass,
                "off_pass": off_pass,
                "on_fails": list(on.get("fails") or []),
                "off_fails": list(off.get("fails") or []),
            }
        )
    return paired


def _opencode_off_dir() -> Path:
    path = Path(tempfile.mkdtemp(prefix="ehm-opencode-off-"))
    _refuse_live(path, "opencode off dir")
    (path / "AGENTS.md").write_text("Answer the user.\n", encoding="utf-8")
    (path / "opencode.jsonc").write_text(
        '{\n  "instructions": ["AGENTS.md"]\n}\n',
        encoding="utf-8",
    )
    return path


def _require_binary(product: str) -> None:
    name = "grok" if product == "grok" else "opencode"
    if shutil.which(name) is None:
        raise RuntimeError(f"{name} is not on PATH; not starting a model run")


def _refuse_repo_workdir(path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    if _under(path, repo):
        raise RuntimeError(f"refusing to run a model in the repo: {path}")


def _refuse_live(path: Path, label: str) -> None:
    if _is_live(path):
        raise RuntimeError(f"refusing to touch a live config ({label}): {path}")


def _refuse_agent(profile: Path) -> None:
    text = str(profile).replace("/", "\\").lower()
    if text.startswith("~\\.grok") or text.endswith("\\.grok") or "\\.grok\\" in text:
        raise ValueError(f"refusing to point --agent at ~/.grok: {profile}")
    if _under(profile, Path.home() / ".grok"):
        raise ValueError(f"refusing to point --agent at ~/.grok: {profile}")


def _is_live(path: Path) -> bool:
    home = Path.home()
    roots = [
        home / ".config" / "kilo",
        home / ".grok",
        home / ".config" / "opencode",
    ]
    if any(_under(path, root) for root in roots):
        return True
    try:
        parts = [part.lower() for part in path.expanduser().resolve().parts]
    except OSError:
        parts = [part.lower() for part in path.expanduser().parts]
    blob = "\\".join(parts)
    return "kilo" in blob and "extension" in blob and "\\dist" in blob


def _under(path: Path, root: Path) -> bool:
    try:
        left = os.path.normcase(str(path.expanduser().resolve()))
        right = os.path.normcase(str(root.expanduser().resolve()))
    except OSError:
        left = os.path.normcase(os.path.abspath(os.path.expanduser(str(path))))
        right = os.path.normcase(os.path.abspath(os.path.expanduser(str(root))))
    right = right.rstrip("\\/")
    return left == right or left.startswith(right + os.sep)


def _has_tool_call(obj: dict) -> bool:
    for key in ("tool_call", "tool_calls", "toolCall", "tool_use"):
        if obj.get(key):
            return True
    return False


def _opencode_part(obj: dict) -> dict:
    part = obj.get("part")
    if isinstance(part, dict):
        return part
    props = obj.get("properties")
    if isinstance(props, dict) and isinstance(props.get("part"), dict):
        return props["part"]
    return {}


def _opencode_tool(obj: dict) -> bool:
    if _is_tool_type(obj.get("type")):
        return True
    part = _opencode_part(obj)
    return _is_tool_type(part.get("type"))


def _is_tool_type(value: object) -> bool:
    return isinstance(value, str) and value in _TOOL_TYPES


def _iter_json(stream: str):
    decoder = json.JSONDecoder()
    index = 0
    length = len(stream.lstrip("\ufeff"))
    body = stream.lstrip("\ufeff")
    while index < length:
        while index < length and body[index].isspace():
            index += 1
        if index >= length:
            return
        try:
            obj, end = decoder.raw_decode(body, index)
        except json.JSONDecodeError:
            newline = body.find("\n", index)
            if newline == -1:
                return
            index = newline + 1
            continue
        yield obj
        index = end


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_controlled(
        root / "dist" / "install",
        root / "dist" / "loop",
        n=50,
        product="grok",
        execute=False,
    )
    print(result["plan"])


if __name__ == "__main__":
    main()
