---
name: origin89-testing
description: Design, add, or review behavior tests for Origin89 changes. Use for feature and bug implementation, test requests, and coverage review; cover distinct success, invalid-input, boundary, and failure paths without inflating trivial test counts.
license: MIT OR Apache-2.0
---

# Origin89 testing

Read the behavior contract, current tests, and repository's test commands. Identify
which inputs, state transitions, outputs, and side effects can vary. Use the
existing test runner and fixtures before adding tooling.

For each changed nontrivial function or behavior, cover at least 3–4 distinct
paths: normal success, invalid input, a boundary, and failure or recovery where
applicable. Add cases for all relevant extra branches. Equivalent happy-path
inputs do not count as distinct paths. For simpler functions, test the meaningful
paths and explain why fewer apply; do not invent failure modes.

For a bug, reproduce the failure and add a regression test that fails for that
reason before the fix where practical. Assert exact results, error variants, state
changes, and forbidden side effects. Never compute expectations with the same
logic being tested or replace useful assertions with existence checks.

Test the implementation itself. Mock external boundaries selectively and verify
adapters with integration or contract tests. Inject time, randomness, and I/O
when needed for deterministic tests. Bound waits, isolate fixtures, and clean up
after failure. Normal tests must not depend on live credentials or connected
equipment.

Use unit tests for decisions, integration tests for interactions between
components, and end-to-end tests for critical user flows. Add property tests or
fuzzing for broad input spaces, retaining failing seeds. Review snapshots and
test changes against the actual contract. Do not delete assertions, skip
failures, or weaken tolerances to pass CI.

For AI adapters, replay sanitized fixtures for tool calls, partial responses,
invalid output, retries, and cancellation. Keep live model evaluations separate
and report model/version and evaluation limits. For physical control, use the
embedded fault matrix and mark hardware evidence separately from simulation.

Run focused tests, then the repository's required affected-package and consumer
checks. Report commands, paths tested, outcomes, and remaining gaps. Coverage
percentages and test counts cannot establish safety or zero defects.

Summarize the important paths in the PR using a sentence or short list. The
3–4-path requirement concerns the tests, not the size of the PR description.
Use a behavior matrix when it helps review a complex change; do not add rows
for inapplicable cases or repeat every test name.
