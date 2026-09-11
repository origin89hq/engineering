---
name: origin89-embassy
description: Implement or review Embassy tasks, HAL adapters, peripheral ownership, linking, and firmware resource use in Origin89. Use for Embassy firmware work alongside the embedded safety skill and the consuming repository's board-specific firmware references.
license: MIT OR Apache-2.0
---

# Origin89 Embassy firmware

Adapted from Origin89's existing `embassy-firmware` skill. Preserve local bench
references and board configuration; this shared skill does not replace them.
Read the installed Embassy versions, features, linker scripts, and local firmware
guide before using APIs or commands. See [project firmware references](references/origin.md).

## Keep the existing architecture

`o89-core` owns decisions without naming peripherals. `firmwares/o89-stm32`
implements the clock, storage, I/O, and bus adapters. A behavior returns a typed
`Decision`; it never writes an output. ESP32 remains a transport processor and
must not depend on `o89-core`. Verify these boundaries in the consuming repository.

On the controller target and its domain tests, preserve the no-allocator
contract. Use arrays or existing heapless containers with named capacities and
documented behavior when full. Prefer typed enums, newtypes, and structured
errors over strings. Match owned enums exhaustively. Do not introduce production
panic paths or use `#[allow]` to hide defects; justified exceptions use the
local `#[expect]` rule.

## Bound asynchronous work

Give each peripheral or bus a clear owner. Use the existing task and message
interfaces to share access. Keep task iterations bounded and avoid blocking
waits, busy loops, and long CPU work that starve a cooperative executor.

External waits need deadlines, cancellation behavior, and an explicit fault
response. Timers and deliberately idle tasks need documented liveness semantics;
do not wrap every await mechanically in a second timer. Dropping a timed-out
future does not prove a bus write or DMA transfer was canceled safely. Check the
installed HAL's contract and reconcile uncertain device outcomes.

Hardware must enforce safety timing independently of cooperative scheduling.
Feed the watchdog only when the required state machines show healthy progress.
Use `defmt` on the target and the existing host logging policy. Keep hot interrupt
paths within the measured timing and floating-point constraints of the actual MCU.

## Verify the actual image

Pin Embassy crate releases exactly or use a reviewed Git revision. Read release
notes before upgrades, check feature names against that version, and revalidate
target behavior. Do not replace a qualified pin with a floating latest dependency.

Check the memory map and linker arguments. Measure the linked release image
against usable application space after bootloader and update reservations, not
the chip's advertised flash. Keep `bench` features and flash addresses explicit;
a bench configuration is not a production image.

Use the repository's fast host tests during edits and run all required checks
before completing firmware work. In the controller repo, `cargo xtask check`
checks specification artifacts and cross-target builds; host tests alone miss
target layout and linking failures. Preserve compile-fail tests for type-state
contracts. Capture benchmark/timing evidence instead of repeating old durations.

For a new peripheral pattern, distinguish a compiling example from a bench-proven
configuration. Turn bench findings into simulator faults and regression tests,
then record the exact board, firmware, capture, and result in the local bench log.
Use the embedded safety procedure before flashing or operating equipment.
