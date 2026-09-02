---
name: caching-and-upstream-perf
description: >-
  Principles for caching and rate-limiting calls to a slow, flaky, or
  rate-limited third-party/upstream API, independent of backend stack. Use
  when adding cached responses, tuning TTLs or QPS/rate limits, reducing
  upstream fan-out, adding debounced search, or when the user mentions
  performance, caching, rate limits, or N+1 calls to an external API.
---

# Caching and upstream performance

Most latency and reliability risk in an app that wraps a third-party API is the **outbound
call**, not local rendering. Prefer cache + coalescing + rate-limit caps over micro-optimizing
UI. This repo's own backend skill (if any) has the exact types/helpers — this skill covers the
*why* and the shape of each rule so it transfers across implementations (an in-memory
coalescing cache, HTTP `Cache-Control` headers, or anything else).

## Backend caching

- **Coalesce concurrent cache misses** (a "singleflight" or `GetOrLoad`-style pattern) so that
  N simultaneous requests for the same not-yet-cached key trigger exactly one upstream call,
  not N — this avoids a "thundering herd" hitting the upstream at once.
- **Match TTL to how often the data actually changes**: short TTLs (seconds) for live/in-progress
  data, longer TTLs (hours) for stable aggregates. Don't use one blanket TTL for everything.
- **Cap memory**: bound cache size/entry count, or sweep periodically — don't let an unbounded
  key space (e.g. raw user-supplied query text) grow the cache indefinitely.
- **Never cache without a TTL**, and never give live/frequently-changing data an hours-long TTL.
- **Communicate cache freshness to clients** where relevant (e.g. `Cache-Control` with
  `stale-while-revalidate`/`stale-if-error` for longer TTLs) rather than treating the cache as
  invisible to the client.

## Respecting the upstream

- **Cap outbound QPS/concurrency** to the upstream, separate from your own server's capacity —
  a third-party API's own rate limits are usually the real constraint, not your server's CPU.
- **Avoid N+1 fan-out**: batch requests when the upstream has a batch endpoint; reuse cached
  sub-results across a fan-out instead of re-fetching shared pieces per item.
- **Always go through one client/helper for the upstream** — never scatter raw HTTP calls to
  the third-party API across handlers; that's where QPS caps and caching get bypassed.
- **Never call the real upstream from unit tests** — use a fake/mock server.

## Frontend

- **Debounce user-driven search/frequent-trigger inputs** (a few hundred ms is typical) so
  typing doesn't stampede the backend/upstream on every keystroke.
- **Abort in-flight requests on cleanup** (e.g. `AbortController`) so a component unmount or a
  new request supersedes a stale one instead of racing it.
- Don't reach for memoization by default — follow this repo's existing patterns for when it's
  actually needed.

## Verification

- Hit the same cached path twice locally and confirm the second response is fast / no
  duplicate upstream call in logs.
- For a coalescing cache specifically: prove concurrent identical misses actually coalesce to
  one upstream call, not N (a small concurrent-load script or test is the only way to prove
  this — reading the code isn't enough).

## Anti-patterns

- Ad-hoc caching (a raw map, or manual get/set) instead of this repo's real cache abstraction
  — raw get+set races under concurrent misses (no coalescing).
- Caching without a TTL, or an hours-long TTL on live/frequently-changing data.
- Unbounded parallel upstream calls per request with no concurrency cap or coalescing.
- Calling the real upstream API from unit tests.
