# dani-foundations

A Claude Code plugin marketplace holding process/docs skills shared across personal project
repos, plus a repo-scaffold template — so a skill fix or improvement lands once instead of
being hand-copied (and hand-drifted) into every repo.

## What's here

- **`foundations` plugin** (`plugins/foundations/`) — 7 shared skills:
  - `doc-writer` — README / API doc (JSDoc/GoDoc) / inline comment generation
  - `pr-ready` — pre-PR CI-parity checklist and PR description guidance
  - `definition-of-done` — post-edit format/lint/test/build verification
  - `dependabot-triage` — reviews and classifies open Dependabot PRs by risk
  - `coverage-gap-diagnosis` — names specific untested behavior, not just a bare percentage
  - `pr-summary-draft` — drafts a why-first PR Summary from the actual diff
  - `test-generator` — framework-agnostic unit test structure, coverage, and quality rules

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

Tagged (`v1`, ...) so consumers can pin rather than track `main`. Bump the plugin's
`plugins/foundations/.claude-plugin/plugin.json` `version` and cut a new tag when publishing
a change consumers should pick up.
