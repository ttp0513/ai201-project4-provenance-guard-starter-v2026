#!/usr/bin/env python3
"""Score the fixed human and AI calibration texts without using HTTP.

This is a diagnosis tool, not another detector. It calls the two signal
modules directly so a calibration change can be checked without starting the
Flask service, triggering rate limits, or writing submission audit entries.

Examples:

    python run_calibration.py
    python run_calibration.py --offline
    python run_calibration.py --limit 2
    python run_calibration.py --style-only
"""

import argparse
import os
import statistics
import time

import detector
import scoring
import stylometry
from scenarios import SCENARIOS


def scenario_texts(name: str) -> list[str]:
    """Return the fixed texts for one named evaluation scenario."""
    for scenario in SCENARIOS:
        if scenario.get("name") == name:
            return scenario["texts"]
    raise RuntimeError(f"Calibration scenario not found: {name}")


def mean(values: list[float]) -> float:
    """Return a readable average for one group of signal scores."""
    return statistics.mean(values) if values else float("nan")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the two signals directly on the fixed calibration texts."
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Score only this many human and AI texts for a quick check.",
    )
    parser.add_argument(
        "--style-only",
        action="store_true",
        help="Skip the slower local language model and inspect stylometry only.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use only the downloaded model cache and skip network checks.",
    )
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")

    if args.offline:
        # detector.py imports the model libraries lazily, so setting this here
        # prevents Hugging Face network checks while preserving first-run
        # downloads for the normal service and detector.py commands.
        os.environ["HF_HUB_OFFLINE"] = "1"

    groups = {
        "human": scenario_texts("score spread - human writing"),
        "ai": scenario_texts("score spread - AI writing"),
    }
    if args.limit is not None:
        groups = {name: texts[: args.limit] for name, texts in groups.items()}

    results = []
    print("\nOffline calibration (higher score = more AI-like)\n")
    print(f"{'ID':<5} {'Origin':<7} {'Model':>8} {'Style':>8} {'Combined':>10} {'Seconds':>9}")
    print("-" * 54)

    for origin, texts in groups.items():
        for index, text in enumerate(texts, 1):
            started = time.perf_counter()
            style_score = stylometry.style_signal(text)
            model_score = None
            combined_score = None

            if not args.style_only:
                try:
                    model_score = detector.model_signal(text)
                except detector.DetectorUnavailable as exc:
                    print(f"\nDetector unavailable: {exc}")
                    return 1
                combined_score = scoring.combine_signals(model_score, style_score)

            elapsed = time.perf_counter() - started
            sample_id = f"{origin[0].upper()}{index:02d}"
            model_text = f"{model_score:.4f}" if model_score is not None else "skipped"
            combined_text = (
                f"{combined_score:.4f}" if combined_score is not None else "skipped"
            )
            print(
                f"{sample_id:<5} {origin:<7} {model_text:>8} "
                f"{style_score:>8.4f} {combined_text:>10} {elapsed:>9.3f}"
            )
            results.append(
                {
                    "origin": origin,
                    "model": model_score,
                    "style": style_score,
                    "combined": combined_score,
                }
            )

    print("\nGroup averages")
    print("-" * 54)
    for origin in ("human", "ai"):
        group = [result for result in results if result["origin"] == origin]
        style_average = mean([result["style"] for result in group])
        if args.style_only:
            print(f"{origin:<7} style={style_average:.4f}")
            continue

        model_average = mean([result["model"] for result in group])
        combined_average = mean([result["combined"] for result in group])
        print(
            f"{origin:<7} model={model_average:.4f} "
            f"style={style_average:.4f} combined={combined_average:.4f}"
        )

    print("\nSeparation (AI average minus human average; positive is expected)")
    print("-" * 54)
    human = [result for result in results if result["origin"] == "human"]
    ai = [result for result in results if result["origin"] == "ai"]
    signals = ("style",) if args.style_only else ("model", "style", "combined")
    for signal in signals:
        separation = mean([result[signal] for result in ai]) - mean(
            [result[signal] for result in human]
        )
        direction = "expected direction" if separation > 0 else "reversed or tied"
        print(f"{signal:<10} {separation:+.4f}  {direction}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
