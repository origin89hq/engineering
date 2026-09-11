# Repository tooling

Use `just` as the normal entry point for repository commands. Node and TypeScript
use pnpm for package management and Biome for formatting and linting. Rust keeps
rustfmt and Clippy. Hardware checks keep the existing domain tools.

## Preferred stack

These are our defaults for new work. A shared stack makes it easier to reuse
code, review changes, and move between projects. Choose the parts the product
needs; existing repositories keep their architecture unless a migration has a
concrete benefit. Explain departures in the repository's maintained docs.

| Area | Preferred tools | Use |
| --- | --- | --- |
| Web applications | TypeScript, [React](https://react.dev/), [Vite](https://vite.dev/guide/) | Interactive product interfaces, local development, and frontend builds |
| Navigation | [TanStack Router](https://tanstack.com/router/latest/docs/overview) | Typed routes and URL search parameters |
| Server state | [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview) | Fetching, caching, mutations, and invalidation |
| UI and styling | [shadcn/ui](https://ui.shadcn.com/docs), [Tailwind CSS](https://tailwindcss.com/docs/styling-with-utility-classes) | Component source we can adapt and styling with shared brand tokens |
| HTTP APIs and hosting | [Cloudflare Workers](https://developers.cloudflare.com/workers/), [Hono](https://hono.dev/docs) | Hosted applications and TypeScript APIs using Web Standards |
| Runtime validation | [Zod](https://zod.dev/) | Validate external inputs and derive TypeScript types from schemas |
| Web testing | [Vitest](https://vitest.dev/guide/), [Playwright](https://playwright.dev/docs/intro) | Unit and integration tests, plus browser tests for critical user flows |
| Content sites and docs | [Astro](https://docs.astro.build/en/concepts/why-astro/) | Pages whose main job is to deliver content, with interactive components where needed |
| Native services and tools | [Rust](https://www.rust-lang.org/), [Tokio](https://tokio.rs/tokio/tutorial) | Host applications, device integrations, and asynchronous I/O where needed |
| Desktop applications | [Tauri](https://v2.tauri.app/), Rust, React | A web interface with native capabilities implemented in Rust |
| MCU firmware | Rust, [Embassy](https://embassy.dev/), target-supported HALs | Embedded tasks and peripheral access within the board's resource constraints |

Use additional TanStack libraries when the interface needs them. Router owns
navigation and URL state; Query owns server-state caching. Keep local component
state local. Add cloud storage, queues, or coordination services when the data
and runtime requirements call for them.

For host Rust, prefer [Serde](https://serde.rs/) for serialization,
[tracing](https://docs.rs/tracing/latest/tracing/) for structured diagnostics,
[thiserror](https://docs.rs/thiserror/latest/thiserror/) for typed errors, and
[anyhow](https://docs.rs/anyhow/latest/anyhow/) for application-level error context
where callers do not need a typed contract. Select crates and features for the
actual target; MCU firmware follows the [embedded standard](embedded.md) and
[Embassy guidance](../skills/origin89-embassy/SKILL.md).

Reuse the [shared brand assets and tokens](brand.md) when adapting UI components.
Check offline behavior explicitly for products that need it. Keep exact versions
in manifests and lockfiles under the [dependency standard](dependencies.md), and
update this section when our preferred choices change.

## A consistent command interface

Start with `just --list`. Document these recipes when they apply to the repo:

| Recipe | Contract |
| --- | --- |
| `just fmt` | Format files |
| `just fmt-check` | Check formatting without modifying files |
| `just lint` | Run the configured static checks without fixing files |
| `just typecheck` | Run the TypeScript/framework type checker where applicable |
| `just test` | Run the documented normal test suite |
| `just build` | Build the relevant outputs |
| `just check` | Run all required offline checks |

The default recipe lists available commands. It must not deploy, flash, migrate,
or operate hardware. Keep those actions in explicit separate recipes. Add focused
recipes such as `test-fast` or board-specific checks when the work needs them.
Recipe names do not substitute for inspecting what their commands do.

Keep one implementation of each check. The Node starter has `just check` invoke
`pnpm check`; package scripts own the actual checks. Release automation can keep
calling `pnpm check` with the same result. Never have `pnpm check` invoke
`just check` when the latter already calls it. Mixed Rust/Node/hardware
repositories must include each language's required checks without recursion or
omissions.

Verify the current stable `just` release when adopting it, document a supported
version, and pin it in the repository's tool-manager or CI setup. Do not install
tools automatically inside recipes. Quote parameters and avoid interpolating
untrusted data into shell fragments. Keep timeouts and long-job handling aligned
with the [working rules](development.md).

## Biome

Install a verified stable `@biomejs/biome` as an exact pnpm dev dependency.
Commit the lockfile and a version-matching `biome.json` or `biome.jsonc`. The
[starter configuration](../templates/typescript/biome.json) enables formatting,
recommended lint checks, and import organization. It also rejects explicit
`any`.

The [package fragment](../templates/typescript/package.fragment.json) supplies
formatting and lint scripts. Merge it with existing scripts and dependencies,
and include `pnpm run lint` in `pnpm check` before type checks, tests, and
builds. Keep the compiler, tests, accessibility checks, and hardware validation
alongside Biome.

Use `pnpm exec biome ci . --error-on-warnings` for non-mutating CI validation.
Apply formatting through `pnpm run format`, or safe lint fixes deliberately through
`pnpm run lint:fix`, then review the diff. Do not apply unsafe fixes blindly or
add suppressions just to silence a defect. A narrow exception needs a reason.

Use Biome for supported source formats. Retain a narrowly scoped tool for syntax
or framework rules Biome does not cover. Do not run two formatters over the same
files with competing rules. Document the gap and configure generated, vendored,
and build-output paths explicitly; do not exclude authored source indiscriminately.

## Adoption

Merge the appropriate [Node](../templates/just/node.justfile) or
[host Rust](../templates/just/rust.justfile) starter into the repository's
`justfile`. Firmware repositories include specification checks and builds for
each target. Hardware repositories use separate recipes to import fabrication
files into the board's archive and validate them with the board's Gerber rules.
Validation must not rewrite or replace archived files. Preserve existing tools
and constraints.

Sources: [Biome setup and CI](https://biomejs.dev/guides/getting-started/) and
[the just manual](https://just.systems/man/en/).
