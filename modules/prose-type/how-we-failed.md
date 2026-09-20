# How we failed (type)

| Killed claim | Why it failed | Current property |
|---|---|---|
| Body `0.875rem` to match Claude’s `--cds-font-size-body` | Kilo chrome root is ~13px, so 0.875rem became ~11px. Brave looked big; Kilo looked tiny. | **T1** `16px` lock |
| Port the 2,000-line `--cds-*` palette | That is Claude’s whole app theme, not chat readability. | tokens.json only |
| Treat `assistant-message` as the tool-row root | Tool rows live on collapsible/tool slots. Styling the assistant bubble did not fix tool-row density. | Kilo adapter comments; not a portable token |

Type without the writing contract still fails. Run both checkers.
