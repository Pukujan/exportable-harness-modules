# Handoff

**Read this before searching.** The previous agent in this workspace had no project `AGENTS.md`, so Kilo did not inject a task. It then found a stale plan that says the GitHub repo is empty and went looking across the disk. That search was the bug. The pack is already here.

Continuity, if a session is gone: `PROJECT.md`, then `checkpoints/CURRENT.md`, then the active task. That protocol is from `project-continuity-modules` at `9328f36` (PCM 0.4.0). It does not replace this handoff, and it does not make the missing config history exist.

GitHub Issues own task scope, acceptance, and lifecycle. Merged history owns accepted docs. PR checks and merge records own delivery. A local task file is a projection, not the authority. Before a push, sync the checkpoint. After a push, write a receipt on the leaf issue. Required CI and auto-merge are mandatory before calling work delivered. A completed task is not active. Do not close an issue from a commit message. Use `Refs #<number>` for progress. Live Kilo, Grok, and OpenCode configs stay untouched. The adoption leaf is https://github.com/Pukujan/exportable-harness-modules/issues/2. Parent: none.

## Where you are

| Item | Value |
| --- | --- |
| Folder | `D:\claude\exportable-harness-modules` |
| Remote | https://github.com/Pukujan/exportable-harness-modules |
| Known-good commits | `abeb2bb` preserve overlay, `0439c69` workspace file |
| Agent Manager worktree | `.kilo/worktrees/sugared-provelone` (detached at the workspace commit; not a second project) |

## Owner gold

2026-09-21: VS Code Kilo was unusable on every model. After turn routing, the output prompt, paragraph shape, webview type, and screenshot-before-claim, the owner said it works extremely well. Do not risk that install.

## Already in the tree

- `PRESERVE.md` — the five behaviors and what a TUI can copy
- `pack/evidence.md` — copy test vs path test; do not invent the missing history
- `adapters/tui/AGENTS.md` — routing + writing paste for a throwaway TUI
- `adapters/opencode/` and `adapters/grok/` — how to score that paste without touching live config
- `adapters/kilo/known-good/` — the prompt text that is working
- `modules/turn-routing/` — chat vs research vs code vs long run
- `modules/writing-contract/` — paragraph shape
- `modules/prose-type/adapters/kilo/kilo-claude-markdown.css` — snapshot of the live stylesheet
- `modules/css-hot-reload/` and `modules/screen-vision/` — 12s gate and capture policy

## Next

Owner-authorized change: **[issue #12](https://github.com/Pukujan/exportable-harness-modules/issues/12)** reconciles adapters/kilo/codex.md. Parent: none; dependency: #9, implemented through merged PRs #10 and #11. Source issue/comment revision: 2026-09-24T17:50:25Z. Task EHM-0012, branch issue-12-reconcile-codex, primary writer owner session directly. As of 2026-09-24T18:02:51Z, static review and local checks pass; PR gates and merge are pending. Read tasks/TASK-EHM-0012-reconcile-codex.md and artifacts/issue-12/codex-reconciliation.md for the scoped change. The live issue's subsequent merge receipt owns delivery and supersedes this pending state. Refs #12.

Historical goal text below stays **historical**; issue 12 does not resume it.

The long run is `GOAL.md`. It is frozen. A `/goal` that says to follow that file until acceptance is the start. It does not morph itself. Pi already passes the text rules. Grok chat is the current miss.

Not started, and not implied by a doc edit: a new export of the 2026-09-21 session, ordered diffs of the live Kilo config, or a W3C PROV graph. Do not backfill those from memory.

## Do not

Follow the fossil plan. Mine transcripts. Patch the live Kilo config. Resume harness-on-steroids from this folder.
