# Codex reconciliation evidence

Prompt review found **all requested clauses present** in one complete write of adapters/kilo/codex.md. This is a static contract review and repository check, not a live-model behavior score. Refs #12.

## Scope and sources

Task authority is **[leaf #12](https://github.com/Pukujan/exportable-harness-modules/issues/12)**; parent: none; dependency: [#9](https://github.com/Pukujan/exportable-harness-modules/issues/9). Primary writer: owner session directly, branch issue-12-reconcile-codex. The issue's requested runtime is Astra on cb/gpt-6-astra; no independent runtime attestation is available in these artifacts. Kilo did not write this prompt.

Source revision is **2026-09-24T17:50:25Z** for the issue/comments read before editing, including the [writer/branch record](https://github.com/Pukujan/exportable-harness-modules/issues/12#issuecomment-5819255443). Base commit: 37e5c2dc28b720b7c77b5f74fdbd69e75b50781d. Dependency #9 remains open; merged PRs #10 and #11 supply its code dependency. Current lifecycle and delivery facts belong to the live issue and PR.

| Source | Revision and supported claim |
| --- | --- |
| Internal: adapters/kilo/codex.md; modules/turn-routing/AGENTS.fragment.md; modules/writing-contract/AGENTS.fragment.md | Pukujan/exportable-harness-modules @ 37e5c2dc28b720b7c77b5f74fdbd69e75b50781d. Question/goal distinction, readable paragraphs, first-two-word meaning, payload bold. |
| Internal: pack/evidence.md; PRESERVE.md | Same repository/commit. Copy tests do not prove historical edit order or CSS; preserve the live installation and missing-evidence boundaries. |
| External: "Codex / ChatGPT Work agent prompt" | https://github.com/Pukujan/harness-on-steroids/blob/5b9a003755e698f043cf84e864a4dcab7d7e9a32/.kilo/agent/codex.md ; accessed 2026-09-24. Published observation/wait/delegation/write/verification loop and its reported counts. Underlying corpus validity was not checked. |
| Scope: "Astra owns the reconciled Codex prompt" | https://github.com/Pukujan/exportable-harness-modules/issues/12 ; accessed 2026-09-24. Required routing, writing, provenance, evaluation, and delivery constraints. |

## Reconciliation decisions

Question routing takes **precedence** over the upstream "loop for every user ask": supplied facts require no tool; a missing fact permits observation without edits. Named changes permit the necessary edit after inspection without a /goal gate. Long jobs retain both /goal and explicit go, then persist with the loop.

Work discipline retains **seven stages**: look, burst observation, wait, split only if warranted, write only when authorized, inspect every write/failure, and ground claims across turns. The source's absolute post-observation edit ban conflicts with the named-change route; the prompt states that exception explicitly. Historical counts remain reported context, never enforced quotas. Shell inspection is a capability fallback, not permission to mutate first. Delegation remains conditional on authorization.

Scoring separates **text from traces**. Six dimensions require evidence; failures cannot average away forbidden writes, missing gates, edit-first behavior, missing post-edit observation, or fabricated evidence. Question-only sessions do not write evaluation logs: the separately authorized evaluator does. N/A and unknown cannot become a passed behavioral case.

## Iteration 001

Timestamp: **2026-09-24T18:02:51Z**. Previous iteration: none. What changed: replaced adapters/kilo/codex.md once with the complete reconciled prompt; no later patch to that path. Working-byte SHA-256: 9c85c341ae044133abd8f5ce3d4b649693df7d7c58ee3fede2d96c39b20eb949. Git-normalized blob: 3518c09b3287bb683179c82cf89a8e7cc9d0b231. Git line-ending normalization may change the working-byte hash on another checkout; compare the blob for repository content.

| What ran | Observed result |
| --- | --- |
| Get-Content -Raw -Encoding UTF8 -LiteralPath adapters/kilo/codex.md | Complete post-write read; frontmatter and all sections intact. |
| git diff --check | Exit 0; no whitespace errors. Git emitted a line-ending normalization advisory. |
| git diff --stat / git diff --numstat | One product file changed: 62 insertions, 21 deletions. |
| Get-FileHash -Algorithm SHA256 -LiteralPath adapters/kilo/codex.md; git hash-object adapters/kilo/codex.md | Content identifiers recorded above. |
| python checkers/run_all.py | Exit 0, ALL PORTABLE CHECKERS PASSED. Existing pack checks, not a new prompt behavior test. |
| python -m continuity validate --root . | Exit 0, VALID, using installed continuity 0.4.0 in the isolated checkout. |
| Manual source/requirement walkthrough below | Static contract review passes; live reply scores unknown because no model session was run. |

| Static case | Contract finding | Live behavior |
| --- | --- | --- |
| Supplied-fact question / missing-fact question / research | Answer/no tool; needed lookup only; no edits. | Unknown |
| Named edit | Inspect target first, perform bounded edit, inspect diff and suitable checks. | Unknown |
| Long request: neither gate, goal only, go only, both gates | First three do not start; both gates activate persistent loop. | Unknown |
| Status during authorized job | Answer, then resume same scope unless stopped. | Unknown |
| Slow command / failed command | Await completion, inspect result/failure before mutation. | Unknown |
| External / internal / unavailable evidence | Title+URL+access date+claim; path+commit; unknown preserved. | Unknown |
| Opening / bold / paragraph shape | Semantic first-two-word rule, payload bold, whole-sentence ban, no unbolded wall. | Unknown |
| Iteration evidence | Timestamp, change, exact run, result, artifacts, prior reference; append-only. | Unknown |

Result: **static review and local checks pass**. Reply-rubric points: not awarded; coverage: no captured live replies/traces. Existing checkers inspect other pack rules and fixtures and cannot certify the new adapter. A later behavioral run must freeze the inputs and record all cases prescribed in adapters/kilo/codex.md; a short semantic inspection alone cannot award a live pass. No live Kilo test was needed to validate this reversible documentation change.

Next action is **PR delivery**: synchronize task/checkpoint, push with a receipt, require check and continuity validate on the current-base candidate, request auto-merge, then post the exact merge SHA on issue 12. CI, merge, and issue lifecycle are pending as of this note; later receipts on the live issue supersede this as-of state without rewriting the iteration.

## Iteration 002

Timestamp: **2026-09-24T18:04:38Z**. Previous iteration: 001 above. Prompt change: none; normalized blob remains 3518c09b3287bb683179c82cf89a8e7cc9d0b231. Added the issue/task projection, as-of checkpoint/handoff updates, and this evidence note. No catalog or generated index covers this new issue-specific note.

Validation initially **failed** after task creation: python -m continuity validate --root . exited 1 because TASK-EHM-0012-reconcile-codex.md lacked the required Checkpoint log heading. Read the failure, added that heading to the task file, reread it, and reran the same command: exit 0, VALID. git diff --check also exited 0. The adapter was not rewritten.

Result: **projections validate** locally. This correction changes task metadata structure only; iteration 001 product checks still apply. No live reply score is awarded. Next action remains checkpoint/push and required PR delivery gates.
