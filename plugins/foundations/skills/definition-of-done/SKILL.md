---
name: definition-of-done
description: >
  Verifies changes by running this repo's format check, lint, tests, and
  build. Use after substantive edits to application code, styles,
  server/proxy, or config, or when the user asks to validate or finish a task.
---

# Definition of done

After **substantive** edits (features, components, core library code, server/proxy, styles,
build/CI config), run this repo's format/lint/test/build commands from the repo root, in
order — check this repo's `AGENTS.md`'s Test/CI parity section, or its own local
`definition-of-done`-equivalent skill, for the exact command names:

1. Format check (fix if needed)
2. Lint
3. Tests
4. Build

Fix failures before considering the task complete.

For small, localized edits, the **smallest** relevant check is enough (e.g. a focused test
file, or lint only). Do **not** require the full suite or a deploy-shaped build for every tweak.

## Coverage threshold policy

The standard across these repos is a **ratchet, not a fixed target**: the coverage
threshold in CI config is set to roughly the repo's current actual coverage (not some
universal percentage), and only ever raised as test suites grow — never lowered to make a
change easier to land. Different repos legitimately have different threshold numbers
because they're at different points in that ratchet, not because the policy itself
differs. When a change meaningfully improves coverage, consider raising the threshold in
the same PR; don't lower it to get a change through.

## When to also run a deploy-shaped build

If the change touches deploy base path, client API base, or static hosting config (e.g. a
Pages/CDN subpath, an env-driven API URL), build the way CI builds for deploy — see this
repo's deploy skill or `AGENTS.md`, if any.

## Related

- Before opening a PR, use the **pr-ready** skill (full coverage-mode test run matches CI).
