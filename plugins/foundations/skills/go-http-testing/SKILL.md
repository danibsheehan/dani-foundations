---
name: go-http-testing
description: >-
  Writes or updates Go HTTP handler, middleware, and service tests using
  httptest, independent of router library. Covers both dependency shapes —
  faking an upstream HTTP API and mocking an internal Go interface — plus
  middleware tests (CORS, rate limiting, logging, body caps). Use when adding
  or changing Go backend code, writing *_test.go for HTTP handlers,
  middleware, or services, or when the user mentions Go tests or httptest.
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

3. **Pick the fake shape based on what the handler actually depends on** — these are two
   distinct, equally valid shapes, not one default with an exception:
   - **Dependency is an external HTTP API**: fake it with `httptest.Server` (or a plain
     `http.HandlerFunc`) whose paths and query strings match exactly what the real client
     sends — this proves the client builds requests correctly, not just that the handler
     parses a hardcoded response.
   - **Dependency is an internal Go interface** (the handler wraps a service/DB layer, not
     an HTTP client): fake it at the interface boundary instead — a hand-rolled struct with
     one function field per interface method (`mockThing{createFn: ..., resolveFn: ...}`),
     constructed fresh per test case. Reaching for `httptest.Server` here has nothing to
     connect to; it's solving a problem the handler doesn't have.

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
   where relevant. For the concurrent-convergence test shape itself, see
   `foundations:go-testing`.

8. **Middleware tests** — router-agnostic: wrap the middleware under test around a stub inner
   `http.Handler`, drive it with `httptest.NewRecorder`/`httptest.NewRequest`, and assert on
   the concern that middleware owns:
   - **CORS**: allowed origin gets the right `Access-Control-Allow-Origin`, a disallowed
     origin gets none, and an `OPTIONS` preflight is short-circuited before the inner handler
     runs.
   - **Rate limiting**: assert the limit triggers (status + body), and assert two distinct
     caller keys (e.g. different `RemoteAddr`) land in independent buckets — a test that only
     ever uses one caller key would still pass against a broken always-same-bucket
     implementation.
   - **Logging**: redirect the default logger to a buffer for the test, `t.Cleanup` it back,
     and assert on the structured fields (method, path, status, request id) rather than the
     literal log line format.
   - **Body-size caps**: cover both a known `Content-Length` over the cap (rejected before the
     handler reads the body) and an unknown/chunked length that only fails once actually read.

## Anti-patterns

- Building the handler/service under test by hand in every test file instead of a shared
  helper, when one exists.
- Hitting a real external API from a unit test.
- Skipping router-level testing for a handler that reads URL params via the router — this can
  produce a false green that misses a real routing bug.
- Reaching for `httptest.Server` when the handler's dependency is a Go interface, not an HTTP
  client — fake the interface directly instead (see item 3 above).

## Reference

- This repo's own testing skill or `AGENTS.md`, if present, for the shared test helper name,
  fixture examples, and exact test commands.
- **`foundations:go-testing`** for the cross-cutting mechanics this skill builds on
  (concurrent-convergence tests, retry/backoff testing, config-loading tests) that aren't
  specific to HTTP.
