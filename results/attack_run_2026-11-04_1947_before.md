# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 19:47
- Auto-marked BROKE (5xx, crash, no response): **0**
- Manually judged: **42 HELD, 14 BROKE**

The script recorded the outcomes, and I judged them using my system policy.
An `unsure` result does not accuse the writer or declare AI text human. A
malformed input breaks the system when it is scored instead of safely rejected.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `f17a44ef-089c-4a2e-b789-35c2eded0098` | human | 0.324 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `a2425872-7769-4ad8-ba5c-e769a00f404d` | human | 0.350 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `48895bad-6d5e-4d73-a17b-fcdd05873630` | unsure | 0.449 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `2318320e-1300-4937-b5c2-ddf83db0e7d2` | unsure | 0.541 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `550a12f1-ba49-4c34-9380-b65be5b69a71` | human | 0.223 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `81e94905-4b3c-4708-b104-7b347ec436be` | unsure | 0.375 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `a7bbcb16-ff78-4773-8e96-63f2914782cc` | unsure | 0.603 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `fdecd694-84f3-4498-beee-482816e20e2d` | human | 0.301 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `9ec37e62-3f93-4848-8960-b867e3d56194` | unsure | 0.460 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `8bd42637-92a7-4dac-b4b9-0292bc0c7c5d` | ai | 0.820 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0ea3dbca-880d-461a-8033-6a27d713b128` | unsure | 0.471 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `3ff5042d-9b5d-46ac-8dce-c71b79b55aef` | unsure | 0.623 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `d24da162-78ec-4d62-b8dc-2ee5237b6772` | unsure | 0.614 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `182dc99b-15db-4382-8861-6662f6eb80cf` | unsure | 0.570 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `52b0e158-08a8-4873-b8f2-596e05cd1d4a` | ai | 0.696 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `abcd9fcf-cd71-4f16-8b9e-be02bf1e268e` | unsure | 0.564 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `9e26a5a2-9ad8-4fbf-b8e7-d5534e106288` | ai | 0.662 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `e8b67033-3b77-4083-89e8-57830340c585` | human | 0.231 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `389c1e55-43f9-495b-9e5f-d02014b3eb12` | human | 0.292 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ff20c65a-8300-47e2-9714-cf1ed985fcfc` | human | 0.148 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a0cb02b1-ea3e-43ad-9b24-57575e46e73e` | unsure | 0.462 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `028c4e6a-495f-4d4a-914e-8a84a1092d82` | unsure | 0.352 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `76299cdb-9b7c-45b5-aac0-b77dac416a1f` | unsure | 0.374 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `17403eda-dd2d-4cab-9982-857c510ec2a7` | unsure | 0.447 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `984e9cef-9a6f-40a5-987a-fb16b16bebc6` | human | 0.250 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `2d3fb04b-5e4e-4892-ba99-15032b0b0497` | unsure | 0.431 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `ecc36f67-2266-4719-9a0f-102c8506c39a` | ai | 0.824 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `2601dc22-5625-4f7b-82a1-de8a5e31f2d3` | ai | 0.923 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `d9583911-36b9-4c27-8fbb-db1f65a8506c` | ai | 0.944 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `1e6f8b9b-c34b-48d3-83b6-4d86e9c414b4` | ai | 0.797 | BROKE |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cbce3a07-9ea5-47da-82ee-524ff0a8a097` | human | 0.322 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2b108755-91fa-41dc-8b6b-43b530e54884` | human | 0.322 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5295c8ae-0ec2-4b0b-80d8-bdea36e18edb` | human | 0.322 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `38bd7b50-2d58-496e-88f7-84e67d159ae0` | human | 0.322 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `462dd1b8-3972-47bf-9c34-5169dfd31ad8` | human | 0.322 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9c5728df-ad70-4d86-9526-7d64de2a35f8` | human | 0.322 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 6 | 4 |
| `false_positive` | 8 | 6 | 2 |
| `flood_same_creator` | 12 | 12 | 0 |
| `malformed` | 20 | 14 | 6 |
| `prompt_injection` | 6 | 4 | 2 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "f17a44ef-089c-4a2e-b789-35c2eded0098",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3241,
  "model_score": 0.1635,
  "style_score": 0.4848,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "a2425872-7769-4ad8-ba5c-e769a00f404d",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.3497,
  "model_score": 0.5943,
  "style_score": 0.105,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "48895bad-6d5e-4d73-a17b-fcdd05873630",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4491,
  "model_score": 0.6662,
  "style_score": 0.2321,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "2318320e-1300-4937-b5c2-ddf83db0e7d2",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5412,
  "model_score": 0.6114,
  "style_score": 0.4709,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "550a12f1-ba49-4c34-9380-b65be5b69a71",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2229,
  "model_score": 0.3212,
  "style_score": 0.1247,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "81e94905-4b3c-4708-b104-7b347ec436be",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3746,
  "model_score": 0.5727,
  "style_score": 0.1766,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "a7bbcb16-ff78-4773-8e96-63f2914782cc",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.6027,
  "model_score": 0.5862,
  "style_score": 0.6192,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "fdecd694-84f3-4498-beee-482816e20e2d",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3009,
  "model_score": 0.2452,
  "style_score": 0.3566,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "9ec37e62-3f93-4848-8960-b867e3d56194",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4602,
  "model_score": 0.7042,
  "style_score": 0.2162,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "8bd42637-92a7-4dac-b4b9-0292bc0c7c5d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8203,
  "model_score": 0.9792,
  "style_score": 0.6614,
  "label": "This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "0ea3dbca-880d-461a-8033-6a27d713b128",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4708,
  "model_score": 0.6175,
  "style_score": 0.3242,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "3ff5042d-9b5d-46ac-8dce-c71b79b55aef",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6232,
  "model_score": 0.7387,
  "style_score": 0.5077,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "d24da162-78ec-4d62-b8dc-2ee5237b6772",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6137,
  "model_score": 0.8051,
  "style_score": 0.4223,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "182dc99b-15db-4382-8861-6662f6eb80cf",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5696,
  "model_score": 0.8329,
  "style_score": 0.3064,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "52b0e158-08a8-4873-b8f2-596e05cd1d4a",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6956,
  "model_score": 0.8005,
  "style_score": 0.5906,
  "label": "This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "abcd9fcf-cd71-4f16-8b9e-be02bf1e268e",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5636,
  "model_score": 0.8814,
  "style_score": 0.2458,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "9e26a5a2-9ad8-4fbf-b8e7-d5534e106288",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.6618,
  "model_score": 0.8816,
  "style_score": 0.442,
  "label": "This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "e8b67033-3b77-4083-89e8-57830340c585",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2307,
  "model_score": 0.3223,
  "style_score": 0.1392,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "389c1e55-43f9-495b-9e5f-d02014b3eb12",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.2916,
  "model_score": 0.4625,
  "style_score": 0.1207,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "ff20c65a-8300-47e2-9714-cf1ed985fcfc",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1481,
  "model_score": 0.2044,
  "style_score": 0.0917,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a0cb02b1-ea3e-43ad-9b24-57575e46e73e",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4617,
  "model_score": 0.5943,
  "style_score": 0.3292,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "028c4e6a-495f-4d4a-914e-8a84a1092d82",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3517,
  "model_score": 0.4998,
  "style_score": 0.2035,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "76299cdb-9b7c-45b5-aac0-b77dac416a1f",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.3736,
  "model_score": 0.6401,
  "style_score": 0.1072,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "17403eda-dd2d-4cab-9982-857c510ec2a7",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4472,
  "model_score": 0.5583,
  "style_score": 0.3361,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "984e9cef-9a6f-40a5-987a-fb16b16bebc6",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.25,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "2d3fb04b-5e4e-4892-ba99-15032b0b0497",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4306,
  "model_score": 0.0112,
  "style_score": 0.85,
  "label": "The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "ecc36f67-2266-4719-9a0f-102c8506c39a",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8238,
  "model_score": 0.9976,
  "style_score": 0.65,
  "label": "This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "2601dc22-5625-4f7b-82a1-de8a5e31f2d3",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9234,
  "model_score": 0.9969,
  "style_score": 0.85,
  "label": "This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "d9583911-36b9-4c27-8fbb-db1f65a8506c",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9443,
  "model_score": 0.9064,
  "style_score": 0.9822,
  "label": "This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "1e6f8b9b-c34b-48d3-83b6-4d86e9c414b4",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.7975,
  "model_score": 0.9876,
  "style_score": 0.6074,
  "label": "This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "cbce3a07-9ea5-47da-82ee-524ff0a8a097",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.0287,
  "style_score": 0.6159,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "2b108755-91fa-41dc-8b6b-43b530e54884",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.0287,
  "style_score": 0.6159,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "5295c8ae-0ec2-4b0b-80d8-bdea36e18edb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.0287,
  "style_score": 0.6159,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "38bd7b50-2d58-496e-88f7-84e67d159ae0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.0287,
  "style_score": 0.6159,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "462dd1b8-3972-47bf-9c34-5169dfd31ad8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.0287,
  "style_score": 0.6159,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "9c5728df-ad70-4d86-9526-7d64de2a35f8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3223,
  "model_score": 0.0287,
  "style_score": 0.6159,
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
