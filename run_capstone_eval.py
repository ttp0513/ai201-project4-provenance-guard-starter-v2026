#!/usr/bin/env python3
"""Run all five capstone criteria three times without changing the system.

Start the service first, then run:

    python run_capstone_eval.py

The command makes one warm-up request, runs the same ten scenarios in each of
three trials, retrieves the matching audit entries, and writes the complete
evidence under results/. A missed criterion is a valid result, not a script
error.
"""

from __future__ import annotations

import json
import re
import statistics
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests

import config
from run_reliability_session import BASE_URL, CASES, fetch_json


ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
JSON_OUTPUT = RESULTS_DIR / "capstone_criteria_results.json"
LOG_OUTPUT = RESULTS_DIR / "capstone_criteria_log.jsonl"
REPORT_OUTPUT = RESULTS_DIR / "capstone_criteria_report.md"
TRIAL_COUNT = 3
VARIANT_CASE_COUNT = 5


def latin_words(text: str) -> list[str]:
    """Return the ordered words used to verify meaning-preserving variants."""

    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())


def contains_text_key(value) -> bool:
    """Find a raw text field anywhere inside a structured log entry."""

    if isinstance(value, dict):
        return any(
            key == "text" or contains_text_key(child)
            for key, child in value.items()
        )
    if isinstance(value, list):
        return any(contains_text_key(child) for child in value)
    return False


def expected_instability_reasons(body: dict) -> set[str]:
    """Recalculate the guard conditions independently from route reason codes."""

    variants = body.get("variant_results", [])
    if not variants:
        return set()

    guesses = {item["guess"] for item in variants}
    scores = [float(item["combined_score"]) for item in variants]
    disagreements = [
        abs(float(item["model_score"]) - float(item["style_score"]))
        for item in variants
    ]

    reasons = set()
    if len(guesses) > 1:
        reasons.add("label_changed")
    if round(max(scores) - min(scores), 4) >= config.RELIABILITY_MAX_SCORE_RANGE:
        reasons.add("large_score_range")
    firm_label_consensus = len(guesses) == 1 and guesses.issubset({"human", "ai"})
    if (
        round(max(disagreements), 4)
        >= config.RELIABILITY_MAX_SIGNAL_DISAGREEMENT
        and not firm_label_consensus
    ):
        reasons.add("signals_disagree")
    return reasons


def run_live_trials() -> tuple[dict, list[dict]]:
    """Warm the model, then make the same ten requests in three trials."""

    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=15)
        health_response.raise_for_status()
        health = fetch_json(health_response)
    except requests.RequestException as exc:
        raise RuntimeError(
            "Nothing answered. Start the service with "
            r".\.venv\Scripts\python.exe app.py"
        ) from exc

    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    warmup_payload = {
        "creator_id": f"capstone_criteria_warmup_{run_stamp}",
        "text": "The warm-up request loads the local model before measured trials.",
    }
    warmup_response = requests.post(
        f"{BASE_URL}/reliability-check",
        json=warmup_payload,
        timeout=300,
    )
    if warmup_response.status_code != 200:
        raise RuntimeError(
            f"Warm-up failed with HTTP {warmup_response.status_code}: "
            f"{fetch_json(warmup_response)}"
        )

    trials = []
    content_ids = set()
    for trial_number in range(1, TRIAL_COUNT + 1):
        responses = []
        for case_id, text in CASES:
            payload = {
                "creator_id": f"capstone_criteria_t{trial_number}_{case_id}_{run_stamp}",
                "text": text,
            }
            wall_started = time.perf_counter()
            response = requests.post(
                f"{BASE_URL}/reliability-check",
                json=payload,
                timeout=300,
            )
            wall_latency_ms = round((time.perf_counter() - wall_started) * 1000, 2)
            body = fetch_json(response)
            content_id = body.get("content_id")
            if isinstance(content_id, str):
                content_ids.add(content_id)
            responses.append(
                {
                    "case_id": case_id,
                    "status_code": response.status_code,
                    "wall_latency_ms": wall_latency_ms,
                    "body": body,
                }
            )
            print(
                f"trial {trial_number} {case_id}: HTTP {response.status_code}, "
                f"{body.get('stability', body.get('error', 'unknown'))}, "
                f"{body.get('latency_ms', 'n.a.')} ms server"
            )
        trials.append({"trial": trial_number, "responses": responses})

    log_response = requests.get(f"{BASE_URL}/log?limit=5000", timeout=30)
    log_response.raise_for_status()
    all_logs = fetch_json(log_response).get("entries", [])
    matching_logs = [
        entry for entry in all_logs if entry.get("content_id") in content_ids
    ]
    return {
        "started_at": run_stamp,
        "base_url": BASE_URL,
        "health_before_warmup": health,
        "warmup_status": warmup_response.status_code,
        "trial_count": TRIAL_COUNT,
        "case_count_per_trial": len(CASES),
        "trials": trials,
    }, matching_logs


