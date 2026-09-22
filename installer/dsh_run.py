"""DeepSeek harness on/off using the yolo-auto key. Does not write live configs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from installer.corpus import asks  # noqa: E402
from installer.score import score_reply  # noqa: E402

DSH_HOME = Path(r"C:\Users\pujan\AppData\Local\Temp\kilo\deepseek-home")
DSH_BIN = Path(r"C:\Users\pujan\AppData\Local\Temp\kilo\deepseek-harness\node_modules\@deepseek-ai\dsh\lib\bin.js")
OFF_PATCH = DSH_HOME / "off.patch.yml"
ON_PATCH = DSH_HOME / "on.patch.yml"
PACK = (ROOT / "dist" / "install" / "pi" / "SYSTEM.md").read_text(encoding="utf-8")


def write_on_patch() -> None:
    body = ["- id: agent-default-model", "  config:", "    provider: yolo-auto", "    model: qwen3.8-flash", "- id: system-prompt", "  config:", "    includeHarnessIdentity: false", "    personaPrefix: |"]
    for line in PACK.splitlines():
        body.append("      " + line)
    ON_PATCH.write_text("\n".join(body) + "\n", encoding="utf-8")


def reply_text(stream: str) -> str:
    marker = "dsh: reasoning:"
    text = stream
    if marker in text:
        text = text.split(marker, 1)[1]
    parts = [part.strip() for part in text.replace("\r\n", "\n").split("\n\n") if part.strip()]
    if not parts:
        return ""
    return parts[-1]


def run_arm(ask: str, patch: Path) -> tuple[str, bool, int, str]:
    if not os.environ.get("QWEN_API_KEY"):
        return "", False, 127, "QWEN_API_KEY missing"
    env = os.environ.copy()
    env["DSH_HOME"] = str(DSH_HOME)
    argv = [
        "node",
        str(DSH_BIN),
        "--profile",
        "headless",
        "--patch",
        str(patch),
        ask,
    ]
    try:
        proc = subprocess.run(
            argv,
            cwd=os.environ.get("TEMP", "."),
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
    raw = (proc.stdout or "") + "\n" + (proc.stderr or "")
    text = reply_text(proc.stdout or "")
    tools = "tool" in (proc.stderr or "").lower() and "dsh: reasoning" not in (proc.stderr or "")
    err = "" if proc.returncode == 0 and text else raw[-400:]
    if "429" in raw or "pressure" in raw:
        err = "429 pressure"
    return text, tools, proc.returncode, err


def main() -> None:
    start = int(sys.argv[1])
    n = int(sys.argv[2])
    out = Path(sys.argv[3]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    write_on_patch()
    jsonl = out / "pairs.jsonl"
    done = set()
    if jsonl.exists():
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                done.add((row["id"], row["arm"]))
    for ask in asks()[start : start + n]:
        for arm, patch in (("off", OFF_PATCH), ("on", ON_PATCH)):
            if (ask["id"], arm) in done:
                continue
            text, tools, code, err = run_arm(ask["text"], patch)
            if "429" in err or "pressure" in err:
                print("rate limited, stopping")
                return
            scored = score_reply(ask["kind"], text, tools)
            row = {
                "id": ask["id"],
                "kind": ask["kind"],
                "arm": arm,
                "product": "deepseek",
                "text": text,
                "tools_started": tools,
                "pass": scored["pass"],
                "fails": scored["fails"],
                "returncode": code,
                "error": err,
            }
            with jsonl.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            time.sleep(2)
    print(f"wrote {jsonl}")


if __name__ == "__main__":
    main()
