---
name: doc-writer
description: >
  Generates high-quality documentation for JavaScript/TypeScript and Go codebases.
  Use this skill whenever a user asks to write, generate, update, improve, or create
  documentation of any kind — including README files, API docs (JSDoc/GoDoc), inline
  code comments, or function-level docstrings. Trigger even for vague requests like
  "document this", "add docs to my code", "write a README", "explain this function",
  or "make this repo easier to understand". When in doubt, use this skill.
---

# Doc Writer Skill

Generates clear, consistent, production-quality documentation for JS/TS and Go projects.
Covers three output types: **README files**, **API/function docs**, and **inline code comments**.
All output is written in Markdown (`.md`) unless writing inline source annotations.

---

## Step 1: Classify the Request

Determine which doc type(s) are needed:

| Request                                                     | Doc Type                               |
| ----------------------------------------------------------- | -------------------------------------- |
| "Write a README", "document this repo"                      | → README                               |
| "Document this function/class/interface", "add JSDoc/GoDoc" | → API Docs                             |
| "Add comments", "explain what this code does inline"        | → Inline Comments                      |
| Mixed / ambiguous                                           | → Ask, or default to README + API Docs |

---

## Step 2: Gather Context

Before writing, read the relevant files:

- **README**: Scan repo structure, `package.json` / `go.mod`, existing README if any, entry points, exported symbols
- **API Docs**: Read the specific file(s) containing the functions/types to document
- **Inline Comments**: Read the specific functions or blocks to annotate

Use the shell to explore if needed:

```bash
# JS/TS: find exported functions/types
grep -rn "^export " src/ --include="*.ts" | head -40

# Go: find exported symbols
grep -rn "^func \|^type \|^var \|^const " *.go | grep -v "_test.go" | head -40

# Repo overview
find . -maxdepth 2 -name "*.md" -o -name "package.json" -o -name "go.mod" | head -20
```

---

## Step 3: Write the Documentation

Read the appropriate reference file for the doc type before writing:

- **README** → read `references/readme.md`
- **API Docs (JS/TS)** → read `references/jsdoc.md`
- **API Docs (Go)** → read `references/godoc.md`
- **Inline Comments** → read `references/inline-comments.md`

Then produce the output following those guidelines exactly.

---

## Step 4: Deliver Output

Write directly into the repo at the file's natural location, then show the result in chat:

- **README**: Edit `README.md` at the repo root in place (don't overwrite unrelated sections).
- **API Docs**: Edit the JSDoc/GoDoc comments into the source file(s) being documented.
- **Inline Comments**: Edit the annotated comments into the source file(s) in place.
- If multiple files: edit each, then summarize all changes together.

Always tell the user:

1. What was generated and which files changed
2. Any gaps (e.g., "I couldn't find a description for `X` — you may want to fill that in")

## Accuracy checklist (applies to any repo)

- **Reflect what's actually shipped** — describe real, current behavior from the code, not
  planned/future work. Never list an unshipped feature as done.
- **Match the actual scripts/commands** — a README's Run/Scripts section should name the
  same commands `package.json`/`go.mod`/`Makefile` actually defines, not a remembered or
  aspirational set.
- **Keep stack/version claims aligned with the real manifest** — if this repo has an
  automated check for this (a script comparing README/`AGENTS.md` stack claims against
  `package.json`/`go.mod`/CI versions — see `check_stack_docs.py` as a reference
  implementation, already present in more than one of these repos), make sure the doc
  change would pass it, not just read plausibly.
- **Keep config docs aligned with actual env/config usage** — documented env var names
  should match `.env.example` and what the code actually reads, not what used to be true.
- **Prefer short tables and copy-pasteable commands** over long prose where either works.

## Style defaults (applies to any repo, unless the repo's own README already established a
different tone deliberately)

- Prefer plain-case section headers over ALL-CAPS or heavy decorative styling in body
  content.
- Add a one-sentence plain-English lead-in before a jargon-heavy table or list, so a
  less-familiar reader isn't dropped straight into terminology.
- Reserve decorative flourish (banners, ASCII art, badges) for the top of the README and
  an optional closing note — not scattered through body sections.

## Design-token / palette-sync pattern (if this repo has one)

If this repo has a design-token source file (e.g. `src/styles/tokens.css`,
`_tokens.scss`, or similar) that feeds a README color/palette table and/or a generated
diagram (e.g. a `docs/*-palette.svg`), all three must stay in sync whenever a token value
changes: update the token file, the README table, and regenerate or hand-edit the diagram
in the same left-to-right/same order. This is a recurring pattern across these repos, not
a one-off — check for this setup (a styles/tokens file + a README palette table) even if
it isn't called out elsewhere, and keep all three in sync if you find it.

## Anything else repo-specific

If this repo's `AGENTS.md` documents something beyond the above (a doc convention truly
specific to this product, not a generic principle), follow that too.
