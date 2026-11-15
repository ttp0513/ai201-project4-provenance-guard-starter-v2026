#!/usr/bin/env python3
"""Run the ten-case Milestone 3 reliability session against the live service.

Start the service in another terminal, then run:

    python run_reliability_session.py

The script saves the matching structured audit entries and a short cost
summary under results/. Submitted text is not copied into either output file.
"""

from __future__ import annotations

import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


BASE_URL = os.getenv("AI201_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
LOG_OUTPUT = RESULTS_DIR / "capstone_milestone3_log.jsonl"
SUMMARY_OUTPUT = RESULTS_DIR / "capstone_milestone3_summary.md"

# These cases test formatting sensitivity, not known human/AI authorship.
# Each creator_id is unique so the normal per-caller rate limit does not turn
# this instrumentation run into a rate-limit test.
CASES = [
    ("case_01_plain", "The service worked exactly as expected"),
    (
        "case_02_comma",
        "The checkout was quick, but the return instructions were difficult to find.",
    ),
    (
        "case_03_unicode",
        "The editor called it “helpful”—although the first explanation was unclear.",
    ),
    (
        "case_04_whitespace",
        "Customer support answered quickly.\n\nThe second response was more useful.",
    ),
    (
        "case_05_semicolon",
        "The product arrived on time; however, the package (and one label) was damaged.",
    ),
    (
        "case_06_quotes",
        "I don't agree with the message, 'Everything was perfect,' because I waited an hour.",
    ),
    (
        "case_07_hyphen",
        "The self-service page was easy-to-use, but the confirmation email arrived late.",
    ),
    ("case_08_short", "Good service, slow delivery."),
    (
        "case_09_formal",
        "The revised procedure improved the clarity of the instructions and reduced unnecessary repetition.",
    ),
    (
        "case_10_informal",
        "I liked it overall, but the app was kinda confusing and I had to try twice.",
    ),
]


def fetch_json(response: requests.Response) -> dict:
    """Return a JSON object or a readable fallback for a non-JSON response."""

    try:
        body = response.json()
    except requests.JSONDecodeError:
        return {"error": "non_json_response", "message": response.text[:300]}
    return body if isinstance(body, dict) else {"response": body}


def write_outputs(started_at: str, health: dict, runs: list[dict], logs: list[dict]) -> None:
    """Save the structured run record and measured local cost summary."""

    RESULTS_DIR.mkdir(exist_ok=True)
    LOG_OUTPUT.write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in logs),
        encoding="utf-8",
    )

    successes = [run for run in runs if run["status_code"] == 200]
    server_latencies = [float(run["latency_ms"]) for run in successes]
    wall_latencies = [float(run["wall_latency_ms"]) for run in runs]
    total_model_calls = sum(int(run.get("model_calls", 0)) for run in successes)

    lines = [
        "# Capstone Milestone 3 Run",
        "",
        f"- Started: `{started_at}`",
        f"- Service: `{BASE_URL}`",
        f"- Model: `{health.get('detector_model', 'unknown')}`",
        f"- Detector loaded before run: `{health.get('detector_loaded', False)}`",
        f"- Cases attempted: `{len(runs)}`",
        f"- Successful cases: `{len(successes)}`",
        "",
        "## Results",
        "",
        "| Case | HTTP | Stability | Final guess | Model calls | Server latency (ms) | Reasons |",
        "| --- | ---: | --- | --- | ---: | ---: | --- |",
    ]
    for run in runs:
        reasons = ", ".join(run.get("reasons", [])) or run.get("error", "")
        lines.append(
            f"| {run['case_id']} | {run['status_code']} | "
            f"{run.get('stability', '')} | {run.get('guess', '')} | "
            f"{run.get('model_calls', 0)} | {run.get('latency_ms', '')} | "
            f"{reasons} |"
        )

    lines.extend(
        [
            "",
            "## Measured Cost",
            "",
            f"- Total local model calls: `{total_model_calls}`",
            f"- Total wall time: `{sum(wall_latencies) / 1000:.2f} seconds`",
            f"- Average server latency: `{statistics.mean(server_latencies):.2f} ms`"
            if server_latencies
            else "- Average server latency: `not available`",
            f"- Maximum server latency: `{max(server_latencies):.2f} ms`"
            if server_latencies
            else "- Maximum server latency: `not available`",
            "- Hosted API calls: `0`",
            "- Hosted API charge: `$0.00`",
            "",
            "Cost is measured as wall-clock latency and local GPT-2 calls because",
            "the service runs on the student's computer and does not call a paid API.",
            "The first request may include model-loading time.",
            "",
            "## Structured Log",
            "",
            f"The `{LOG_OUTPUT.name}` file contains the {len(logs)} matching audit entries.",
            "It stores input hashes and counts instead of submitted text.",
            "",
        ]
    )
    SUMMARY_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"Checking {BASE_URL}/health")
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=15)
        health_response.raise_for_status()
        health = fetch_json(health_response)
    except requests.RequestException as exc:
        print("Nothing answered. Start the service in another terminal:")
        print(r"  .\.venv\Scripts\python.exe app.py")
        print(f"Connection error: {exc}")
        return 1

    runs = []
    content_ids = set()
    for case_id, text in CASES:
        payload = {"creator_id": f"capstone_m3_{case_id}", "text": text}
        wall_started = time.perf_counter()
        try:
            response = requests.post(
                f"{BASE_URL}/reliability-check",
                json=payload,
                timeout=300,
            )
            wall_latency_ms = round((time.perf_counter() - wall_started) * 1000, 2)
            body = fetch_json(response)
        except requests.RequestException as exc:
            wall_latency_ms = round((time.perf_counter() - wall_started) * 1000, 2)
            response = None
            body = {"error": "request_failed", "message": str(exc)}

        status_code = response.status_code if response is not None else 0
        content_id = body.get("content_id")
        if isinstance(content_id, str):
            content_ids.add(content_id)
        run = {
            "case_id": case_id,
            "status_code": status_code,
            "content_id": content_id,
            "stability": body.get("stability"),
            "guess": body.get("guess"),
            "model_calls": body.get("model_calls", 0),
            "latency_ms": body.get("latency_ms"),
            "wall_latency_ms": wall_latency_ms,
            "reasons": body.get("reasons", []),
            "error": body.get("error"),
        }
        runs.append(run)
        print(
            f"{case_id}: HTTP {status_code}, "
            f"{run.get('stability') or run.get('error')}, "
            f"{wall_latency_ms:.2f} ms wall time"
        )

    try:
        log_response = requests.get(f"{BASE_URL}/log?limit=5000", timeout=30)
        log_response.raise_for_status()
        all_entries = fetch_json(log_response).get("entries", [])
    except requests.RequestException as exc:
        print(f"Could not retrieve the audit log: {exc}")
        return 1

    matching_logs = [
        entry for entry in all_entries if entry.get("content_id") in content_ids
    ]
    write_outputs(started_at, health, runs, matching_logs)
    print(f"Saved {len(matching_logs)} entries to {LOG_OUTPUT}")
    print(f"Saved cost summary to {SUMMARY_OUTPUT}")

    if len(matching_logs) != len(CASES):
        print(
            f"Expected {len(CASES)} successful log entries but found "
            f"{len(matching_logs)}. Read the summary before continuing."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
