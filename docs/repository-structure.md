# Repository structure

Use this layout for Origin89 repositories with multiple applications or shared
libraries. Create directories when they have code to hold. A single package,
hardware repository, or standards repository does not need an empty monorepo.

```text
apps/              Deployable web, desktop, and service applications
crates/            Rust libraries, host tools, and shared domain logic
packages/          TypeScript libraries, UI components, clients, and bindings
firmwares/         MCU workspace when target constraints require separation
Cargo.toml         Host workspace membership, shared dependencies, and lints
Cargo.lock         Host dependency resolution
pnpm-workspace.yaml
pnpm-lock.yaml
package.json       Private workspace root and shared package scripts
justfile           Repository command interface
```

This follows the broad organization of [GitButler](https://github.com/gitbutlerapp/gitbutler),
which uses application, crate, and package directories with root
[pnpm](https://github.com/gitbutlerapp/gitbutler/blob/master/pnpm-workspace.yaml)
and [Cargo](https://github.com/gitbutlerapp/gitbutler/blob/master/Cargo.toml) workspaces.
Origin89 keeps its own pnpm, Biome, just, testing, and firmware requirements.

## Workspace ownership

Use one pnpm workspace and lockfile for related Node/TypeScript packages. The
root package is private and pins `packageManager`. A typical workspace starts with:

```yaml
packages:
  - apps/*
  - packages/*
```

Add other paths only when they contain package manifests, such as a Rust crate
that generates a Node binding. Use `workspace:` dependencies between local
packages and declared `exports`; do not import another app's private `src/` files.
Use pnpm catalogs for dependencies shared by several packages. Each package still
declares its own direct dependencies; root hoisting must not conceal missing ones.

Use a root Cargo workspace for compatible Rust crates. Centralize common versions
in `workspace.dependencies`, shared package settings in `workspace.package`, and
lints in `workspace.lints`; member crates explicitly inherit them. Select the
resolver for the chosen edition and toolchain. Declare the MSRV and keep it tested.
Keep internal dependencies as workspace/path dependencies, with versions where
publication needs them. Use a single lockfile per workspace.

Keep MCU firmware in a separate `firmwares/` workspace when targets, dependency
features, linker settings, or release profiles require it. Exclude it explicitly
from the host workspace and retain its own lockfile and target checks. Share
portable `no_std` crates across that boundary; do not move hardware adapters or
allocator dependencies into domain crates to make a workspace check convenient.
A host build cannot replace an actual firmware build.

## Reuse with clear boundaries

Before adding a component, search existing packages and crates for the same
behavior. Reuse or improve a suitable public API. Extract shared code when known
callers need the same behavior and the package has a clear purpose. Avoid
speculative utility packages and dependency cycles.

- Applications compose shared libraries and own deployment-specific configuration.
- Domain crates own typed rules and invariants, with I/O behind explicit boundaries.
- UI packages own reusable components, behavior, and accessibility. Consumers use
  the [brand package](brand.md) for identity, tokens, fonts, and approved artwork.
- Clients and generated bindings come from one authoritative schema or protocol.
  Regenerate them through one command and check for drift; do not hand-maintain
  parallel Rust and TypeScript definitions.
- Test shared behavior in its owning package and exercise its integration in
  consumers. Changes to exported contracts require checking affected consumers.

Give each package a clear purpose and public API. Keep its configuration local
when it differs for a real reason. Centralize common configuration when sharing
it reduces maintenance without coupling unrelated release cycles.

## Adoption

Follow the existing repository map during ordinary changes. Restructure through
a focused change that updates imports, workspace membership, CI paths, package
exports, release configuration, and contributor commands together. Do not move
files as incidental cleanup.

Pure hardware repositories keep their board, CAD, enclosure, and fabrication
layout. Brand keeps editable sources and its generated package. Engineering keeps
standards, skills, templates, and their checks. Structure should help someone find
and change the product. Do not create empty folders or duplicate documentation.
