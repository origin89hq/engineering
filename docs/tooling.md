# Repository tooling

Use `just` as the normal entry point for repository commands. Node and TypeScript
use pnpm for package management and Biome for formatting and linting. Rust keeps
rustfmt and Clippy. Hardware checks keep the existing domain tools.

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
