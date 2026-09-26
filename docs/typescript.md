# Node and TypeScript standard

## Use pnpm

Use pnpm for installation, dependency changes, workspace commands, and local
tools. Keep an exact `packageManager` pin and one workspace lockfile. Do not add
npm, Yarn, or Bun lockfiles or replace commands with `npx`.

```sh
pnpm install --frozen-lockfile
pnpm run lint
pnpm run typecheck
pnpm run test
pnpm run build
```

These are recommended script names. Define their real commands in `package.json`
and make CI run them; do not claim an absent script was executed. Use filters for
affected workspace packages, then test consumers of changed shared contracts.
For release packages, `pnpm check` must build and validate everything that ships.

Use the latest supported Node LTS line for new production projects. Pin and
verify dependencies through the [dependency standard](dependencies.md). Preserve
an existing framework's runtime and module constraints during incremental work.

## Biome and just

Biome is the standard formatter and linter for supported source formats. Use an
exact dev dependency and version-matched config. Keep type checking and tests
separate from Biome, and include all of them in the required checks. Use `just`
recipes as the normal command interface, backed by pnpm scripts. See the
[tooling standard](tooling.md) and its copyable config and recipes.

## Make types describe valid values

Enable `strict`, `noUncheckedIndexedAccess`, and `exactOptionalPropertyTypes`
for new TypeScript projects. The [base fragment](../templates/typescript/tsconfig.base.json)
contains these checks; merge it with the framework's configuration. Select module,
target, libraries, and resolution for the actual runtime. New Node-only projects
should prefer ESM; do not force Node settings into browser or framework configs.

Treat untrusted input as `unknown`, then validate it at the boundary. A type cast
does not validate JSON, configuration, hardware telemetry, or an HTTP response.
Avoid `any`, unproved non-null assertions, and double casts that silence a real
modeling problem. A narrow interoperability exception needs a reason and tests.

Use discriminated unions for state and error outcomes. Distinguish missing,
invalid, stale, and zero values. Keep units explicit. Exported APIs should have
clear input and return types; let local inference handle obvious intermediate
values. Do not add a schema library when existing validation already meets the
contract.

Build types so invalid values cannot be constructed:

- Replace a bag of optional fields with variants. `{ done: boolean; doneAt?: Date }`
  admits `done: true` without a time; `{ kind: 'open' } | { kind: 'done'; at: Date }`
  does not.
- Brand IDs and units that share a primitive when mixing them is a real risk,
  such as `string & { readonly __brand: 'DeviceId' }`. Create them only in the
  validating parser.
- End every `switch` on a union with a `default` branch that assigns the value
  to `never` and throws, so a new variant fails compilation at each consumer:
  `default: { const unhandled: never = state; throw new Error(\`Unhandled state: ${JSON.stringify(unhandled)}\`); }`.
  An unused `never` binding fails Biome's unused-variable lint.
- Use `satisfies` to check a literal without widening it. Use `as` only after
  validation has proved the claim. A type guard must check every property it
  asserts; a guard that lies is worse than a cast.
- Derive types from the owning schema, generated client, or existing type with
  `z.infer`, `Pick`, `ReturnType`, or `typeof` instead of a parallel interface.
- Strengthen a type only where the weaker one forces a non-null assertion, cast,
  or "cannot happen" throw. Precision that removes no failure is extra upkeep.

## Handle I/O and asynchronous work

Await or deliberately manage every promise. Propagate cancellation where supported
and define timeout, retry, cleanup, and partial-failure behavior. Retries of writes
need idempotency or reconciliation; do not repeat an uncertain device command.
Do not swallow errors, log secrets, or invent a successful fallback.

Keep browser-only and server-only code separated. Validate authorization on the
trusted side. Bound collections, buffers, payloads, queues, and expensive work
when their size comes from an external input. Release subscriptions and resources
when components unmount or operations finish.

## Test and document

Use the existing test runner; choose a new one only for a concrete need. Cover
success, rejection, boundaries, and failure/recovery under the [testing standard](testing.md).
Test adapters against realistic schemas and critical user flows through their
public interface. For UI changes, check keyboard behavior, accessibility, and
relevant viewport sizes.

Type checking and build success do not replace runtime tests. Update examples,
schemas, generated clients, and consumer tests when a public contract changes.

Sources: [TypeScript strict checks](https://www.typescriptlang.org/tsconfig/strict.html),
[indexed access checks](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html),
and [exact optional properties](https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html).
