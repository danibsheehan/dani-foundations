# dani-foundations

A shared toolbox of AI coding-assistant instructions ("skills") for [Claude
Code](https://claude.com/claude-code), used across several of Danielle's personal project
repos.

**In plain English:** each of Danielle's projects uses Claude Code as a coding assistant, and
many of them need the same guidance — "write a test this way," "fill out a PR description
like this," "check accessibility like that." Rather than pasting the same instructions into
every project and letting them quietly drift apart over time, this repo holds the shared
instructions once. Every project subscribes to it; a fix or improvement here reaches all of
them at once.

_Everything past this point gets into the technical specifics — what's in the toolbox, and
how a project wires it in._

## What's here

- **`foundations` plugin** (`plugins/foundations/`) — 18 shared skills, each a short
  instruction file Claude Code reads automatically when it's relevant:
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
  - `bugbot-fix-verify` — verifies an automated review-bot finding against ground truth before
    fixing it, and re-verifies the fix doesn't open a new gap
  - `caching-and-upstream-perf` — caching/rate-limiting principles for wrapping a slow or
    rate-limited third-party API, independent of backend stack
  - `doc-sync-patch` — patches doc version claims to match the real manifest once a stack-docs
    drift check flags them
  - `react-vitest-testing` — React + Vitest + Testing Library mechanics (mock the API client,
    `renderHook` loading-race gotcha, roles/loading/error/empty checklist)
  - `vue-vitest-testing` — Vue 3 + Vitest mechanics (`@vue/test-utils` mount, `defineEmits`,
    composables, Pinia/router setup)
  - `angular-vitest-testing` — Angular + Vitest mechanics (`TestBed`, `HttpTestingController`,
    Input/Output, Router navigation)
  - `go-http-testing` — Go HTTP handler/service testing mechanics (`httptest` fakes,
    router-aware handler tests, the validation/success/upstream-failure minimum bar)

  These skills describe the generic shape of each task and defer to each consuming repo's
  own `AGENTS.md` / local skills for exact commands and framework-specific patterns (React,
  Vue, Angular, Go, etc.) — they're deliberately not a replacement for repo-specific skills
  like a project's own TipTap or RxJS integration skill.

- **`templates/`** — `AGENTS.md.template` and `CLAUDE.md.template` capturing the skeleton
  shape shared across these repos (Stack/Install/Configure/Run/Test-CI-parity/Conventions/
  Constraints/Definition-of-done headings), plus `dependabot.yml.template` capturing the
  already-standardized Dependabot grouping convention (npm minor/patch grouped for
  auto-merge, every other ecosystem ungrouped for individual review). Copy these in when
  bootstrapping a new repo and fill in the repo-specific prose; not auto-synced into
  existing repos.

## Standards established here (beyond the skills themselves)

- **Required CI check naming**: single-stack repo → one required check named `quality`
  (or `quality` + `unit-tests` if build/lint and tests are split into separate jobs);
  multi-stack repo → `<Stack> (...)` per stack, plus an optional dedicated lint check. This
  is the target convention `dependabot-triage`/`pr-ready` assume — not a guarantee every
  consuming repo has already renamed its jobs to match.
- **Coverage threshold policy**: a ratchet, not a fixed target — the threshold in CI config
  should sit at roughly the repo's current actual coverage and only ever go up, never down
  to land a change easier. Different repos legitimately have different numbers; the policy
  is what's shared, not the number.
- **Dependabot grouping**: see `templates/dependabot.yml.template` above — already
  identical in practice across all 4 repos before this was ever written down.

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
