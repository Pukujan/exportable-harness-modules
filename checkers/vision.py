"""Portable vision properties: PNG magic, size, dimensions, 12s gate."""

from __future__ import annotations

import os
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "modules" / "css-hot-reload" / "adapters" / "kilo" / "verify-css.ps1"
SCREEN_VERIFY = ROOT / "modules" / "screen-vision" / "scripts" / "verify-css.ps1"
FIXTURE_DIR = ROOT / "modules" / "screen-vision" / "goldens"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MIN_BYTES = 8 * 1024
MIN_DIM = 100
DESKTOP_MIN_WIDTH = 1200


def _chunk(tag: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)


def write_png(path: Path, width: int, height: int) -> None:
    # Incompressible pixels so a 1200-wide fixture stays above the 8 KB floor.
    raw = b"".join(b"\x00" + os.urandom(width * 3) for _ in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"".join(
        [
            PNG_MAGIC,
            _chunk(b"IHDR", ihdr),
            _chunk(b"IDAT", zlib.compress(raw, 9)),
            _chunk(b"IEND", b""),
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def png_info(path: Path) -> tuple[int, int, int]:
    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise ValueError("not a PNG")
    if data[12:16] != b"IHDR":
        raise ValueError("missing IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height, len(data)


def check_png(path: Path, *, desktop: bool) -> list[str]:
    fails: list[str] = []
    if not path.is_file():
        return [f"P1 missing {path}"]
    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        fails.append("P2 not a PNG")
        return fails
    if len(data) <= MIN_BYTES:
        fails.append(f"P3 too small {len(data)}")
    width, height, _ = png_info(path)
    if width < MIN_DIM or height < MIN_DIM:
        fails.append(f"P4 dimensions {width}x{height}")
    if desktop and width < DESKTOP_MIN_WIDTH:
        fails.append(f"P9 width {width} < {DESKTOP_MIN_WIDTH}")
    return fails


def _has_12s_gate(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return "WaitSeconds -lt 12" in text or "wait at least 12" in text.lower()


def run() -> int:
    fails = 0
    fixture = FIXTURE_DIR / "desktop-min.png"
    write_png(fixture, 1200, 120)
    for prop, ok in [
        ("P2-P4-P9 fixture", check_png(fixture, desktop=True)),
    ]:
        if ok:
            print(f"FAIL {prop} {ok}")
            fails += 1
        else:
            print(f"PASS {prop} {fixture.name}")

    tiny = FIXTURE_DIR / "too-small.png"
    write_png(tiny, 80, 80)
    tiny_fails = check_png(tiny, desktop=True)
    if not tiny_fails:
        print("FAIL red PNG should fail P4/P9")
        fails += 1
    else:
        print(f"PASS red PNG rejected {tiny_fails}")

    for path, label in [(VERIFY, "css-hot-reload verify"), (SCREEN_VERIFY, "screen-vision verify")]:
        if not path.is_file():
            print(f"FAIL P8 missing {label}")
            fails += 1
            continue
        if _has_12s_gate(path):
            print(f"PASS P8 {label} 12s gate")
        else:
            print(f"FAIL P8 {label} missing 12s clamp")
            fails += 1

    shot = ROOT / "modules" / "screen-vision" / "scripts" / "screenshot.ps1"
    if shot.is_file() and "Write-Output $outPath" in shot.read_text(encoding="utf-8"):
        print("PASS P1 screenshot prints a path")
    else:
        print("FAIL P1 screenshot script missing")
        fails += 1

    return fails


if __name__ == "__main__":
    raise SystemExit(1 if run() else 0)
