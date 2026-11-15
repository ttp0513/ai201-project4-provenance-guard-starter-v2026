# Synthetic Qualtrics Data Dictionary

These files imitate the parts of a Qualtrics CSV export needed for this
student prototype. They do not contain real respondents or measured fraud
rates.

## Files

- `qualtrics_synthetic_export.csv` contains three header rows followed by 80
  synthetic responses. It does not contain evaluation labels.
- `qualtrics_synthetic_labels.csv` stores the expected result and scenario
  explanation. The evaluation runner may join this file only after scoring.
- `generate_survey_scenarios.py` rebuilds both files deterministically.

The export has 40 legitimate, 24 suspicious, and 16 ambiguous scenarios. This
balance was selected to test different paths in a small prototype. It is not
an estimate of real survey traffic.

## Qualtrics-Style Header Rows

| Row | Purpose |
| --- | --- |
| 1 | Internal field name used by code. |
| 2 | Human-readable question or field label. |
| 3 | Synthetic import metadata that identifies the source field. |
| 4 onward | Synthetic response data. |

## Export Fields

| Variable | Meaning | Plausible value or range | Synthetic assumption |
| --- | --- | --- | --- |
| `StartDate` | Time the response began. | ISO 8601 timestamp. | Generated in a three-day test window. |
| `EndDate` | Time the response ended. | ISO 8601 timestamp at or after `StartDate`. | Calculated from start time plus duration. |
| `Status` | Qualtrics response-type field. | Text category. | Set to `IP Address` as a familiar export value; no IP is stored. |
| `Progress` | Percent of survey completed. | 0 to 100. | All test rows are complete at 100. |
| `Duration (in seconds)` | Elapsed survey time. | Non-negative integer. | Includes fast, ordinary, and interrupted sessions. Fast completion is not proof of automation. |
| `Finished` | Whether Qualtrics marks the response finished. | `True` or `False`. | All rows are `True` so this unit focuses on integrity risk rather than partial-response handling. |
| `RecordedDate` | Time the platform recorded the response. | ISO 8601 timestamp. | Two seconds after `EndDate`. |
| `ResponseId` | Unique response identifier. | Synthetic ID such as `R_SYN_0001`. | Unique in the export and safe to log. |
| `ExternalReference` | Participant reference supplied by the survey workflow. | Empty or a study-specific identifier. | Synthetic IDs repeat in selected scenarios so the evaluator can derive prior-submission counts. It is not a verified identity. |
| `DistributionChannel` | How the survey link was distributed. | Qualtrics channel name. | Set to `anonymous` for this prototype. |
| `UserLanguage` | Language selected for the survey. | Language code such as `EN` or `ES`. | Mostly English, with a few Spanish-interface scenarios. Text language alone is not a risk signal. |
| `Q2_TEXT` | Open-ended reason for the respondent's rating. | Free text. | Includes original, repeated, short, typo-containing, and polished responses. AI-like writing alone cannot create a high-risk result. |
| `Q_RecaptchaScore` | reCAPTCHA risk score exported by Qualtrics. | Blank or 0.0 to 1.0. | Lower values represent higher automation concern only when status is `Complete`. Values are invented test inputs, not observed statistics. |
| `Q_RecaptchaStatus` | Whether the reCAPTCHA check completed. | `Complete` or `Error`. | Error rows represent unavailable evidence rather than confirmed fraud. |
| `Q_RecaptchaError` | Reason the reCAPTCHA result is unavailable. | Blank or short text. | Contains a generic synthetic error message only when status is `Error`. |
| `Q_BallotBoxStuffing` | Qualtrics duplicate-prevention indicator. | `True` or `False`. | Set in some suspicious scenarios. It remains evidence to review, not ground truth. |
| `Q_PrivateBrowserDetected` | Qualtrics private-browser indicator. | `True` or `False`. | Used alone in some ambiguous cases to test false-positive protection. |
| `Q_DuplicateRespondent` | Qualtrics duplicate-respondent indicator. | `True` or `False`. | Set in some suspicious scenarios and treated as one input among several. |

## Evaluation-Only Fields

| Variable | Meaning | Allowed values | Leakage rule |
| --- | --- | --- | --- |
| `ResponseId` | Join key back to the export. | Synthetic response ID. | May be used only to join results after scoring. |
| `expected_label` | Expected review category for the scenario. | `legitimate`, `ambiguous`, `suspicious`. | Must never be passed to the scoring route. |
| `scenario_family` | Short name for the test pattern. | Documented synthetic category. | Used only to diagnose which patterns pass or fail. |
| `label_reason` | Why the scenario received its expected label. | Plain-language explanation. | Used only in the evaluation report. |

## Features Derived Later

The future evaluation runner may calculate these values from the export before
calling `/survey-risk`:

- prior submissions for the same `ExternalReference` earlier in time;
- exact or near-duplicate text frequency within the batch;
- completion-time indicators based on documented prototype thresholds.

These are behavioral features, not labels. The scorer must not use
`expected_label`, `scenario_family`, or `label_reason` as inputs.

## Limits

- Synthetic rows can prove that code paths work, but cannot establish real
  detection accuracy.
- The participant reference may be missing, shared, reused for a valid reason,
  or changed by an attacker.
- reCAPTCHA and Qualtrics fraud fields can be unavailable or wrong.
- Completion time and duplicate text need survey-specific context.
- Human review is required before taking action against a respondent.

## Format References

- [Qualtrics: Understanding Your Dataset](https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/download-data/understanding-your-dataset/)
- [Qualtrics: Fraud Detection](https://www.qualtrics.com/support/survey-platform/survey-module/survey-checker/fraud-detection/)
