# Verification for equipment changes

Record each hazard and the conditions under which the claimed invariant applies.
Identify the responsible reviewer and required evidence before release. Use the
repository's safety-change record when available.

| Condition | Check |
| --- | --- |
| Normal operation | Intended transition and feedback within specified limits |
| Missing, stale, malformed, or conflicting sensor data | Defined unknown-state handling; no forbidden transition |
| Boot, reset, brownout, watchdog, shutdown | Actual output defaults and recovery behavior |
| Disconnect, duplicate, delayed, or reordered messages | Bounded processing, deduplication, and state reconciliation |
| Command/feedback disagreement or stuck actuator | Fault detection, response, and independent protection |
| Full queue, retry exhaustion, timer wrap, memory pressure | Bounded resources and preserved invariants |
| Corrupt state or interrupted update | Validation, compatibility, and recoverable activation |

For each applicable row, record the stimulus, acceptance limit, observed result,
and evidence location. Mark irrelevant cases with a reason. Define additional
cases for the equipment; this table cannot enumerate every system hazard.

Host tests verify domain logic. Target builds verify compilation and linked size.
Simulation can inject faults. Controlled bench tests must establish physical
output states, timing, electrical behavior, and recovery that those checks cannot.
Record board revision, firmware hash, toolchain, fixture, conditions, instruments,
and results. Missing bench access remains an explicit verification gap.

Review changes to safety behavior with a qualified person independent of the
implementation before deployment. Follow the product's applicable standards and
qualification process; do not infer a safety integrity level from a language,
toolchain, skill, or passing tests.
