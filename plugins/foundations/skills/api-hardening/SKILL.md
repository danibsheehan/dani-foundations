---
name: api-hardening
description: >
  Backend/API hardening principles: input validation, safe upstream calls, generic
  client-facing errors, CORS/rate-limit/body-size defaults, and safe logging. Use when
  adding or changing API routes/handlers, a proxy to an external service, validation,
  CORS, rate limiting, timeouts, or SSRF-safe URL construction, regardless of backend stack.
---

# API hardening

Stack-agnostic principles for any backend that accepts client requests and/or calls an
upstream API. This repo's own backend-specific skill or `AGENTS.md` (if any) has the exact
middleware names, config keys, and file locations — this skill covers the *why* and the
shape of the rule so it transfers across a Node/Express proxy, a Go API, or anything else.

## Validate before calling upstream

- Parse and validate path/query params (IDs, dates, enums) before using them — reject
  malformed input with a clear 4xx, not by passing it through and letting the upstream
  call fail confusingly.
- Never build an upstream URL by concatenating raw, client-supplied strings into a path —
  that's an SSRF vector. Build paths from fixed templates plus validated parameters, or an
  explicit allowlist of subpaths.
- The upstream base URL/host should come from server-side config/env, never from a request
  body or query parameter.

## Never leak raw upstream errors to clients

- On an upstream failure, respond with a **generic** client-facing message (e.g. "bad
  gateway", "failed to reach upstream service") — not the raw error string, stack trace, or
  upstream response body.
- Log the actual detail server-side, tagged with a request ID, so it's still debuggable.
- If this repo already threads a request ID through responses (e.g. an `X-Request-ID`
  header), surface it to the client so a user/support request can be correlated back to the
  server-side log without leaking the upstream detail itself.

## CORS, rate limits, and body size — explicit, not implicit

- CORS should allowlist actual origins, not default to `*` in anything beyond local dev,
  unless the API is genuinely meant to be public and credential-free.
- Rate-limit and cap inbound request body size with real, documented values (even generous
  ones) rather than leaving either unbounded.
- Keep error response shapes consistent (e.g. always `{ "error": "..." }` or always the
  same envelope) so clients can handle failures uniformly.

## Testing

- Never call a real external/upstream API from unit tests — mock the client/HTTP layer.
- Add or extend validation tests whenever a validation rule changes.

## Adding a new route/endpoint that calls upstream

1. Decide whether the client can call the upstream service directly in some deployment
   modes (e.g. a static-hosted build with no backend proxy) — don't assume a server-side
   proxy always exists if this repo has more than one deploy target.
2. Allowlist the upstream subpath pattern; validate every dynamic segment.
3. Respond with a consistent error shape for both validation failures and upstream
   failures; preserve upstream status codes for successful passthrough where that's this
   repo's existing convention.
4. Add/extend validation tests for any non-trivial input rule.

## Anti-patterns

- Returning a raw upstream error message or stack trace in a JSON response.
- Disabling rate limiting or defaulting CORS to allow-all in a production config without an
  explicit, reviewed reason.
- Hitting a real external API from a test suite.
- Introducing credentialed/cookie-based CORS without a deliberate auth design.
- Building an upstream URL from unvalidated client input.

## Reference

- This repo's own backend-security skill or `AGENTS.md`, if present, for exact middleware,
  config keys, and file locations.
- This repo's threat-model doc, if one exists — update it in the same change as any of the
  above (CORS allowlist, rate-limit trust boundary, body caps, outbound URL policy).
