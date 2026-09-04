---
name: go-testing
description: >-
  Tests cross-cutting Go idioms that don't vary by app shape: concurrent
  idempotency/coalescing convergence, retry/backoff via an injectable seam,
  env/config-loader defaults, and table-driven predicate/classifier tests. Use
  when writing or reviewing Go tests for a dedup/coalesce/singleflight-style
  loader, retry-with-backoff logic, a config.Load() reading environment
  variables, or a typed-error classifier function — independent of whether the
  app is an HTTP service, CLI, or library.
---

# Go testing (cross-cutting)

Patterns that apply to Go code regardless of whether it's behind an HTTP handler, a CLI, or
a library — the mechanics don't vary by app shape. This repo's own local testing skill or
`AGENTS.md` (if any) has the app-specific helpers and commands; for HTTP-handler-specific
mechanics (fakes, router-aware tests, middleware), see **`foundations:go-http-testing`**
instead.

## Concurrent idempotency / coalescing convergence

When a function is meant to produce one result under concurrent callers — a coalescing
cache load, a dedup-on-create path, anything singleflight-shaped — prove it with real
concurrency, not a single-threaded call:

```go
const workers = 16
var wg sync.WaitGroup
wg.Add(workers)
results := make(chan string, workers)
errs := make(chan error, workers)

for i := 0; i < workers; i++ {
    go func() {
        defer wg.Done()
        got, err := underTest.Do(ctx, sameKey)
        if err != nil {
            errs <- err
            return
        }
        results <- got
    }()
}
wg.Wait()
close(results)
close(errs)

for err := range errs {
    t.Fatal(err)
}
var first string
for got := range results {
    if first == "" {
        first = got
    } else if got != first {
        t.Fatalf("got %q and %q, want one winner", first, got)
    }
}
```

This pattern shows up in two distinct forms — an in-memory cache's coalescing loader
(assert the underlying load/fetch function ran exactly once) and a DB-backed dedup-on-create
path (assert exactly one row exists for the shared key afterward) — same shape, different
side-effect assertion. Always assert the side-effect count (load calls, row count), not just
that all callers got the same value — a bug that calls the underlying loader N times but
happens to return the same cached value each time would still pass a value-only check.

## Retry/backoff via injectable seam

Retry logic is only testable if its non-determinism (which attempt succeeds, how long it
waits) can be controlled from the test. Give the constructor (or a test-only variant of it)
a seam to inject that:

- A **generator/factory function** parameter so a specific attempt can be forced to fail or
  collide (e.g. a code-generator that returns a colliding value on the first call, a valid
  one on the second) — proves the retry path actually re-attempts rather than just proving
  the happy path.
- **Backoff duration** as its own pure function, tested table-driven against each attempt
  number, including the capped/max case.
- Any **sleep-with-cancellation** helper tested for both outcomes: returns before the
  duration elapses when the context is already canceled, and returns nil after sleeping when
  it isn't.

## Config/env-loading tests

For a `Load()`-style function that reads its configuration from environment variables:

- Maintain **one explicit list of every env key `Load()` reads**, and reset all of them via
  `t.Setenv(key, "")` in a single shared helper before each defaults test — a test that
  forgets to reset a key silently depends on whatever happens to be set in the parent process
  environment.
- Assert defaults with a **full struct comparison** against the expected `Config{}` literal,
  not field-by-field — a field-by-field style silently stops catching new fields added to the
  struct later.
- When the env-key list and the loader drift out of sync (a new field added to one but not
  the other), that's a real bug this test is meant to catch — keep the list current rather
  than only adding entries when a test happens to fail.

## Table-driven predicate/classifier tests

For a small named predicate that classifies an error (retryable vs. not, a specific typed
error vs. any other), test it table-driven and always include:

- The **nil-error** case.
- A **generic/unrelated error** case (proves the predicate isn't accidentally true for
  everything).
- Every **typed/sentinel value** the predicate is meant to recognize, asserted individually
  rather than only through the code path that happens to produce it.

## Anti-patterns

- **Wall-clock sleeps with no assertion on what happened during them** — a test that sleeps
  past a TTL or a retry window but only checks the final state, not the call/side-effect
  count, will still pass against a broken implementation that did the work more (or fewer)
  times than expected.
- **Skipping the "failed operation must not leave partial state" case** — a failed load must
  not populate the cache; a failed create must not leave a row behind. Test the negative
  explicitly, don't infer it from the success-path test.
- **Asserting only a status/loading flag** instead of the actual converged value — some
  async paths start in a state that happens to look like "done" before the real work
  finishes, so a flag-only assertion can pass for the wrong reason.

## Reference

- This repo's own testing skill or `AGENTS.md`, if present, for the shared test helper name,
  fixture examples, and exact test commands.
- **`foundations:go-http-testing`** for HTTP-handler-specific mechanics (fakes, router-aware
  tests, middleware tests) that build on these.
