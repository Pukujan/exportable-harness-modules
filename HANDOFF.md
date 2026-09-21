# Handoff

**Read this before searching.** The previous agent in this workspace had no project `AGENTS.md`, so Kilo did not inject a task. It then found a stale plan that says the GitHub repo is empty and went looking across the disk. That search was the bug. The pack is already here.

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
- `adapters/kilo/known-good/` — the prompt text that is working
- `modules/turn-routing/` — chat vs research vs code vs long run
- `modules/writing-contract/` — paragraph shape
- `modules/prose-type/adapters/kilo/kilo-claude-markdown.css` — snapshot of the live stylesheet
- `modules/css-hot-reload/` and `modules/screen-vision/` — 12s gate and capture policy

## Next

Nothing, until the owner says go. Likely later work, not started: a same-prompt compare on a **copy** or a TUI, never by reverting the live window.

## Do not

Follow the fossil plan. Mine transcripts. Patch the live Kilo config. Resume harness-on-steroids from this folder.