def evaluate_criterion_1(trials: list[dict]) -> dict:
    """Check deterministic, unique, wording-preserving variants."""

    baseline = {}
    trial_details = []
    total_passed = 0
    for trial in trials:
        passed = 0
        cases = []
        for response in trial["responses"][:VARIANT_CASE_COUNT]:
            body = response["body"]
            variants = body.get("variant_results", [])
            pairs = [(item.get("name"), item.get("text")) for item in variants]
            texts = [item.get("text", "") for item in variants]
            original_words = latin_words(texts[0]) if texts else []
            wording_preserved = bool(texts) and all(
                latin_words(text) == original_words for text in texts
            )
            no_duplicates = len(texts) == len(set(texts))
            case_id = response["case_id"]
            if trial["trial"] == 1:
                baseline[case_id] = pairs
            deterministic = pairs == baseline.get(case_id)
            case_passed = (
                response["status_code"] == 200
                and wording_preserved
                and no_duplicates
                and deterministic
            )
            passed += int(case_passed)
            cases.append(
                {
                    "case_id": case_id,
                    "passed": case_passed,
                    "wording_preserved": wording_preserved,
                    "no_duplicates": no_duplicates,
                    "deterministic": deterministic,
                    "variant_names": [name for name, _ in pairs],
                }
            )
        total_passed += passed
        trial_details.append(
            {"trial": trial["trial"], "passed": passed, "total": 5, "cases": cases}
        )
    return {
        "target": "15/15 cases",
        "trial_details": trial_details,
        "total_passed": total_passed,
        "total": 15,
        "verdict": "MET" if total_passed == 15 else "MISSED",
    }


def evaluate_criterion_2(trials: list[dict]) -> dict:
    """Check reason coverage and cautious handling of every unstable result."""

    required_coverage = {"label_changed", "large_score_range", "signals_disagree"}
    trial_details = []
    all_trials_passed = True
    for trial in trials:
        coverage = set()
        unstable_cases = 0
        handled_cases = 0
        examples = {}
        for response in trial["responses"]:
            body = response["body"]
            expected = expected_instability_reasons(body)
            if not expected:
                continue
            unstable_cases += 1
            coverage.update(expected)
            for reason in expected:
                examples.setdefault(reason, response["case_id"])
            actual = set(body.get("reasons", []))
            handled = (
                response["status_code"] == 200
                and body.get("stability") == "unstable"
                and body.get("guess") == "unsure"
                and body.get("human_review") is True
                and expected.issubset(actual)
            )
            handled_cases += int(handled)
        trial_passed = coverage == required_coverage and handled_cases == unstable_cases
        all_trials_passed = all_trials_passed and trial_passed
        trial_details.append(
            {
                "trial": trial["trial"],
                "coverage": sorted(coverage),
                "coverage_count": len(coverage),
                "handled_cases": handled_cases,
                "unstable_cases": unstable_cases,
                "examples": examples,
                "passed": trial_passed,
            }
        )
    return {
        "target": "3/3 reasons covered and 100% unstable cases handled in every trial",
        "trial_details": trial_details,
        "verdict": "MET" if all_trials_passed else "MISSED",
    }


