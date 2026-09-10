---
name: authz-object-level-access
description: >
  Authorization and object-level access control: confirming a request is not
  just authenticated but permitted to act on the specific resource it
  targets. Use when adding or changing any endpoint or handler that reads or
  writes a specific resource/record, regardless of stack.
---

# Authorization & object-level access control

Stack-agnostic principles for preventing broken object-level authorization (BOLA/IDOR) —
where a request is correctly authenticated but never checked against whether the caller is
allowed to act on the *specific* object it targets. This repo's own backend-specific skill or
`AGENTS.md` (if any) has the exact middleware, ORM scoping pattern, or DB policy in use — this
skill covers the *why* and the shape of the rule so it transfers across stacks.

## Authentication isn't authorization

- Confirming a request carries a valid session/token proves *who* is calling, not *what
  they're allowed to do*. Every state-changing endpoint (not just reads) needs an explicit
  authorization check in addition to authentication.
- Don't assume a read-only endpoint is lower-risk than a write — leaking one user's data to
  another user is still a real vulnerability even without a state change.

## Object-level scoping

- Enforce that a user can only read/write their own data (or data they've been explicitly
  granted access to) via one of: app-code checks on every handler, ORM query scoping (e.g.
  always filtering by the authenticated user's ID), or a DB-level policy (e.g. Postgres
  row-level security).
- Don't rely on the client only ever *asking* for its own data — a request that supplies
  someone else's object ID must still be rejected server-side.

## Never trust a client-supplied ID for identity

- Derive the acting user from the authenticated session/token, never from a request body or
  query parameter (e.g. a `userId` field the client sends).
- A client-supplied identifier for the *target* object (e.g. `/orders/123`) is fine to
  accept — it's the identity of the *actor* that must never come from the request itself.

## Testing

- For any new or changed endpoint that reads/writes a specific resource, add a test that
  authenticates as one user and attempts to access/modify another user's object — expect a
  403/404, not the object's data or a successful write.
- Add this test alongside the happy-path test for the endpoint, not as an afterthought.

## Anti-patterns

- Checking only that a request is authenticated, with no per-object authorization check.
- Trusting a client-supplied user/owner ID to determine whose data to act on.
- Scoping a query by a resource ID alone, without also scoping by the authenticated user.
- Skipping the "wrong owner" test case because the happy path already passes.

## Reference

- This repo's own auth skill or `AGENTS.md`, if present, for the exact middleware, ORM
  scoping pattern, or DB policy in use.
