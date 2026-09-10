# Origin89 release standard

Describe the change, review its version and release notes, then publish the
validated package. Each repository releases independently.

The release template covers public npm packages using Changesets and pnpm. Rust
crates, firmware, hardware, and deployed applications need their own publication
steps; this template does not publish them.

## Contributing a release

1. Make the change and run the repository's `pnpm check` command.
2. Run `pnpm changeset`. Select the affected packages, bump type, and describe
   the result for their users.
3. Include the generated `.changeset/*.md` file in the same PR as the change.
4. Merge the reviewed PR to the default branch. Changesets opens or updates
   one release PR containing the versions and changelogs.
5. Review that PR, run its checks, and merge it when ready to publish.

Feature PRs add changesets. The release PR applies them, regenerates versioned
outputs, and updates changelogs. Multiple changes can collect in one release.

| Bump | Use when | Example |
| --- | --- | --- |
| Patch | Correct an existing contract | Fix an export or manifest entry |
| Minor | Add a compatible capability | Add a token, asset, or API |
| Major | Require consumers to migrate | Remove or rename an export or API |

Bumps are explicit, including before 1.0. A major changeset takes 0.x to 1.0.
Docs, tests, or internal tooling changes that do not affect the shipped package
need no changeset; explain that in the PR. The check template validates pending
changesets without requiring a release for every PR.

Commit subjects stay short and carry no attribution trailers; see the
[commit skill](../skills/origin89-commits/SKILL.md). Changesets determine version
bumps from release notes, independently of commit prefixes.

## Commands and versioned outputs

| Command | Contract |
| --- | --- |
| `pnpm changeset` | Add a release note and explicit bump choice |
| `pnpm changeset status` | Inspect a pending release plan |
| `pnpm check` | Build and validate everything that will ship |
| `pnpm release:version` | Apply changesets, update the lockfile, regenerate outputs, and validate |
| `pnpm release:publish` | Run Changesets publication; normally CI handles it |

The starter version command is:

```sh
changeset version && pnpm install --lockfile-only --ignore-scripts && pnpm check
```

The lockfile refresh also handles workspace dependency changes. A single-package
repo with no version-dependent lockfile entries can omit it. `pnpm check` must
regenerate tracked files containing the package version before validating them.
A repo with a different build layout adapts that command and documents it in
its local release guide.

Use independent package versions by default. Add Changesets `fixed` or `linked`
groups only when there is a reason to coordinate package versions. In a
workspace, mark the root package private and make each publishable package's
visibility explicit. Private packages are excluded by the starter config.

Use `just check` to call the same `pnpm check` command. Include Biome, type
checks, tests, and build/asset verification as applicable. Release jobs can keep
invoking the package script directly; do not introduce a recursive call between
the two entry points.

## Automation

The [starter workflows](../templates/workflows/) use Changesets' select-mode,
version, pack, and publish actions. A default-branch push either updates the
release PR, publishes a version ready for publication, or does nothing.
Maintainers choose when to merge the release PR.

The version job runs the repo's version command before writing the release PR.
The pack job runs `pnpm check`, checks that regeneration left no tracked
changes, and packs the package. The publish job receives those tarballs and uses
npm trusted publishing. Only that job has OIDC permission.

Keep action versions pinned to full commit SHAs. Package and workflow templates
own their exact tool versions; do not maintain a second inventory in this guide.
Verify current stable versions when adopting or updating them, and validate the
result through the same release dry run.

GitHub release notes come from the generated changelog. Single-package tags use
`v<version>`; workspace tags use `<package-name>@<version>`. Preserve existing
published tags during migration and document any change in tag convention.

Repositories that attach ZIPs, PDFs, binaries, or other files extend their
workflow to build and validate them before publication. Record their names,
version source, and recovery procedure in the local release guide.

## Activation

For each adopting repository:

- Enable **Settings → Actions → General → Allow GitHub Actions to create and
  approve pull requests**. Default token permissions can remain read-only;
  the workflow declares each job's permissions.
- Configure npm trusted publishing for the exact repository and workflow
  filename. A new package may need its first publication and publisher setup
  before automation can take over.
- Use one publisher for the same package/version. Retire the previous
  tag-triggered workflow when enabling the new one.
- With the default `GITHUB_TOKEN`, release PRs do not automatically trigger
  their PR workflows. Run the check workflow manually on
  `changeset-release/<default-branch>` before merging. For automatic PR checks,
  configure an Origin89 GitHub App and pass its installation token through the
  version action's `github-token` input.
- Keep release commits and merge messages free of `[skip ci]`.

The manual release workflow operates only on the default branch. It reconciles
the current release state; it is not a version-bump form.

## Recovery

- **Versioning or validation failed:** fix the sources or generated outputs in
  a PR. A rerun uses the original commit and cannot pick up a new fix.
- **npm rejected publication:** fix the publisher settings or permissions and
  rerun the failed job for the same release commit and prepared artifacts.
- **npm succeeded but the tag or GitHub release failed:** inspect all three
  separately. Restore only the missing records at the original release commit,
  using that version's changelog. A rerun alone may not recreate missing records
  after npm already accepted the version.
- **Additional release assets failed:** follow the repo's documented recovery
  procedure using the artifacts from the original validated release.
- **A published package is wrong:** ship a corrective changeset and a new version.

Preserve published versions and tags. Do not publish different contents under an
existing version or move a published tag.

## Adopting and updating the standard

Follow the [adoption guide](adopting.md). Keep a short local release document
with the package names, commands, generated files, workflow filename, extra
assets, and any exceptions. Link to this policy. Review template updates through
that repo's normal PR process; keep version pins in configuration.

Sources: [Changesets automation](https://changesets.dev/guide/automating),
[configuration](https://changesets.dev/guide/config), and
[npm trusted publishing](https://docs.npmjs.com/trusted-publishers/).
