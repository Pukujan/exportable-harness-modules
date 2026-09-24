"""Export every local Kilo session once, redacted, and do not overwrite existing files."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import bootstrap_pack as bp  # noqa: E402

OUT = ROOT / "artifacts" / "sessions"
DB = Path.home() / ".local" / "share" / "kilo" / "kilo.db"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    ids = [row[0] for row in con.execute("SELECT id FROM session ORDER BY time_created")]
    written = 0
    skipped = 0
    for sid in ids:
        path = OUT / f"{sid}.json"
        if path.exists():
            skipped += 1
            continue
        export, _n = bp.export_session(con, sid)
        path.write_text(json.dumps(export, ensure_ascii=False), encoding="utf-8")
        written += 1
        print(f"wrote {sid} {path.stat().st_size}")
    records = []
    for path in sorted(OUT.glob("ses_*.json")):
        data = path.read_bytes()
        records.append(
            {
                "path": f"artifacts/sessions/{path.name}",
                "byte_size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    manifest = {
        "export_kind": "kilo_session_gather_index",
        "note": "Later gather of local kilo.db. Not the 2026-09-20 ingest. Not W3C PROV. Existing files were not overwritten.",
        "gathered_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "session_count": len(records),
        "newly_written": written,
        "left_untouched": skipped,
        "files": records,
    }
    manifest_path = OUT / "gather-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"manifest {len(records)} new {written} skipped {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
