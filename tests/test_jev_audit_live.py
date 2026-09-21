"""Live adapter tests replace the network boundary; never require credentials."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import jev_audit as audit
import jev_audit_live as live
sys.path.pop(0)

MODEL = "jev-1.13.0"
CASES = TOOLS.parent / "tests/fixtures/jev-audit/cases.json"


def response():
    return {"model": MODEL, "answers": {"coverage": {
        "type": "choice", "choice": "partial", "confidence": 1,
        "probabilities": {label: int(label == "partial") for label in audit.LABELS},
    }}, "usage": {"input_tokens": 100, "output_tokens": 20}}


class LiveTests(unittest.TestCase):
    def setUp(self):
        self.cases = audit.cases_from(audit.load_json(CASES))

    def test_credential_file_is_literal_and_errors_do_not_echo_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "key.env"
            path.write_text("# local only\nTYPESAFE_API_KEY=test-secret\n")
            self.assertEqual(live.api_key(path), "test-secret")
            for content in ("", "OTHER=test-secret", "TYPESAFE_API_KEY=test-secret\nOTHER=x", "TYPESAFE_API_KEY=bad value"):
                path.write_text(content)
                with self.assertRaises(audit.Invalid) as caught:
                    live.api_key(path)
                self.assertNotIn("test-secret", str(caught.exception))
        with patch.dict('os.environ', {}, clear=True), self.assertRaises(audit.Invalid):
            live.api_key()

    def test_success_records_real_origin_hashes_and_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "recording.json"
            send = MagicMock(return_value=response())
            self.assertTrue(live.run(self.cases, MODEL, "secret", path, 6, send))
            recording = audit.load_json(path)
            self.assertEqual(send.call_count, 6)
            self.assertEqual(recording["origin"], "live")
            self.assertNotIn("secret", path.read_text())
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            report = audit.evaluate(self.cases, MODEL, recording, 0.8)
            self.assertEqual(report["status_counts"]["answered"], 6)
            self.assertEqual(report["known_usage"]["input_tokens"], 600)

    def test_budget_and_existing_output_prevent_all_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "recording.json"
            send = MagicMock()
            for budget in (0, 5, 7):
                with self.assertRaises(audit.Invalid):
                    live.run(self.cases, MODEL, "secret", path, budget, send)
            path.write_text("keep")
            with self.assertRaises(FileExistsError):
                live.run(self.cases, MODEL, "secret", path, 6, send)
            self.assertEqual(path.read_text(), "keep")
            send.assert_not_called()

    def test_failure_stops_without_retry_and_preserves_prior_success(self):
        for failure in (TimeoutError("secret"), audit.Invalid("HTTP 429"), {"model": MODEL}, {"confidence": float("nan")}):
            with self.subTest(failure=type(failure).__name__), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "recording.json"
                send = MagicMock(side_effect=[response(), failure])
                self.assertFalse(live.run(self.cases, MODEL, "secret", path, 6, send))
                self.assertEqual(send.call_count, 2)
                self.assertNotIn("secret", path.read_text())
                report = audit.evaluate(self.cases, MODEL, audit.load_json(path), 0.8)
                self.assertEqual(report["status_counts"]["answered"], 1)
                self.assertEqual(report["status_counts"]["missing"], 4)
                self.assertEqual(report["review_required"], 5)

    def test_https_contract_bounded_response_and_no_redirect(self):
        for status, payload, succeeds in ((200, json.dumps(response()).encode(), True), (302, b'', False), (401, b'secret', False), (200, b' ' * (live.MAX_RESPONSE_BYTES + 1), False), (200, b'not-json', False), (200, b'{"model":1,"model":2}', False)):
            with self.subTest(status=status, size=len(payload)), patch.object(live.http.client, "HTTPSConnection") as connection:
                client = connection.return_value
                client.getresponse.return_value.status = status
                client.getresponse.return_value.read.return_value = payload
                if succeeds:
                    self.assertEqual(live.post({"model": MODEL}, "secret"), response())
                else:
                    with self.assertRaises((audit.Invalid, ValueError)):
                        live.post({"model": MODEL}, "secret")
                connection.assert_called_once_with("api.typesafe.ai", timeout=20)
                self.assertEqual(client.request.call_args.args[:2], ("POST", "/v1/systemone"))
                self.assertEqual(client.request.call_args.kwargs["headers"]["Authorization"], "Bearer secret")
                client.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
