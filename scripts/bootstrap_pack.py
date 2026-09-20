"""Export redacted session bytes, copy Kilo adapters, ingest local FOSSIL events."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

PACK_ROOT = Path(__file__).resolve().parents[1]
PACK_ID = "pack_70d838252b9cbbdca9f5b07e068103d3"
PRIMARY = "ses_f4930aa1affeXv0fw5Syzn0Z8Y"
RELATED = ["ses_f4342410effev426tiKI9M4YUg"]
KILO_DB = Path.home() / ".local/share/kilo/kilo.db"
KILO_STORAGE = Path.home() / ".local/share/kilo/storage"
CONFIG = Path.home() / ".config/kilo"
SKILL = Path.home() / ".kilo/skills/screen-vision"
FOSSIL_SRC = Path(r"D:\claude\fossil-core\src")
FOSSIL_ROOT = Path(r"D:\claude\fossil-core")
WORKTREE_PLAN = Path(
    r"D:\claude\hades\hades-product\.kilo\worktrees\colorful-income\.kilo\plans\harness-ux-fossil-pack.md"
)
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

REDACT_PATTERNS = [
    (re.compile(r"(KILO_SERVER_PASSWORD['\"\s:=]+)[^\s'\"\\]+", re.I), r"\1[REDACTED]"),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-]+"), r"\1[REDACTED]"),
    (re.compile(r"sk-[A-Za-z0-9]{10,}"), "[REDACTED_TOKEN]"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "[REDACTED_TOKEN]"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "[REDACTED_TOKEN]"),
    (
        re.compile(
            r'(?i)("(?:password|secret|token|access_token|refresh_token|api_key|apikey)"\s*:\s*")[^"]+'
        ),
        r"\1[REDACTED]",
    ),
    (re.compile(r"(?i)(authorization['\"\s:=]+)[^\s'\"\\]+"), r"\1[REDACTED]"),
]


def redact(text: str) -> tuple[str, int]:
    count = 0
    out = text
    for pattern, repl in REDACT_PATTERNS:
        out, n = pattern.subn(repl, out)
        count += n
    return out, count


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clm(name: str) -> str:
    return "clm_" + hashlib.sha256(name.encode("utf-8")).hexdigest()[:24]


def write_json(path: Path, obj: object) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
    path.write_bytes(data)
    return data


def export_session(conn: sqlite3.Connection, session_id: str) -> tuple[dict, int]:
    conn.row_factory = sqlite3.Row
    session = conn.execute("SELECT * FROM session WHERE id=?", (session_id,)).fetchone()
    if session is None:
        raise SystemExit(f"missing session {session_id}")
    session_obj = {k: session[k] for k in session.keys() if k != "share_url"}
    messages = []
    for row in conn.execute(
        "SELECT id, time_created, time_updated, data FROM message WHERE session_id=? ORDER BY time_created",
        (session_id,),
    ):
        raw, n = redact(row["data"] or "")
        messages.append(
            {
                "id": row["id"],
                "time_created": row["time_created"],
                "time_updated": row["time_updated"],
                "data": json.loads(raw) if raw.startswith("{") else raw,
            }
        )
    parts = []
    redactions = 0
    for row in conn.execute(
        "SELECT id, message_id, time_created, time_updated, data FROM part WHERE session_id=? ORDER BY time_created",
        (session_id,),
    ):
        raw, n = redact(row["data"] or "")
        redactions += n
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = raw
        parts.append(
            {
                "id": row["id"],
                "message_id": row["message_id"],
                "time_created": row["time_created"],
                "time_updated": row["time_updated"],
                "data": payload,
            }
        )
    todos = [dict(r) for r in conn.execute("SELECT content, status, priority, position FROM todo WHERE session_id=?", (session_id,))]
    export = {
        "export_kind": "kilo_session_verbatim_redacted",
        "source_status": "verbatim",
        "redaction_policy": "strip auth.json / KILO_SERVER_PASSWORD / tokens / bearer / secret fields",
        "redaction_replacements": redactions,
        "exported_at": NOW,
        "session_id": session_id,
        "session": session_obj,
        "messages": messages,
        "parts": parts,
        "todos": todos,
    }
    return export, redactions


def copy_adapters() -> None:
    mapping = [
        (CONFIG / "kilo-claude-markdown.css", PACK_ROOT / "modules/prose-type/adapters/kilo/kilo-claude-markdown.css"),
        (CONFIG / "AGENTS.md", PACK_ROOT / "modules/writing-contract/adapters/kilo/AGENTS.md"),
        (CONFIG / "kilo-css-hotreload.js", PACK_ROOT / "modules/css-hot-reload/adapters/kilo/kilo-css-hotreload.js"),
        (CONFIG / "patch-kilo-chat-css.ps1", PACK_ROOT / "modules/css-hot-reload/adapters/kilo/patch-kilo-chat-css.ps1"),
        (CONFIG / "watch-kilo-chat-css.ps1", PACK_ROOT / "modules/css-hot-reload/adapters/kilo/watch-kilo-chat-css.ps1"),
        (CONFIG / "install-kilo-chat-css-persist.ps1", PACK_ROOT / "modules/css-hot-reload/adapters/kilo/install-kilo-chat-css-persist.ps1"),
        (SKILL / "scripts/verify-css.ps1", PACK_ROOT / "modules/css-hot-reload/adapters/kilo/verify-css.ps1"),
        (SKILL / "scripts/verify-css.ps1", PACK_ROOT / "modules/screen-vision/scripts/verify-css.ps1"),
        (SKILL / "scripts/screenshot.ps1", PACK_ROOT / "modules/screen-vision/scripts/screenshot.ps1"),
        (SKILL / "SKILL.md", PACK_ROOT / "modules/screen-vision/adapters/kilo/SKILL.md"),
        (SKILL / "references/spec.md", PACK_ROOT / "modules/screen-vision/adapters/kilo/spec.md"),
        (SKILL / "tests/validate_png.py", PACK_ROOT / "modules/screen-vision/tests/validate_png.py"),
        (CONFIG / "command/see.md", PACK_ROOT / "modules/screen-vision/adapters/kilo/see.md"),
        (CONFIG / "agent/vision.md", PACK_ROOT / "modules/screen-vision/adapters/kilo/vision.md"),
    ]
    for src, dest in mapping:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"copied {src.name} -> {dest.relative_to(PACK_ROOT)}")


def record_artifact(path: Path, media_type: str, records: list[dict]) -> str:
    data = path.read_bytes()
    digest = sha256_bytes(data)
    artifact_id = "art_" + digest[:32]
    blob = PACK_ROOT / "artifacts/blobs/sha256" / digest[:2] / digest
    blob.parent.mkdir(parents=True, exist_ok=True)
    if not blob.exists():
        blob.write_bytes(data)
    records.append(
        {
            "artifact_id": artifact_id,
            "path": str(path.relative_to(PACK_ROOT)).replace("\\", "/"),
            "byte_size": len(data),
            "content_hash": {"algorithm": "sha256", "digest": digest},
            "media_type": media_type,
        }
    )
    return artifact_id


def ingest(session_path: Path, artifact_id_hint: str, message_ids: list[str]) -> dict:
    sys.path.insert(0, str(FOSSIL_SRC))
    from fossil_core.application.ingest.pack_validation import KnowledgePackValidator
    from fossil_core.application.ingest.reviewed_evidence import (
        ReviewedClaimDraft,
        ReviewedEvidenceIngestService,
        ReviewedSource,
    )
    from fossil_core.artifact_store import ArtifactStore
    from fossil_core.event_store import DurableEventStore
    from fossil_core.source import SourceSnapshotStore

    manifest = json.loads((PACK_ROOT / "pack/manifest.json").read_text(encoding="utf-8"))
    artifact_store = ArtifactStore(PACK_ROOT / "artifacts")
    source_store = SourceSnapshotStore(
        PACK_ROOT / "sources",
        artifact_store,
        FOSSIL_ROOT / "schemas/source-snapshot/v1.schema.json",
        FOSSIL_ROOT / "schemas/citation/v1.schema.json",
    )
    event_store = DurableEventStore(
        PACK_ROOT / "events", FOSSIL_ROOT / "schemas/events/v1.schema.json"
    )
    service = ReviewedEvidenceIngestService(
        source_store=source_store,
        event_store=event_store,
        pack_validator=KnowledgePackValidator(
            FOSSIL_ROOT / "schemas/knowledge-pack/v1.schema.json"
        ),
    )

    current = [
        (
            "writing-answer-first",
            "Human-facing replies must start with the answer and must not force TL;DR on ordinary chat turns.",
        ),
        (
            "writing-real-paragraphs",
            "User-facing answers must use real paragraphs, not 1-4 crushed lines or a telegram break every 2-3 lines.",
        ),
        (
            "type-16px",
            "Chat prose body size is 16px with line-height 1.5 and headings 22/18/16, with pre-wrap on fenced code.",
        ),
        (
            "hot-reload-12s",
            "CSS verification must wait at least 12 seconds after patch before capture.",
        ),
        (
            "vision-png",
            "Visual claims require a PNG capture (magic, >8KB, >=100px; desktop width >=1200) that the agent reads.",
        ),
    ]
    killed = [
        (
            "always-tldr",
            "Every reply should open with ## TL;DR.",
            "writing-answer-first",
        ),
        (
            "body-0875rem",
            "Claude-like body type is 0.875rem.",
            "type-16px",
        ),
        (
            "hide-all-reasoning",
            "Hide all reasoning in the Kilo chat UI.",
            "writing-real-paragraphs",
        ),
        (
            "css-wait-3s",
            "Waiting 3 seconds after a CSS patch is enough before screenshot.",
            "hot-reload-12s",
        ),
        (
            "assistant-message-tool-root",
            "The assistant-message node is the tool-row layout root.",
            "vision-png",
        ),
    ]

    drafts = []
    for name, text in current:
        drafts.append(
            ReviewedClaimDraft(
                subject_ref=clm(name),
                claim_text=text,
                reason="Proposed from redacted session bytes plus passing portable checkers; not self-promoted to CURRENT_BEST.",
            )
        )
    for name, text, _repl in killed:
        drafts.append(
            ReviewedClaimDraft(
                subject_ref=clm(name),
                claim_text=text,
                reason="Historical claim later killed in this session. Recorded so supersession is queryable.",
            )
        )

    source_bytes = session_path.read_bytes()
    receipt = service.ingest(
        pack_manifest=manifest,
        source=ReviewedSource(
            data=source_bytes,
            source_kind="conversation",
            source_role="primary",
            locator={"identifier": PRIMARY},
            retrieved_at=NOW,
            published_at=NOW,
            media_type="application/json",
            quality={
                "authority": 0.9,
                "directness": 1.0,
                "independence": 1.0,
                "reproducibility": 1.0,
                "timeliness": 1.0,
                "notes": "verbatim-redacted Kilo session export; secrets stripped",
            },
        ),
        claims=drafts,
        review_ref="review:exportable-harness-modules:colorful-income-v1",
        actor={
            "actor_type": "agent",
            "actor_id": "kilo-colorful-income-pack-builder",
            "model_id": "xai/grok-4.6",
            "harness_version": "kilo-code",
            "skill_id": "skill_research-ingestion",
            "skill_version": "1.1.0",
        },
        occurred_at=NOW,
        recorded_at=NOW,
        correlation_id="colorful-income-kilo-ux-v1",
    )

    snap_id = receipt["source"]["snapshot_id"]
    art_id = receipt["source"]["artifact_id"]

    conversation = {
        "schema_version": "dkg.event.v1",
        "event_type": "conversation.ingested",
        "occurred_at": NOW,
        "recorded_at": NOW,
        "pack_id": PACK_ID,
        "actor": {
            "actor_type": "importer",
            "actor_id": "kilo-session-export",
            "harness_version": "kilo-code",
            "skill_id": "skill_research-ingestion",
            "skill_version": "1.1.0",
        },
        "subject_refs": [PRIMARY],
        "correlation_id": "colorful-income-kilo-ux-v1",
        "idempotency_key": f"conversation.ingested:{PRIMARY}:v1",
        "evidence_refs": [art_id],
        "source_snapshot_refs": [snap_id],
        "payload": {
            "conversation_id": PRIMARY,
            "source_status": "verbatim",
            "source_artifact_ids": [art_id],
            "message_ids": message_ids[:50] or [PRIMARY],
            "lineage_id": "lineage_colorful_income_kilo_ux_v1",
        },
        "provenance": {"method": "kilo_db_export_redacted"},
    }
    committed = [event_store.commit(event_store.validate(conversation))]

    for name, _text, replacement in killed:
        event = {
            "schema_version": "dkg.event.v1",
            "event_type": "claim.superseded",
            "occurred_at": NOW,
            "recorded_at": NOW,
            "pack_id": PACK_ID,
            "actor": {
                "actor_type": "agent",
                "actor_id": "kilo-colorful-income-pack-builder",
                "model_id": "xai/grok-4.6",
                "harness_version": "kilo-code",
                "skill_id": "skill_research-ingestion",
                "skill_version": "1.1.0",
            },
            "subject_refs": [clm(name)],
            "correlation_id": "colorful-income-kilo-ux-v1",
            "idempotency_key": f"claim.superseded:{name}:v1",
            "evidence_refs": [art_id],
            "source_snapshot_refs": [snap_id],
            "payload": {
                "from_state": "proposed",
                "superseded_by": clm(replacement),
                "reason": f"Killed during colorful-income UX work; replaced by {replacement}",
            },
            "provenance": {"method": "session_reversal_record"},
        }
        committed.append(event_store.commit(event_store.validate(event)))

    receipt["conversation_event_ids"] = [c["event_id"] for c in committed[:1]]
    receipt["supersession_event_ids"] = [c["event_id"] for c in committed[1:]]
    receipt["artifact_id_hint"] = artifact_id_hint
    return receipt


def main() -> None:
    copy_adapters()
    conn = sqlite3.connect(str(KILO_DB))
    records: list[dict] = []

    export, n = export_session(conn, PRIMARY)
    session_path = PACK_ROOT / "artifacts/sessions" / f"{PRIMARY}.json"
    write_json(session_path, export)
    print(f"exported {PRIMARY} redactions={n} messages={len(export['messages'])} parts={len(export['parts'])}")
    art = record_artifact(session_path, "application/json", records)

    for sid in RELATED:
        try:
            rel, rn = export_session(conn, sid)
        except SystemExit:
            continue
        path = PACK_ROOT / "artifacts/sessions" / f"{sid}.json"
        write_json(path, rel)
        record_artifact(path, "application/json", records)
        print(f"exported related {sid} redactions={rn}")

    for kind in ("session_share", "session_diff"):
        src = KILO_STORAGE / kind / f"{PRIMARY}.json"
        if src.is_file():
            dest = PACK_ROOT / "artifacts/kilo-storage" / kind / f"{PRIMARY}.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            raw, rn = redact(src.read_text(encoding="utf-8"))
            dest.write_text(raw, encoding="utf-8")
            record_artifact(dest, "application/json", records)
            print(f"copied {kind} redactions={rn}")

    if WORKTREE_PLAN.is_file():
        dest = PACK_ROOT / "artifacts/plans/harness-ux-fossil-pack.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(WORKTREE_PLAN, dest)
        record_artifact(dest, "text/markdown", records)

    recon = PACK_ROOT / "artifacts/reconstructed/session-audit.md"
    record_artifact(recon, "text/markdown", records)

    hashes = {
        "pack_id": PACK_ID,
        "exported_at": NOW,
        "primary_session_id": PRIMARY,
        "artifacts": records,
    }
    write_json(PACK_ROOT / "artifacts/hashes.json", hashes)
    manifest_path = PACK_ROOT / "artifacts/manifest.jsonl"
    manifest_path.write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in records),
        encoding="utf-8",
    )

    message_ids = [m["id"] for m in export["messages"]]
    receipt = ingest(session_path, art, message_ids)
    write_json(PACK_ROOT / "artifacts/ingest-receipt.json", receipt)
    print("ingest status", receipt.get("status"), "proposals", receipt.get("proposal_count"))
    print("supersessions", receipt.get("supersession_event_ids"))


if __name__ == "__main__":
    main()
