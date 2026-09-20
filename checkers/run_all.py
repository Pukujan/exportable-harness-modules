"""Run portable checkers. No Kilo UI required."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from checkers import hot_reload, tokens, vision, writing  # noqa: E402


def main() -> int:
    total = 0
    for name, mod in [
        ("writing", writing),
        ("tokens", tokens),
        ("hot-reload", hot_reload),
        ("vision", vision),
    ]:
        print(f"=== {name} ===")
        failed = mod.run()
        total += failed
        print()
    if total:
        print(f"{total} FAILED")
        return 1
    print("ALL PORTABLE CHECKERS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
