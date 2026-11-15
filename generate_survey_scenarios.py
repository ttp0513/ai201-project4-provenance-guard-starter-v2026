"""Generate the synthetic Qualtrics-style capstone data.

The export intentionally keeps evaluation labels in a separate file. This
prevents the future risk scorer from reading the expected answer as an input.
Run from the repository root with:

    python generate_survey_scenarios.py
"""

from __future__ import annotations

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent / "capstone_data"
EXPORT_PATH = OUTPUT_DIR / "qualtrics_synthetic_export.csv"
LABELS_PATH = OUTPUT_DIR / "qualtrics_synthetic_labels.csv"

FIELDS = [
    "StartDate",
    "EndDate",
    "Status",
    "Progress",
    "Duration (in seconds)",
    "Finished",
    "RecordedDate",
    "ResponseId",
    "ExternalReference",
    "DistributionChannel",
    "UserLanguage",
    "Q2_TEXT",
    "Q_RecaptchaScore",
    "Q_RecaptchaStatus",
    "Q_RecaptchaError",
    "Q_BallotBoxStuffing",
    "Q_PrivateBrowserDetected",
    "Q_DuplicateRespondent",
]

QUESTION_ROW = [
    "Start Date",
    "End Date",
    "Response Type",
    "Progress",
    "Duration (in seconds)",
    "Finished",
    "Recorded Date",
    "Response ID",
    "External Data Reference",
    "Distribution Channel",
    "User Language",
    "Please explain the main reason for your rating.",
    "Fraud Detection: reCAPTCHA score",
    "Fraud Detection: reCAPTCHA status",
    "Fraud Detection: reCAPTCHA error",
    "Fraud Detection: ballot-box stuffing",
    "Fraud Detection: private browser",
    "Fraud Detection: duplicate respondent",
]

IMPORT_ID_ROW = [
    '{"ImportId":"startDate","timeZone":"UTC"}',
    '{"ImportId":"endDate","timeZone":"UTC"}',
    '{"ImportId":"status"}',
    '{"ImportId":"progress"}',
    '{"ImportId":"duration"}',
    '{"ImportId":"finished"}',
    '{"ImportId":"recordedDate","timeZone":"UTC"}',
    '{"ImportId":"_recordId"}',
    '{"ImportId":"externalDataReference"}',
    '{"ImportId":"distributionChannel"}',
    '{"ImportId":"userLanguage"}',
    '{"ImportId":"QID2_TEXT"}',
    '{"ImportId":"Q_RecaptchaScore"}',
    '{"ImportId":"Q_RecaptchaStatus"}',
    '{"ImportId":"Q_RecaptchaError"}',
    '{"ImportId":"Q_BallotBoxStuffing"}',
    '{"ImportId":"Q_PrivateBrowserDetected"}',
    '{"ImportId":"Q_DuplicateRespondent"}',
]

LEGITIMATE_TEXTS = [
    "The checkout was easy, but I had to search for the return policy before ordering.",
    "Customer support answered my question clearly and followed up the next morning.",
    "I liked the product quality. The delivery box was damaged, although the item was fine.",
    "The app is useful for checking my account, but the sign-in screen sometimes freezes.",
    "The store was clean and the employee helped me compare two options without rushing me.",
    "Shipping took one day longer than expected, so I would like more accurate tracking updates.",
    "The instructions were understandable after I read them twice. A short example would help.",
    "I use this service because the monthly price is reasonable and canceling is straightforward.",
    "The appointment started late, but the staff explained the delay and treated me respectfully.",
    "I found what I needed, yet the website filters reset when I returned to the results page.",
]

SUSPICIOUS_TEXTS = [
    "Great service and excellent quality. I am completely satisfied with every part of the experience.",
    "The product met all expectations and the process was fast, convenient, and highly recommended.",
    "Everything worked perfectly. The company delivered outstanding value and exceptional customer care.",
    "Very good experience with no issues. I would recommend this service to everyone I know.",
]

AMBIGUOUS_TEXTS = [
    "It was fine. I got what I needed.",
    "Good service, but the wait was longer than I expected.",
    "The product works well and arrived on time. I do not have anything else to add.",
    "I had a positive experience overall, although the website could be easier to navigate.",
]


def iso_time(value: datetime) -> str:
    """Return a Qualtrics-like timestamp without changing the instant."""

    return value.isoformat(timespec="seconds")


def build_row(
    number: int,
    *,
    start: datetime,
    duration: int,
    text: str,
    external_reference: str,
    language: str = "EN",
    recaptcha_score: str = "0.92",
    recaptcha_status: str = "Complete",
    recaptcha_error: str = "",
    ballot_box: str = "False",
    private_browser: str = "False",
    duplicate_respondent: str = "False",
) -> dict[str, str | int]:
    """Build one response row using only fields available before review."""

    end = start + timedelta(seconds=duration)
    return {
        "StartDate": iso_time(start),
        "EndDate": iso_time(end),
        "Status": "IP Address",
        "Progress": 100,
        "Duration (in seconds)": duration,
        "Finished": "True",
        "RecordedDate": iso_time(end + timedelta(seconds=2)),
        "ResponseId": f"R_SYN_{number:04d}",
        "ExternalReference": external_reference,
        "DistributionChannel": "anonymous",
        "UserLanguage": language,
        "Q2_TEXT": text,
        "Q_RecaptchaScore": recaptcha_score,
        "Q_RecaptchaStatus": recaptcha_status,
        "Q_RecaptchaError": recaptcha_error,
        "Q_BallotBoxStuffing": ballot_box,
        "Q_PrivateBrowserDetected": private_browser,
        "Q_DuplicateRespondent": duplicate_respondent,
    }


