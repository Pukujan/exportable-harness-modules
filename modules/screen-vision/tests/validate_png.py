import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MIN_BYTES = 8 * 1024
MIN_DIM = 100


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_png.py <png-path>")

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"P1 missing file: {path}")

    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        fail("P2 not a PNG")

    if len(data) <= MIN_BYTES:
        fail(f"P3 file too small: {len(data)} bytes")

    if data[12:16] != b"IHDR":
        fail("P4 missing IHDR")

    width, height = struct.unpack(">II", data[16:24])
    if width < MIN_DIM or height < MIN_DIM:
        fail(f"P4 dimensions too small: {width}x{height}")

    print(f"PASS {path} {width}x{height} {len(data)} bytes")


if __name__ == "__main__":
    main()
