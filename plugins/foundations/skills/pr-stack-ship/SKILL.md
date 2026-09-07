---
name: pr-stack-ship
description: >
  Ships a pr-chunk-plan'd task as a stack of small branches and PRs —
  branches, commits, and opens a PR per chunk as each is completed, and
  retargets/rebases later PRs in the stack as earlier ones merge. Use while
  executing chunked work, or when asked to ship/stack current work as
  separate PRs.
---

# PR stack ship

Companion to **pr-chunk-plan**: once a task is broken into chunks, this skill ships each
chunk as its own branch and PR, stacked on the one before it, instead of letting all the
work accumulate on a single branch.

## Scope note (explicit permission)

This skill may branch, commit, push, and run `gh pr create` / `gh pr edit` **without
per-action confirmation**. This is a deliberate, scoped exception to the "don't push or open
a PR without being asked" default used elsewhere (see **pr-ready**, **pr-summary-draft**).
The exception applies only to work that has gone through **pr-chunk-plan** — it is not
blanket permission to push or open PRs for ad hoc, unplanned work.

## Detecting chunk completeness

A chunk is done when its task-list item's stated sub-goal is actually met **and** it passes
the smallest relevant check (per **definition-of-done**) — not when the diff crosses some
line-count threshold. Completeness is about the chunk's goal, not its size.

## Shipping a completed chunk

1. Create a branch stacked on the previous chunk's branch (the first chunk branches from the
   repo's main branch).
2. Commit the chunk's changes on that branch.
3. Push the branch.
4. Open a PR: `gh pr create --base <previous-chunk-branch-or-main>` with a chunk-scoped
   Summary and How-to-verify, following **pr-summary-draft**'s method but scoped to just
   this chunk's diff (not the whole feature).
5. Start the next chunk's work on a new branch stacked on the one just pushed.

## Maintaining the stack as PRs merge

When an earlier chunk's PR actually merges (confirm via `gh pr view <n> --json state` or
explicit user confirmation — never speculatively):

1. Retarget the next PR's base to main: `gh pr edit <next> --base main`.
2. Rebase that branch onto main to drop the now-merged commits.
3. Force-push with `git push --force-with-lease` (never plain `--force`).

Only touch the PR immediately after the one that merged — don't retarget or rebase further
down the stack until each predecessor in turn has merged.

## Anti-patterns

- Squashing the whole stack into one PR at the end — this defeats the purpose of chunking.
- Force-pushing without `--force-with-lease`.
- Retargeting or rebasing a stack entry before its predecessor has actually merged.
- Using this skill's auto-push/PR permission for work that was never chunk-planned.
