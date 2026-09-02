---
name: doc-sync-patch
description: >-
  Patches README/AGENTS.md so their stated stack versions (language, framework,
  build tool, Node/Go version) match the actual manifests and CI config. Use
  when a stack-docs-drift check fails (e.g. check_stack_docs.py), after
  bumping a major dependency or CI runtime version (including a Dependabot
  merge), or when the user mentions stack docs drift or version badges.
---

# Doc sync patch

If this repo has a stack-docs-drift checker (a script comparing README/`AGENTS.md` stack
claims against `package.json`/`go.mod`/`.nvmrc`/CI config — `check_stack_docs.py` is the
reference implementation, already shared by more than one of these repos), it only
**detects** drift — it doesn't fix anything. A dependency bump (manual or via Dependabot)
touches the manifest but never the docs, so after almost every version-bump PR a human has to
hand-edit the docs that quote versions. This skill does that patch.

## Order of work

### 1. Read the current failure (or the source of truth directly)

Run this repo's stack-docs checker if it has one. Each error line should name the exact
doc/value mismatch. If it's already green, read the source files directly instead — you may
have been asked to pre-emptively sync docs after a manual bump.

### 2. Read the source of truth

- The package manifest (`package.json`, `go.mod`, etc.) for framework/language/build-tool
  versions.
- `.nvmrc` or equivalent for the runtime version (preferred source if CI pins to it).
- The CI workflow file, only if there's no separate version-pin file.

### 3. Patch every location the checker validates — values only

Common locations: README badges quoting a version, a README "Tech stack" or "Prerequisites"
section, `AGENTS.md`'s Stack line. Edit **values only** — do not reword surrounding prose, and
do not touch the manifests themselves (this skill syncs docs to already-bumped dependencies;
it does not bump dependencies).

### 4. Verify

Re-run the stack-docs checker; it should pass. If it still fails, re-read the error — it
names the file and the exact expected value.

## Anti-patterns

- Patching only one doc file and skipping another the checker also validates.
- Guessing a version instead of reading it from the actual manifest/`.nvmrc`/CI config.
- Changing dependency versions in the manifests as part of this skill — that's a separate,
  deliberate upgrade decision, not a docs sync.
- Leaving the stack-docs check red after editing.

## Reference

- This repo's stack-docs checker, if any (e.g. `check_stack_docs.py`), is the source of the
  exact rules each doc must match.
- Run as part of this repo's PR-readiness flow — see the **pr-ready** skill.
