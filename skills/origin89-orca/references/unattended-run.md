# Unattended and scheduled runs

Leaving work running is safe only with a checkable finish condition, an isolated
worktree, stated authority, and a record the user can audit on return.

## Agree on the contract before the user leaves

Confirm these from the request, and ask for anything missing before the user
leaves. Nobody can answer once they are gone.

- **Done predicate:** a check that passes or fails, such as "no callers of the old
  parser remain and `just check` passes". A duration is not a predicate.
- **Base and isolation:** the base ref and a `new-child` worktree per writer.
  Never work in the user's active checkout.
- **Authority:** exactly which of commit, push, open PR, and merge were granted.
  Without an answer, keep changes uncommitted or committed locally in the child
  worktree, as the request allows, and push nothing. Merge only with explicit
  permission, a fresh review verdict at the PR head that will be merged, and its
  required checks green. Unattended runs never publish releases, flash firmware,
  or operate equipment.
- **Limits:** a deadline and a stop rule for dead ends, such as "stop and write up
  why after three failed approaches".

## Run the loop

Drive one task with one worker, or a queue with one owner worker per item. Keep
at most one writer per branch; the coordinator alone rebases or retargets a
stack, following [gh-stack](../../origin89-gh-stack/SKILL.md) for dependent PRs.

Each iteration makes the smallest change the evidence supports and checks it
against the predicate. Keep it, committing if authorized, when it helped; discard
it when it did not. A plateau means change approach, not stop. Never weaken the
predicate, skip checks, or delete assertions to finish.

Before counting a queue item as done, have a fresh reviewer from the other agent
family check its head SHA, using the review panel when the change warrants it.
Any change to the patch voids the earlier verdict.

The coordinator waits with the orchestration guide's bounded `check --wait`, not
a sleep loop. Count only side effects as progress: commits, pushes, PR or CI
changes, and reports. When a worker exceeds its expected runtime with no side
effect, inspect it with `worker-list` and `worker-read`, and stop or replace it
only with the positive proof the guide requires.

A worker that needs an action outside its authority, or one that cannot be undone,
escalates to the coordinator. The coordinator parks that Task, optionally with a
`gate-create` so dependent Tasks wait, keeps the other items moving, and lists the
decision in its report. The user sees it only there. For PRs the run opens,
follow [review follow-up](../../origin89-commits/references/pr-review-follow-up.md).

## Keep a decision log

Keep an untracked log in the coordinator's scratch directory: time, item,
decision, reason, evidence, and result. Do not commit it; put the conclusions a
reviewer needs in each PR body. Confirmed problems outside scope get issues under
[unfinished-work tracking](../../origin89-working/SKILL.md#track-unfinished-work)
when issue filing is authorized; otherwise list issue drafts in the report.

## Report on return

Before reporting, have a reviewer from the other agent family read the log and
the diffs and list what most needs the user's attention. Then report, per item,
the predicate state, branch or PR links, what was kept, what was discarded, parked
decisions, gaps, and the log path. Lead with the items that need the user.

## Scheduled automations

An automation run is one agent session with no coordinator, inbox, or second
reviewer, so it needs its own smaller contract. Create an `orca automations` job
only when the user asks for recurring work, and check
`orca automations create --help` for current flags.

- The prompt names one output (an issue comment, an issue, or a PR), the granted
  authority (read-only unless stated), and where the run records what it did:
  in that output, not a local log. There is no runtime-limit flag, so a time limit
  in the prompt is advisory.
- Use `--precheck` so runs without work are skipped. It must exit non-zero only
  when idle. Let a failing query start the run, so the agent reports the failure
  instead of every run silently skipping:
  `out=$(gh issue list --repo owner/repo --label needs-triage --json number -q '.[].number') || exit 0; test -n "$out"`.
  Test the precheck directly for both the idle and non-idle cases.
- Create the job with `--disabled`, run it once with `orca automations run`, read
  the result with `orca automations runs`, and enable it only after that run is
  right.
- Without `--workspace`, each run gets a new worktree. Name who removes
  finished run worktrees, or the job accumulates them. `--reuse-session` needs a
  `--workspace` naming a dedicated Orca worktree, never the user's checkout.
- Name the job's owner and purpose. List and remove jobs that no longer earn
  their cost.
