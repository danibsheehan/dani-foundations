---
name: github-pages-deploy
description: >
  GitHub Pages project-site deploy: base-path handling, workflow structure, and dist
  layout, framework-agnostic. Use when editing deploy, base-href/base-path, static
  hosting, or GitHub Actions for a GitHub Pages–hosted repo.
---

# GitHub Pages deploy

A GitHub **project site** (not a user/org site) lives at
`https://<user>.github.io/<repository-name>/` — the repo name is part of the URL path, so
the app's build must know its own base path at build time, or assets/routes silently
break once deployed.

## The base-path rule

Whatever this repo's build tool calls it — Vite's `VITE_PUBLIC_PATH`/`base`, Angular's
`--base-href`, webpack's `publicPath`, etc. — it must be set to `/<repository-name>/`
(leading **and** trailing slash) to match the Pages URL. Check this repo's build config or
`AGENTS.md` for the exact mechanism and env var/flag name.

Prefer deriving the repo name at build time (e.g. `${{ github.event.repository.name }}` in
the workflow) over hardcoding it, so a repo rename doesn't silently break the next deploy —
if it is hardcoded, keep it in exactly one place and update it deliberately on a rename.

## Workflow shape

- **Trigger**: push to `main` (and optionally `workflow_dispatch` for a manual redeploy).
- **Build**: install deps, run the production build with the base-path set as above.
- **Deploy**: `actions/upload-pages-artifact` from the build output directory, then
  `actions/deploy-pages` targeting the `github-pages` environment.
- If build and deploy are split across two workflows/jobs (e.g. a test workflow uploads the
  build artifact, a separate deploy workflow consumes it via `workflow_run`), download any
  cross-job artifact into `${{ runner.temp }}`, **not** the workspace root, and don't mix an
  artifact download with a checkout in the same job — that combination is a known
  `actions/artifact-poisoning` risk CodeQL flags.

## One-time repo setup

**Settings → Pages → Build and deployment → Source: GitHub Actions** (not "Deploy from a
branch"). Without this, `deploy-pages` has nothing to publish to.

## Pre-release / local verification

1. Run this repo's lint/test suite if behavior changed.
2. Build with the same base-path CI uses (see above), then serve/preview the build output
   locally — not just dev mode, since dev mode doesn't exercise the base-path.
3. Confirm assets load from the right path (no wrong-origin or 404 chunk loads), and that
   any API calls the app makes still resolve correctly under the deployed base path. A
   wrong base-path setting usually shows up as missing JS/CSS or failed chunk loads, not a
   clean error.

## Scope notes

- A local dev server/proxy (if this repo has one) is typically not part of the Pages
  deploy — Pages serves a static build only. Don't assume a proxy/backend exists in
  production if this repo's Pages deploy is static-only.
- No secrets are needed for a purely static Pages deploy of public data/APIs; keep `.env*`
  local as usual if the build reads any.
