"""Offline contract tests; synthetic responses are never model-evaluation evidence."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/jev_audit.py"
CASES = ROOT / "tests/fixtures/jev-audit/cases.json"
spec = importlib.util.spec_from_file_location("jev_audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
MODEL = "jev-1.13.0"


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.cases = audit.cases_from(audit.load_json(CASES))
        self.requests = audit.prepare(self.cases, MODEL)

    def recording(self, choice="supported", confidence=0.9):
        # This is an intentionally explicit test double, not saved Jev output.
        probabilities = {label: (0.94 if label == choice else 0.02) for label in audit.LABELS}
        entry = self.requests["requests"][0]
        return {"version": 1, "origin": "synthetic", "observations": [{
            "id": entry["id"], "request_sha256": entry["request_sha256"], "elapsed_ms": 25,
            "response": {"model": MODEL, "usage": {"input_tokens": 1000, "output_tokens": 20},
                         "answers": {"coverage": {"type": "choice", "choice": choice,
                                                   "confidence": confidence, "probabilities": probabilities}}},
        }]}

    def evaluate(self, recording, **kwargs):
        return audit.evaluate(self.cases, MODEL, recording, 0.8, **kwargs)

    def test_prepare_excludes_expected_labels_and_review_conclusions(self):
        original = copy.deepcopy(self.cases)
        for case in self.cases:
            case.update(expected="unrelated", label_rationale="SECRET_LABEL", review_url="SECRET_REVIEW", kind="synthetic", group="SECRET_GROUP")
        self.assertEqual(self.requests, audit.prepare(self.cases, MODEL))
        self.assertNotIn("SECRET", json.dumps(self.requests))
        body = self.requests["requests"][0]["body"]
        self.assertEqual(set(body), {"model", "state", "questions"})
        self.assertEqual(body["state"], original[0]["state"])
        self.assertEqual(set(body["questions"]["coverage"]["criteria"]), set(audit.LABELS))

    def test_changed_evidence_or_model_invalidates_recording(self):
        record = self.recording()
        for change in ("evidence", "model"):
            with self.subTest(change=change):
                cases = copy.deepcopy(self.cases)
                model = MODEL
                if change == "evidence":
                    cases[0]["state"]["evidence"][0]["text"] += " changed"
                else:
                    model = "jev-1.14.0"
                report = audit.evaluate(cases, model, record, 0.8)
                self.assertEqual(report["results"][0]["status"], "invalid")
                self.assertEqual(report["results"][0]["action"], "needs_review")

    def test_wrong_confident_support_is_counted_as_false_reassurance(self):
        report = self.evaluate(self.recording())
        self.assertEqual(report["false_reassurance"], 1)
        self.assertEqual(report["correct"], 0)
        self.assertEqual(report["status_counts"], {"answered": 1, "missing": 5, "invalid": 0, "service_error": 0})
        self.assertEqual(report["review_required"], 5)
        self.assertEqual(report["by_case_kind"]["review-derived"], {"cases": 2, "answered": 1, "correct": 0})
        self.assertEqual(report["by_case_kind"]["synthetic"], {"cases": 4, "answered": 0, "correct": 0})
        self.assertTrue(report["advisory_only"])
        self.assertIn("not model performance", report["measurement"])
        self.assertIsNone(report["savings_usd"])

    def test_supported_case_false_alarm_and_correct_gap_have_distinct_metrics(self):
        record = self.recording("partial")
        report = self.evaluate(record)
        self.assertEqual(report["correct"], 1)
        self.assertEqual(report["confusion"]["partial"]["partial"], 1)
        self.assertEqual(report["results"][0]["action"], "inspect_gap")
        self.assertEqual(report["review_required"], 6)
        self.assertEqual(report["uncertain_or_failed"], 5)
        self.assertEqual(report["flagged_gaps"], 1)
        entry = record["observations"][0]
        entry.update(id=self.cases[1]["id"], request_sha256=self.requests["requests"][1]["request_sha256"])
        report = self.evaluate(record)
        self.assertEqual(report["false_gap_flags"], 1)

    def test_low_confidence_and_missing_context_always_request_review(self):
        for choice, confidence, action in (("supported", 0.79, "needs_review"), ("partial", 0.8, "inspect_gap"), ("insufficient_context", 1, "needs_review")):
            with self.subTest(choice=choice, confidence=confidence):
                report = self.evaluate(self.recording(choice, confidence))
                self.assertEqual(report["results"][0]["action"], action)

    def test_bad_response_variants_cannot_look_clean(self):
        changes = [
            lambda response: response.update(model="jev-latest"),
            lambda response: response.update(answers={}),
            lambda response: response["answers"].update(extra={}),
            lambda response: response["answers"]["coverage"].update(type="score"),
            lambda response: response["answers"]["coverage"].update(choice="pass"),
            lambda response: response["answers"]["coverage"].update(confidence=True),
            lambda response: response["answers"]["coverage"].update(confidence=10 ** 400),
            lambda response: response["answers"]["coverage"].update(confidence=float("nan")),
            lambda response: response["answers"]["coverage"].update(probabilities={"supported": 1}),
            lambda response: response["answers"]["coverage"]["probabilities"].update(partial=2),
            lambda response: response["answers"]["coverage"]["probabilities"].update(supported=0.1),
            lambda response: response["answers"]["coverage"].update(choice="partial"),
        ]
        for index, change in enumerate(changes):
            with self.subTest(index=index):
                record = self.recording()
                change(record["observations"][0]["response"])
                report = self.evaluate(record)
                self.assertEqual(report["results"][0]["status"], "invalid")
                self.assertEqual(report["results"][0]["action"], "needs_review")
                self.assertEqual(report["false_reassurance"], 0)

    def test_service_failure_and_empty_recording_remain_explicit(self):
        record = self.recording()
        record["observations"][0].pop("response")
        record["observations"][0]["error"] = "timeout"
        report = self.evaluate(record)
        self.assertEqual(report["status_counts"]["service_error"], 1)
        self.assertEqual(report["review_required"], 6)
        self.assertIsNone(report["accuracy_of_valid_answers"])
        record["observations"] = []
        report = self.evaluate(record)
        self.assertEqual(report["status_counts"]["missing"], 6)
        self.assertIsNone(report["median_recorded_elapsed_ms"])

    def test_record_identity_and_metadata_errors_are_rejected(self):
        for variant in ("duplicate", "unknown", "origin", "both"):
            with self.subTest(variant=variant):
                record = self.recording()
                if variant == "duplicate":
                    record["observations"] *= 2
                elif variant == "unknown":
                    record["observations"][0]["id"] = "missing-case"
                elif variant == "origin":
                    record.pop("origin")
                else:
                    record["observations"][0]["error"] = "timeout"
                    self.assertEqual(self.evaluate(record)["results"][0]["status"], "invalid")
                    continue
                with self.assertRaises(audit.Invalid):
                    self.evaluate(record)

    def test_usage_and_cost_never_assume_missing_measurements_are_zero(self):
        cases = self.cases[:1]
        record = self.recording("partial")
        report = audit.evaluate(cases, MODEL, record, 0.8, 2, 4)
        self.assertAlmostEqual(report["estimated_recorded_cost_usd"], 0.00208)
        self.assertEqual(report["median_recorded_elapsed_ms"], 25)
        record["observations"][0]["response"].pop("usage")
        report = audit.evaluate(cases, MODEL, record, 0.8, 2, 4)
        self.assertIsNone(report["estimated_recorded_cost_usd"])
        self.assertFalse(report["usage_complete"])
        self.assertEqual(report["status_counts"]["answered"], 1)
        for price in (-1, float("inf"), True):
            with self.subTest(price=price), self.assertRaises(audit.Invalid):
                audit.evaluate(cases, MODEL, record, 0.8, price, 0)

    def test_malformed_answer_retains_complete_recorded_cost(self):
        record = self.recording()
        record["observations"][0]["response"]["answers"] = {}
        report = audit.evaluate(self.cases[:1], MODEL, record, 0.8, 2, 4)
        self.assertEqual(report["status_counts"]["invalid"], 1)
        self.assertTrue(report["usage_complete"])
        self.assertAlmostEqual(report["estimated_recorded_cost_usd"], 0.00208)
        record["observations"][0]["response"]["usage"]["input_tokens"] = None
        report = audit.evaluate(self.cases[:1], MODEL, record, 0.8, 2, 4)
        self.assertFalse(report["usage_complete"])
        self.assertIsNone(report["estimated_recorded_cost_usd"])

    def test_live_hundredth_rounding_is_preserved_without_normalizing(self):
        for probabilities, valid in (([0.17, 0.81, 0.0, 0.01], True),
                                     ([0.17, 0.81, 0.02, 0.01], True),
                                     ([0.16, 0.80, 0.0, 0.0], False),
                                     ([0.20, 0.81, 0.02, 0.01], False),
                                     ([0.1701, 0.81, 0.0, 0.01], False)):
            with self.subTest(probabilities=probabilities):
                record = self.recording("partial", 0.75)
                distribution = dict(zip(audit.LABELS, probabilities))
                record["observations"][0]["response"]["answers"]["coverage"]["probabilities"] = distribution
                report = self.evaluate(record)
                self.assertEqual(report["results"][0]["status"], "answered" if valid else "invalid")
                if valid:
                    self.assertTrue(report["results"][0]["rounded_probabilities"])
                    self.assertAlmostEqual(report["results"][0]["probability_sum"], sum(probabilities))
                    self.assertEqual(report["results"][0]["action"], "needs_review")

    def test_expanded_corpus_and_group_reporting_preserve_all_cases(self):
        cases = audit.cases_from(audit.load_json(CASES.with_name("expanded.json")))
        requests = audit.prepare(cases, MODEL)
        self.assertEqual(len(requests["requests"]), 24)
        report = audit.evaluate(cases, MODEL, {"version": 1, "origin": "synthetic", "observations": []}, 0.8)
        self.assertEqual(len(report["by_group"]), 4)
        self.assertEqual(sum(group["cases"] for group in report["by_group"].values()), 24)
        self.assertEqual(sum(group["review_required"] for group in report["by_group"].values()), 24)
        self.assertEqual(report["by_group"]["km43-pr-43"]["cases"], 12)
        changed = copy.deepcopy(cases)
        changed[0]["expected"] = "supported"
        modified = audit.evaluate(changed, MODEL, {"version": 1, "origin": "synthetic", "observations": []}, 0.8)
        self.assertNotEqual(report["case_annotations_sha256"], modified["case_annotations_sha256"])
        self.assertEqual(requests, audit.prepare(changed, MODEL))

    def test_invalid_case_metadata_and_request_bounds(self):
        for variant in ("duplicate", "empty", "label", "unexpected_state", "too_large"):
            with self.subTest(variant=variant):
                data = {"version": 1, "cases": copy.deepcopy(self.cases)}
                if variant == "duplicate":
                    data["cases"].append(data["cases"][0])
                elif variant == "empty":
                    data["cases"] = []
                elif variant == "label":
                    data["cases"][0]["expected"] = "pass"
                elif variant == "unexpected_state":
                    data["cases"][0]["state"]["expected"] = "partial"
                else:
                    data["cases"][0]["state"]["evidence"] *= 3
                with self.assertRaises(audit.Invalid):
                    audit.cases_from(data)
        for model in ("jev-latest", "jev-preview", "other-model"):
            with self.subTest(model=model), self.assertRaises(audit.Invalid):
                audit.prepare(self.cases, model)
        big = copy.deepcopy(self.cases[:1])
        big[0]["state"]["evidence"] = [{"source": "synthetic:budget", "text": "a" * 20_000} for _ in range(4)]
        with self.assertRaisesRegex(audit.Invalid, "too large"):
            audit.prepare(audit.cases_from({"version": 1, "cases": big}), MODEL)

    def test_json_boundary_rejects_duplicate_keys_nonfinite_and_oversized_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            for content in ('{"version":1,"version":2}', '{"elapsed":NaN}', " " * (audit.MAX_FILE_BYTES + 1)):
                path.write_text(content)
                with self.subTest(content=content[:30]), self.assertRaises(audit.Invalid):
                    audit.load_json(path)

    def test_cli_operates_without_network_or_credentials_in_disposable_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, "-I", str(SCRIPT)]
            result = subprocess.run(command + ["prepare", "--cases", str(CASES), "--model", MODEL], cwd=directory, env={}, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(result.stdout)["requests"]), 6)
            recording = Path(directory) / "recording.json"
            recording.write_text(json.dumps(self.recording("partial")))
            result = subprocess.run(command + ["evaluate", "--cases", str(CASES), "--model", MODEL, "--recording", str(recording), "--threshold", "0.8"], cwd=directory, env={}, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["correct"], 1)
            self.assertEqual(report["status_counts"]["missing"], 5)
            self.assertEqual(set(Path(directory).iterdir()), {recording})
            result = subprocess.run(command + ["evaluate", "--cases", str(CASES), "--model", MODEL], cwd=directory, env={}, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertIn("requires --recording and --threshold", result.stderr)


if __name__ == "__main__":
    unittest.main()