def make_dataset() -> tuple[list[dict[str, str | int]], list[dict[str, str]]]:
    """Create deterministic scenarios and their separately stored labels."""

    rows: list[dict[str, str | int]] = []
    labels: list[dict[str, str]] = []
    base_time = datetime(2026, 10, 20, 13, 0, tzinfo=timezone.utc)

    def add(row: dict[str, str | int], label: str, family: str, reason: str) -> None:
        rows.append(row)
        labels.append(
            {
                "ResponseId": str(row["ResponseId"]),
                "expected_label": label,
                "scenario_family": family,
                "label_reason": reason,
            }
        )

    # 40 legitimate responses. Some include typos, fast completion, or a
    # missing reCAPTCHA result so one weak signal does not equal automation.
    for i in range(40):
        number = i + 1
        text = LEGITIMATE_TEXTS[i % len(LEGITIMATE_TEXTS)]
        if i in {6, 17, 31}:
            text += " I was kinda confused at first, but it worked after I tryed again."
        language = "ES" if i in {8, 22} else "EN"
        duration = 38 + (i * 17) % 410
        kwargs: dict[str, str] = {}
        family = "legitimate_normal"
        reason = "Normal completion pattern with an original response."
        if i in {3, 27}:
            duration = 18 + i % 3
            family = "legitimate_fast_reader"
            reason = "Fast completion is the only unusual behavior."
        elif i in {11, 35}:
            duration = 1300 + i * 11
            family = "legitimate_interrupted_session"
            reason = "Long duration can result from an interrupted session."
        elif i in {14, 32}:
            kwargs = {
                "recaptcha_score": "",
                "recaptcha_status": "Error",
                "recaptcha_error": "Verification unavailable",
            }
            family = "legitimate_unavailable_recaptcha"
            reason = "reCAPTCHA is unavailable, but the remaining behavior is normal."
        add(
            build_row(
                number,
                start=base_time + timedelta(minutes=i * 19),
                duration=duration,
                text=text + f" My visit number was {number}.",
                external_reference=f"P_SYN_{number:03d}",
                language=language,
                **kwargs,
            ),
            "legitimate",
            family,
            reason,
        )

    # 24 suspicious responses. Patterns occur in groups so repeated account
    # references and duplicate text can be derived from the full batch.
    for j in range(24):
        number = 41 + j
        cluster = j // 4
        external_reference = f"P_REPEAT_{cluster:02d}"
        text = SUSPICIOUS_TEXTS[j % len(SUSPICIOUS_TEXTS)]
        score = "0.08" if j % 3 else "0.18"
        add(
            build_row(
                number,
                start=base_time + timedelta(days=1, seconds=j * 47),
                duration=7 + j % 8,
                text=text,
                external_reference=external_reference,
                recaptcha_score=score,
                ballot_box="True" if j % 2 == 0 else "False",
                duplicate_respondent="True" if j % 3 != 0 else "False",
            ),
            "suspicious",
            "coordinated_repeat_submission",
            "Several behavioral indicators occur together: fast completion, repeated identity, or duplicate content.",
        )

    # 16 ambiguous responses. Each has limited or conflicting evidence and
    # should be routed to review rather than treated as confirmed abuse.
    for k in range(16):
        number = 65 + k
        kwargs = {}
        family = "ambiguous_single_weak_signal"
        reason = "Only one weak indicator is present."
        duration = 22 + (k * 29) % 240
        external_reference = f"P_AMB_{number:03d}"
        if k in {0, 4, 8, 12}:
            kwargs["private_browser"] = "True"
            family = "ambiguous_private_browser_only"
            reason = "Private browsing alone does not establish automation."
        elif k in {1, 5, 9, 13}:
            kwargs["recaptcha_score"] = "0.28"
            family = "ambiguous_low_recaptcha_only"
            reason = "A low reCAPTCHA score appears without supporting behavior."
        elif k in {2, 6, 10, 14}:
            duration = 12
            family = "ambiguous_fast_short_answer"
            reason = "A short answer can be completed quickly by a real respondent."
        else:
            # Two submissions share a participant reference but have different
            # text and otherwise normal behavior.
            external_reference = f"P_AMB_REPEAT_{k % 2}"
            family = "ambiguous_repeat_participant"
            reason = "A repeated participant may be allowed in a multi-wave study."
        add(
            build_row(
                number,
                start=base_time + timedelta(days=2, minutes=k * 23),
                duration=duration,
                text=AMBIGUOUS_TEXTS[k % len(AMBIGUOUS_TEXTS)] + f" Reference {number}.",
                external_reference=external_reference,
                **kwargs,
            ),
            "ambiguous",
            family,
            reason,
        )

    return rows, labels


def write_files() -> None:
    """Write the three-row export and the separate evaluation labels."""

    rows, labels = make_dataset()
    OUTPUT_DIR.mkdir(exist_ok=True)

    with EXPORT_PATH.open("w", newline="", encoding="utf-8") as export_file:
        writer = csv.DictWriter(export_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(dict(zip(FIELDS, QUESTION_ROW, strict=True)))
        writer.writerow(dict(zip(FIELDS, IMPORT_ID_ROW, strict=True)))
        writer.writerows(rows)

    with LABELS_PATH.open("w", newline="", encoding="utf-8") as labels_file:
        writer = csv.DictWriter(
            labels_file,
            fieldnames=["ResponseId", "expected_label", "scenario_family", "label_reason"],
        )
        writer.writeheader()
        writer.writerows(labels)

    print(f"Wrote {len(rows)} response rows to {EXPORT_PATH}")
    print(f"Wrote {len(labels)} evaluation labels to {LABELS_PATH}")


if __name__ == "__main__":
    write_files()
