# Adopt the Origin89 standards

Choose the pieces the repository needs. The commit skill can be adopted without
Changesets. The release starter targets public npm packages using pnpm.

## Shared skills on the next task

Maintain shared skills in engineering. Each adopting repo has a setup script and
an ignored cache. At the start of a new task, `just skills-sync` checks
engineering's `main` revision, downloads changed skills, and links them through
`.agents/skills/`. Shared edits reach the repo on its next successful refresh.

Merge these files in an adoption PR:

| Source here | Destination |
| --- | --- |
| `templates/agents/sync-engineering.py` | `.origin89/sync-engineering.py` |
| `templates/agents/AGENTS.md` | Merge into root `AGENTS.md` |
| `templates/agents/gitignore.fragment` | Merge into `.gitignore` |
| `templates/just/skills.justfile` | Merge into root `justfile` |

The bootstrap uses Python 3.9+ standard libraries, `just`, and read access to the
public GitHub repository. No third-party skill installer or GitHub credentials
are needed. Run `just skills-sync` after setup and verify the next task follows
the root instruction. Engineering must first be published on `main`; a local
unpublished change is not available to remote consumers.

The ignored cache records its source revision and file hashes automatically.
Namespaced skill symlinks point to the current snapshot; existing snapshots stay
available for tasks already using them. The command prints an immutable `path`.
Read `skills/origin89-working/SKILL.md` and relevant skills beneath that path for
the task. Do not manually record source checkout hashes in contributor docs.

This is a task-start instruction, not a background update service. Codex supports
[symlinked skill folders](https://learn.chatgpt.com/docs/build-skills), while its
[agent instructions are loaded per run](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
An active session's skill selector may not refresh immediately; read the files
under the printed snapshot path to load the updated instructions in that task.
For another assistant, configure the same start step in its native instructions.
A link to this repo alone does not load any skills.

If the network request fails, the script uses the verified cache and reports
that it could not check for updates. Run
`python3 .origin89/sync-engineering.py --offline` to use the cache without a
network request. First use requires a network connection. Invalid downloads or
modified cache files stop the refresh; resolve the reported error before using
the shared skills. Report cached use and failures accurately.

Keep project-specific skills alongside the shared ones. The updater refuses to
replace a local folder or a custom link with the same name. Reconcile those files
in the adoption PR, preserving their stronger constraints and notices. An
interrupted refresh can leave `sync.lock`; confirm that no refresh is running
before removing that lock and retrying. Do not run concurrent refreshes in one repo.

Do not edit cached skills. Propose changes here; merged skill content reaches
consumers on their next successful refresh. Local architecture, commands, pinouts,
and exceptions stay in the consuming repo. Shared skills preserve the user's
authorization and cannot grant permission to publish or operate equipment.

Optionally merge `templates/pull_request_template.md` into the repo's existing PR
template. For new TypeScript projects, merge
`templates/typescript/tsconfig.base.json` into the framework-compatible config.
Do not replace existing compiler options wholesale. For equipment projects, use
`templates/safety/change-record.md` to record hazards and verification evidence.

Adopt [brand integration](brand.md) for branded surfaces. Verify the published
package, pin it with pnpm, and validate imports or generated copies in a production
build. A brand checkout or unpublished release is not a production dependency.

## Biome and just

Merge `templates/typescript/biome.json` and
`templates/typescript/package.fragment.json` for Node/TypeScript tooling. Keep
the Biome dependency and schema versions aligned. Keep or add the repo's
typecheck, test, and build scripts and ensure `pnpm check` includes the Biome
lint check.

Merge `templates/just/node.justfile` or `templates/just/rust.justfile` into the
root `justfile`. Include all required checks for mixed and embedded projects,
including `cargo xtask check` where required. Hardware recipes select exact
board rules and exports. Record the supported just version and install it in
local/CI setup. See [the tooling standard](tooling.md); templates do not install
their own tools.

## Changesets setup

Merge these pieces into a branch in the target repo:

| Source here | Destination |
| --- | --- |
| `templates/changesets/.changeset/` | `.changeset/` |
| `templates/changesets/package.fragment.json` | Merge into `package.json` |
| `templates/changesets/docs/releases.md` | `docs/releases.md`, completed for the repo |
| `templates/workflows/origin89-release.yml` | `.github/workflows/origin89-release.yml` |
| `templates/workflows/origin89-check.yml` | Merge into existing CI, or add as `.github/workflows/origin89-check.yml` |

The JSON file is a fragment: preserve the existing package name, version,
scripts, dependencies, exports, and package visibility. Verify the latest stable
pnpm before pinning a version. Keep an older version only for a documented
compatibility constraint. Plan and validate major toolchain migrations
separately. Review `access: public` for every publishable package.

For manual copies, replace every `$default-branch` placeholder in the workflows
with the repository's default branch. Set `baseBranch` in the Changesets config
to match. To offer templates through **Actions → New workflow**, copy the
reviewed workflow YAML files and matching `.properties.json` files into
`origin89hq/.github/workflow-templates/`. GitHub then replaces the workflow
placeholder when creating a copy. The picker does not read this engineering
repository, install package scripts, or install the Changesets config.

Keep `templates/changesets/example.md` as an example. Do not copy it into the
active `.changeset/` directory or publish its example package name.

Define `pnpm check` to build and validate everything that will ship. The version
command calls it after changing versions, so it must regenerate tracked versioned
outputs. In a workspace, make the root private and explicitly mark public package
manifests for publication.

Run `pnpm install` and include the updated lockfile in the adoption PR. The
starter adds an exact Changesets CLI dependency. Include `CHANGELOG.md` in each
package's publish file list if that list is restrictive.

## Existing releases and CI

Preserve an existing publisher's filename if npm trusted publishing is already
bound to it. For example, brand uses `publish-brand.yml`. Configure the publisher
for the final filename and remove duplicate publication triggers.

Complete any outstanding release repair first. Add a real initial changeset
when the adoption changes the shipped package. If nothing is pending and a
package's declared version has never been published, the release workflow can
publish that version on the first default-branch push.

Integrate the validation steps with existing CI instead of replacing it. The
starter job is named `package`; use a unique job/check name if one already exists,
and update required-check settings deliberately.

Enable the settings in the [release standard](releases.md#activation), complete
the local release guide, and verify a release-version and package dry run in a
temporary copy before enabling publication. The default GitHub token requires
a manual check run on the generated release PR; the guide describes the GitHub
App alternative.

## Updating templates

Shared skill content follows `main` through the task-start refresh. The bootstrap
script, workflow, compiler, and tooling templates are executable configuration:
update adopted copies through a normal PR, preserving local behavior and running
the affected checks. The bootstrap does not download and execute a replacement
for itself. Keep this code small and covered by the tests in `tests/`.

Link common standards from the local contribution guide; do not duplicate policy
or maintain an adoption-status inventory. Introduce a pinned reusable workflow
when several repos share a stable implementation and it reduces total upkeep.
Use the [repository structure](repository-structure.md) and
[documentation placement](documentation.md) rules when adding new material.
