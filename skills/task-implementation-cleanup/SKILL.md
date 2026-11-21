---
name: task-implementation-cleanup
description: Implement a scoped product task or bug fix in a Pugi repository, then clean up the affected area, update relevant existing documentation, and add focused regression tests.
---

# Task implementation and local cleanup

Use this workflow when implementing a feature, fixing a bug, or changing an existing behavior in a Pugi repository.

1. Read the workspace and repository `AGENTS.md`/`CLAUDE.md`, the owning module's rules, and any Jira/spec acceptance criteria. Identify the source of truth, affected consumers, existing tests, and existing docs before editing.
2. Make the smallest change that satisfies the requested behavior. Prefer explicit control flow over nested ternaries. Preserve API and product invariants; do not invent additional scope.
3. Add or update focused tests for the changed behavior, especially the reported regression, boundary conditions, and relevant failure path. Follow the owning repository's runner and test conventions. Do not add broad snapshots or redundant tests.
4. Clean only the affected area: remove dead branches, duplicate logic, stale comments, and unnecessary complexity when their status is confirmed from current callers. Keep unrelated cleanup out of the change. Do not create a new abstraction solely to make a diff look smaller.
5. Update the existing documentation that owns changed behavior, contracts, configuration, or operational steps. Preserve historical records and established language/format. Do not create a parallel tracker or duplicate a fact already maintained elsewhere.
6. Review the final diff for scope, behavior, typing, accessibility/security where applicable, and test quality. Run only relevant targeted checks unless the user asks for the full quality gate. Report exact commands/results and clearly mark anything not run.

The repository's instructions govern test authorization and required checks. This skill does not authorize commits, pushes, merges, deploys, Jira changes, or other external actions.
