# Testing standard

Tests should fail when a required behavior breaks. Test count and coverage help
find gaps; neither establishes correctness on its own.

## Cover distinct paths

For each new or changed nontrivial function or public behavior, cover at least
3–4 distinct paths. Start with this matrix and extend it for the actual contract.

| Path | Examples | Assert |
| --- | --- | --- |
| Ordinary success | Valid input, supported state | Exact result and intended side effects |
| Invalid input | Malformed payload, unsupported value, missing field | Specific rejection and absence of forbidden side effects |
| Boundary | Empty input, minimum/maximum, exact deadline, overflow | The documented inclusive/exclusive behavior |
| Failure and recovery | Timeout, cancellation, dependency failure, retry | Error, state, cleanup, retry limits, and recovery behavior |

Count distinct behavioral cases, including parameterized cases. Do not multiply
equivalent happy-path inputs to reach four. Exercise every relevant branch and
transition, even when it requires more cases. If a getter, wrapper, or constant
has fewer meaningful paths, test those paths and briefly record why fewer apply.
Pure documentation and formatting changes need relevant validation, not invented
unit tests. A small control function can still require extensive fault coverage.

For example, an equipment-reading parser should accept a documented reading,
reject a missing unit, handle its exact allowed limits, and reject truncated or
out-of-range input. A controller consuming that reading also needs stale-input,
disconnect, restart, conflict, and actuator-feedback cases. Parser tests do not
cover the controller's contract.

## Write tests that can catch defects

- Name the behavior and expected outcome. Use explicit fixtures and assertions
  on values, error variants, state changes, and relevant side effects.
- For bug fixes, add a regression test and observe the intended failure against
  the old implementation where practical. A setup or compilation error does not
  demonstrate the bug.
- Prefer whole-result assertions when the full value is part of the contract.
  Avoid assertions that only check that a value exists or no exception occurred.
- Keep test logic simpler than production logic. Do not calculate the expected
  answer with the same algorithm being tested.
- Mock an external boundary when needed; keep the behavior under test real.
  Pair mocks with integration or contract tests for the actual adapter.
- Review snapshot changes. Use targeted assertions for critical invariants and
  do not approve snapshot churn without understanding the behavioral change.
- Before keeping a test, ask whether it would still pass if every function it
  imports returned `undefined` or a default value. If so, it cannot catch a defect.
  Common hollow shapes: only `toBeDefined`/`not.toThrow`/`is_ok()`; only
  "mock was called"; a restated constant, config default, or prompt string; and
  assertions on fixture data the subject never processed. Assert the payload a
  mock received or the resulting state, test the code that reads a constant, and
  delete a test that has no observable assertion to make.
- Never delete assertions, skip failures, loosen tolerances, or change expected
  values solely to make CI pass. Changes to expectations need a changed contract.

## Choose the right level

Use unit tests for calculations and transitions, integration tests for persistence
and protocol adapters, and end-to-end tests for critical user journeys. Changes
to schemas or APIs need compatibility tests with their consumers. Race fixes need
a reproducer for the ordering that failed, not only repeated happy-path execution.

Use property tests or fuzzing for parsers, numeric conversions, serialization,
and broad input spaces. Retain failing seeds as regression cases. For unsafe or
concurrent Rust, consider Miri, Loom, or a bounded verifier where supported; record
the tool, modeled assumptions, and limits. These tools supplement ordinary tests.

For AI integrations, replay versioned, sanitized fixtures for tool calls, partial
streams, malformed outputs, retries, and cancellation. Keep live provider checks
separate from deterministic CI. Record the provider/model version and evaluation
criteria when a result depends on live model behavior. Never use a live model's
opinion as the only oracle for correctness or a safety decision.

For the Origin89 controller, tests must consume committed wire vectors directly
and keep their generator independent. Keep compile-fail tests for type-state
invariants and simulated-season tests for switching and chatter. Every bench
finding becomes a simulator fault and regression. Prove that a new fail-safe test
fails when its guard is removed, using a disposable copy or exact-file backup;
restore the working contents, never an older Git version. Long endurance runs are
planned hardware sessions with a bounded scope, not the default unit-test loop.

## Keep tests reproducible

Inject clocks, randomness, and I/O where needed. Prefer a virtual clock to real
sleeps. Isolate temporary directories, ports, state, and environment variables.
Bound waits and clean up resources even after failure. Default test commands must
not need live credentials, public network services, or connected equipment.

Run the targeted tests, then the required suite for affected modules and
consumers. Use coverage to find untested error paths and explain remaining gaps.
Check the behavior matrix even when a coverage target or minimum test count is
met.

## Record evidence

In the PR, list the paths tested, commands run, and their outcomes. Identify any
checks that require another platform or hardware. For hazardous behavior, attach
the [safety record](../templates/safety/change-record.md) with fault-injection and
bench evidence. Host tests and simulations must be labeled as such.
