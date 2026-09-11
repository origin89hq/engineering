# Origin89 engineering

Shared development standards, repository templates, and agent skills for
Origin89. Each repository documents its architecture, commands, and release
configuration.

Start with [contributing](CONTRIBUTING.md) and the [adoption guide](docs/adopting.md).

| Standard | Covers |
| --- | --- |
| [Repository structure](docs/repository-structure.md) | apps, crates, packages, workspaces, and reuse |
| [Documentation](docs/documentation.md) | Useful docs, private research, and maintenance cost |
| [Working practices](docs/development.md) | Complete work, deliberate commands, AI-assisted development, review |
| [AI review setup](docs/code-review.md) | Codex and Copilot reviews, with optional `@claude` requests |
| [Rust](docs/rust.md) | Typed domain models, ownership, errors, unsafe code, verification |
| [Node and TypeScript](docs/typescript.md) | pnpm, strict types, runtime validation, async behavior |
| [Tooling](docs/tooling.md) | Preferred stack for web, native, and firmware work; repository commands |
| [Testing](docs/testing.md) | 3–4 distinct paths, regressions, integration, fault testing |
| [Dependencies](docs/dependencies.md) | Verified latest stable versions, compatibility, lockfiles |
| [Embedded and hardware](docs/embedded.md) | Hazards, control ownership, physical evidence, release gates |
| [Brand integration](docs/brand.md) | Shared tokens, fonts, logos, Buddy, asset provenance |
| [Writing](docs/writing.md) | Clear docs and messages without filler or invented claims |
| [Releases](docs/releases.md) | Changesets, changelogs, publishing, recovery |

## Shared skills

| Skill | Use for |
| --- | --- |
| [origin89-working](skills/origin89-working/SKILL.md) | Baseline for every task |
| [origin89-commits](skills/origin89-commits/SKILL.md) | Branches, commits, PRs, and bounded background review follow-up |
| [origin89-gh-stack](skills/origin89-gh-stack/SKILL.md) | Stacked branches and dependent pull requests with gh stack |
| [origin89-review](skills/origin89-review/SKILL.md) | Concrete defects, compatibility, test and safety evidence |
| [origin89-testing](skills/origin89-testing/SKILL.md) | Tests for distinct behavior and failure paths |
| [origin89-rust](skills/origin89-rust/SKILL.md) | Rust implementation and review |
| [origin89-typescript](skills/origin89-typescript/SKILL.md) | Node and TypeScript with pnpm |
| [origin89-embedded](skills/origin89-embedded/SKILL.md) | Firmware, hardware, and equipment commands |
| [origin89-embassy](skills/origin89-embassy/SKILL.md) | Embassy adapters, tasks, linking, and existing bench workflows |
| [origin89-brand](skills/origin89-brand/SKILL.md) | Consistent package-based brand integration |
| [origin89-writing](skills/origin89-writing/SKILL.md) | Every AI-written document and message |

Adopting repositories run `just skills-sync` at the start of each new task. The
managed cache fetches updated skills from engineering and preserves local skills.
See [adoption](docs/adopting.md) for setup, offline behavior, and assistant loading.
Edit common skills here; keep repository-specific commands and constraints local.

## Templates and maintenance

`templates/` contains agent guidance, a PR template, strict TypeScript checks,
a safety-change record, and Changesets/Actions starters. The release starter
covers public npm packages, including pnpm workspaces. Rust, firmware, hardware,
and deployed applications keep their own publication mechanisms.

Run `just check` for the refresh bootstrap's offline behavioral tests. See
[skill validation](docs/skill-validation.md) for instruction review scenarios.
Upstream-derived skills retain their notices and licenses. Internal RFCs
and research belong in [internal-research](https://github.com/origin89hq/internal-research).

[origin89hq/.github](https://github.com/origin89hq/.github) holds the
organization profile and community defaults. GitHub's workflow picker reads that
repository's `workflow-templates/`; templates here need explicit adoption or a
reviewed mirror. Each adopting repository configures CI and review to enforce
these standards.
