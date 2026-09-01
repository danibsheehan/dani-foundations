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

## Repo-specific conventions

If this repo has its own local `doc-writer`-named skill or a documentation section in
`AGENTS.md`, follow those repo-specific rules (e.g. keeping a design-token table or an
SVG diagram in sync with a README) in addition to the steps above.
