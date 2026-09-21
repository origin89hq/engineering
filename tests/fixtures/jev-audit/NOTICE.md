# Firmware audit fixture provenance

Code and requirement excerpts in `cases.json` are from
[Origin89 firmware](https://github.com/origin89hq/firmware), licensed under
MIT OR Apache-2.0; these excerpts are redistributed under MIT.
Copyright (c) Origin89 contributors. See the repository's
[MIT license](../../../LICENSE-MIT).

Every real excerpt has a GitHub URL with its exact revision and line range:

- Before correction: `f662ddd4a2100c80bd2cce2136ac6b957f61aa75`.
- After correction: `62f13883184035d0e966a76bbe9c76064fa85c88`.
- Review: [F-036 coverage mismatch](https://github.com/origin89hq/firmware/pull/58#discussion_r4057310354).
- Correction: [test: correct partition coverage claims](https://github.com/origin89hq/firmware/commit/62f13883184035d0e966a76bbe9c76064fa85c88).

Claims and labels are pilot annotations based on that review, not verbatim
statements by the author or independently adjudicated ground truth. Two cases
are marked `review-derived`; four altered claims or invented tests are marked
`synthetic`. All belong to the same evaluation group and must stay in the same
dataset split. The full-coverage claim over the corrected test is intentionally
invented; the actual correction keeps F-036 uncovered.

No provider responses are bundled. Unit tests create explicitly synthetic
responses to exercise the evaluator, never to establish model performance.
