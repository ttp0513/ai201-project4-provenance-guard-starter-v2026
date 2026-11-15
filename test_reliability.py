"""Unit tests for the capstone reliability engine."""

import re
import unittest

import reliability


def result(model, style, combined, guess):
    """Create a complete fake scorer result for a unit test."""

    return {
        "model_score": model,
        "style_score": style,
        "combined_score": combined,
        "guess": guess,
        "label": f"{guess} test label",
    }


class VariantTests(unittest.TestCase):
    def test_variants_are_deterministic_and_keep_word_order(self):
        text = "The  service—despite delays,\nworked well."

        first = reliability.make_variants(text)
        second = reliability.make_variants(text)

        self.assertEqual(first, second)
        self.assertEqual(first[0], {"name": "original", "text": text})
        self.assertEqual(len({item["text"] for item in first}), len(first))

        original_words = re.findall(r"[A-Za-z]+", text.lower())
        for variant in first:
            self.assertEqual(
                re.findall(r"[A-Za-z]+", variant["text"].lower()),
                original_words,
            )

    def test_duplicate_variants_are_scored_once(self):
        calls = []

        def scorer(text):
            calls.append(text)
            return result(0.2, 0.2, 0.2, "human")

        analysis = reliability.analyze("Simple words only.", scorer)

        self.assertEqual(analysis["variant_count"], 1)
        self.assertEqual(len(calls), 1)


class ReliabilityAssessmentTests(unittest.TestCase):
    def test_stable_scores_keep_the_original_label(self):
        analysis = reliability.analyze(
            "A plain sentence with ordinary words.",
            lambda text: result(0.2, 0.2, 0.2, "human"),
        )

        self.assertEqual(analysis["stability"], "stable")
        self.assertEqual(analysis["final_guess"], "human")
        self.assertFalse(analysis["human_review"])
        self.assertEqual(analysis["reasons"], ["stable_across_variants"])

    def test_label_change_forces_unsure(self):
        def scorer(text):
            if "," in text:
                return result(0.8, 0.8, 0.8, "ai")
            return result(0.2, 0.2, 0.2, "human")

        analysis = reliability.analyze(
            "Clear wording, with removable punctuation.", scorer
        )

        self.assertTrue(analysis["label_changed"])
        self.assertEqual(analysis["final_guess"], "unsure")
        self.assertTrue(analysis["human_review"])
        self.assertIn("label_changed", analysis["reasons"])

    def test_large_score_range_is_reported_without_a_label_change(self):
        def scorer(text):
            score = 0.34 if "," in text else 0.10
            return result(score, score, score, "human")

        analysis = reliability.analyze(
            "Clear wording, with removable punctuation.", scorer
        )

        self.assertFalse(analysis["label_changed"])
        self.assertEqual(analysis["score_range"], 0.24)
        self.assertIn("large_score_range", analysis["reasons"])
        self.assertEqual(analysis["final_guess"], "unsure")

    def test_signal_disagreement_is_reported(self):
        analysis = reliability.analyze(
            "Simple words only.",
            lambda text: result(0.9, 0.2, 0.55, "unsure"),
        )

        self.assertEqual(analysis["max_signal_disagreement"], 0.7)
        self.assertIn("signals_disagree", analysis["reasons"])
        self.assertTrue(analysis["human_review"])

    def test_incomplete_scorer_result_fails_visibly(self):
        with self.assertRaisesRegex(ValueError, "style_score"):
            reliability.analyze(
                "Simple words only.",
                lambda text: {"model_score": 0.2},
            )


if __name__ == "__main__":
    unittest.main()
