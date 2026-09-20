# How we failed (hot-reload)

| Killed claim | Why it failed | Current property |
|---|---|---|
| Wait 3 seconds after CSS patch | The Kilo webview poller often had not swapped styles yet. Screenshots lied. | **H1** 12s gate |
| Screenshot in the same turn as the patch | Same race. Agents reported visual success from CSS-only reasoning. | **H2** verify script only |
| Hide all reasoning forever | Users still needed a short preview while the model thought. | Kilo `reasoning_display: preview`; completed reasoning can stay collapsed |
