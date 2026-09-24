"""Start a harness with the staged pack. Does not write live configs."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from installer.stage import is_live, stage  # noqa: E402

DEST = ROOT / "dist" / "install"
PRODUCTS = ("grok", "pi", "opencode", "deepseek", "kilo")


def ensure_staged() -> Path:
    if is_live(DEST):
        raise SystemExit("refusing to stage into a live config")
    if not (DEST / "receipt.json").is_file():
        stage(DEST, allow_live=False)
    return DEST


def command(product: str, ask: str) -> list[str]:
    dest = ensure_staged()
    if product == "grok":
        return [
            "grok",
            "-p",
            ask,
            "--model",
            "grok-4.7",
            "--output-format",
            "streaming-json",
            "--agent",
            str(dest / "grok" / "chat-profile.md"),
            "--max-turns",
            "2",
            "--no-subagents",
            "--permission-mode",
            "plan",
        ]
    if product == "pi":
        node = shutil.which("node") or "node"
        cli = Path(r"C:\Users\pujan\AppData\Local\nvm\v24.14.1\node_modules\@earendil-works\pi-coding-agent\dist\bundle\cli.js")
        prompt = (dest / "pi" / "SYSTEM.md").read_text(encoding="utf-8")
        return [
            node,
            str(cli),
            "-p",
            "--no-session",
            "--no-context-files",
            "--provider",
            "yolo-auto",
            "--model",
            "qwen3.8-flash",
            "--system-prompt",
            prompt,
            ask,
        ]
    if product == "opencode":
        return [
            "opencode",
            "run",
            "--dir",
            str(dest / "opencode"),
            "--model",
            "yolo-auto/qwen3.8-flash",
            "--format",
            "json",
            ask,
        ]
    if product == "deepseek":
        dsh = Path(r"C:\Users\pujan\AppData\Local\Temp\kilo\deepseek-harness\node_modules\@deepseek-ai\dsh\lib\bin.js")
        patch = Path(r"C:\Users\pujan\AppData\Local\Temp\kilo\deepseek-home\off.patch.yml")
        if not dsh.is_file():
            raise SystemExit("deepseek CLI is not on an NTFS temp install; refusing to write a live config")
        return ["node", str(dsh), "--profile", "headless", "--patch", str(patch), ask]
    if product == "kilo":
        raise SystemExit("kilo has no start flag that replaces the prompt; CSS is a stylesheet copy, not a launcher")
    raise SystemExit(f"unknown product: {product}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch a harness with the staged pack.")
    parser.add_argument("product", choices=PRODUCTS)
    parser.add_argument("ask", nargs="?", default="Say hello in one sentence. Do not edit files.")
    parser.add_argument("--print", action="store_true", dest="print_only")
    args = parser.parse_args(argv)
    argv_out = command(args.product, args.ask)
    if args.print_only:
        print("\n".join(argv_out))
        print("live_configs_written: false")
        return 0
    env = os.environ.copy()
    if args.product == "pi":
        env["PI_CODING_AGENT_DIR"] = str(DEST / "pi")
        env["PI_CODING_AGENT_SESSION_DIR"] = str(Path(os.environ.get("TEMP", ".")) / "ehm-pi-sessions")
    if args.product == "deepseek":
        env["DSH_HOME"] = r"C:\Users\pujan\AppData\Local\Temp\kilo\deepseek-home"
    proc = subprocess.run(argv_out, cwd=os.environ.get("TEMP", "."), env=env, check=False)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
