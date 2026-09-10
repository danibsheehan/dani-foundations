---
name: injection-prevention
description: >
  Injection-class vulnerability prevention: XSS/HTML injection, SQL/NoSQL
  injection, command injection, template injection, path traversal, and
  hardcoded secrets in new code. Use when writing or changing code that
  renders, stores, or passes user-supplied content to a template engine,
  shell, SQL/NoSQL query, or filesystem path, regardless of stack.
---

# Injection prevention

Stack-agnostic principles for handling user-supplied content safely at every point it's
rendered, stored, or passed to another interpreter. This repo's own backend-specific skill
or `AGENTS.md` (if any) has the exact sanitization library, ORM, or template engine in use —
this skill covers the *why* and the shape of the rule so it transfers across stacks.

This skill defers to **api-hardening** for SSRF-safe upstream URL construction and
CORS/rate-limit/body-size defaults, and to **authz-object-level-access** for permission
checks — covered there, not restated here.

## Render user content safely

- Rely on the template engine's/framework's default auto-escaping for any user-supplied
  value rendered into HTML.
- Never use a raw-HTML sink (`dangerouslySetInnerHTML`, `.innerHTML`, a `| safe`/`|raw`
  template filter, `v-html`) on user-supplied content without passing it through an explicit
  sanitization library first.

## Query safely

- Never build a SQL/NoSQL query by concatenating or interpolating raw user input into the
  query string.
- Use parameterized queries, prepared statements, or an ORM's query builder for every value
  that comes from a request.

## Never shell out with unsanitized input

- Never build a shell command by concatenating user input into a string passed to a
  `shell:true`-style call.
- Use an argument-array API (e.g. `execFile`, not `exec`/`system`) so user input is passed as
  a discrete argument, never interpreted by a shell.

## Path traversal

- Never build a filesystem path by concatenating raw user input onto a base directory.
- Validate/normalize the input and confirm the resolved path stays under an allowed root
  before reading or writing it.

## Template injection

- Never compile or render a user-controlled string *as* a template. Only render fixed,
  developer-authored templates, passing user data in as variables/context, never as the
  template source itself.

## Secrets in new code

- Never hardcode an API key, token, password, or other secret in source. Read it from
  env/config or a secret manager.
- Never log a secret value, even at debug level.

## Testing

- Add a payload test case for any new input path that reaches a render/query/shell/path
  sink — e.g. `<script>alert(1)</script>` for a render path, `' OR '1'='1` for a query path,
  `../../etc/passwd` for a path-handling function.
- Add or extend these tests whenever a new sink or validation rule is introduced.

## Anti-patterns

- Concatenating user input directly into a SQL string, shell command, filesystem path, or
  template source.
- Disabling a template engine's auto-escaping for a value that includes user input.
- Sanitizing at only one of several places the same user input flows through.
- Hardcoding a secret in source "temporarily" during development.

## Reference

- **api-hardening** for SSRF-safe upstream URL construction and CORS/rate-limit/body-size
  defaults.
- **authz-object-level-access** for authentication/authorization checks.
- This repo's own security skill or `AGENTS.md`, if present, for the exact sanitization
  library, ORM, or template engine in use.
