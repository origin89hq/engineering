# Configure AI code reviews

Keep detailed review criteria in [origin89-review](../skills/origin89-review/SKILL.md)
and the domain skills. Give each reviewer its native entry point, plus a few
local rules about behavior that is easy to misunderstand. Review instructions
guide findings; CI and repository protection enforce merge requirements.

| Reviewer | Entry point | Shared guidance |
| --- | --- | --- |
| Claude | `CLAUDE.md` and the workflow prompt | Each workflow checks out engineering's `main` skills before starting |
| Codex | `Code Review Rules` in root or scoped `AGENTS.md` | Use available shared skills; keep essential local rules in `AGENTS.md` |
| Copilot | `.github/copilot-instructions.md` and root `AGENTS.md` | Use available shared skills; keep essential local rules in the native files |

Claude's checkout resolves one revision per job, so skill changes reach its next
review after merging to engineering's `main`. Workflow templates and native
instruction files remain installed configuration: update them through consumer
PRs. Codex and Copilot use their existing review integrations; an ignored skill
cache on a developer's machine is not present in a fresh hosted review.

## Claude workflows

Adapted from offgrid-equipment's
[mention workflow](https://github.com/origin89hq/offgrid-equipment/blob/main/.github/workflows/claude.yml)
and [automatic review workflow](https://github.com/origin89hq/offgrid-equipment/blob/main/.github/workflows/claude-code-review.yml).
Copy the matching files from `templates/workflows/` into `.github/workflows/`:

Preserve existing workflow filenames when updating an installation; avoid
creating a second automatic reviewer for the same events.

- `claude.yml` handles `@claude` requests. The request determines whether Claude
  should answer, review, or implement a fix. Generated branch prefixes use the
  triggering GitHub username; configure `branch_prefix` if an agreed nickname
  or another local convention applies.
- `claude-code-review.yml` reviews open, non-draft PRs from branches in the same
  repository. It loads the shared review and domain skills, retains the
  plugin's read/comment tool grants, and cancels superseded review runs.

Install the Claude GitHub App for the adopting repository and configure its
`CLAUDE_CODE_OAUTH_TOKEN` secret, or adapt authentication using
[Anthropic's setup guide](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md).
Neither template installs the application's dependencies or runs `just check`.
Reviewers inspect CI for the actual PR head and report unavailable evidence.

The mention workflow can make changes through the App when requested. The
automatic workflow authorizes comments only. The workflow's read permissions
do not restrict the separately issued App token; the prompt and tool grants are
not a replacement for token permissions. Keep the action's default write-access
requirement and bot restrictions. The automatic template skips forks; do not
switch to `pull_request_target` with untrusted PR code to expose secrets there.
See [Anthropic's security guidance](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md).

Both templates pin the action version and use the shared skills as instructions,
without executing engineering's setup scripts. Preserve local constraints when
adopting them, and keep publication or equipment operation out of review jobs.

## Codex

Merge the `Code Review Rules` section from `templates/agents/AGENTS.md` into the
root instructions, then add repository-specific checks close to the code they
govern. For example, a dataset repo should flag a guessed value becoming sourced
evidence; firmware should flag stale input enabling an actuator. State the safe
behavior and any legitimate exception. Avoid duplicating lint rules.

The existing Codex GitHub App reads these rules; no additional workflow is
needed. For a one-off emphasis, use a focused request such as
`@codex review for lost provenance in the import`. Keep essential checks in the
repository's `AGENTS.md` and use shared skills when they are available; do not
assume a coding environment's setup runs during GitHub review. See
[Codex review customization](https://learn.chatgpt.com/docs/third-party/github#customize-what-codex-reviews).

## Copilot

Merge `templates/agents/copilot-instructions.md` into
`.github/copilot-instructions.md`, preserving existing project context. For rules
that apply to specific paths, use `.github/instructions/*.instructions.md` with
an `applyTo` glob, or scoped repository instructions where supported. Keep the
root review rules useful on their own.

Copilot reads review instructions from the PR head, so their changes can be
reviewed before merging. This setup adds instructions to the existing reviewer,
with no extra workflow. Its review skills can also live in `.github/skills/`;
use local skills there for project-specific review work. Keep the detailed
central policy in engineering and disclose when it was unavailable, instead of
claiming that a remote link loaded it. Verify applied guidance in the review session.
See [Copilot review configuration](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review#customizing-copilots-reviews-with-custom-instructions).

## Validate an adoption

Run actionlint on the installed workflows and check their secret names and
permissions. Exercise checkout/setup steps without a model call first. Then use
a representative PR to verify that the selected reviewer reads the expected
rules, reports a real contract violation, and leaves an intentional pattern
alone. Syntax checks do not establish review quality. Enabling automatic reviews
or requesting a live review uses the configured account's review allowance.
