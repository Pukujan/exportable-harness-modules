# Hot-reload recipe

## Portable

Any adapter must expose a “verify CSS” command that:

1. Applies the current CSS.
2. Waits ≥ 12 seconds.
3. Captures the chat surface.
4. Prints one PNG path.

Do not fold the wait into the model’s “I’ll wait” prose. Put it in the script so it cannot be skipped.

## Kilo reference

1. `patch-kilo-chat-css.ps1` copies `kilo-claude-markdown.css` to `dist/kilo-user-markdown.css` and appends a 1s fetch poller to `webview.js` if missing.
2. `kilo-css-hotreload.js` polls that override file.
3. `verify-css.ps1` patches, clamps wait to 12s, then screenshots VS Code.
4. `watch-kilo-chat-css.ps1` re-patches after a Kilo extension update.

Window reload is for poller-JS install or extension updates, not for CSS-only edits.
