# Pi copy adapter

Pi’s built-in catalog has no `yolo-auto` provider. This folder is a throwaway config directory, not a write to `~/.pi/agent/`.

Point `PI_CODING_AGENT_DIR` at this folder. Pass `--api-key` from `QWEN_API_KEY` at run time. Do not put the key in this file. Model id is `qwen3.8-flash`. If Pi rejects that provider, record the error. Do not fall back to Google.
