"""Say whether a Kilo config is sending the pack prompt. Read-only by default."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from installer.stage import is_live  # noqa: E402

MARKER = "The first two words of every heading, list item, and paragraph must already carry the point."
PACK_AGENTS = ("build", "code", "plan", "general")
KNOWN = ROOT / "adapters" / "kilo" / "known-good" / "agent-prompt.txt"


def load_config(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # kilo.jsonc may contain comments. Strip // lines and retry.
        stripped = "\n".join(line for line in text.splitlines() if not line.strip().startswith("//"))
        return json.loads(stripped)


def agent_prompts(config: dict) -> dict[str, str]:
    agent = config.get("agent")
    if not isinstance(agent, dict):
        return {}
    out = {}
    for name, body in agent.items():
        if isinstance(body, dict) and isinstance(body.get("prompt"), str):
            out[name] = body["prompt"]
    return out


def report(path: Path) -> int:
    prompts = agent_prompts(load_config(path))
    print(f"config: {path}")
    misses = 0
    for name in PACK_AGENTS:
        text = prompts.get(name, "")
        ok = MARKER in text
        print(f"{name}: {'pack' if ok else 'NOT pack'}")
        if not ok:
            misses += 1
    for name in sorted(prompts):
        if name in PACK_AGENTS:
            continue
        print(f"{name}: not the pack agent")
    if not prompts:
        print("no agent prompts found")
        return 1
    print("other agents use the product default and will not match this setup")
    return 1 if misses else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check whether Kilo agents send the pack prompt.")
    parser.add_argument("config", type=Path, nargs="?", default=Path.home() / ".config" / "kilo" / "kilo.jsonc")
    args = parser.parse_args(argv)
    if not args.config.is_file():
        print(f"missing config: {args.config}")
        return 1
    if is_live(args.config):
        print("read-only check of a live config. nothing was written.")
    return report(args.config)


if __name__ == "__main__":
    raise SystemExit(main())
