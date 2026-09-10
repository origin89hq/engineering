# Adopt the Origin89 standards

Choose the pieces the repository needs. The commit skill can be adopted without
Changesets. The release starter targets public npm packages using pnpm.

## Shared skills on the next task

Maintain shared skills in engineering. Each adopting repo has a setup script and
an ignored cache. At the start of a new task, `just skills-sync` checks
engineering's `main` revision, downloads changed skills, and links them through
`.agents/skills/` and `.claude/skills/`. Shared edits reach the repo on its next
successful refresh.

Merge these files in an adoption PR:

| Source here | Destination |
| --- | --- |
| `templates/agents/sync-engineering.py` | `.origin89/sync-engineering.py` |
| `templates/agents/AGENTS.md` | Merge into root `AGENTS.md` |
| `templates/agents/CLAUDE.md` | Merge the import into root `CLAUDE.md` |
| `templates/agents/claude-settings.fragment.json` | Merge into `.claude/settings.json` |
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
Claude reads `CLAUDE.md` at startup. Import `@AGENTS.md` there so the task-start
instructions load, instead of relying on a sentence asking Claude to open another
file. Keep any stronger local instructions below the import. Its project skills
use `.claude/skills/`; the bootstrap links both assistants to the same cache.
After first adding that directory, restart Claude and confirm the skill list.
The settings fragment disables Claude's default commit and PR attribution;
merge it without changing permissions, hooks, or other local settings. See
[Claude's memory documentation](https://code.claude.com/docs/en/memory#agentsmd)
and [attribution settings](https://code.claude.com/docs/en/settings).
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

## Contribution metadata checks

Copy `templates/workflows/origin89-contribution.yml` into `.github/workflows/`.
Replace `$default-branch` with the target branch and `$engineering-commit` with
the full reviewed engineering commit SHA. The shared action checks conventional
PR titles and commit subjects, common attribution footers, and hard-wrapped
prose paragraphs. The shared skill recommends
`<name-or-nickname>/<what-you-are-working-on>` branches. Personal prefixes have
no shared default: the checker cannot infer a contributor's preferred nickname.
To enforce an agreed prefix, configure both `branch-owner` (the GitHub login)
and `branch-prefix` (the name or nickname followed by `/`) in the consuming
workflow. Without that configuration, branch names are not checked. Other
contributors' branch names are unaffected by an individual's configuration.

The workflow runs on PR metadata events using read-only permissions. It needs
Python 3 and GitHub CLI, both present on GitHub-hosted Ubuntu runners. It reads
PR metadata through the API and runs the pinned action; never add a checkout or
execution of PR-head code to this `pull_request_target` workflow. See
[GitHub's event documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target).

Merge the shared action before its adoption PRs. The metadata workflow becomes
active when installed on the default branch. Verify a run before making its
`contribution` check required where repository protection is available. Until
then, a failed run is visible but does not prevent merging. Existing application
checks stay required. Update the action pin through reviewed dependency PRs.

This checks formatting, not whether a user authorized a push or whether a PR's
claims are true. Review those against the task and actual validation. Markdown
lists, tables, quotes, code examples, and intentional line breaks are allowed;
the prose check is not a complete Markdown parser. An incomplete commit response
or a changed head fails the check instead of reporting a partial pass. GitHub's
PR commit endpoint returns at most 250 commits; split larger PRs before review.

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
