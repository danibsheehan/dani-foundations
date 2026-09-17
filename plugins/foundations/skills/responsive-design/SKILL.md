---
name: responsive-design
description: >
  Responsive UI layout: mobile-first breakpoints, fluid sizing, and testing across
  viewport widths. Use when building or reviewing UI that must adapt across screen
  sizes, fixing fixed-width/overflow layout bugs, or choosing breakpoint strategy.
---

# Responsive Design

Framework-agnostic principles for UI that adapts across screen sizes. This repo likely
has its own established breakpoint values, container patterns, or a design-system's own
responsive primitives — check for an existing convention in `AGENTS.md` or an existing
component before inventing a new one; extend what's already there rather than introducing
a second approach to the same problem.

This skill covers layout and sizing only. It doesn't duplicate:
- **`accessibility-a11y`** — touch-target sizing, pinch-zoom/reflow at 400%, and other a11y
  concerns that overlap with responsive layout.
- **`bundle-performance`** — responsive image weight, `srcset`/lazy-loading, and other
  perf concerns that overlap with responsive images.

## Principles

- **Mobile-first authoring** — write the base (no-media-query) styles for the smallest
  viewport, then add complexity as the viewport grows, rather than writing for desktop
  and overriding downward.
- **Fluid layout over fixed dimensions** — prefer flex/grid layouts that adapt to
  available space over containers with fixed pixel widths or heights that clip or
  overflow at narrow widths.
- **Relative units for scaling sizes** — `rem`, `%`, `vw`/`vh` for anything that should
  scale with viewport or user font-size preference; reserve fixed `px` for things that
  genuinely shouldn't scale (e.g. hairline borders).
- **Fluid type and spacing** — prefer `clamp()`/`min()`/`max()` for type and spacing that
  needs to scale smoothly, instead of a stack of fixed-`px` overrides at every breakpoint.
- **Content-driven breakpoints** — choose breakpoints where *this content* visually
  breaks (text wraps awkwardly, a grid gets cramped), not a fixed list of named device
  widths; a breakpoint tied to "iPhone width" or "iPad width" goes stale as devices change.
- **Container queries where supported** — for a component that needs to respond to its
  own container's size rather than the full viewport (e.g. a card reused in a sidebar and
  a full-width section), prefer a container query over a viewport media query.
- **No horizontal overflow** — the page or component should never force horizontal
  scrolling at a narrow viewport; trace overflow back to a fixed-width ancestor, an
  un-wrapped flex row, or an image without a max-width constraint.

## Checklist when adding or changing UI

1. **No horizontal scroll** — layout reflows cleanly at narrow widths without clipping or
   forcing horizontal scroll.
2. **No fixed-width traps** — no container relies on a fixed pixel width/height that
   clips content at a narrower viewport.
3. **Scales without override stacks** — text and spacing scale smoothly (fluid units or
   `clamp()`), not via a long list of one-off breakpoint overrides.
4. **Media scales in its container** — images/video/embeds scale within their container
   rather than overflowing or leaving fixed dead space.
5. **Behaves in-between breakpoints** — grid/flex wrapping looks reasonable at widths
   between the named breakpoints, not just exactly at them.
6. **Orientation change** — portrait/landscape rotation on a touch device doesn't break
   the layout.

## Verification (manual)

- Check the changed UI at roughly narrow (~375px), medium (~768px), and wide (~1024px+)
  viewport widths, using whatever preview mechanism is available (browser resize/device
  toolbar, project's own Storybook/preview tooling, etc.).
- Also check a couple of in-between/odd widths (not just the exact breakpoint values) to
  catch layout that only looks right exactly at a named breakpoint.
- Confirm no horizontal scrollbar appears at the narrowest width tested.

When in doubt, match this repo's existing, most-responsive components before inventing a
new pattern for the same kind of problem.
