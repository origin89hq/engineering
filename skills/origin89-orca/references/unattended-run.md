# Unattended and scheduled runs

Leaving work running is safe only with a checkable finish condition, an isolated
worktree, stated authority, and a record the user can audit on return.

## Agree on the contract before the user leaves

Confirm these from the request. Ask only for what is missing.

- **Done predicate:** a check that passes or fails, such as "no callers of the old
  parser remain and `just check` passes". A duration is not a predicate.
- **Base and isolation:** the base ref and a `new-child` worktree per writer.
  Never work in the user's active checkout.
- **Authority:** which of commit, push, open PR, and merge are granted. Default to
  local commits and pushed branches with ready PRs for the user to land. Merge
  only with explicit permission and a fresh review verdict at the merged SHA.
  Unattended runs never publish releases, flash firmware, or operate equipment.
- **Limits:** a deadline and a stop rule for dead ends, such as "stop and write up
  why after three failed approaches".

## Run the loop

Drive one task with one worker, or a queue with one owner worker per item. Keep
at most one writer per branch; the coordinator alone rebases or retargets a
stack, following [gh-stack](../../origin89-gh-stack/SKILL.md) for dependent PRs.

Each iteration makes the smallest change the evidence supports, checks it against
the predicate, commits it if it helped, and discards it if it did not. A plateau
means change approach, not stop. Never weaken the predicate, skip checks, or
delete assertions to finish.

Before counting a queue item as done, have a fresh reviewer from another agent
family check its head SHA, using the review panel when the change warrants it.
Any push that changes the patch voids the earlier verdict.

The coordinator waits with the orchestration guide's bounded `check --wait`, not
a sleep loop. Count only side effects as progress: commits, pushes, PR or CI
changes, and reports. When a worker exceeds its expected runtime with no side
effect, inspect it with `worker-list` and `worker-read`, and stop or replace it
only with the positive proof the guide requires.

An action outside the granted authority, or one that cannot be undone, gets a
decision gate for the user. Park that item and keep the others moving. For PRs
the run opens, follow [review follow-up](../../origin89-commits/references/pr-review-follow-up.md).

## Keep a decision log

Keep an untracked log in the coordinator's scratch directory: time, item,
decision, reason, evidence, and result. Do not commit it; put the conclusions a
reviewer needs in each PR body. Confirmed problems outside scope get issues under
[unfinished-work tracking](../../origin89-working/SKILL.md#track-unfinished-work).

## Report on return

Before reporting, have a reviewer from another agent family read the log and the
diffs and list what most needs the user's attention. Then report, per item, the
predicate state, PR links, what landed, what was discarded, open gates, gaps,
and the log path. Lead with the items that need the user.

## Scheduled automations

Create an `orca automations` job only when the user asks for recurring work.
Check `orca automations create --help` for current flags.

- Create it with `--disabled`, run it once with `orca automations run`, read the
  result with `orca automations runs`, and enable it only after that run is right.
- Use `--precheck` so runs without work are skipped. The command must exit
  non-zero when there is nothing to do; a query that prints nothing but exits 0
  still starts the agent. For example:
  `test -n "$(gh issue list --repo owner/repo --label needs-triage --json number -q '.[].number')"`.
- The prompt states the same contract as an unattended run, including authority
  and a per-run time limit. Scheduled runs file issues or open PRs; they do not
  merge, publish, or post outside the repository unless the user granted it.
- Prefer a new worktree per run. Use `--reuse-session` only when later runs need
  the previous session's context.
- Name the job's owner and purpose. List and remove jobs that no longer earn
  their cost.
