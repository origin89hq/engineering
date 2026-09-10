---
name: origin89-embedded
description: Develop or review embedded firmware, hardware designs, and device-control commands in Origin89. Use when changes can affect physical equipment, board configuration, protection, timing, or actuation; require evidence proportional to the hazard.
---

# Origin89 embedded and hardware

Treat physical consequences as part of the contract. Determine the board revision,
firmware, MCU, power domain, actuator, control owner, and relevant hazard before
changing behavior. Read current schematics, datasheets, errata, and local safety
requirements. Never infer a pinout, limit, polarity, or safe output state.

Read the repository's existing firmware, behavior, protocol, fault-injection,
and bench skills. Preserve them during adoption. For Embassy work, also read the
installed `origin89-embassy` skill or local `embassy-firmware` guide. Hardware
repositories retain their importer, immutable exports, and board-specific checks.

## Preserve safety boundaries

Identify safe behavior for boot, reset, brownout, watchdog, lost communication,
invalid or stale input, and recovery. Safe does not always mean de-energized;
derive it from the actual equipment and hazard. Account for hardware defaults
before firmware starts and while the processor is unresponsive.

Preserve deterministic control ownership. In the Origin89 controller design,
STM32 owns decisions and actuation and ESP32 carries transport; verify the current
repository's architecture. Model and remote-client advice must be bounded,
versioned, expiring, and map invalid or missing input to `unknown`. Advice must
not bypass limits, lockouts, interlocks, or the authoritative controller.

Make state transitions, guards, timeouts, retry limits, and recovery explicit.
Check units, numeric bounds, timer wrap, memory budgets, queue capacity, interrupt
latency, DMA ownership, and actual target capabilities. Distinguish accepted
commands from observed actuator state. Reconcile uncertain outcomes before retrying
writes. Check behavior when persistence or firmware updates lose power.

## Collect evidence

Connect each relevant hazard to an invariant, implementation, test, result, and
reviewer. Cover ordinary success, invalid input, boundaries, and failures, then
extend the cases for every hazardous transition. Read
[verification requirements](references/verification.md) for the fault matrix and
release evidence. For board or electrical changes, also read
[hardware review](references/hardware-review.md).

Use host tests and simulation first. Build the actual target and inspect release
memory and timing results. Distinguish host, simulated, bench, and live evidence.
Do not call a change safe or certified because it compiles or passes tests.

## Execute within the task

Inspect command effects before running unfamiliar scripts. Keep build and check
commands separate from flashing, erasing, calibration, and actuation. Before a
hardware operation, confirm the exact target, expected effect, safe setup,
recovery path, and existing authorization for that operation. If these are unknown,
continue offline work and report the specific missing information.

Unresolved hazards or failed safety checks block deployment of affected behavior.
Do not bypass protections to finish a task. Require the local independent safety
review and physical verification before equipment release. AI assistance does
not supply certification or a guarantee that errors are impossible.
