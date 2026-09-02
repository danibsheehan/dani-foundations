---
name: pr-summary-draft
description: >-
  Drafts a why-first PR Summary and How-to-verify section by reading the
  actual diff and commits on the current branch, not just which paths
  changed. Use when opening a PR, updating a PR description, asked to draft
  a PR summary, or when the user asks what changed and why on this branch.
---

# PR summary draft

Most PR templates have a **Summary** and **How to verify** section, but nothing scaffolds
them automatically. Left to a generic pass, that produces a file list (`Changed App.tsx,
lib/foo.ts`) instead of the _why_. This skill reads the real diff and writes the Summary a
human reviewer would actually want.

## Order of work

### 1. Read the actual change, not just file names

```bash
git diff main...HEAD          # or the PR's base branch if not main
git log --oneline main...HEAD
```

Read the diff content for the changed files — hunks, not just a file list. Prioritize files
that changed _behavior_ (components, lib/core logic, server/config) over mechanical diffs
(formatting-only, generated/lockfile changes).

### 2. Identify the why

Look for the motivation in, roughly this priority order:

1. What the conversation/task that produced this branch was actually trying to fix or add.
2. Commit messages, if they explain intent (not just "wip" / "fix").
3. What the diff implies: a bug fix (what broke, for whom), a new capability (what it unlocks),
   a refactor (what got harder to maintain and why this fixes it).

If the diff's purpose is genuinely ambiguous — e.g. a mixed-bag branch, or a change whose intent
isn't evident from code or conversation — ask the user rather than inventing a plausible-sounding
motivation. A wrong guess is worse than a question.

### 3. Write the Summary

Follow this repo's PR template (if any) and the **pr-ready** skill's guidance exactly:

- Lead with **why** (motivation / problem), then what changed for users, API, or data.
- 1–3 short bullets. Do not stop at a file list or restate commit subjects.
- Weak: `Update Card.tsx and CardEffect.ts.`
- Stronger: `The card shimmer was recalculating on every scroll frame even when the card was
  off screen; gate it behind an IntersectionObserver so idle cards stop costing paint time.`

If this repo already has automated PR scaffolding (e.g. a bot-posted checklist or
verify-command comment, a path-based PR guide action), don't re-derive or duplicate that
mechanical content here — check for it first. This skill's Summary should add the *why*
that automation can't infer from file paths alone, not restate what's already posted.

### 4. Write How to verify

User-facing steps: UI paths to exercise, expected before/after behavior, or the commands run
(lint / test / build — see **pr-ready**). Use `N/A` for tooling-only changes. Skip this section
entirely (or keep it minimal) if this repo's automated PR scaffolding already posts a
verify-command checklist — don't restate it.

### 5. Apply it

- **New PR**: `gh pr create --title "..." --body "$(cat <<'EOF' ... EOF)"` with the Summary and
  How to verify sections filled in. Only create the PR if the user asked for one.
- **Existing PR**: `gh pr edit <number> --body-file <file>` — read the current body first
  (`gh pr view <number> --json body`) before overwriting it. If this repo's PR automation
  manages a marker block in the body (e.g. an HTML comment marker it updates on each push),
  preserve that block untouched — don't hand-edit or remove it.

## Anti-patterns

- Summaries that restate the diff (`Changed X.tsx, Y.ts`) instead of explaining motivation.
- Guessing "why" when it isn't evident from the diff, commits, or conversation — ask instead.
- Duplicating this repo's own automated path-based checklist/verify-command output by hand.
- Removing or hand-editing an automation-managed marker block in an existing PR body.
- Opening, editing, or pushing a PR without being asked.

## Reference

- This repo's PR template, if any: `.github/pull_request_template.md`.
- Full pre-PR flow: **pr-ready** skill.
