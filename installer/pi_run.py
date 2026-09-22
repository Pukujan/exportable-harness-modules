"""Pi on/off shard. Uses a throwaway PI_CODING_AGENT_DIR. Does not write ~/.pi/agent."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from installer.corpus import asks  # noqa: E402
from installer.score import score_reply  # noqa: E402

PI_DIR = ROOT / "dist" / "install" / "pi"
ON_PROMPT = (PI_DIR / "SYSTEM.md").read_text(encoding="utf-8")
OFF_PROMPT = "Answer the user."


def extract_pi(stream: str) -> tuple[str, bool]:
    texts: list[str] = []
    tools = False
    decoder = json.JSONDecoder()
    body = stream.lstrip("\ufeff")
    index = 0
    while index < len(body):
        while index < len(body) and body[index].isspace():
            index += 1
        if index >= len(body):
            break
        try:
            obj, end = decoder.raw_decode(body, index)
        except json.JSONDecodeError:
            newline = body.find("\n", index)
            if newline == -1:
                break
            index = newline + 1
            continue
        index = end
        if not isinstance(obj, dict):
            continue
        if obj.get("toolResults"):
            tools = True
        event = obj.get("assistantMessageEvent")
        if isinstance(event, dict) and event.get("type") == "text_delta" and isinstance(event.get("delta"), str):
            texts.append(event["delta"])
        message = obj.get("message") if obj.get("type") in ("message_end", "turn_end") else None
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue
        piece = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "toolCall" or block.get("type") == "tool_use":
                tools = True
            if block.get("type") == "text" and isinstance(block.get("text"), str):
                piece.append(block["text"])
        if piece:
            texts = piece
    return "".join(texts).strip(), tools


def run_arm(prompt: str, ask: str, session_dir: Path, agent_dir: Path) -> tuple[str, bool, int, str]:
    key = os.environ.get("QWEN_API_KEY", "")
    if not key:
        return "", False, 127, "QWEN_API_KEY missing"
    env = os.environ.copy()
    env["PI_CODING_AGENT_DIR"] = str(agent_dir)
    env["PI_CODING_AGENT_SESSION_DIR"] = str(session_dir)
    node = shutil.which("node") or "node"
    cli = Path(r"C:\Users\pujan\AppData\Local\nvm\v24.14.1\node_modules\@earendil-works\pi-coding-agent\dist\bundle\cli.js")
    if not cli.is_file():
        cli = Path(r"C:\nvm4w\nodejs\node_modules\@earendil-works\pi-coding-agent\dist\bundle\cli.js")
    argv = [
        node,
        str(cli),
        "-p",
        "--no-session",
        "--no-context-files",
        "--mode",
        "json",
        "--provider",
        "yolo-auto",
        "--model",
        "qwen3.8-flash",
        "--api-key",
        key,
        "--system-prompt",
        prompt,
        ask,
    ]
    try:
        proc = subprocess.run(
            argv,
            cwd=str(Path(os.environ.get("TEMP", "."))),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "", False, 124, "timeout"
    except OSError as exc:
        return "", False, 127, str(exc)
    raw = proc.stdout or ""
    text, tools = extract_pi(raw)
    err = "" if proc.returncode == 0 else (proc.stderr or "")[-500:]
    if not text:
        err = f"stdout_len={len(raw)} stderr={(proc.stderr or '')[-240:]} head={raw[:180]}"
        if "429" in raw or "pressure" in raw:
            err = "429 pressure"
    return text, tools, proc.returncode, err


def main() -> None:
    start = int(sys.argv[1])
    n = int(sys.argv[2])
    out = Path(sys.argv[3]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    session_dir = out / "sessions"
    session_dir.mkdir(exist_ok=True)
    agent_dir = out / "agent"
    if not (agent_dir / "models.json").is_file():
        if agent_dir.exists():
            shutil.rmtree(agent_dir)
        shutil.copytree(PI_DIR, agent_dir)
    jsonl = out / "pairs.jsonl"
    done = set()
    if jsonl.exists():
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done.add((row["id"], row["arm"]))
    selected = asks()[start : start + n]
    for ask in selected:
        for arm, prompt in (("off", OFF_PROMPT), ("on", ON_PROMPT)):
            if (ask["id"], arm) in done:
                continue
            text, tools, code, err = run_arm(prompt, ask["text"], session_dir, agent_dir)
            if "429" in err or "pressure" in err:
                print("rate limited, stopping")
                return
            scored = score_reply(ask["kind"], text, tools)
            time.sleep(2)
            row = {
                "id": ask["id"],
                "kind": ask["kind"],
                "arm": arm,
                "product": "pi",
                "text": text,
                "tools_started": tools,
                "pass": scored["pass"],
                "fails": scored["fails"],
                "returncode": code,
                "error": err,
            }
            with jsonl.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {jsonl}")


if __name__ == "__main__":
    main()
