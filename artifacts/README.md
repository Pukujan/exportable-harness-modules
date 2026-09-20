# Artifacts

- `sessions/*.json` — verbatim-redacted Kilo session export from `kilo.db`. Secrets stripped. Cite these bytes.
- `kilo-storage/` — `session_share` / `session_diff` JSON for the primary session.
- `reconstructed/` — labeled reconstruction, not the transcript.
- `plans/` — the harness-ux-fossil-pack plan that produced this pack.
- `ingest-receipt.json` — local reviewed-ingest receipt (`status: proposed`). Not a live MCP `fossil.commit`.
- `manifest.jsonl` / `hashes.json` / `blobs/` — content hashes.

Pack write target: `pack_70d838252b9cbbdca9f5b07e068103d3` only.
