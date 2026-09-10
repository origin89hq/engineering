# Dependencies and tool versions

Use the latest stable release when selecting or updating a dependency. Verify
the version at the time of the change, then record the selected version in the
manifest and lockfile. Do not rely on a version remembered by an assistant.

## Select a version

1. Check the official registry and release notes. Confirm the package identity,
   maintained upstream, release channel, runtime requirements, and relevant API
   changes. A dist-tag alone is not a compatibility review.
2. Select the latest stable version compatible with the repository's supported
   runtimes, targets, and public API. For a new project, start with current stable
   tooling and the latest supported Node LTS line.
3. If the newest stable release cannot be used, state the constraint and exact
   version chosen in the PR. Record an owner and upgrade condition for a lasting
   exception. Treat major upgrades as deliberate migrations.
4. Update the manifest and lockfile together. Review transitive changes and run
   the affected tests and build. Avoid unrelated dependency upgrades in feature PRs.

Pre-releases, nightly toolchains, Git dependencies, and overrides require a
specific documented reason. Keep security fixes prompt. Preserve package-manager
integrity and supply-chain checks; wait or investigate a blocked release instead
of disabling the policy. For hardware already under qualification, requalify
dependency and toolchain changes before using them in a release.

## Node and TypeScript

Use pnpm throughout. Examples below inspect metadata without installing a package:

```sh
pnpm view typescript@latest version engines --json
pnpm outdated
```

After reviewing compatibility, install the version returned by the registry with
`pnpm add <package>@<verified-version>` or
`pnpm add -D -E <tool>@<verified-version>` as appropriate. Angle-bracket values
are placeholders, not executable commands.

Pin `packageManager` to an exact pnpm version. Pin build and test tools exactly;
libraries may use intentional semver ranges for runtime or peer dependencies.
Commit one `pnpm-lock.yaml` per workspace and use `pnpm install --frozen-lockfile`
in CI. Run declared tools with `pnpm exec`. For a justified one-off tool, use
`pnpm dlx <tool>@<verified-version>`; do not leave floating tool downloads in CI.

Use the repository's Node version file or version-manager configuration locally
and in CI. New production Node projects use the latest LTS line; libraries test
their declared supported range. The starter workflows select an LTS major and
receive its patch updates. Projects needing byte-level toolchain reproducibility
can pin the exact patch in a version file read by CI.

Biome is an exact dev dependency with a matching config schema. Verify the current
stable just release and pin its selected version in the repository's supported
tool setup. Recipes must not download floating tools as an implicit side effect.

## Rust

Check crate releases and requirements with the registry and `cargo info`. Use
`cargo add <crate>@<verified-version>` when introducing a dependency, and review
enabled features. Prefer workspace dependency declarations for shared crates.

Commit `Cargo.lock` for reproducible repository builds, including library
workspaces. Use `--locked` for checks and builds. Library manifests still express
the compatibility range consumers resolve; test that range and the declared
minimum supported Rust version where relevant. Update lockfiles using Cargo,
not hand edits. Pin Git dependencies to reviewed revisions when unavoidable.

Pin the main toolchain in `rust-toolchain.toml` and document the MSRV separately.
For new projects use the latest stable release and supported edition. Existing
targets may require a qualified or vendor-supported version; record that constraint.

## Keep the baseline current

Review dependency and toolchain updates regularly through normal PRs. A repository
may configure an update bot, but do not auto-merge major or safety-relevant changes.
Updating this guide does not upgrade consuming repositories automatically.

Sources: [pnpm installation and compatibility](https://pnpm.io/installation),
[Node release policy](https://nodejs.org/en/about/previous-releases), and
[Cargo manifests and lockfiles](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html).
