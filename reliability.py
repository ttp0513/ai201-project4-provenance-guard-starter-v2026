"""Measure whether Provenance Guard gives a stable answer.

This module does not decide whether writing is human or AI. It asks a narrower
question: does the existing decision stay similar after small formatting
changes that preserve the words and their order?

The scoring function is passed in by the caller. This keeps the reliability
logic independent from Flask and lets unit tests use a small fake scorer
instead of loading GPT-2.
"""

from __future__ import annotations

import re
import string
from collections.abc import Callable

import config


ScoreResult = dict[str, float | str]
Scorer = Callable[[str], ScoreResult]

# Replace typographic characters with common plain-text forms. This changes
# formatting, not the words or their order.
PUNCTUATION_TRANSLATION = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
)

# Keep sentence-ending marks and apostrophes. Remove punctuation that often
# changes during copy, paste, or light editing while preserving word order.
LIGHT_PUNCTUATION_TO_REMOVE = "".join(
    character
    for character in string.punctuation
    if character not in ".?!'"
)
LIGHT_PUNCTUATION_TRANSLATION = str.maketrans(
    {character: " " for character in LIGHT_PUNCTUATION_TO_REMOVE}
)


def _normalize_whitespace(text: str) -> str:
    """Collapse spaces, tabs, and line breaks into single spaces."""

    return re.sub(r"\s+", " ", text).strip()


def _standardize_punctuation(text: str) -> str:
    """Convert common Unicode punctuation to plain-text equivalents."""

    return text.translate(PUNCTUATION_TRANSLATION)


def _reduce_punctuation(text: str) -> str:
    """Remove non-terminal punctuation without changing word order."""

    standardized = _standardize_punctuation(text)
    reduced = standardized.translate(LIGHT_PUNCTUATION_TRANSLATION)
    return _normalize_whitespace(reduced)


def make_variants(text: str) -> list[dict[str, str]]:
    """Return deterministic, unique versions of the same wording.

    Some text already has simple spacing and punctuation. Duplicate variants
    are removed so the service does not pay for the same model call twice.
    The original text is always first and is never modified.
    """

    candidates = [
        ("original", text),
        ("normalized_whitespace", _normalize_whitespace(text)),
        ("standardized_punctuation", _standardize_punctuation(text)),
        ("punctuation_light", _reduce_punctuation(text)),
    ]

    variants: list[dict[str, str]] = []
    seen_text: set[str] = set()
    for name, variant_text in candidates:
        if variant_text in seen_text:
            continue
        seen_text.add(variant_text)
        variants.append({"name": name, "text": variant_text})
    return variants


def _validate_result(result: ScoreResult) -> None:
    """Reject incomplete scorer output before producing false stability."""

    required = {
        "model_score",
        "style_score",
        "combined_score",
        "guess",
        "label",
    }
    missing = required.difference(result)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"scorer result is missing: {names}")

    for key in ("model_score", "style_score", "combined_score"):
        value = result[key]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{key} must be a number")
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"{key} must be between 0.0 and 1.0")

    if result["guess"] not in {"human", "unsure", "ai"}:
        raise ValueError("guess must be human, unsure, or ai")


def assess_results(variant_results: list[dict]) -> dict:
    """Calculate stability measurements and the guarded final decision."""

    if not variant_results:
        raise ValueError("at least one variant result is required")

    combined_scores = [float(item["combined_score"]) for item in variant_results]
    guesses = {str(item["guess"]) for item in variant_results}
    disagreements = [
        abs(float(item["model_score"]) - float(item["style_score"]))
        for item in variant_results
    ]

    score_range = round(max(combined_scores) - min(combined_scores), 4)
    max_signal_disagreement = round(max(disagreements), 4)
    label_changed = len(guesses) > 1

    reasons: list[str] = []
    if label_changed:
        reasons.append("label_changed")
    if score_range >= config.RELIABILITY_MAX_SCORE_RANGE:
        reasons.append("large_score_range")
    if max_signal_disagreement >= config.RELIABILITY_MAX_SIGNAL_DISAGREEMENT:
        reasons.append("signals_disagree")

    unstable = bool(reasons)
    original = variant_results[0]
    if unstable:
        final_guess = "unsure"
        final_label = (
            "The detector was not stable across the reliability checks, so "
            "this result needs human review."
        )
    else:
        final_guess = str(original["guess"])
        final_label = str(original["label"])
        reasons.append("stable_across_variants")

    # Existing AI and unsure decisions already require review. The reliability
    # guard also routes any newly unstable result to review.
    human_review = unstable or final_guess != "human"

    return {
        "stability": "unstable" if unstable else "stable",
        "score_range": score_range,
        "label_changed": label_changed,
        "max_signal_disagreement": max_signal_disagreement,
        "final_guess": final_guess,
        "final_label": final_label,
        "human_review": human_review,
        "reasons": reasons,
    }


def analyze(text: str, scorer: Scorer) -> dict:
    """Score each unique variant and return the reliability assessment."""

    variant_results = []
    for variant in make_variants(text):
        score_result = scorer(variant["text"])
        _validate_result(score_result)
        variant_results.append(
            {
                "name": variant["name"],
                "text": variant["text"],
                "model_score": round(float(score_result["model_score"]), 4),
                "style_score": round(float(score_result["style_score"]), 4),
                "combined_score": round(float(score_result["combined_score"]), 4),
                "guess": str(score_result["guess"]),
                "label": str(score_result["label"]),
            }
        )

    assessment = assess_results(variant_results)
    return {
        "original_result": variant_results[0],
        "variant_results": variant_results,
        "variant_count": len(variant_results),
        **assessment,
    }
