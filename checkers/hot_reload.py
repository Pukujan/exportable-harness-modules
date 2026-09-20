"""Portable CSS hot-reload gate. Kilo poller is adapter-only."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "modules" / "css-hot-reload" / "adapters" / "kilo" / "verify-css.ps1"
HOT = ROOT / "modules" / "css-hot-reload" / "adapters" / "kilo" / "kilo-css-hotreload.js"
RECIPE = ROOT / "modules" / "css-hot-reload" / "recipe.md"


def run() -> int:
    fails = 0
    verify = VERIFY.read_text(encoding="utf-8")
    if "WaitSeconds -lt 12" not in verify:
        print("FAIL H1 verify-css does not clamp wait to 12s")
        fails += 1
    else:
        print("PASS H1 12s clamp")
    if "Start-Sleep -Seconds $WaitSeconds" in verify:
        print("PASS H1 sleep uses clamped wait")
    else:
        print("FAIL H1 missing sleep after patch")
        fails += 1
    if "Start-Sleep -Seconds 3" in verify or "Start-Sleep -Seconds 2" in verify:
        print("FAIL H2 2s/3s wait still present")
        fails += 1
    else:
        print("PASS H2 no 2s/3s wait")

    if HOT.is_file() and "kilo-claude-hot-start" in HOT.read_text(encoding="utf-8"):
        print("PASS H5 Kilo poller adapter present")
    else:
        print("FAIL H5 missing Kilo poller adapter")
        fails += 1

    recipe = RECIPE.read_text(encoding="utf-8")
    if "12" in recipe:
        print("PASS H1 recipe mentions 12s")
    else:
        print("FAIL H1 recipe missing 12s")
        fails += 1

    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
