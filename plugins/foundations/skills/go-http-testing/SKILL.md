---
name: go-http-testing
description: >-
  Writes or updates Go HTTP handler and service tests using httptest fakes
  and table-driven cases, independent of router library. Use when adding or
  changing Go backend code, writing *_test.go for HTTP handlers or services
  that call an upstream API, or when the user mentions Go tests or httptest.
---

# Go HTTP testing

Framework-scoped patterns for testing Go HTTP handlers and the services/clients they call.
This repo's own local testing skill or `AGENTS.md` (if any) has the app-specific shared test
helpers and exact commands — this skill covers the Go/`httptest` mechanics that don't vary by
app.

## Conventions

1. **Package** — test files typically live in the same package as the code under test (or a
   package matching the layer, e.g. a services/config/middleware package), so tests can use
   the same production types.

2. **Shared test helpers, not ad hoc setup** — if this repo has a shared helper for building a
   test instance of the handler/service under test (wiring config, cache, fake upstream
   client), use it rather than constructing dependencies by hand in every test file.

3. **Fake the upstream with `httptest.Server`** (or a plain `http.HandlerFunc`) whose paths
   and query strings match exactly what the real client sends — this proves the client builds
   requests correctly, not just that the handler parses a hardcoded response.

4. **Router-aware tests when the handler reads URL params** — if the handler uses a router's
   URL-param extraction (e.g. `chi.URLParam`, a path variable), register the **same path
   pattern** used in production routing on a real router instance in the test, then
   `ServeHTTP` with `httptest.NewRecorder`/`httptest.NewRequest`. Testing the handler function
   directly (bypassing the router) gives a false green for any bug in how the param is
   extracted.

5. **Minimum coverage per HTTP handler**:
   - **Validation** — table-driven bad-input cases (missing/malformed params) → the
     handler's actual 4xx status.
   - **Success** — 2xx status, correct content type, response body decodes into the expected
     type with correct field values.
   - **Upstream failure** — the fake upstream returns a non-2xx/error → the handler's actual
     failure status (never a real network call in the test).

6. **Minimal, realistically-shaped fake response bodies** — enough valid JSON/structure to
   exercise the code path, not a full realistic payload. Reuse an existing fixture in the same
   area when one already covers the same shape.

7. **Services/clients (cache, HTTP client wrappers)** — table-driven unit tests next to the
   package. Exercise concurrency-sensitive behavior (e.g. a coalescing cache's concurrent-miss
   behavior) and error paths without a real network call; use short TTLs/controlled clocks
   where relevant.

## Anti-patterns

- Building the handler/service under test by hand in every test file instead of a shared
  helper, when one exists.
- Hitting a real external API from a unit test.
- Skipping router-level testing for a handler that reads URL params via the router — this can
  produce a false green that misses a real routing bug.

## Reference

- This repo's own testing skill or `AGENTS.md`, if present, for the shared test helper name,
  fixture examples, and exact test commands.
