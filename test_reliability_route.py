"""Integration tests for POST /reliability-check."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import app as app_module


class ReliabilityRouteTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()
        self.creator_number = 0

    def post(self, text):
        self.creator_number += 1
        return self.client.post(
            "/reliability-check",
            json={
                "creator_id": f"reliability_route_{id(self)}_{self.creator_number}",
                "text": text,
            },
        )

    @patch("app.audit.log_decision")
    @patch("app.stylometry.style_signal", return_value=0.2)
    @patch("app.detector.model_signal", return_value=0.2)
    def test_stable_result_is_returned_and_logged(
        self, model_signal, style_signal, log_decision
    ):
        response = self.post("Simple words only.")
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["stability"], "stable")
        self.assertEqual(body["guess"], "human")
        self.assertFalse(body["human_review"])
        self.assertIn("original_result", body)
        self.assertIn("latency_ms", body)
        model_signal.assert_called_once()
        style_signal.assert_called_once()
        log_decision.assert_called_once()
        self.assertEqual(
            log_decision.call_args.kwargs["event"], "reliability_check"
        )

    @patch("app.audit.log_decision")
    @patch("app.stylometry.style_signal")
    @patch("app.detector.model_signal")
    def test_label_change_forces_unsure(
        self, model_signal, style_signal, log_decision
    ):
        def score(text):
            return 0.8 if "," in text else 0.2

        model_signal.side_effect = score
        style_signal.side_effect = score

        response = self.post("Clear wording, with removable punctuation.")
        body = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["stability"], "unstable")
        self.assertEqual(body["guess"], "unsure")
        self.assertTrue(body["human_review"])
        self.assertTrue(body["label_changed"])
        self.assertIn("label_changed", body["reasons"])
        self.assertGreater(body["variant_count"], 1)
        log_decision.assert_called_once()

    @patch("app.audit.log_rejection")
    @patch("app.detector.model_signal")
    def test_invalid_input_is_rejected_before_model_work(
        self, model_signal, log_rejection
    ):
        response = self.post("hello")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "unsupported_text")
        model_signal.assert_not_called()
        log_rejection.assert_called_once()
        self.assertEqual(
            log_rejection.call_args.kwargs["route"], "reliability_check"
        )

    @patch("app.audit.log_rejection")
    @patch(
        "app.detector.model_signal",
        side_effect=app_module.detector.DetectorUnavailable(),
    )
    def test_unavailable_detector_returns_503_and_is_logged(
        self, model_signal, log_rejection
    ):
        response = self.post("Enough ordinary words to reach the detector.")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json()["error"], "detector_unavailable")
        log_rejection.assert_called_once()

    @patch("app.stylometry.style_signal", return_value=0.2)
    @patch("app.detector.model_signal", return_value=0.2)
    def test_real_audit_entry_has_measurements_but_not_text(
        self, model_signal, style_signal
    ):
        with TemporaryDirectory() as temp_dir:
            log_dir = Path(temp_dir)
            log_path = log_dir / "audit.jsonl"
            with (
                patch.object(app_module.config, "LOG_DIR", log_dir),
                patch.object(app_module.config, "AUDIT_LOG", log_path),
            ):
                response = self.post("Simple words only.")
                entries = app_module.audit.read_entries()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        required_fields = {
            "timestamp",
            "content_id",
            "creator_id",
            "guess",
            "model_score",
            "style_score",
            "combined_score",
            "label",
            "status",
        }
        self.assertTrue(required_fields.issubset(entry))
        self.assertEqual(entry["event"], "reliability_check")
        self.assertIn("latency_ms", entry)
        self.assertIn("variant_results", entry)
        self.assertNotIn("text", entry["variant_results"][0])


if __name__ == "__main__":
    unittest.main()
