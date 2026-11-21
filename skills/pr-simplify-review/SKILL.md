---
name: pr-simplify-review
description: Review a Pugi pull request or proposed diff for correctness and maintainability, then simplify the changed code without altering intended behavior.
---

# PR simplify and code review

Use this workflow when preparing, reviewing, or updating a pull request. Review the full requested diff and its relevant source context.

## Review

- Establish the comparison base and read the PR description, linked task/spec, repository instructions, and relevant existing implementation.
- Check behavior against acceptance criteria separately from code quality. Look for regressions, missing error/boundary handling, unsafe input or authorization assumptions, type holes, accessibility issues, and missing focused tests.
- Report only actionable findings supported by the diff/source. Include file and line, impact, and priority; distinguish confirmed defects from questions or improvement suggestions. Skip style preferences already enforced by tooling.
- Check comments, naming, duplicated logic, overly broad responsibilities, unnecessary indirection, dead code introduced by the change, and nested ternaries.

## Simplify

- Simplify only code in the changed scope and preserve externally observable behavior, contracts, and error semantics.
- Prefer early returns, named predicates/helpers when they clarify intent, and explicit branches over nested ternaries. Avoid clever expressions, speculative generalization, or extracting one-use wrappers without a clear readability benefit.
- Add or adjust a focused regression test when a simplification changes a behavior boundary or when review finds a concrete defect. Do not rewrite unrelated code to satisfy a subjective preference.

## Close out

- Re-read the final diff and verify any changed paths with the narrowest relevant checks permitted by the repository instructions.
- For UI changes, use the repository's PR workflow for before/after screenshots when required; screenshots must come from the actual application state.
- Summarize findings, simplifications made, tests/checks run, and remaining uncertainty. A review does not itself authorize commit, push, merge, or Jira changes.
