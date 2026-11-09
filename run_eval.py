#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])

    # Use the complete scenario name so similarly named scenarios, such as the
    # human and AI score-spread groups, do not share one rate-limit identity.
    scenario_slug = "_".join(scenario["name"].lower().split())
    return [
        {"text": text, "creator_id": f"eval_{scenario_slug}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def read_log_entries(args, requests):
    """Read the public audit endpoint and return its list of entries."""
    response = requests.get(f"{args.url}/log", timeout=args.timeout)
    response.raise_for_status()
    payload = response.json() if response.content else {}
    return payload.get("entries", [])


def rejection_count(entries, creator_id):
    """Count logged rejections belonging to one test caller."""
    return sum(
        entry.get("creator_id") == creator_id
        and entry.get("status") == "rejected"
        for entry in entries
    )


def result_summary(result):
    """Produce one short terminal label for a detailed result dictionary."""
    if result.get("guess"):
        return result["guess"]
    if result.get("appeal_status"):
        return result["appeal_status"]
    if result.get("check"):
        return f"{result['check']}={result.get('status', 'error')}"
    if result.get("status") is not None:
        return f"HTTP {result['status']}"
    return "—"


def run_appeal_scenario(scenario, trial, args, requests):
    """Submit one text, appeal its ID, and confirm both audit entries exist."""
    appeal_case = scenario["appeal"]
    creator_id = f"eval_appeal_trial_{trial}"
    submit_body = {
        "text": appeal_case["text"],
        "creator_id": creator_id,
    }

    try:
        submit_response = requests.post(
            f"{args.url}/submit",
            json=submit_body,
            timeout=args.timeout,
        )
        submit_payload = submit_response.json() if submit_response.content else {}
        content_id = submit_payload.get("content_id")

        result = {
            "submit_status": submit_response.status_code,
            "content_id": content_id,
            "submit_guess": submit_payload.get("guess"),
            "appeal_http_status": None,
            "appeal_status": None,
            "original_decision_preserved": False,
            "appeal_logged": False,
            "matching_log_entries": [],
        }

        # A failed submission cannot be appealed, but its result still belongs
        # in the report so the criterion receives an honest miss.
        if submit_response.status_code != 200 or not content_id:
            result["error"] = "The submission did not return a content_id."
            return result

        appeal_response = requests.post(
            f"{args.url}/appeal",
            json={
                "content_id": content_id,
                "reasoning": appeal_case["reasoning"],
            },
            timeout=args.timeout,
        )
        appeal_payload = appeal_response.json() if appeal_response.content else {}
        result["appeal_http_status"] = appeal_response.status_code
        result["appeal_status"] = appeal_payload.get("status")

        # Read through the public route, just as a reviewer would. This proves
        # the appeal response was not merely returned without being recorded.
        matching_entries = [
            entry for entry in read_log_entries(args, requests)
            if entry.get("content_id") == content_id
        ]
        result["matching_log_entries"] = matching_entries
        result["original_decision_preserved"] = any(
            entry.get("status") == "decided" for entry in matching_entries
        )
        result["appeal_logged"] = any(
            entry.get("event") == "appeal"
            and entry.get("status") == "under_review"
            for entry in matching_entries
        )
        return result
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            results = []
            if scenario.get("appeal"):
                results.append(
                    run_appeal_scenario(scenario, trial, args, requests)
                )
            else:
                for i, body in enumerate(bodies_for(scenario), 1):
                    preview = describe(body)
                    creator_id = body.get("creator_id") if isinstance(body, dict) else None
                    before_rejections = None
                    if scenario.get("check_rejection_log") and creator_id:
                        before_rejections = rejection_count(
                            read_log_entries(args, requests),
                            creator_id,
                        )
                    try:
                        response = requests.post(f"{args.url}/submit", json=body,
                                                 timeout=args.timeout)
                        payload = response.json() if response.content else {}
                        result = {
                            "status": response.status_code,
                            "guess": payload.get("guess"),
                            "confidence": payload.get("confidence"),
                            "model_score": payload.get("model_score"),
                            "style_score": payload.get("style_score"),
                            "label": payload.get("label"),
                            "error": payload.get("error"),
                            "sent": preview,
                        }
                        if before_rejections is not None:
                            after_rejections = rejection_count(
                                read_log_entries(args, requests),
                                creator_id,
                            )
                            result["rejection_logged"] = (
                                after_rejections > before_rejections
                            )
                        results.append(result)
                    except Exception as exc:  # noqa: BLE001
                        results.append({
                            "status": None,
                            "error": f"{type(exc).__name__}: {exc}",
                            "sent": preview,
                        })

                if scenario.get("check_health"):
                    try:
                        health_response = requests.get(
                            f"{args.url}/health",
                            timeout=args.timeout,
                        )
                        health_payload = (
                            health_response.json() if health_response.content else {}
                        )
                        results.append({
                            "check": "health_after_trial",
                            "status": health_response.status_code,
                            "ok": health_payload.get("ok"),
                        })
                    except Exception as exc:  # noqa: BLE001
                        results.append({
                            "check": "health_after_trial",
                            "status": None,
                            "error": f"{type(exc).__name__}: {exc}",
                        })

            trials.append(results)
            summaries = [result_summary(result) for result in results]
            print(f"  trial {trial}: {', '.join(summaries)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
