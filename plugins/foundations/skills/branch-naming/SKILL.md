---
name: branch-naming
description: >
  States the branch naming convention (<type>/<slug>, Conventional-Commits-style
  type prefixes) used across these repos. Use whenever creating a branch, or
  when asked about branch naming conventions, what to name a branch, or how to
  name a branch for some work.
---

# Branch naming

Every branch name follows:

```
<type>/<slug>
```

## Types

Mirrors the [Conventional Commits](https://www.conventionalcommits.org/) type set, so a
branch's type lines up with the commit type(s) it will contain:

- `feat` — new feature or capability
- `fix` — bug fix
- `docs` — documentation only (README, comments, this repo's skills)
- `chore` — maintenance/tooling, no source behavior change (deps, config, cleanup)
- `refactor` — code change that is neither a feature nor a fix
- `test` — adding or fixing tests only
- `perf` — performance improvement
- `ci` — CI/CD workflow changes
- `build` — build system or dependency changes

Pick the type that matches the change's actual intent, not its size. A test-only change is
`test`, not `chore`; a pure refactor is `refactor`, not `fix`, even if it happens alongside a
bug investigation.

## Slug

- Lowercase, hyphen-separated, no underscores or spaces.
- Short and descriptive of the change, not the ticket or task tracker.
- No ticket/issue numbers — this repo's branches don't tie to an external tracker ID.

Examples: `feat/branch-naming-skill`, `fix/login-redirect-loop`, `docs/readme-skill-list`,
`refactor/extract-slug-validator`.

## Related

- **pr-stack-ship** and **pr-chunk-plan** — the skills that actually create and ship
  branches; this skill defines the naming convention they follow.
