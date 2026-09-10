# Embedded and hardware standard

Changes to control logic, firmware, electrical designs, protection settings, or
device commands can affect physical equipment. Identify the possible harm, define
the permitted behavior, and collect evidence before claiming the change is ready
for deployment. These instructions do not certify a product or guarantee zero defects.

Read the consuming repository's instructions, domain skills, and current
configuration. Preserve its behavior, protocol, fault-injection, bench, source
import, and fabrication checks. Exact commands and board constraints stay there.

## Establish the system boundary

Record the board revision, part numbers, firmware version, target, power domain,
actuator, and authoritative controller. Read the applicable datasheet, reference
manual, errata, schematic, and existing safety requirements. Cite document revision
and section for limits. Do not invent pinouts, ratings, timing values, or safe states.

Preserve the documented control owner. In the Origin89 controller architecture,
the STM32 owns decisions, persistence, timing, and actuation; the ESP32 provides
transport. AI and remote clients provide bounded, versioned, expiring advice.
Missing, invalid, or stale advice becomes `unknown`, with a defined controller
response. Verify the consuming repository's current architecture before changing it.

A safe state depends on the equipment and hazard. De-energizing every output is
not universally safe. Record the output behavior for boot, reset, brownout, lost
communications, invalid sensors, shutdown, and recovery. Account for the actual
hardware defaults before firmware starts and while a processor is unresponsive.

## Design for faults

- Represent state transitions explicitly. Define guards, invariants, timeouts,
  hysteresis, retry limits, and recovery conditions. Manual lockouts and physical
  interlocks must remain authoritative.
- Treat sensor quality, units, plausibility, and freshness as part of the value.
  Reject out-of-range or malformed inputs; never turn missing data into a plausible
  zero or retain a stale value indefinitely.
- Bound execution time, memory, queues, and retries. Review interrupt latency,
  priority, atomic support, DMA ownership, and critical sections for the actual MCU.
  A watchdog must detect lost progress, not be fed by a timer that hides a hung task.
- Distinguish command acceptance from observed actuator state. Handle duplicate,
  delayed, reordered, and uncertain commands. Reconcile actual state before
  retrying a write that may already have taken effect.
- Check signedness, endianness, fixed-point scaling, timer wrap, overflow, checksum,
  length, and schema-version handling at protocol boundaries.
- Plan power-loss behavior during persistence and firmware updates. Validate images
  and hardware compatibility before activation; define recovery and rollback.
- Keep safety independent of a network, browser, cloud service, or model response.
  Do not bypass protection or remove diagnostic evidence to make a test pass.

## Verification evidence

Use the [safety change record](../templates/safety/change-record.md) for changes
that alter hazardous behavior. Connect each hazard to an invariant,
implementation, test, result, and responsible reviewer. Cover the 3–4 normal
behavior paths and all applicable faults, regardless of the test count.

| Failure | Evidence to collect where applicable |
| --- | --- |
| Sensor missing, stale, implausible, or conflicting | Defined unknown-state handling and inhibited forbidden transitions |
| Boot, reset, brownout, watchdog, or power loss | Output behavior before initialization and during recovery |
| Disconnect, malformed frame, duplicate or delayed command | Bounded handling, no unintended actuation, and reconciliation |
| Stuck actuator or command/feedback disagreement | Detection, independent protection, and documented fault response |
| Timer wrap, full queue, exhausted retries, memory pressure | Bounded execution and preserved safety invariants |
| Interrupted update or corrupt persisted state | Compatibility checks and a recoverable state |

Run host tests for domain logic, build the actual target in its release profile,
and inspect linked memory use. Use simulation and fault injection before hardware.
Test timing, electrical behavior, and output defaults on a controlled bench with
the right isolation and protections. Record board revision, firmware hash, fixture,
conditions, instrument evidence, and acceptance limits. Clearly label tests that
remain simulated or unperformed.

For board changes, preserve editable CAD sources and validate the netlist, ERC,
DRC, stackup, BOM, footprints, polarity, isolation, protection, and manufacturer
requirements that apply. Design-rule checks cannot establish thermal behavior,
component suitability, or system safety by themselves. Fabrication outputs must
match the reviewed sources and revision.

## Commands and release decisions

Keep ordinary build/check commands separate from flashing and live actuation.
Before a hardware operation, confirm the exact target, expected effect, safe
test setup, recovery path, and authorization for that operation. If the target or
safety conditions are unknown, continue with offline analysis and report the
specific missing evidence; do not guess or run a command against attached hardware.

Unresolved hazards, unverified output polarity, missing protection, or failed
safety tests block deployment of the affected behavior. A qualified reviewer
independent of the implementation must assess safety-relevant changes before
equipment release. AI review can support that work but cannot replace physical
verification or the accountable safety decision.

Use the standards and qualification process applicable to the product and market.
Do not declare IEC, ISO, or other compliance based on these guidelines. If a
qualified compiler is required, select a supported version and target and follow
its qualification conditions; that does not certify the whole application.

Sources: [Embedded Rust concurrency](https://docs.rust-embedded.org/book/concurrency/),
[Ferrocene qualification scope](https://ferrocene.dev/en), and the consuming
repository's controlled hardware and safety documents. This is Origin89 policy,
not a claim that these sources mandate every rule above.
