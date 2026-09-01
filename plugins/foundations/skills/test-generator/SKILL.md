---
name: test-generator
description: Generates thorough, idiomatic unit tests for JavaScript/TypeScript projects, framework-agnostic. Use this skill whenever the user wants to write tests, generate test files, add test coverage, test a function/module/component, or asks anything like "write tests for this", "generate specs", "add unit tests", "how do I test this", or "improve my test coverage". For framework-specific patterns (React, Vue, Angular, etc.), also check this repo's own local testing skill or AGENTS.md.
---

# Test Generator

Generate thorough, idiomatic unit tests for JS/TS modules and functions. This skill covers
the framework-agnostic parts of test generation — structure, coverage, and quality — that
hold regardless of which UI framework or test runner a repo uses.

**This repo likely has its own local testing skill or `AGENTS.md` section** covering its
specific framework (React, Vue, Angular, etc.), test runner conventions, and mocking
patterns (HTTP client, state store, router). Check for one and follow it for anything
framework-specific; use this skill for the parts that don't vary by framework.

## Workflow

1. **Understand the code** — Read the file(s) provided. Identify:
   - Type: UI component, hook/composable, store/state module, plain module, or server-side helper
   - Dependencies: state, injected context, routing, HTTP client, async flows
   - Public API: props/inputs, emitted events/callbacks, exposed methods, exported functions

2. **Plan the test suite** — Before writing, outline:
   - Which behaviours need a `describe` block
   - Happy-path cases
   - Edge cases (empty input, `null`/`undefined`, boundary values)
   - Error cases (rejected promises, thrown errors, failed requests)
   - Async flows (`async`/`await`, waiting for state updates)

3. **Generate the test file** — Follow this repo's framework-specific conventions (see above)
   for imports, mounting/rendering, and mocking; follow the conventions below for everything else.

4. **Show tests in chat** — Display the generated test file in a code block so the user can review it.

5. **Save to disk** — Write to the correct path (see Naming below), aligned with the project's
   test-runner include patterns.

## Spec / test file conventions

### Naming

| Source file             | Test file (common)      |
| ------------------------ | ------------------------ |
| `Foo.tsx` / `Foo.vue`    | `Foo.test.tsx` / `Foo.test.ts` (next to the component, or under `__tests__/` if the project prefers) |
| `useFoo.ts` (hook/composable) | `useFoo.test.ts`    |
| `foo.ts` (plain module)  | `foo.test.ts`             |

Place the test file **next to** the source file unless the user or repo convention says otherwise.

### Structure template

```typescript
describe('MyModule', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should <expected behaviour> when <condition>', () => {
    // ...
  });

  describe('methodName()', () => {
    it('should <happy path>', () => {
      /* ... */
    });
    it('should <edge case>', () => {
      /* ... */
    });
    it('should <error path>', () => {
      /* ... */
    });
  });
});
```

## Plain TypeScript patterns

```typescript
import { chunkIds } from './chunkIds';

it('returns empty chunks for empty input', () => {
  expect(chunkIds([], 10)).toEqual([]);
});
```

Use a mock function for callbacks and fake timers when testing timers — see this repo's test
runner docs for the exact API (`vi.fn()`/`vi.useFakeTimers()` for Vitest, `jest.fn()` for Jest).

## Test coverage checklist

- [ ] Creation / mount (components) or first call (hooks/functions)
- [ ] Each public function or user-visible behaviour — happy path
- [ ] Edge cases: `null`, `undefined`, empty string/array
- [ ] Async: promises settled, state updates flushed where needed
- [ ] Emitted events / callback invocations and prop/input updates (components)
- [ ] Mocks restored between tests
- [ ] HTTP or external modules: success and failure paths

## Quality rules

- **One main assertion focus per `it`** — keep tests easy to diagnose.
- **Descriptive names** — `it('returns an empty list when items is null')` not `it('works')`.
- **Avoid magic values** — use named constants or clear variables for fixtures.
- **Reset state** — fresh mounts/instances and cleared mocks between tests.
- **No `any` unless unavoidable** — keep types in tests.
- **Test behaviour, not private internals** — prefer public API, emitted events/callbacks, and rendered/returned output.

## Output

1. Show the complete test file in a code block in chat.
2. Save the file to disk at the path that matches project conventions.
3. Briefly summarise:
   - Number of `describe` / `it` blocks
   - Mocking strategy (HTTP, routing, state)
   - Any gaps where the user should supply real API payloads or routes
