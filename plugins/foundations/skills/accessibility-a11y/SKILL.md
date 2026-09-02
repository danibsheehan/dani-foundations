---
name: accessibility-a11y
description: >
  Accessibility for web UI: keyboard use, focus, ARIA, screen-reader announcements,
  reduced motion, and semantic structure. Use when improving a11y, auditing new UI,
  fixing focus traps, aria-labels, live regions, color/contrast, or motion.
---

# Accessibility (a11y)

Framework-agnostic accessibility principles and a working checklist. This repo likely has
its own established patterns (live regions, focus-visible styles, custom interactive
widgets) — check for a local accessibility note in `AGENTS.md` or an existing component
before inventing a new pattern; extend what's already there rather than introducing a
second convention for the same problem.

## Patterns to look for and extend (not regress)

- **Live regions** — visually-hidden `aria-live="polite"` (+ `aria-atomic="true"`) for
  dynamic status text that isn't already an alert or dialog.
- **Errors** — `role="alert"` on error banners/messages.
- **Loading** — `role="status"` (or `aria-busy`) for loading copy/spinners.
- **Custom interactive widgets** (anything that isn't a native `<button>`/`<input>` but
  behaves like one) — `role`, `tabindex="0"`, a descriptive `aria-label`, and `@keydown`
  handling for Space/Enter at minimum.
- **Toggle/pressed state** — native `button` with `aria-pressed`, not color alone, for any
  on/off UI control.
- **Decorative elements** — `aria-hidden="true"` on purely decorative
  images/icons/ornaments so screen readers skip them.
- **Meaningful images** — descriptive `alt` text; empty `alt=""` only when genuinely
  decorative (and document that choice).
- **Reduced motion** — `prefers-reduced-motion: reduce` should skip or simplify
  non-essential animation (CSS `@media` and/or a JS check before triggering heavy
  animation/video/Lottie-style players). For an animation library that loads a separate
  data/player file (e.g. a Lottie JSON), check the reduced-motion preference *before*
  fetching that file at all — skip the load, not just the playback, so reduced-motion users
  don't pay the network/parse cost for an animation they'll never see.
- **Focus rings** — prefer `:focus-visible` over bare `:focus` so mouse users don't get a
  ring on click, but keyboard users still see one clearly.
- **Moving focus programmatically after an action** (e.g. after search results or a new
  section appears) — target a landmark or heading with `tabindex="-1"` rather than trying to
  focus non-focusable content directly; this lets you call `.focus()` on it without adding it
  to the natural tab order.

## `index.html` / document baseline

- `lang` attribute set on the root HTML element (update if localizing).
- A meaningful `<title>` and `noscript` fallback message, if applicable.

## Checklist when adding or changing UI

1. **Keyboard** — full path completable without a mouse; logical Tab order; Space/Enter work
   on custom controls; no focus trapped on hidden/disabled content.
2. **Names** — every interactive control has a visible label or `aria-label`/`aria-labelledby`;
   form inputs are associated with their labels.
3. **State** — busy/loading, expanded/collapsed, pressed/selected state is exposed to
   assistive tech, not just shown visually.
4. **Motion** — honor `prefers-reduced-motion`; never rely on motion alone to convey
   essential information.
5. **Color** — never rely on color alone for status; check contrast for text and focus
   rings, especially on themed/branded surfaces.
6. **Headings** — preserve a sensible heading hierarchy when introducing new sections
   (screen reader users navigate by heading structure).

## Verification (manual)

- Keyboard-only pass on the changed flow.
- A screen reader spot-check (VoiceOver on macOS, NVDA on Windows) on the changed region.
- Optional: an automated audit (axe DevTools, Lighthouse accessibility score) on a
  production-shaped build.

When in doubt, match this repo's existing, most-accessible components before inventing a
new pattern for the same kind of problem.
