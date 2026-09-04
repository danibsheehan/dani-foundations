# Doc drift check

Compares what a README/`AGENTS.md` *claims* against what the code *does*, and reports gaps —
it does not fix anything. For stack-*version* claims (README badges, a "Tech stack" table)
already flagged by an automated checker script, use **`foundations:doc-sync-patch`** instead;
this is for broader, self-directed drift detection with no checker required.

## Workflow

Copy this checklist and track progress:

```
Drift Check Progress:
- [ ] Step 1: Extract documented claims
- [ ] Step 2: Extract actual facts from code
- [ ] Step 3: Diff and classify each mismatch
- [ ] Step 4: Report findings
- [ ] Step 5: Fix only if asked
```

**Step 1: Extract documented claims** — from the README/`AGENTS.md`, pull:
- Documented behavior/interface — whichever applies to this project: HTTP routes and
  methods, exported CLI commands, public library functions.
- Config table: flags, env vars, defaults, ports, file paths.
- Project-layout / file-tree description.

**Step 2: Extract the same facts from the code**
- Route/command/export registration, however this stack expresses it (router `.Handle`/
  `.Get` calls, `http.HandleFunc`, a CLI command list, exported symbols).
- The literal defaults passed into config/init functions (a hardcoded port, DB path,
  timeout).
- The actual package/directory structure.

**Step 3: Diff and classify each mismatch**
- **Missing from docs** — exists in code, not mentioned in the docs.
- **Stale in docs** — documented but no longer exists, or the documented value no longer
  matches the code.
- **Drifted layout** — the docs' project-layout section lists directories/files that don't
  match what's actually on disk.

**Step 4: Report findings** — a plain list, with file/line references for both the doc claim
and the code fact. Nothing fixed yet.

**Step 5: Fix only if asked** — if the user confirms they want it fixed, edit only the
affected sections (don't regenerate the whole file), following the matching doc-type
reference (`readme.md`, etc.) for style.
