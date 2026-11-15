"""Focused tests for the validation and configuration feedback changes."""

import unittest
from unittest.mock import patch

import app as app_module
import config
import detector


class SubmitValidationTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()
        self.creator_number = 0

    def submit(self, text: str):
        self.creator_number += 1
        return self.client.post(
            "/submit",
            json={
                "creator_id": f"validation_test_{self.creator_number}",
                "text": text,
            },
        )

    @patch("app.audit.log_rejection")
    def test_character_limit_runs_before_language_check(self, log_rejection):
        response = self.submit("x" * (config.MAX_TEXT_CHARACTERS + 1))

        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.get_json()["error"], "text_too_large")
        log_rejection.assert_called_once()

    @patch("app.audit.log_rejection")
    def test_word_limit_is_reachable(self, log_rejection):
        text = "a " * (config.MAX_TEXT_WORDS + 1)
        self.assertLess(len(text), config.MAX_TEXT_CHARACTERS)

        response = self.submit(text)

        self.assertEqual(response.status_code, 413)
        self.assertIn("words", response.get_json()["message"])
        log_rejection.assert_called_once()

    @patch("app.audit.log_rejection")
    def test_unsupported_control_character_is_rejected(self, log_rejection):
        response = self.submit("ordinary words\x00")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "unsupported_text")
        log_rejection.assert_called_once()

    @patch("app.audit.log_rejection")
    def test_minimum_supported_words_is_configured(self, log_rejection):
        response = self.submit("hello")

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            str(config.MIN_LATIN_WORDS),
            response.get_json()["message"],
        )
        log_rejection.assert_called_once()

    @patch("app.audit.log_decision")
    @patch("app.detector.model_signal", return_value=0.4)
    def test_valid_text_still_reaches_scoring(self, model_signal, log_decision):
        response = self.submit(
            "This ordinary paragraph contains enough words for both signals."
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("style_score", response.get_json())
        model_signal.assert_called_once()
        log_decision.assert_called_once()


class ScoringPolicyTests(unittest.TestCase):
    def test_style_weights_sum_to_one(self):
        total = (
            config.STYLE_WEIGHT_SENTENCE_SPREAD
            + config.STYLE_WEIGHT_TYPE_TOKEN_RATIO
            + config.STYLE_WEIGHT_PUNCTUATION_DENSITY
        )
        self.assertAlmostEqual(total, 1.0)

    @patch("detector.perplexity")
    def test_configured_model_midpoint_maps_to_half(self, perplexity):
        perplexity.return_value = config.DETECTOR_PERPLEXITY_MIDPOINT

        self.assertEqual(detector.model_signal("unused by mock"), 0.5)


if __name__ == "__main__":
    unittest.main()
