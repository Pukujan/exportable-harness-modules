# CSS hot-reload

## Goal

After a CSS patch, the agent must wait long enough for the harness to pick up the file before it captures the screen. Guessing from CSS text is not verification.

## Properties

- **H1** A CSS-verify script waits **at least 12 seconds** after patching before capture.
- **H2** Agents must not screenshot immediately after a CSS patch (`Start-Sleep 2` / `Start-Sleep 3` is a fail).
- **H3** CSS-only edits should not require a window reload once the poller is loaded.
- **H4** Writing-rule changes (`AGENTS.md`) need a **new chat**. Reload does not inject them into an old thread.
- **H5** Optional Kilo adapter: a 1s poller copies user CSS into the webview; a watcher re-patches `dist/` after extension updates.

## Recipe

1. Write tokens to the user CSS file.
2. Run the verify script (patch + **12s** + capture).
3. Read the PNG.
4. If wrong, fix and repeat from step 2.

## Not in scope

- Shipping only patched `dist/webview.js` as the module
- Claiming the poller is portable. Other harnesses need their own reload story; they must still honor **H1**.
