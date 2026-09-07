---
name: pr-chunk-plan
description: >
  Breaks a feature-shaped or multi-file task into an ordered sequence of
  small, independently reviewable chunks before implementation starts. Use
  when a task is estimated to touch 3+ files or bundles multiple distinct
  concerns (e.g. data model + API + UI), before writing any code. Skip for
  single-file or one-line fixes.
---

# PR chunk plan

Large PRs are hard to review and hard for automated checks to reason about. This skill
splits a task into small, independently reviewable pieces **before** implementation starts,
instead of writing everything on one branch and discovering afterward that it's too big.

## When this fires

Trigger on either signal:

- The task is estimated to touch **3+ files**.
- The task is **feature-shaped** — it bundles multiple distinct concerns (e.g. a data model
  change + an API endpoint + UI wiring), even if the file count looks small at a glance.

Do **not** trigger on:

- A one-line or single-file fix (typo, single-function bugfix, config value tweak).
- A **mechanical** multi-file change with no independently reviewable seam — e.g. a
  rename/find-replace across many files, a lockfile bump, a formatting-only pass. Touching
  many files isn't the same as having many distinct concerns; a mechanical change is one
  reviewable unit no matter how many files it spans.

## How to chunk

Do just enough exploration of the codebase to see the real shape of the change — don't
guess at chunks from the request text alone. Then split along the change's natural seams
(commonly data layer → API/service → UI → tests, but the actual seams come from what this
specific task needs, not a fixed template).

Each chunk must:

1. Be **independently reviewable** — a reviewer can understand and judge it without needing
   to see later chunks.
2. Leave the repo in a **working state** on its own where feasible (builds, existing tests
   pass) — not a half-wired intermediate state.
3. Be **ordered** so later chunks depend only on earlier ones, never the reverse.

## Tracking the plan

Record the chunk list using the task-tracking tool (todo list), one item per chunk, in
order. This is what **pr-stack-ship** reads to know what chunk is next and when a chunk's
stated goal is met.

State the plan briefly to the user as normal task narration. This is not a blocking approval
gate — proceed with implementation once the plan is recorded, consistent with a bias toward
not stopping to ask when the direction is reasonably clear.

## Handoff

Once the chunk plan exists, implement chunk by chunk. As each chunk's goal is met, **the
pr-stack-ship skill** takes over: branching (named per **branch-naming**), committing, and
opening that chunk's PR before work continues on the next chunk.

## Anti-patterns

- Chunking a trivial, single-concern change just because it touches a few files.
- Splitting a chunk by line count or file name instead of by reviewable concern (e.g. "part
  1 of the UI, part 2 of the UI" with no real boundary between them).
- Recording a chunk plan and then implementing everything on one branch anyway.
