# Evidence spec

This is not a sixth UX behavior. It says what a later agent may cite, and what it may not invent.

Two tests are different. Do not treat them as one.

**Copy test.** Paste the known-good prompt, or the TUI instruction file, onto a new config. Run `python checkers/run_all.py`. That proves the written rules can be reapplied. It does not prove which edit came first.

**Path test.** An ordered trail of the live Kilo config, the 2026-09-21 session, and an accepted provenance graph. This repo cannot run that test. The bytes are absent. Do not reconstruct them from chat memory and check them in as evidence.

## Properties

- **E1 Copy is not history.** Passing the checkers and matching `adapters/kilo/known-good/` proves the end state can be reapplied. It does not prove edit order.
- **E2 Cite the session bytes, not the audit.** Claims about what was said cite `artifacts/sessions/` and the hash in `artifacts/hashes.json`. If `artifacts/reconstructed/session-audit.md` disagrees, the session JSON wins.
- **E3 The stored diff is not the config trail.** `artifacts/kilo-storage/session_diff/` adds three plan files. It is not a history of the instruction file, the agent prompt, or the stylesheet.
- **E4 Dates do not match.** The export and the proposed events are stamped 2026-09-20. The owner’s “this works” signal and the preserve commits are 2026-09-21. Do not cite the export as that day’s transcript.
- **E5 Provenance here is FOSSIL-shaped and unaccepted.** Events use `dkg.event.v1`. The receipt status is `proposed`. Accepted count is zero. The receipt is non-authoritative. This is not W3C PROV. Do not rewrite these events into `prov:Entity` records.
- **E6 Do not backfill.** Missing config diffs and the later session are absent. An agent must not reconstruct them and pack them as verbatim evidence.
- **E7 Secrets stay out.** A later export, only if the owner asks for one, is redacted first. `unredacted/` is gitignored. That capture is a separate go. It is not part of a doc edit.

## What a copy test may claim

A headless `grok -p` or `opencode run` on a **throwaway directory** may be scored for routing and writing: did a question get an answer, and does the reply start with the result in real paragraphs.

That score is a later text check. It is not the 2026-09-20 session, and it is not proof the live VS Code window still matches the snapshot. It cannot confirm CSS. Do not point the experiment at `~/.config/kilo/` or the installed extension `dist/`.
