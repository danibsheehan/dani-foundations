---
name: coverage-gap-diagnosis
description: >-
  Reads local coverage output for the files changed on this branch and names
  the specific untested branches/error paths, instead of a bare percentage.
  Use when coverage is close to a threshold, dropped, or the user asks
  what's undertested, to diagnose a coverage gap, or why coverage failed.
---

# Coverage gap diagnosis

CI's coverage step usually only shows an aggregate percentage against a configured
threshold. It never says which lines, in which changed files, are actually untested.
This skill does that, locally, before or instead of waiting on the CI comment.

## Order of work

### 1. Find the changed source files

```bash
git diff --name-only main...HEAD -- '*.ts' '*.tsx' '*.js' '*.go' \
  | grep -v -e '\.test\.' -e '_test\.go$'
```

Adjust the glob to this repo's actual source layout. Exclude test files themselves. Also
check this repo's coverage config (e.g. `vite.config.ts`'s `test.coverage.exclude`, or
equivalent) for files deliberately excluded from coverage measurement (WebGL/DOM/animation
code covered indirectly via UI, generated code, etc.) — a gap there isn't a gap this skill
(or CI) can see.

### 2. Generate coverage

Run this repo's coverage command (see its `AGENTS.md` — typically `npm run test:coverage`
or similar). The coverage tool should print a per-file table with an uncovered-lines column
and write an HTML/XML report for deeper inspection.

### 3. Find uncovered lines in the changed files

Read the terminal table's row for each changed file, or open the generated HTML report for
the annotated source (usually red = uncovered).

### 4. Describe what's untested, not just where

Read the actual source at each uncovered range. Say what _behavior_ is missing a test — an
error branch, a specific prop/state combination, an empty-state render, an API failure path —
not just "lines 58–83 uncovered." Cross-reference this repo's test-generation skill's coverage
checklist (creation/mount, happy path, edge cases, async, HTTP success/failure) if one exists —
if the uncovered range is the HTTP-failure branch specifically, say so.

### 5. Report

One list: file:lines → what's untested → the specific missing test case. This skill diagnoses;
it doesn't write the tests unless asked — offer to, don't assume.

## Anti-patterns

- Reporting bare percentages or raw line numbers with no description of the missing behavior —
  that's what the CI coverage comment already gives you; this skill exists to go further.
- Flagging gaps in files the branch didn't touch (noise) — scope to the diff.
- Flagging gaps in files the coverage config deliberately excludes as if they were measurable gaps.
- Writing test code without being asked.

## Reference

- This repo's coverage thresholds/exclude list — check its Vite/Jest/Go coverage config.
- This repo's own test-generation skill, if present, for the coverage checklist this diagnoses against.
- Full pre-PR flow: **pr-ready** skill.
