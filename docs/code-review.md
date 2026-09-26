# Configure AI code reviews

Use the existing Codex and Copilot integrations for automatic PR reviews.
Claude runs only on an explicit `@claude` request; do not install an automatic
Claude review workflow.

Keep detailed review criteria in [origin89-review](../skills/origin89-review/SKILL.md)
and the domain skills. Give each reviewer its native entry point, plus a few
local rules about behavior that is easy to misunderstand. Review instructions
guide findings; CI and repository protection enforce merge requirements.

PR authors follow [background review follow-up](../skills/origin89-commits/references/pr-review-follow-up.md)
after opening a PR. The commit skill owns scheduling, time limits, fixes, and
cleanup; the review skill owns how to assess findings. Hosted review jobs keep
their review scope and do not start an authoring monitor.

| Reviewer | Entry point | Shared guidance |
| --- | --- | --- |
| Codex | `Code Review Rules` in root or scoped `AGENTS.md` | Use available shared skills; keep essential local rules in `AGENTS.md` |
| Copilot | `.github/copilot-instructions.md` and root `AGENTS.md` | Use available shared skills; keep essential local rules in the native files |
| Open Code Review (pilot) | `.github/workflows/ocr-review.yml` caller | Reads neither `AGENTS.md` nor the shared skills; uses its built-in language rules and optional `.opencodereview/rule.json` |

Native instruction files remain installed configuration: update them through
consumer PRs. An ignored skill cache on a developer's machine is not present
in a fresh hosted review.

## Open Code Review

[Open Code Review](https://open-codereview.ai) (OCR) runs its own review agent
against a configured model. Treat its findings as unverified; it skips test
files and Markdown by default.

Locally, developers who have configured `ocr` get an extra pass before opening
a PR, as described in [local Open Code Review](../skills/origin89-review/references/open-code-review.md).
Nothing is installed or configured for people who have not.

On PRs, the [reusable workflow](../.github/workflows/ocr-review.yml) posts
inline findings and a summary comment. It is a pilot in km43 and firmware,
running alongside CodeRabbit, to decide whether OCR can replace it. Copy the
[caller template](../templates/workflows/ocr-review.yml) to
`.github/workflows/ocr-review.yml`, replace `ENGINEERING_COMMIT_SHA`, and grant
the repository the `OCR_LLM_AUTH_TOKEN` organization secret, which holds the
model provider's API key. The defaults use Ollama Cloud with `glm-5.2` and a
one-million-token budget per run; callers can override `llm_url`, `llm_model`,
and `max_tokens_budget`.

The workflow reviews only same-repository, non-draft, non-Dependabot PRs, so
fork PRs cannot spend the quota. Callers use `pull_request_target`, so the
workflow that receives the secret always comes from the base branch and a PR
cannot replace it. This is safe only because the action checks out the base
and reads the PR head as git objects: it never runs PR code, and its model tools
can only read the repository and post comments. Keep it that way; adding a step
that builds or runs PR code would expose the secret. The job has
`contents: read` and `pull-requests: write`, a 20-minute limit, and pins the
action by commit. Callers pin the reusable workflow to a reviewed engineering
commit, because the job passes the secret to that code; bump each caller's SHA
when the workflow changes. Update the pinned action and `ocr_version` together.

## Optional `@claude` requests

The [mention template](../templates/workflows/claude.yml) is adapted from
offgrid-equipment's [mention workflow](https://github.com/origin89hq/offgrid-equipment/blob/main/.github/workflows/claude.yml).
Copy it to `.github/workflows/claude.yml` when the repo needs explicit Claude
requests. Preserve the existing filename when updating an installation.

Mention `@claude` in a new issue or PR conversation comment, or in an issue's
title or body when opening or assigning it. Inline review replies and submitted
reviews do not invoke Claude. Copilot review events can require workflow approval
before the job's mention check runs, even when nobody requested Claude.

The request determines whether Claude should answer, review, or implement a fix.
Generated branch prefixes use the triggering GitHub username; configure
`branch_prefix` if an agreed nickname or another local convention applies.
The workflow checks out engineering's `main` skills at one revision per job,
so merged skill changes reach the next request. It does not execute engineering's
setup scripts. Update the installed workflow through consumer PRs.

Install the Claude GitHub App for the adopting repository and configure its
`CLAUDE_CODE_OAUTH_TOKEN` secret, or adapt authentication using
[Anthropic's setup guide](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md).
The template does not install application dependencies or run `just check`.
Claude inspects CI for the actual PR head and reports unavailable evidence.

The mention workflow can make changes through the App when requested. The
workflow's read permissions do not restrict the separately issued App token;
the prompt and tool grants are not a replacement for token permissions. Keep
the action's default write-access requirement and bot restrictions. Do not use
`pull_request_target` with untrusted PR code to expose secrets there.
See [Anthropic's security guidance](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md).

The template pins the action version. Preserve local constraints when adopting
it, and keep publication or equipment operation out of review jobs.

To retire an existing automatic reviewer, disable its workflow with
`gh workflow disable claude-code-review.yml --repo owner/repo`, replacing the
repository and filename as needed. Cancel any unfinished runs, remove the file
through a PR, and check pending PRs for copies that could restore it. Keep the
mention workflow and local Claude instructions available for explicit requests.

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

Check native instruction files and any installed mention workflow. Run actionlint
on workflow changes, check secret names and permissions, and exercise checkout
steps without a model call first. Use a representative PR to verify that Codex
and Copilot read the expected rules, report a real contract violation, and leave
an intentional pattern alone. Syntax checks do not establish review quality.
Live reviews and explicit Claude requests use the configured account's allowance.
