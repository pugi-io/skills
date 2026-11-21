---
name: workspace-knowledge-sync
description: Reconcile existing workspace documentation and Graphify with current repository, PR and task evidence when the user requests knowledge maintenance or a graph refresh. Do not trigger for a simple code question or single documentation edit.
---

# Workspace knowledge synchronization

Use current source files for implementation behavior, GitHub for PR heads/reviews/checks and the issue tracker for task status. Memory, old reports and graph edges are navigation aids, not proof of current state. Focus on the latest 48–72 hours while preserving older decisions and unresolved history. The recency window is not an exclusion cutoff: when reconciling unresolved tasks, inspect status/comment history plus linked PR, merge and staging deployment evidence for at least the prior three weeks, and follow older linked work when needed. Implementation can predate its deployment or the most recent Jira update by weeks.

## What works today

| Step | Surface | Status |
|---|---|---|
| Reconcile existing workspace documentation | Files in the established workspace docs structure | Available |
| Refresh code/document knowledge graphs | Configured Graphify corpus and local tooling | Available when configured sources are accessible |
| Refresh PR or Jira semantics in Graphify | Source-specific graph ingestion | Not available unless the configured pipeline explicitly supports those sources |

## Documentation

1. Discover repository boundaries and existing workspace documentation outside Git checkouts. Identify living guides, dated snapshots, architecture/API references, roadmap, changelog and task/PR/Jira status documents.
2. Compare claims against current primary evidence. Correct only demonstrated stale claims, update links and current status, and reconcile duplicates without erasing meaningful history. Separate implementation, plans, acceptance and unverified behavior.
3. For Jira, paginate the assigned-issue query and each issue's comment feed through its final page. Record full comment totals and clearly label whether analysis covered every comment or only latest/recent comments; do not treat an embedded comment count as comment evidence.
4. Follow the existing document structure. Avoid a new top-level file when an established destination exists. Do not write private information into a broader-access document.
5. For a recovery/sync handoff, keep a concise dated entry in the existing maintenance log: distinguish fetch from pull, list exact verified before/after SHAs for mutations, record conflicts and resolution evidence, name checks actually run, and state which requested surfaces were not refreshed. Never convert a prior session's report into current evidence without rereading the source.

For workspace-wide PR/Jira reconciliation, keep `docs/PULL-REQUEST-WORKFLOW.md` as a concise rule guide and append dated operational snapshots to `docs/pr-drafts/2026-10-26-review-fixes/STATUS-REFRESH.md`. Keep `docs/GRAPHIFY-MAINTENANCE.md` as a concise runbook; put detailed graph backup, candidate, provenance, coverage and integrity records in `docs/history/GRAPHIFY-MAINTENANCE-HISTORY-2026-11-18.md`. Do not duplicate one live snapshot across multiple guides.

### PR, Jira and deployment evidence

- Keep implementation, review, deployment, staging QA handoff, acceptance and production release as separate states. A merge to a QA branch does not prove deployment.
- Do not change `Rejected By QA` without the user's explicit decision to start a new QA pass.
- `In Review` means the full code implementation is complete and every associated implementation PR is merged. `Ready QA` is the handoff after code completion, merge of all associated implementation PRs, and deployment of all required changes/dependencies to staging or production; record the exact target URL, deployed SHA/run and QA scenarios. It means QA can begin, not that acceptance passed. Keep production deployment evidence separate. Preserve existing `Ready QA` and `Done` statuses during sync unless the user explicitly asks to change them.
- Production deployment, deployed SHA and smoke are separate release evidence. Do not infer production behavior from staging or repository state.
- Repeated syncs must re-read current Jira and GitHub fields, preserve dated history, and correct superseded claims without duplicating current-state snapshots.
- For each active assigned issue, use the issue history and linked changes/deploys to determine when work was actually implemented and when its exact SHA reached staging. Do not leave completed work in an active status just because the relevant PR or deploy is older than the latest comment; do not promote partial fixes merely because an older PR merged.
- During PR reconciliation, compare each recorded base SHA with the target branch's freshly fetched SHA. Verify mergeability against that current base with `git merge-tree` or an isolated equivalent; a clean comparison means no conflict, not that the PR branch is synchronized or its checks are current. Preserve Draft state and historical notes unless current evidence or explicit instructions justify a change.
- If an explicit task authorizes `git push --no-verify`, document the manually run hook-equivalent checks and any remaining verification gap; do not make it a standing default for later tasks.
- `--no-verify` on `git push` skips push hooks only; it does not bypass a commit hook that runs earlier. Record hook configuration, manual equivalents and remaining gaps separately for commit and push. Do not report a push, CI result, mergeability calculation, or deployment as complete until that surface returns current evidence.
- When a local check fails because the host differs from the target runner, retain the exact failure and verify on the supported runner. Do not translate a local environment failure into either a code defect or a passing check without matching evidence.

### Conflicting evidence

- Resolve apparent conflicts by checking source, scope, commit/version and timestamp first. Current implementation claims come from the relevant source and tests; PR state from the current GitHub PR/head; Jira state from the issue's current fields and history. A dated note may remain valid as history while no longer describing current state.
- If sources describe different scopes or times, document each with its source/date and update only the current-state claim. Preserve meaningful prior decisions as dated history.
- If equally authoritative current sources still disagree, do not blend them into an invented answer or delete either record. Record the contradiction and provenance, mark the affected conclusion unresolved, and continue unrelated documentation/Graphify work. Ask the responsible owner only when resolving that contradiction is necessary to proceed with a consequential change.
- For Git merge conflicts encountered while gathering evidence, follow the conflict-resolution workflow in [workspace-sync](../workspace-sync/SKILL.md): preserve both sides, resolve from code/history/tests when unambiguous, and never treat a path overlap or unavailable fetch as a proven conflict.

## Graphify

1. Inspect the configured root and every configured leaf corpus, ignore rules, output locations, incremental semantics, deletion/collision behavior and current integrity before refresh. Save a verified backup and record baseline graph/manifest hashes and counts before writing.
2. Refresh only the requested sources with supported tooling. Prefer isolated candidates; where supported, set `GRAPHIFY_OUT` to a candidate output directory so the source checkout and active graph stay untouched. Compare node IDs, raw directed edge keys, provenance, manifest/source coverage and confirmed source deletions before promotion. `--force` may be used only on an isolated candidate after the active graph and manifest have verified backups; never use it to overwrite active data before the loss comparison. Retain the active graph if the candidate loses unverified history or live-source coverage. Code-only extraction does not refresh Markdown semantics, GitHub PRs or Jira. Preserve historical knowledge and unrelated working changes; remove only confirmed obsolete temporary records.
3. Verify JSON parsing, duplicate node IDs, duplicate raw edge keys, dangling endpoints, provenance, extraction warnings and coverage/count changes where available. Report collisions, dropped nodes, unavailable sources and incomplete semantic extraction. Do not claim a semantic refresh when only code was indexed. Re-runs must compare against the current baseline and avoid duplicating snapshots or deleting existing history.

## Completion report

Link changed documents. Summarize verified current facts, historical decisions retained, sources refreshed, integrity evidence and remaining gaps. Never infer production behavior from source code alone or invent statuses.
