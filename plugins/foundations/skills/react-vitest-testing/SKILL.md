---
name: react-vitest-testing
description: >-
  Writes or updates Vitest + Testing Library tests for React apps: mocked API
  client, renderHook, jsdom, and accessibility-first queries. Use when adding
  or changing code under a React app's src/, writing *.test.tsx, fixing flaky
  UI/hook tests, or when the user mentions React, Vitest, RTL, or test
  coverage in a React codebase.
---

# React + Vitest + Testing Library

Framework-scoped patterns for React apps using Vitest and Testing Library, found identical
across more than one such repo. This repo's own local testing skill or `AGENTS.md` (if any)
has the app-specific mocking (which modules to mock, fixture shapes) — this skill covers the
React/Vitest/RTL mechanics that don't vary by app.

## Stack shape

- **Runner**: Vitest, with `test.environment: 'jsdom'`.
- **Matchers**: `@testing-library/jest-dom/vitest`, loaded via a shared setup file (commonly
  `src/test/setup.ts`).
- **Components/hooks**: `@testing-library/react` (`render`, `screen`, `within`, `waitFor`,
  `renderHook`).
- **Interactions**: `@testing-library/user-event`, preferred over firing raw DOM events.

## Conventions

1. **File placement** — colocate `Component.test.tsx` next to `Component.tsx`; shared test
   setup lives in one file only, not scattered per-suite.
2. **Mock the API/HTTP client module**, not the network layer — `vi.mock('<path to api
   client>')` and `vi.mocked(fetchX)` for individual functions. Never call a real backend in
   unit tests; assert on the mock's call args (URLs, params) instead.
3. **`renderHook`** — mock the functions a hook calls, resolve with minimal typed fixtures.
   Assert with `waitFor` on `result.current.data`/`error`/mock-call-args, **not only
   `loading === false`** — some hooks start with `loading: false` before the async call
   kicks off, so asserting on the loading flag alone races and can pass for the wrong reason.
4. **UI components** — prefer roles and accessible names (`getByRole('button', { name: /…/
   })`) over test IDs or DOM structure. Cover **loading**, **error**, and **empty** states
   whenever the component surfaces them (a visible message or empty UI, not a silent gap).
5. **Controlled props** — if a parent must react to a child's `onChange`/callback, use a
   small stateful test harness rather than asserting the callback fired in isolation.
6. **Debounced search/input** — use real timers with a `setTimeout` flush, or `waitFor`;
   `userEvent` combined with fake timers frequently deadlocks unless `advanceTimers` is wired
   correctly — avoid that combination unless you've confirmed it works.
7. **DOM cleanup** — a global `cleanup()` in the shared setup file's `afterEach` prevents
   duplicate roles/elements leaking across tests. If it's ever disabled, unmount explicitly
   between tests.
8. **Error boundaries** — stub `console.error` when testing `componentDidCatch`-style
   behavior so the test output stays quiet, and restore it after the suite.

## Anti-patterns

- **Importing a production module before its `vi.mock` factory runs** — keep mock factories
  at the top of the file (or use `vi.hoisted`); this is especially easy to get wrong when
  testing code that reads `import.meta.env` at import time, which needs `vi.resetModules()` +
  a dynamic `import()` instead of a static one.
- **Consuming one shared `Response` object for two separate `.json()` reads** — a `Response`
  body can only be read once; a second read on the same object throws or returns empty.
- Asserting pixel layout, chart-library internals, or other implementation detail instead of
  data, labels, or roles.
- Duplicating a large fixture/snapshot when a minimal typed object would do.

## Reference

- This repo's own testing skill or `AGENTS.md`, if present, for exact mock paths, fixture
  shapes, and commands (`test:run`, `test:coverage`).
