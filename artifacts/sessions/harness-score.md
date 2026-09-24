# Throwaway harness score

Asks from `frozen-asks.md`. Live Kilo, Grok, and OpenCode configs were not edited.

## Streamed rerun, 2026-09-22

Grok used `grok-4.7` and `--output-format streaming-json`. OpenCode used `--model yolo-auto/qwen3.8-flash` and `--format json`, so the reply arrived as events. Pi used a throwaway config directory, not `~/.pi/agent/`, and `PI_CODING_AGENT_DIR` pointed at `adapters/pi/`. The key was passed at run time and is not in the repo.

| Harness | Model | Chat ask | Code ask |
| --- | --- | --- | --- |
| Grok | grok-4.7 | Pass. Bold lead, blank line, no TL;DR heading, no “I'll”, no tools. | Pass. First sentence states the change. Short. |
| OpenCode | yolo-auto/qwen3.8-flash | Pass. Bold lead, blank line, no TL;DR open, no “I'll”. It still mentioned the global instruction file, so this is not a clean pack-only proof. | Pass. First sentence states the change. Short. |
| Pi | yolo-auto/qwen3.8-flash | First try failed on a bold TL;DR line. Second try opened with “No” but the bold was in the last paragraph. Third try, after requiring bold in the first paragraph, dropped the bold and the blank line, and still printed the label. Captures are in `artifacts/sessions/captures/`. | Pass on the earlier code ask. | |

Pi’s first try failed before any reply: `Unknown provider "yolo-auto"`, because the throwaway `models.json` had an empty key and Pi refused to load the provider. A one-character placeholder, not the secret, made the provider visible. The key itself stayed in the environment.

## Earlier non-streamed run

Grok on grok-4.7, plain output, also passed both asks. OpenCode that round used the live build model, qwen3.8-27b, and the blank line was not visible. That run is not the score above.
