---
name: bugbot-fix-verify
description: >-
  Verifies a Cursor Bugbot (or similar automated review bot) PR comment's claim
  against the actual code, docs, or live behavior before fixing it -- then
  re-verifies the fix actually resolves it and hasn't introduced a new
  regression. Use when the user shares a Bugbot comment link/ID, says "bugbot
  comment" or "bugbot flagged," or asks to fix a bot-reported finding.
---

# Bugbot fix verify

Automated review bot findings are usually right, but "usually" isn't "always" — and even a
correct finding's suggested fix can be wrong, incomplete, or introduce a new problem.

## Order of work

### 1. Fetch the actual finding

```bash
gh api repos/<owner>/<repo>/pulls/<pr>/comments --jq '.[] | select(.id == <id>) | {path, line, body}'
```

Read the full body — severity, exact cited locations, and reasoning. Don't act on the title
alone.

### 2. Verify the claim against ground truth, not the comment's own explanation

- **Code-level claim** (a logic gap, a wrong condition, a wrong file watched): read the
  actual file(s) at the cited locations yourself. Trace through the logic or run it — don't
  just agree it sounds plausible.
- **External-behavior claim** (a deprecated API, browser/platform semantics, a library's
  execution order, a framework's default behavior): check the authoritative source — the
  language's own doc tool, the library's own docs, or fetch the vendor's documentation. A
  plausible-sounding claim about how a platform/library behaves is still just a claim until
  checked against its actual docs.
- **If ground truth is itself ambiguous** (e.g. a requirement documented in two conflicting
  places), say so, and treat the actual PR as a live test with an easy rollback path rather
  than guessing confidently.

### 3. Fix precisely, not just plausibly

Apply the narrowest fix that resolves the confirmed issue, matching this codebase's existing
conventions (naming, error handling, comment style) — don't take a bot's suggested patch as-is
without reading whether it actually fits.

### 4. Re-verify the fix actually resolves it

Run whatever check would have caught the original finding — the actual command (a test suite,
lint run, or a rebuilt output inspection), not just "looks right." A green CI run alone isn't
enough if the finding's own claim is checkable more directly by actually watching it happen.

### 5. Check the fix didn't open a new gap

Especially when the fix touches logic, precedence, or classification (tiers, conditionals,
priority order): re-run the *original* finding's own reasoning against the new state before
pushing. A fix that closes one gap can accidentally open a different one in the same area.

## Anti-patterns

- Applying a bot's suggested patch without reading and understanding it.
- Treating the comment's own explanation as verified fact — it's a claim, not ground truth.
- Fixing the literal symptom without checking whether the fix reintroduces the same class of
  bug elsewhere (see step 5).
- Declaring a check "fixed" without confirming it's actually green end-to-end — not just the
  one line the finding pointed at.
- Skipping verification because severity is Low/Medium — severity reflects blast radius, not
  confidence; low-severity findings are just as often correct as high-severity ones.

## Reference

- Fetch findings: `gh api repos/<owner>/<repo>/pulls/<pr>/comments`.
- Complements the **pr-ready** skill — run this on any open bot findings before considering
  a PR ready.
