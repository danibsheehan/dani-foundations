# README Writing Guide

This guide covers **application repos** (a product someone runs, not a published library) —
the shape used across these personal projects. For an actual published package meant to be
`npm install`ed or `go get`ed by others, a classic Installation/Quick-Start/API-Reference
library README is still the right shape; use judgment if this repo is that kind of project
instead.

## Structure

A **required core**, always present and in this order, plus a **recommended pool** included
only when the inclusion rule for that section actually applies. Don't include a pool section
just because another repo has it — check the rule.

### Required core (fixed order)

```markdown
# Project Name

> One-line tagline — what it does and who it's for

## Contents

<!-- Linked table of contents to every other section in this README. -->

## Start here

<!-- The fastest path for a new reader: what to read/run first, one or two links/commands. -->

## Overview

2–4 sentences. What problem does this solve? What does it do?

## Prerequisites

<!-- Runtime/tool versions and accounts needed before install — Node/Go version, API keys,
     etc. -->

## Install, Run

\`\`\`bash
<!-- exact install + dev-server/build commands -->
\`\`\`

## Configuration

<!-- Table of env vars/options: | Option | Type | Default | Description | -->
```

### Recommended pool (include only when the rule applies)

| Section | Include when… |
| --- | --- |
| `## Features` | The app has distinct end-user-facing capabilities worth listing separately from Overview — skip if Overview already covers it in 2–4 sentences. |
| `## CI` (or a Test/CI-parity pointer) | CI does more than the shared default verify workflow — e.g. extra jobs, a non-standard gate. |
| `## Automation` | A scheduled or agent-driven routine exists beyond the standard human-initiated PR flow. |
| `## Deploy` / `## Deployment` | Deploy is non-default (not just a static GitHub Pages build via the shared workflow) or has secrets/rollback nuance worth documenting. |
| `## Contributing` | The repo accepts outside contributions, or the PR flow differs from what `AGENTS.md` already states for agents. |
| `## License` | A `LICENSE` file exists at the repo root. |
| `## Cursor — legacy compatibility only` | `.cursor/` still exists as a symlink for legacy Cursor compatibility in this repo — drop this section once that symlink is removed. |

Order the included pool sections wherever they read best relative to the required core —
there's no fixed position for them, only a fixed position for the required core itself.

## Tone & Style Rules

- **Active voice**: "Fetches the user record" not "The user record is fetched"
- **Present tense**: "Returns a string" not "Will return a string"
- **No fluff**: No "This amazing library...", no "Easy to use!"
- **Code examples first**: Show before you tell. Readers want to see it work.
- **Concrete over abstract**: "Retries failed requests up to 3 times" > "Handles errors gracefully"
- Tailor length to project complexity — a utility library needs less than a platform

## Inferring Missing Info

If the repo doesn't have a description, infer from:

1. Package name + entry point exports
2. Folder structure (e.g., `handlers/`, `models/`, `api/`)
3. Test file names and assertions
4. Import statements in example files

Flag anything you've inferred so the user can verify.
