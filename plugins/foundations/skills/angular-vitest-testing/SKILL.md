---
name: angular-vitest-testing
description: >-
  Writes or updates Vitest tests for Angular components, services, pipes, and
  directives (via @angular/build:unit-test). Use when adding or changing code
  under an Angular app's src/, writing *.spec.ts, or when the user mentions
  Angular, TestBed, or test coverage in an Angular codebase.
---

# Angular + Vitest

Framework-scoped patterns for Angular apps using Vitest as the test runner (via
`@angular/build:unit-test`). This repo's own local testing skill or `AGENTS.md` (if any) has
the app-specific commands — this skill covers the Angular/Vitest mechanics that don't vary
by app.

## Naming

| Source file | Spec file |
|---|---|
| `foo.component.ts` | `foo.component.spec.ts` |
| `foo.service.ts` | `foo.service.spec.ts` |
| `foo.pipe.ts` | `foo.pipe.spec.ts` |
| `foo.directive.ts` | `foo.directive.spec.ts` |
| `foo.ts` | `foo.spec.ts` |

Place the spec next to the source file.

## Imports and `TestBed` setup

```typescript
import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
```

- Use `TestBed.configureTestingModule({...})` for anything Angular-wired (components,
  services with injected dependencies).
- For plain TS classes/functions with no Angular DI, instantiate directly — no `TestBed`
  needed.
- Mock dependencies with `vi.fn()`/`vi.spyOn()` (Vitest globals).
- Prefer `provideHttpClient()` + `provideHttpClientTesting()` over the legacy
  `HttpClientTestingModule`.

## Patterns

**Component with a template:**

```typescript
fixture = TestBed.createComponent(MyComponent);
component = fixture.componentInstance;
fixture.detectChanges(); // triggers ngOnInit
```

**Mocking a service:**

```typescript
const myServiceSpy = { getData: vi.fn(), save: vi.fn() };
providers: [{ provide: MyService, useValue: myServiceSpy }];
```

**Observables:**

```typescript
it('should emit value', async () => {
  const result = await firstValueFrom(component.value$);
  expect(result).toBe('expected');
});
```

**`@Input`/`@Output`:**

```typescript
component.myInput = 'test';
fixture.detectChanges();
component.myOutput.subscribe((val) => expect(val).toBe('expected'));
component.triggerAction();
```

**Router navigation:**

```typescript
const router = TestBed.inject(Router);
const spy = vi.spyOn(router, 'navigate');
component.goSomewhere();
expect(spy).toHaveBeenCalledWith(['/expected-path']);
```

**HTTP service tests:**

```typescript
it('should GET data', () => {
  service.fetchData().subscribe((data) => expect(data).toEqual(mockData));
  const req = httpMock.expectOne('/api/data');
  expect(req.request.method).toBe('GET');
  req.flush(mockData);
});
```

Call `httpMock.verify()` in `afterEach` whenever a test uses `HttpTestingController`.

## Test coverage checklist

- [ ] Creation/instantiation
- [ ] Each public method — happy path, edge cases (null/empty/boundary), error/exception path
- [ ] Async flows (Promises, Observables, `fakeAsync`/`tick`)
- [ ] Component lifecycle hooks (`ngOnInit`, `ngOnDestroy`)
- [ ] Template interactions, if the component has one
- [ ] `@Input`/`@Output` bindings
- [ ] HTTP request method/URL/payload and error handling (4xx/5xx), for services

## Reference

- This repo's own testing skill or `AGENTS.md`, if present, for exact commands
  (`test:ci`/`test:coverage`) and formatting requirements.
