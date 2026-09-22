"""One Pi call from a background process. Writes lengths, not the API key."""

from pathlib import Path

from installer.pi_run import OFF_PROMPT, run_arm

out = Path(r"D:\claude\exportable-harness-modules\artifacts\sessions\install-loop\pi-bg-debug.txt")
text, tools, code, err = run_arm(
    OFF_PROMPT,
    "Say hello in one sentence.",
    Path(r"D:\claude\exportable-harness-modules\dist\install\pi-sessions-bg"),
    Path(r"D:\claude\exportable-harness-modules\dist\install\pi"),
)
out.write_text(
    f"rc={code} tools={tools} len={len(text)} err={err[:240]}\n{text[:240]}\n",
    encoding="utf-8",
)
print(f"rc={code} len={len(text)}")
