"""Save one Pi stdout stream so the extractor can be checked."""

import os
import shutil
import subprocess
from pathlib import Path

from installer.pi_run import OFF_PROMPT

key = os.environ["QWEN_API_KEY"]
cli = Path(r"C:\Users\pujan\AppData\Local\nvm\v24.14.1\node_modules\@earendil-works\pi-coding-agent\dist\bundle\cli.js")
env = os.environ.copy()
env["PI_CODING_AGENT_DIR"] = str(Path(r"D:\claude\exportable-harness-modules\dist\install\pi"))
argv = [
    shutil.which("node") or "node",
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
    OFF_PROMPT,
    "Say hello in one sentence.",
]
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
out = Path(r"D:\claude\exportable-harness-modules\artifacts\sessions\install-loop\pi-stdout.jsonl")
out.write_text(proc.stdout or "", encoding="utf-8")
print("rc", proc.returncode, "len", len(proc.stdout or ""))
