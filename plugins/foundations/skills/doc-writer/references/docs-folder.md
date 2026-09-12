# docs/ Subfolder Guide

Most repos don't need a `docs/` folder — the root README (structured per `references/readme.md`)
is enough. This guide covers when one is warranted and what belongs in it once it is.

## Threshold: does this repo need a docs/ folder at all?

Create a `docs/` folder once the repo has **its own backend/API surface** — a `backend/`,
`service/`, `server/`-shaped directory (or equivalent) with its own runtime and deploy path,
distinct from a static frontend build. A frontend-only or static app almost never needs one;
the recommended-pool sections in `references/readme.md` (Configuration, Deploy) are enough on
their own.

This is a real trigger to check for, not just a description — if a repo meets this threshold
and has no `docs/` folder, that's a gap worth flagging even if nobody asked about it directly.

## Minimum contents once the threshold is met

- **`configuration.md`** — once env vars/config are numerous or nuanced enough that the
  README's Configuration table would get unwieldy (multiple services, secrets, per-environment
  differences).
- **`deploy.md`** — once deploy has real nuance worth recording: secrets, rollback steps,
  multiple environments/targets, or anything beyond "push triggers the default CI/CD workflow."

Move this content out of the README rather than duplicating it — the README's Configuration/
Deploy sections should shrink to a one-line pointer once the `docs/` version exists.

## Optional additions — earn these, don't pre-empt them

Add these only when the actual thing they document already exists — never speculatively:

- **`adr/`** (Architecture Decision Records) — only once there's a real either/or decision worth
  recording for future readers (e.g. why this cache TTL, why this rate limit), not retroactively
  for every choice ever made. One ADR per decision, numbered.
- **`threat-model.md`** — only once the repo has a real threat surface worth reasoning about
  (handles user data, exposes a public API, etc.) and someone has actually reasoned about it.
- **`slo.md`** — only once there's an actual latency/availability target being tracked, even
  informally — don't invent target numbers to justify the file.

## Shape once a repo has one

- Single-topic files for anything that isn't a decision record (`configuration.md`,
  `deploy.md`, `threat-model.md`, `slo.md`, etc.) — one concern per file.
- A `docs/README.md` index in a **curiosity-driven** style: a table mapping "what a reader
  might be wondering" to the doc that answers it, plus a short glossary of any jargon the docs
  use, and a pointer back to the root README for setup/contributing. `caught-looking/docs/
  README.md` is the reference example for this shape.
- The root README stays the front door (product tour, local setup, stack, contribution path);
  `docs/` is for readers who want the "why," not the "how to run this."
