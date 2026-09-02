---
name: pr-ready
description: >
  Runs this repo's local CI-parity checks and prepares a pull request. Use
  when the user asks to open a PR, prepare a pull request, pre-PR checks,
  make CI pass, or verify before merging.
---

# PR ready

Run before opening or updating a PR. Prefer full gates over "tests only."

## Checklist

```
Pre-PR:
- [ ] Scope: only intended files; no secrets (.env, credentials)
- [ ] This repo's format/lint checks
- [ ] This repo's full test suite (coverage mode if it gates CI)
- [ ] This repo's build
- [ ] Any deploy/hosting-shaped build variant, if config affecting it changed
- [ ] PR summary ready (Summary + How to verify)
```

### 1. Local CI parity

Run this repo's actual commands — check its `AGENTS.md`'s Test/CI parity section, or its
own local `pr-ready`-equivalent skill, for the exact command names (they vary by stack:
`npm run lint` / `go vet` / `make ci-local`, etc.). At minimum, match what the repo's CI
workflow runs on a pull request — the required check should be named `quality` for a
single-stack repo (or `quality` + `unit-tests` if split), or `<Stack> (...)` per stack for
a multi-stack repo (see the `dependabot-triage` skill for the full naming convention):

- Format check
- Lint
- Full test suite, with coverage if CI enforces thresholds
- Build

Faster while iterating (not a substitute before PR): a quick/watch test run instead of the
full coverage suite.

If the change touches a deploy base path, API base URL, or static-hosting config, also
build the way CI builds for deploy (see this repo's deploy skill or `AGENTS.md`, if any).

### 2. PR description

Use this repo's PR template, if any:

- **Summary** — what changed and why (1–3 bullets)
- **How to verify** — commands run and UI paths/behavior to exercise, or `N/A` for tooling-only

See the **pr-summary-draft** skill for how to write this well.

Do not push or create the PR unless the user asked.

### 3. After merge (local cleanup)

When the PR is merged and the user is done with the branch (or asks to clean up):

```bash
git checkout main && git pull origin main
git branch -d <feature-branch>
```

Optionally `git fetch --prune` for stale remote-tracking refs.

## Anti-patterns

- Opening a PR after only a quick test run when coverage thresholds matter.
- Skipping the build/compile step after dependency, config, or asset changes.
- Committing `.env*` or tokens.
- Amending or force-pushing unless the user explicitly requests it.
- Leaving merged feature branches checked out after the user asks to clean up.
