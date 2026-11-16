"""Focused tests for the capstone criterion calculations."""

import unittest

import run_capstone_eval as capstone_eval


class CapstoneEvaluationTests(unittest.TestCase):
    def test_expected_reasons_are_recomputed_from_variant_scores(self):
        body = {
            "variant_results": [
                {
                    "guess": "ai",
                    "combined_score": 0.8,
                    "model_score": 0.9,
                    "style_score": 0.2,
                },
                {
                    "guess": "human",
                    "combined_score": 0.2,
                    "model_score": 0.2,
                    "style_score": 0.2,
                },
            ]
        }

        self.assertEqual(
            capstone_eval.expected_instability_reasons(body),
            {"label_changed", "large_score_range", "signals_disagree"},
        )

    def test_firm_consensus_is_not_counted_as_signal_instability(self):
        body = {
            "variant_results": [
                {
                    "guess": "human",
                    "combined_score": 0.30,
                    "model_score": 0.05,
                    "style_score": 0.55,
                }
            ]
        }

        self.assertEqual(capstone_eval.expected_instability_reasons(body), set())

    def test_nested_raw_text_field_is_detected(self):
        self.assertTrue(
            capstone_eval.contains_text_key(
                {"variant_results": [{"name": "original", "text": "private"}]}
            )
        )
        self.assertFalse(
            capstone_eval.contains_text_key(
                {"variant_results": [{"name": "original", "combined_score": 0.4}]}
            )
        )

    def test_usefulness_criterion_misses_all_unsure_results(self):
        trials = []
        for number in range(1, 4):
            responses = []
            for index in range(10):
                responses.append(
                    {
                        "body": {
                            "stability": "stable" if index < 3 else "unstable",
                            "guess": "unsure",
                            "original_result": {"guess": "unsure"},
                        }
                    }
                )
            trials.append({"trial": number, "responses": responses})

        result = capstone_eval.evaluate_criterion_3(trials)

        self.assertEqual(result["verdict"], "MISSED")
        self.assertEqual(result["trial_details"][0]["stable_count"], 3)
        self.assertEqual(
            result["trial_details"][0]["stable_non_unsure_count"], 0
        )

    def test_latency_criterion_checks_calls_and_variant_count(self):
        trials = []
        for number in range(1, 4):
            responses = [
                {
                    "status_code": 200,
                    "body": {
                        "latency_ms": 50.0,
                        "model_calls": 2,
                        "variant_count": 2,
                    },
                }
                for _ in range(10)
            ]
            trials.append({"trial": number, "responses": responses})

        result = capstone_eval.evaluate_criterion_5(trials)

        self.assertEqual(result["verdict"], "MET")
        self.assertEqual(result["total_passed"], 30)


if __name__ == "__main__":
    unittest.main()
