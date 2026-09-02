---
name: vue-vitest-testing
description: >-
  Writes or updates Vitest tests for Vue 3 components, composables, and Pinia
  stores. Use when adding or changing code under a Vue app's src/, writing
  *.test.ts for a .vue component or composable, or when the user mentions
  Vue, Vitest, @vue/test-utils, or test coverage in a Vue codebase.
---

# Vue 3 + Vitest

Framework-scoped patterns for Vue 3 (Composition API, `<script setup>`) apps using Vitest.
This repo's own local testing skill or `AGENTS.md` (if any) has the app-specific mocking and
commands — this skill covers the Vue/Vitest mechanics that don't vary by app.

## Prerequisites (component/SFC tests)

- `@vue/test-utils` — `mount`, `shallowMount`, stubs, `findComponent`.
- `jsdom` — needed whenever the test environment isn't already `jsdom` globally (Vitest will
  fail clearly if it's missing).

Pure composable/TS-module tests can usually run in Vitest's default `node` environment and
don't need either.

## Conventions

### Mounting a `<script setup>` component

```typescript
// @vitest-environment jsdom  (only needed if the project's default test environment isn't jsdom)
import { mount } from '@vue/test-utils';
import MyCard from './MyCard.vue';

it('renders title from props', () => {
  const wrapper = mount(MyCard, { props: { title: 'Rookie' } });
  expect(wrapper.text()).toContain('Rookie');
});
```

Use `flushPromises()` (from `@vue/test-utils`) after an action that triggers async `setup()`
work or a watcher:

```typescript
await wrapper.find('button').trigger('click');
await flushPromises();
expect(wrapper.emitted('save')).toBeTruthy();
```

### Stubbing children / async components

```typescript
const wrapper = mount(Parent, { global: { stubs: { HeavyChild: true } } });
```

### Testing `defineEmits`

```typescript
const wrapper = mount(Child, { props: { modelValue: '' } });
await wrapper.find('input').setValue('hello');
expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['hello']);
```

### Composables (`useX`) — no mount needed

Call the composable inside a tiny wrapper component if it must run inside `setup()`, or test
extracted pure functions separately:

```typescript
import { useCounter } from './useCounter';

it('increments', () => {
  const { count, inc } = useCounter();
  expect(count.value).toBe(0);
  inc();
  expect(count.value).toBe(1);
});
```

If the composable uses `inject`, `mount` a test parent component that `provide`s the keys.

### Mocking HTTP

```typescript
vi.mock('../api/client', () => ({
  getThing: vi.fn().mockResolvedValue({ data: { items: [] } }),
}));
```

Prefer mocking the module the component imports, not implementation details deep inside
private helpers.

### Router / Pinia

- **Router**: pass `global: { plugins: [router] }` with a test router instance, or stub
  `useRouter`/`useRoute` with `vi.mock('vue-router')`.
- **Pinia**: `import { createPinia, setActivePinia } from 'pinia'` in `beforeEach`, then
  `setActivePinia(createPinia())` before mounting or calling store actions.

## Quality rules

- Reset state in `beforeEach` — fresh Pinia instance, cleared mocks, new `mount`.
- Test behavior (rendered output, emitted events, props) — not private component internals.

## Reference

- This repo's own testing skill or `AGENTS.md`, if present, for exact Vitest config (test
  environment default, include patterns) and commands.
