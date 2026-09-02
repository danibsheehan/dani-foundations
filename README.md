# dani-foundations

A Claude Code plugin marketplace holding process/docs skills shared across personal project
repos, plus a repo-scaffold template — so a skill fix or improvement lands once instead of
being hand-copied (and hand-drifted) into every repo.

## What's here

- **`foundations` plugin** (`plugins/foundations/`) — 11 shared skills:
  - `doc-writer` — README / API doc (JSDoc/GoDoc) / inline comment generation
  - `pr-ready` — pre-PR CI-parity checklist and PR description guidance
  - `definition-of-done` — post-edit format/lint/test/build verification
  - `dependabot-triage` — reviews and classifies open Dependabot PRs by risk
  - `coverage-gap-diagnosis` — names specific untested behavior, not just a bare percentage
  - `pr-summary-draft` — drafts a why-first PR Summary from the actual diff
  - `test-generator` — framework-agnostic unit test structure, coverage, and quality rules
  - `accessibility-a11y` — framework-agnostic a11y checklist (keyboard, ARIA, motion, contrast)
  - `bundle-performance` — bundle-size measurement discipline and runtime perf checks
  - `api-hardening` — backend/API hardening principles (validation, SSRF-safe upstream calls,
    generic client errors, CORS/rate-limit defaults), independent of backend stack
  - `github-pages-deploy` — GitHub Pages project-site base-path handling and workflow shape

  These skills describe the generic shape of each task and defer to each consuming repo's
  own `AGENTS.md` / local skills for exact commands and framework-specific patterns (React,
  Vue, Angular, Go, etc.) — they're deliberately not a replacement for repo-specific skills
  like a project's own TipTap or RxJS integration skill.

- **`templates/`** — `AGENTS.md.template` and `CLAUDE.md.template` capturing the skeleton
  shape shared across these repos (Stack/Install/Configure/Run/Test-CI-parity/Conventions/
  Constraints/Definition-of-done headings). Copy these in when bootstrapping a new repo and
  fill in the repo-specific prose; not auto-synced into existing repos.

## Using this marketplace in a repo

Add to that repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "dani-foundations": {
      "source": { "source": "github", "repo": "danibsheehan/dani-foundations" }
    }
  },
  "enabledPlugins": {
    "foundations@dani-foundations": true
  }
}
```

Foundations skills are namespaced (e.g. `foundations:pr-ready`) and coexist with a repo's own
local `.claude/skills/*` — no naming conflicts.

## Versioning

Bump `plugins/foundations/.claude-plugin/plugin.json`'s `version` on any change consumers
should pick up — Claude Code's plugin install is a per-repo snapshot (pinned to the commit
present at install time), not a live sync, so a version bump alone doesn't push anything;
each consuming repo has to explicitly re-install/update via `/plugins` to pick up a new
version. Git tags on this repo (`v1`, ...) are for human-readable release history only —
they aren't consulted by the plugin install/update mechanism itself (unlike `dani-actions`,
where a git tag ref is exactly what a consumer's `workflow_call` pins to).
