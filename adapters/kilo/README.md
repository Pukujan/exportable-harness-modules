# Kilo-only adapters

These files are a **reference implementation**, not the module.

Portable agents should implement SPECs under `modules/*/SPEC.md` and pass `python checkers/run_all.py`.

Do not vendor Kilo `dist/webview.js`. The poller snippet in `css-hot-reload` is the allowed Kilo-specific hook.

Do not overwrite the live `%USERPROFILE%\.config\kilo\` or the installed extension to run a before/after. `known-good/` is the copy source. The live window is the gold after.

Kilo-only checkers (dist hash, live VS Code capture) may be run from the machine that has the extension installed. They are not required for the portable suite.