def evaluate_criterion_3(trials: list[dict]) -> dict:
    """Check that the guard retains some stable, non-unsure coverage."""

    trial_details = []
    all_trials_passed = True
    for trial in trials:
        stable = [
            response
            for response in trial["responses"]
            if response["body"].get("stability") == "stable"
        ]
        stable_non_unsure = [
            response
            for response in stable
            if response["body"].get("guess") in {"human", "ai"}
        ]
        preserved = all(
            response["body"].get("guess")
            == response["body"].get("original_result", {}).get("guess")
            for response in stable
        )
        trial_passed = len(stable) >= 3 and len(stable_non_unsure) >= 1 and preserved
        all_trials_passed = all_trials_passed and trial_passed
        trial_details.append(
            {
                "trial": trial["trial"],
                "stable_count": len(stable),
                "stable_non_unsure_count": len(stable_non_unsure),
                "stable_guesses_preserved": preserved,
                "passed": trial_passed,
            }
        )
    return {
        "target": "at least 3 stable and 1 stable non-unsure case per trial",
        "trial_details": trial_details,
        "verdict": "MET" if all_trials_passed else "MISSED",
    }


def evaluate_criterion_4(trials: list[dict], logs: list[dict]) -> dict:
    """Check one complete, privacy-preserving audit entry per response."""

    required_fields = {
        "timestamp",
        "content_id",
        "creator_id",
        "input_sha256",
        "input_characters",
        "input_words",
        "model_score",
        "style_score",
        "combined_score",
        "original_guess",
        "guess",
        "stability",
        "reasons",
        "variant_count",
        "model_calls",
        "latency_ms",
        "label",
        "status",
    }
    by_content_id = Counter(entry.get("content_id") for entry in logs)
    logs_by_id = {entry.get("content_id"): entry for entry in logs}
    trial_details = []
    total_passed = 0
    for trial in trials:
        passed = 0
        for response in trial["responses"]:
            content_id = response["body"].get("content_id")
            entry = logs_by_id.get(content_id, {})
            case_passed = (
                by_content_id[content_id] == 1
                and required_fields.issubset(entry)
                and not contains_text_key(entry)
            )
            passed += int(case_passed)
        total_passed += passed
        trial_details.append(
            {"trial": trial["trial"], "passed": passed, "total": 10}
        )
    return {
        "target": "30/30 complete entries with no text fields",
        "trial_details": trial_details,
        "matching_log_entries": len(logs),
        "total_passed": total_passed,
        "total": 30,
        "verdict": "MET" if total_passed == 30 and len(logs) == 30 else "MISSED",
    }


def evaluate_criterion_5(trials: list[dict]) -> dict:
    """Check warm latency and bounded model calls."""

    trial_details = []
    total_passed = 0
    all_latencies = []
    for trial in trials:
        passed = 0
        latencies = []
        for response in trial["responses"]:
            body = response["body"]
            latency = body.get("latency_ms")
            model_calls = body.get("model_calls")
            variant_count = body.get("variant_count")
            if isinstance(latency, (int, float)):
                latencies.append(float(latency))
                all_latencies.append(float(latency))
            case_passed = (
                response["status_code"] == 200
                and isinstance(latency, (int, float))
                and float(latency) < 500
                and isinstance(model_calls, int)
                and 1 <= model_calls <= 4
                and model_calls == variant_count
            )
            passed += int(case_passed)
        total_passed += passed
        trial_details.append(
            {
                "trial": trial["trial"],
                "passed": passed,
                "total": 10,
                "average_latency_ms": round(statistics.mean(latencies), 2),
                "maximum_latency_ms": round(max(latencies), 2),
            }
        )
    return {
        "target": "30/30 under 500 ms with 1-4 calls matching variant count",
        "trial_details": trial_details,
        "total_passed": total_passed,
        "total": 30,
        "hosted_inference_api_calls": 0,
        "average_latency_ms": round(statistics.mean(all_latencies), 2),
        "maximum_latency_ms": round(max(all_latencies), 2),
        "verdict": "MET" if total_passed == 30 else "MISSED",
    }


def format_trial_cell(criterion_number: int, detail: dict) -> str:
    """Keep the report table compact while preserving the measured number."""

    if criterion_number == 1:
        return f"{detail['passed']}/{detail['total']}"
    if criterion_number == 2:
        return (
            f"reasons {detail['coverage_count']}/3; handling "
            f"{detail['handled_cases']}/{detail['unstable_cases']}"
        )
    if criterion_number == 3:
        return (
            f"stable {detail['stable_count']}; non-unsure "
            f"{detail['stable_non_unsure_count']}"
        )
    if criterion_number == 4:
        return f"{detail['passed']}/{detail['total']}"
    return (
        f"{detail['passed']}/{detail['total']}; max "
        f"{detail['maximum_latency_ms']:.2f} ms"
    )


