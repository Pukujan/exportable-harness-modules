# Exportable harness modules — Project Contract

<!-- continuity:project {"id":"exportable-harness-modules","protocol_version":"0.1.0-draft","schema":"project-continuity.project.v1","title":"Exportable harness modules"} -->

## Main goal

Keep the five UX behaviors that made VS Code Kilo usable, so a new config or a TUI can copy them without stripping the live install.

## Why

The live window is the gold after. A later session must be able to resume from this repository, not from a chat that may be gone.

## Scope

The five behavior specs, the known-good copy source, the evidence honesty rules, and a throwaway text-half copy test.

## Non-goals

W3C PROV rewritten from memory. A new export of the 2026-09-21 session unless the owner asks. Ordered diffs of the live Kilo config. Fossil-core ingest. Transcript mining. Editing `~/.config/kilo/` or the installed extension.

## Definition of success

A fresh session can read this contract, the current checkpoint, and the active task, then tell a copy test from a path test without searching the rest of the disk.
