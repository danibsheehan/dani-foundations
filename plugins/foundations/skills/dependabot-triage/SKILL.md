---
name: dependabot-triage
description: >-
  Reviews open Dependabot PRs that an auto-merge workflow didn't already
  merge, reads each one's embedded changelog and required CI status to
  classify risk, and merges only the PRs the user explicitly names. Use
  when asked to review or triage Dependabot PRs, do the weekly dependency
  review, or check the Dependabot backlog.
---

# Dependabot triage

If this repo has a Dependabot auto-merge workflow, it likely already merges low-risk
(patch/minor) bumps once required CI is green — so by the time you run this skill,
what's actually sitting in the backlog is the harder cases: major bumps (typically
never auto-merged), anything CI-red, and anything the auto-merge workflow hasn't
gotten to yet. This skill reads and classifies those; merging still requires the user
to name which PRs.

## Order of work

### 1. List open Dependabot PRs

```bash
gh pr list --author "app/dependabot" --limit 100 --json number,title,labels,createdAt,statusCheckRollup
```

`gh pr list` defaults to 30 results — check this repo's `.github/dependabot.yml` for its
open-PR cap per ecosystem, and note that Dependabot **security updates** can open outside
that cap. Always pass `--limit` explicitly so the backlog isn't silently truncated.

If there are none open, say so and stop — nothing to triage.

### 2. Gather signal per PR

- **Ecosystem / bump shape** from the title and labels (e.g. `npm`, `github_actions`,
  `gomod`) — see this repo's `.github/dependabot.yml`. The standard grouping convention
  across these repos: `npm` bumps are grouped as `npm-minor-and-patch` (minor+patch only,
  auto-mergeable); `github-actions` (and any other ecosystem, e.g. `gomod`) stay ungrouped
  and individually reviewed, since those bumps move a pinned commit/version one at a time
  rather than a routine dependency range. Not every ecosystem gets a distinct label from
  Dependabot (`gomod` commonly doesn't) — if a PR's title/labels don't identify the
  ecosystem clearly, infer it from the target directory in the title (e.g. a monorepo with
  `/backend` and `/frontend` subdirectories per ecosystem).
- **A 0.x package's minor bumps aren't automatically "major"-risk** — only an actual
  major-version bump (or a 0.x → 1.x crossing) should escalate a PR to "needs a look" on
  version-shape alone; routine 0.x-minor churn (common for actively-developed libraries
  still under v1) is otherwise judged the same as any other minor/patch bump.
- **Required CI only** — identify this repo's actual merge-blocking check(s). The naming
  convention: a single-stack repo's required check should be named `quality` (or `quality`
  + `unit-tests` if the build/lint and test steps are split into separate jobs); a
  multi-stack repo (e.g. a separate frontend/backend) uses `<Stack> (...)` per stack, plus
  an optional dedicated lint check. If this repo's actual job names don't match yet, use
  its real names — this is the target convention, not a guarantee every repo has already
  adopted it. Informational checks (e.g. CodeQL, Lighthouse, E2E/SBOM) don't affect
  mergeability regardless of naming.
- **Changelog** — `gh pr view <n> --json body`. Dependabot embeds the release notes in a
  collapsible `<details>` block. Scan for:
  - Security signals: `CVE`, `GHSA`, "security fix" — treat as **Security** regardless of size.
  - Breaking signals: `[BREAKING]`/`[CHANGE]` entries describing removed/renamed APIs, or a
    "minimum required version" bump.
  - Otherwise routine (bugfixes, features, docs).

### 3. Classify each PR

Evaluate in this order — first match wins:

1. **Security** — changelog/advisory references a CVE/GHSA or explicit security fix. Flag first,
   regardless of ecosystem or bump size; recommend merging promptly once required checks are green.
2. **Needs a look** — any of:
   - A **major** version bump (or a 0.x → 1.x jump) — auto-merge typically never touches these.
   - A breaking/minimum-version changelog entry (see step 2).
   - Required checks red.
   - **A GitHub Actions bump, regardless of version delta**, if this repo's `dependabot.yml`
     leaves that ecosystem ungrouped/individually reviewed (a common pattern) — an Actions bump
     moves a trusted pinned SHA/tag, which matters more than the semver delta looks like it does.
     Never auto-classify these as low-risk on bump size alone.
   - Still open after a few days despite being patch/minor — worth checking why auto-merge hasn't
     picked it up (e.g. a merge conflict, or a required check never went green).
3. **Low risk** — a patch/minor bump, required checks green, no breaking/minimum-version changelog
   entries. In the normal case an auto-merge workflow already merges these before you ever see
   them; a tier-3 PR still open usually means something's blocking it (see tier 2's last bullet).

### 4. Report — do not merge yet

One table: PR #, package, bump, tier, one-line why (cite the changelog line that drove the
classification, not just "looks fine"). Stop here by default.

### 5. Merge only what the user names

```bash
gh pr merge <number> --squash
```

Match this repo's existing merge convention (check `git log` if unsure). Merge only PRs the
user explicitly names in their reply (e.g. "merge #212 and #214"). Do not batch-merge an
entire tier on your own initiative — never merge a PR unless asked.

## Anti-patterns

- Merging anything the user didn't explicitly name this session.
- Treating a red **optional** check as blocking, or a green one as sufficient to skip
  reading the changelog.
- Classifying by semver label alone without reading the embedded release notes — they're
  already in the PR body; use them.
- Assuming an auto-merge workflow already handled everything patch/minor without checking —
  it can stall on a merge conflict or a flaky required check.

## Reference

- Config: `.github/dependabot.yml`. Auto-merge workflow, if present: `.github/workflows/dependabot-auto-merge.yml`.
- Required-check source: this repo's CI workflow(s) under `.github/workflows/`.
