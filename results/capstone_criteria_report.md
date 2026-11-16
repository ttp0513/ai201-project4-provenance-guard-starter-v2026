# Capstone Criteria Run

- Started: `20261116T011102Z`
- Trials: `3`
- Same scenarios per trial: `10`
- System changes between trials: `none`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --- | --- | --- | --- | --- | --- |
| 1. Variants preserve wording | 15/15 cases | 5/5 | 5/5 | 5/5 | MET |
| 2. Instability forces unsure | 3/3 reasons covered and 100% unstable cases handled in every trial | reasons 3/3; handling 6/6 | reasons 3/3; handling 6/6 | reasons 3/3; handling 6/6 | MET |
| 3. Useful classifications remain | at least 3 stable and 1 stable non-unsure case per trial | stable 4; non-unsure 1 | stable 4; non-unsure 1 | stable 4; non-unsure 1 | MET |
| 4. Complete private audit entries | 30/30 complete entries with no text fields | 10/10 | 10/10 | 10/10 | MET |
| 5. Warm latency and calls bounded | 30/30 under 500 ms with 1-4 calls matching variant count | 10/10; max 108.46 ms | 10/10; max 91.04 ms | 10/10; max 96.06 ms | MET |

## Actual Output From Run 1

### Criterion 1

```json
{
  "case_id": "case_03_unicode",
  "variant_results": [
    {
      "combined_score": 0.309,
      "guess": "human",
      "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
      "model_score": 0.0695,
      "name": "original",
      "style_score": 0.5486,
      "text": "The editor called it “helpful”—although the first explanation was unclear."
    },
    {
      "combined_score": 0.3422,
      "guess": "human",
      "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
      "model_score": 0.1359,
      "name": "standardized_punctuation",
      "style_score": 0.5486,
      "text": "The editor called it \"helpful\"-although the first explanation was unclear."
    },
    {
      "combined_score": 0.3348,
      "guess": "human",
      "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
      "model_score": 0.0457,
      "name": "punctuation_light",
      "style_score": 0.6239,
      "text": "The editor called it helpful although the first explanation was unclear."
    }
  ]
}
```

### Criterion 2

```json
{
  "content_id": "485ce8a2-2ae7-47ec-af1c-2523a94d4665",
  "guess": "unsure",
  "human_review": true,
  "label": "The detector was not stable across the reliability checks, so this result needs human review.",
  "label_changed": true,
  "latency_ms": 82.57,
  "max_signal_disagreement": 0.1756,
  "model_calls": 2,
  "original_result": {
    "combined_score": 0.45,
    "guess": "unsure",
    "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
    "model_score": 0.5378,
    "name": "original",
    "style_score": 0.3622,
    "text": "Customer support answered quickly.\n\nThe second response was more useful."
  },
  "reasons": [
    "label_changed",
    "large_score_range"
  ],
  "score_range": 0.1315,
  "stability": "unstable",
  "variant_count": 2,
  "variant_results": [
    {
      "combined_score": 0.45,
      "guess": "unsure",
      "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
      "model_score": 0.5378,
      "name": "original",
      "style_score": 0.3622,
      "text": "Customer support answered quickly.\n\nThe second response was more useful."
    },
    {
      "combined_score": 0.3185,
      "guess": "human",
      "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
      "model_score": 0.2754,
      "name": "normalized_whitespace",
      "style_score": 0.3615,
      "text": "Customer support answered quickly. The second response was more useful."
    }
  ]
}
```

### Criterion 3

```json
{
  "case_id": "case_02_comma",
  "stability": "stable",
  "original_guess": "unsure",
  "final_guess": "unsure"
}
```

### Criterion 4

```json
{
  "combined_score": 0.3905,
  "content_id": "944dcaad-8219-4c31-b399-f105ba382c9f",
  "creator_id": "capstone_criteria_t1_case_01_plain_20261116T011102Z",
  "event": "reliability_check",
  "guess": "unsure",
  "human_review": true,
  "input_characters": 38,
  "input_sha256": "26b9d243aebc448d4e909b44dbf4c404fb9635d0ec9f21847a9842cad1cc1699",
  "input_words": 6,
  "label": "The detector was not stable across the reliability checks, so this result needs human review.",
  "label_changed": false,
  "latency_ms": 23.75,
  "max_signal_disagreement": 0.5191,
  "model_calls": 1,
  "model_score": 0.1309,
  "original_guess": "unsure",
  "reasons": [
    "signals_disagree"
  ],
  "score_range": 0.0,
  "stability": "unstable",
  "status": "decided",
  "style_score": 0.65,
  "timestamp": "2026-11-16T01:12:40+00:00",
  "variant_count": 1,
  "variant_results": [
    {
      "combined_score": 0.3905,
      "guess": "unsure",
      "model_score": 0.1309,
      "name": "original",
      "style_score": 0.65
    }
  ]
}
```

### Criterion 5

```json
{
  "case_id": "case_02_comma",
  "latency_ms": 64.37,
  "model_calls": 2,
  "variant_count": 2
}
```

## Producer

`run_capstone_eval.py::main` sent the requests. The five
`evaluate_criterion_*` functions calculated the verdicts.
