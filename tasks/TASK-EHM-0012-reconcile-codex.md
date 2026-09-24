# Reconcile the Codex prompt

<!-- continuity:task {"schema":"project-continuity.task.v1","protocol_version":"0.1.0-draft","id":"EHM-0012","status":"active","owner":"issue-12-primary-writer","priority":"owner-requested","depends_on":[],"goal":"Reconcile the Kilo Codex prompt and deliver it through required CI and auto-merge for issue 12.","why":"One prompt must retain question routing, bounded edits, gated long jobs, Work tool discipline, readable replies, and evidence rules.","acceptance":["Reconciled adapter contains all routing, Work loop, writing, citation, scoring, and iteration requirements.","Timestamped iteration records observed checks and honest limitations.","Required check and continuity validate pass, auto-merge lands, exact merge SHA is posted on issue 12."],"next_action":"Await PR delivery; live issue 12 owns current lifecycle and merge receipt.","issue_url":"https://github.com/Pukujan/exportable-harness-modules/issues/12"} -->

Scope authority: **[leaf #12](https://github.com/Pukujan/exportable-harness-modules/issues/12)**. Parent: none. External issue dependency: [#9](https://github.com/Pukujan/exportable-harness-modules/issues/9), code delivered by PRs #10 and #11; no local task dependency. Source issue/comment revision: 2026-09-24T17:50:25Z. Primary writer: owner session directly; branch: issue-12-reconcile-codex, as recorded in the [issue receipt](https://github.com/Pukujan/exportable-harness-modules/issues/12#issuecomment-5819255443).

As-of state is **active, pending delivery** at 2026-09-24T18:02:51Z. This is a projection; the live issue owns later lifecycle and delivery facts. A merge receipt supersedes this pending state and does not imply another implementation task.

Product change is **adapters/kilo/codex.md**, written once. Research, review, sources, content hash, observed commands, and limitations are in [the iteration note](../artifacts/issue-12/codex-reconciliation.md). Base commit: 37e5c2dc28b720b7c77b5f74fdbd69e75b50781d.

Validation passes **locally**: portable checkers, continuity 0.4.0 validation in the isolated checkout, diff whitespace check, and static contract review. Live-model behavioral scores remain unknown; no claim of CSS or historical replay is made.

Delivery requires **check and continuity validate**, auto-merge to main, then the exact merge SHA posted on issue 12. Refs #12 only. Issue closure is not part of this task's automated actions. No product blockers observed; required CI and merge remain pending as of this projection.

Next action is **publish and verify**: checkpoint/push receipt, PR, required gates, auto-merge, merge receipt. Live configurations and the canonical checkout's prior dirty files remain outside this change. The isolated checkout is inside D:\claude\exportable-harness-modules.

## Checkpoint log

### 2026-09-24 18:05:30 UTC — issue-12-primary-writer

<!-- continuity:checkpoint {"agent":"issue-12-primary-writer","blocked":["Required PR checks and auto-merge pending; not delivered."],"changed":["adapters/kilo/codex.md; evidence note; task/current/handoff projections"],"completed":["Reconciled adapter written once; static review and portable checks passed."],"decisions":["Leaf #12; parent none; dependency #9 delivered through PRs #10 and #11; no live-model score claimed."],"evidence":["artifacts/issue-12/codex-reconciliation.md; python checkers/run_all.py exit 0; python -m continuity validate --root . VALID; Refs #12."],"next_action":"Create PR to main; wait for check and continuity validate; enable auto-merge; post exact merge SHA on issue 12.","protocol_version":"0.1.0-draft","schema":"project-continuity.checkpoint.v1","task_id":"EHM-0012","timestamp":"2026-09-24T18:05:30Z"} -->
<!-- continuity:checkpoint-operation {"payload_sha256":"20ce2fc25b1e045394a0732ce66c97937a2be5b4dcff0e2dc2a3389e7fd421a2","request_id":"issue-12-reconcile-codex-20260924-01","schema":"project-continuity.checkpoint-operation.v1","task_id":"EHM-0012"} -->

Completed:
- Reconciled adapter written once; static review and portable checks passed.

Evidence:
- artifacts/issue-12/codex-reconciliation.md; python checkers/run_all.py exit 0; python -m continuity validate --root . VALID; Refs #12.

Decisions:
- Leaf #12; parent none; dependency #9 delivered through PRs #10 and #11; no live-model score claimed.

Changed:
- adapters/kilo/codex.md; evidence note; task/current/handoff projections

Blocked/uncertain:
- Required PR checks and auto-merge pending; not delivered.

Next:
- Create PR to main; wait for check and continuity validate; enable auto-merge; post exact merge SHA on issue 12.
