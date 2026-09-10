# Contributing to Origin89

Ship changes that another engineer can understand, reproduce, and maintain.
These standards apply equally to work written by people and AI assistants.
The contributor owns the result and the evidence used to support it.

## Before changing code

1. Read the repository's README, `AGENTS.md`, local contribution guide, and
   instructions in the area being changed. Inspect the working tree and preserve
   other people's changes.
2. Identify the expected behavior, callers, data contracts, and failure cases.
   For a bug, reproduce it and add a regression test that fails for that reason.
3. Use the repository's pinned tools. Node/TypeScript work uses pnpm. When
   adding or upgrading a dependency, verify the latest stable version and its
   compatibility using the [dependency standard](docs/dependencies.md).
4. For changes that can affect equipment, identify the hazards and required
   evidence using the [embedded and hardware standard](docs/embedded.md).

For substantial work, write a short plan with the acceptance criteria and the
checks needed to establish them. Keep ordinary fixes small; a typo correction
does not need a design document or new tests.

Use the repository's `just` recipes as the normal command interface. Node and
TypeScript use Biome for formatting and linting, with pnpm underneath. Follow
the [tooling standard](docs/tooling.md) when adding or migrating these checks.

Before adding anything, assess its value and ongoing upkeep. Automate repeated
maintenance; if that is impractical, simplify or choose another approach. Avoid
copied configuration inventories and checkout snapshots. Follow the
[documentation rules](docs/documentation.md): internal RFCs, ADRs, research, and
exploration belong in `internal-research`; product docs need a concrete reader.

Use the [workspace structure](docs/repository-structure.md) for multi-package work.
Reuse existing components and public APIs before adding another implementation.

## Implementation

- Follow the existing architecture and the relevant [Rust](docs/rust.md) or
  [TypeScript](docs/typescript.md) standard. Keep state transitions and error
  handling explicit. Prefer a small, readable change over a new framework.
- Validate external inputs at their boundary. Preserve units, bounds, freshness,
  ownership, and authorization as data passes between components.
- Update source files before generated files. Regenerate tracked schemas,
  manifests, bindings, and assets with the documented command.
- Keep public contracts, documentation, migrations, and release notes consistent
  with the implementation. Explain compatibility changes.
- Do not hide failures with empty catches, optimistic defaults, disabled checks,
  deleted assertions, or broader permissions.

The [working guide](docs/development.md) covers command execution, AI-assisted
work, and review. The [writing standard](docs/writing.md) applies to documentation,
comments, commit messages, PRs, and assistant messages.

For branded interfaces, follow the [brand integration standard](docs/brand.md).
Use the package's public assets and tokens. Make shared identity changes in
brand, keep the editable sources, and release the package before updating
consumers.

## Test the behavior

For each new or changed nontrivial function or behavior, cover at least **3–4
distinct paths**: ordinary success, invalid input, boundaries, and failure or
recovery where applicable. Four examples of the same successful path do not
meet this requirement. Exercise additional branches when the contract needs it.

Simple wrappers or accessors with fewer meaningful paths should have proportionate
coverage; explain the exception briefly in the PR instead of inventing tests.
Hardware control and safety logic require the full fault matrix, even when that
means many more than four cases. See the [testing standard](docs/testing.md).

Run focused checks while editing, then the repository's required checks for the
affected packages and their consumers. Record commands and outcomes. If a check
cannot run, name the missing environment or fixture and the remaining uncertainty.
A compile pass does not establish runtime behavior or hardware safety.

## Pull requests and commits

Keep each PR focused on one result. Use the [PR template](templates/pull_request_template.md)
to explain the problem, resulting behavior, test evidence, and any remaining
work. Include screenshots for meaningful UI changes and evidence files for
hardware verification. Do not pad descriptions with a file-by-file transcript.

Follow the [commit rules](skills/origin89-commits/SKILL.md): short, specific
subjects, usually no body, and no co-author or AI/tool attribution in messages.
Preserve Git authorship and signing settings. Use
`<name-or-nickname>/<what-you-are-working-on>` for branches, respecting the
contributor's established prefix or an explicitly requested name. The same short
conventional subject rules apply to PR titles because they become squash commits.
Write each PR-body paragraph on one physical line; do not copy hard-wrapped
README text into GitHub comments.

Respect the current task's authorization. Preparing changes does not authorize
committing, pushing, publishing, or operating equipment. An action already
authorized within the task does not need repeated confirmation.

For repositories using Changesets, add a changeset when the shipped package
changes. Docs and internal changes without a shipped effect need no release
note; explain that in the PR. See the [release standard](docs/releases.md).

## Ready for review

- The behavior matches the request, including error and boundary cases.
- Tests assert outcomes and relevant side effects; required checks pass.
- Dependency versions, lockfiles, generated outputs, and docs agree.
- The diff contains only intended changes and no secrets or private test data.
- Known limitations and unperformed checks are stated accurately.
- Changes affecting hazardous behavior include the safety evidence and reviewer
  required by the local release process. Unresolved hazards block deployment.

For this engineering repository, also check local Markdown links, JSON fragments,
skill frontmatter, and rendered workflow templates. Changes to executable templates
need a disposable consumer smoke test; changes to prose need a careful review.

Report security issues using the [security policy](https://github.com/origin89hq/.github/blob/main/SECURITY.md).