def write_evidence(run: dict, logs: list[dict], criteria: dict) -> None:
    """Write full machine-readable results and a readable five-row report."""

    RESULTS_DIR.mkdir(exist_ok=True)
    full_result = {**run, "criteria": criteria}
    JSON_OUTPUT.write_text(
        json.dumps(full_result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    LOG_OUTPUT.write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in logs),
        encoding="utf-8",
    )

    names = {
        1: "Variants preserve wording",
        2: "Instability forces unsure",
        3: "Useful classifications remain",
        4: "Complete private audit entries",
        5: "Warm latency and calls bounded",
    }
    lines = [
        "# Capstone Criteria Run",
        "",
        f"- Started: `{run['started_at']}`",
        f"- Trials: `{TRIAL_COUNT}`",
        f"- Same scenarios per trial: `{len(CASES)}`",
        "- System changes between trials: `none`",
        "",
        "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for number in range(1, 6):
        criterion = criteria[str(number)]
        cells = [
            format_trial_cell(number, detail)
            for detail in criterion["trial_details"]
        ]
        lines.append(
            f"| {number}. {names[number]} | {criterion['target']} | "
            f"{cells[0]} | {cells[1]} | {cells[2]} | {criterion['verdict']} |"
        )

    # Paste actual JSON from trial 1 for each criterion, not a description.
    trial_one = run["trials"][0]["responses"]
    response_by_case = {item["case_id"]: item for item in trial_one}
    log_by_id = {entry.get("content_id"): entry for entry in logs}
    examples = {
        1: {
            "case_id": "case_03_unicode",
            "variant_results": response_by_case["case_03_unicode"]["body"].get(
                "variant_results"
            ),
        },
        2: response_by_case["case_04_whitespace"]["body"],
        3: {
            "case_id": "case_02_comma",
            "stability": response_by_case["case_02_comma"]["body"].get("stability"),
            "original_guess": response_by_case["case_02_comma"]["body"]
            .get("original_result", {})
            .get("guess"),
            "final_guess": response_by_case["case_02_comma"]["body"].get("guess"),
        },
        4: log_by_id.get(response_by_case["case_01_plain"]["body"].get("content_id")),
        5: {
            "case_id": "case_02_comma",
            "latency_ms": response_by_case["case_02_comma"]["body"].get("latency_ms"),
            "model_calls": response_by_case["case_02_comma"]["body"].get(
                "model_calls"
            ),
            "variant_count": response_by_case["case_02_comma"]["body"].get(
                "variant_count"
            ),
        },
    }

    lines.extend(["", "## Actual Output From Run 1", ""])
    for number in range(1, 6):
        lines.extend(
            [
                f"### Criterion {number}",
                "",
                "```json",
                json.dumps(examples[number], indent=2, ensure_ascii=False),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Producer",
            "",
            "`run_capstone_eval.py::main` sent the requests. The five",
            "`evaluate_criterion_*` functions calculated the verdicts.",
            "",
        ]
    )
    REPORT_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    try:
        run, logs = run_live_trials()
    except (requests.RequestException, RuntimeError) as exc:
        print(f"Evaluation could not run: {exc}")
        return 1

    criteria = {
        "1": evaluate_criterion_1(run["trials"]),
        "2": evaluate_criterion_2(run["trials"]),
        "3": evaluate_criterion_3(run["trials"]),
        "4": evaluate_criterion_4(run["trials"], logs),
        "5": evaluate_criterion_5(run["trials"]),
    }
    write_evidence(run, logs, criteria)

    print("\nCriterion verdicts")
    for number in range(1, 6):
        print(f"  {number}: {criteria[str(number)]['verdict']}")
    print(f"Saved full results to {JSON_OUTPUT}")
    print(f"Saved {len(logs)} matching log entries to {LOG_OUTPUT}")
    print(f"Saved report to {REPORT_OUTPUT}")

    if len(logs) != TRIAL_COUNT * len(CASES):
        print("The run finished, but the matching log is incomplete.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
