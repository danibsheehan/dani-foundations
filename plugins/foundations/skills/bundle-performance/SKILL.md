---
name: bundle-performance
description: >
  Bundle size and runtime performance for JS/TS frontend apps. Use when the user asks
  about bundle size, gzip, code splitting, lazy loading, asset weight, Lighthouse, Core
  Web Vitals, network waterfalls, or reducing JS/CSS cost.
---

# Bundle and performance

## Measuring bundle size

1. **Production build** — run this repo's production build command (e.g. `npm run build`
   for Vite/webpack/etc.).
2. **Size report** — check for an existing bundle-report script or `build:report`-style
   npm command in this repo before reaching for an external tool; most build tools also
   have a built-in bundle analyzer (e.g. `vite-bundle-visualizer`, webpack's
   `stats.json` + analyzer). List output assets with raw and gzip size, largest first.

Use a size report after dependency upgrades, adding new libraries, or adding large
assets. Compare before/after **on the same machine**, and compare **sizes and asset
counts, not filenames** — hashed chunk names change between builds even when nothing
meaningful did.

3. **Deploy-shaped build** — if this repo's production build differs from a plain local
   build (a subpath base, an API base URL env var, etc. — see this repo's deploy skill or
   `AGENTS.md`), build with the same env/config CI uses before comparing numbers, so the
   report matches what actually ships.

## What usually dominates

- The core framework + any large third-party libraries pulled in at the top level (charting,
  animation, rich-text editors, HTTP clients).
- Media assets (images, video, Lottie/animation JSON) — check that non-essential ones are
  lazy- or viewport-loaded rather than bundled into the initial page weight.

Prefer **dynamic `import()`** for heavy, rarely-used modules instead of adding them to the
main dependency graph. Think twice before adding a new top-level dependency without
checking its size impact first.

## Runtime checks (browser)

- **Lighthouse** — LCP, TBT/INP, and the accessibility/best-practices scores as a byproduct.
- **Network panel** — look for redundant or unbatched requests, and whether responses are
  cached/reused on repeat visits.
- **Framework devtools** (React DevTools Profiler, Vue DevTools, etc.) — check for
  unnecessary re-renders on the changed flow.

## Guardrails

- Don't trade correctness for size without tests — run this repo's test suite where the
  logic (not just the bundling) changed.
- After a meaningful bundle or import-graph change, rebuild and spot-check the production
  preview (not just dev mode) before calling it done.
