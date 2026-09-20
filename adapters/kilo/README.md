# Kilo-only adapters

These files are a **reference implementation**, not the module.

Portable agents should implement SPECs under `modules/*/SPEC.md` and pass `python checkers/run_all.py`.

Do not vendor Kilo `dist/webview.js`. The poller snippet in `css-hot-reload` is the allowed Kilo-specific hook.

Kilo-only checkers (dist hash, live VS Code capture) may be run from the machine that has the extension installed. They are not required for the portable suite.
