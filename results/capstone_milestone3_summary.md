# Capstone Milestone 3 Run

- Started: `2026-11-15T23:40:17+00:00`
- Service: `http://127.0.0.1:5000`
- Model: `gpt2`
- Detector loaded before run: `False`
- Cases attempted: `10`
- Successful cases: `10`

## Results

| Case | HTTP | Stability | Final guess | Model calls | Server latency (ms) | Reasons |
| --- | ---: | --- | --- | ---: | ---: | --- |
| case_01_plain | 200 | unstable | unsure | 1 | 100934.55 | signals_disagree |
| case_02_comma | 200 | stable | unsure | 2 | 64.39 | stable_across_variants |
| case_03_unicode | 200 | unstable | unsure | 3 | 88.56 | signals_disagree |
| case_04_whitespace | 200 | unstable | unsure | 2 | 58.36 | label_changed, large_score_range |
| case_05_semicolon | 200 | unstable | unsure | 2 | 80.63 | large_score_range, signals_disagree |
| case_06_quotes | 200 | stable | unsure | 2 | 65.95 | stable_across_variants |
| case_07_hyphen | 200 | unstable | unsure | 2 | 60.04 | large_score_range, signals_disagree |
| case_08_short | 200 | unstable | unsure | 2 | 54.61 | label_changed, signals_disagree |
| case_09_formal | 200 | unstable | unsure | 1 | 31.04 | signals_disagree |
| case_10_informal | 200 | stable | unsure | 2 | 61.69 | stable_across_variants |

## Measured Cost

- Total local model calls: `19`
- Total wall time: `101.55 seconds`
- Average server latency: `10149.98 ms`
- Maximum server latency: `100934.55 ms`
- Hosted API calls: `0`
- Hosted API charge: `$0.00`

Cost is measured as wall-clock latency and local GPT-2 calls because
the service runs on the student's computer and does not call a paid API.
The first request may include model-loading time.

## Structured Log

The `capstone_milestone3_log.jsonl` file contains the 10 matching audit entries.
It stores input hashes and counts instead of submitted text.
