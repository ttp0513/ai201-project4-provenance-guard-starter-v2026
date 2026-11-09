# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 22:39
- Auto-marked BROKE (5xx, crash, no response): **0**
- Manually judged: **48 HELD, 8 BROKE**

I used the same verdict policy as the before run. An `unsure` result does not
accuse a writer or declare AI text human, and invalid input is held when the
route rejects and logs it safely.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `35754ca3-4482-4fea-a099-6c57d98fe838` | human | 0.324 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `e655e591-95c8-4f18-a4ec-1251a636f46c` | human | 0.350 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `a53f95df-d0ed-42a8-a205-313d550e18e9` | unsure | 0.449 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cfda63ca-975c-4647-b944-3d6048a10152` | unsure | 0.541 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `49167a7c-4fe8-4645-b7dc-5ea96b157540` | human | 0.223 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c1d2c7d0-6a3d-46ea-ad16-62a5b375d8ef` | unsure | 0.375 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e5ade255-570c-42a3-be89-aaf62d265575` | unsure | 0.603 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `17e529a3-e55d-45c3-97e2-9767c973cad8` | human | 0.301 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `3bf28d2b-7406-45b9-afcc-5e6a0d4d7a63` | unsure | 0.460 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `670067a2-2540-4103-a177-49c317bb83e4` | ai | 0.820 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `2fae4dbd-abda-40aa-b23a-24b17443249b` | unsure | 0.471 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `b83078cf-19a8-45b4-b8a2-f68686d9f066` | unsure | 0.623 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `285a31d9-1467-42b3-8239-d91f243e2c69` | unsure | 0.614 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `26f96e2c-36cb-42c5-a53b-79e9ead5bc18` | unsure | 0.570 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `d1f0f892-c6c2-4c72-ae9b-3851f9bebc14` | ai | 0.696 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `c0786d53-a98f-4d64-ac8d-27b91128e718` | unsure | 0.564 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `976d2a44-1cbb-4f72-88b6-b1271b8cd77e` | ai | 0.662 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `19439737-5923-49c4-b5ec-0bbbccee246c` | human | 0.231 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `f110040e-1f44-40f3-93b3-d3acac97968a` | human | 0.292 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b500a080-f8c9-4e76-93fa-b100ff3b3d88` | human | 0.148 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `e875d857-7b71-4c7b-b2a6-902e24aad3e2` | unsure | 0.462 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f0167621-eeaa-477a-8ce1-a43f88380697` | unsure | 0.352 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `700d6fa7-a31e-4618-9e19-d405b9dd1a43` | unsure | 0.374 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b245433d-acd9-43c8-aa7c-469e3a7c9c2a` | unsure | 0.447 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `420eb23c-23c1-441c-8eb8-80a70e6dfcb1` | human | 0.322 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0f02ec88-c537-46d4-947a-1b9c42a6055d` | human | 0.322 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4bef9404-1efc-4c2d-b0b0-df83834aa5f6` | human | 0.322 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8c963c15-f9ab-4804-b1b5-5d2fe23f4a65` | human | 0.322 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5449d23b-2282-4a33-a256-176c612c59b4` | human | 0.322 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c6b1e9d6-43ce-45be-8cae-589dcd29105b` | human | 0.322 | HELD |
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
| `malformed` | 20 | 20 | 0 |
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
  "content_id": "35754ca3-4482-4fea-a099-6c57d98fe838",
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
  "content_id": "e655e591-95c8-4f18-a4ec-1251a636f46c",
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
  "content_id": "a53f95df-d0ed-42a8-a205-313d550e18e9",
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
  "content_id": "cfda63ca-975c-4647-b944-3d6048a10152",
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
  "content_id": "49167a7c-4fe8-4645-b7dc-5ea96b157540",
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
  "content_id": "c1d2c7d0-6a3d-46ea-ad16-62a5b375d8ef",
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
  "content_id": "e5ade255-570c-42a3-be89-aaf62d265575",
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
  "content_id": "17e529a3-e55d-45c3-97e2-9767c973cad8",
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
  "content_id": "3bf28d2b-7406-45b9-afcc-5e6a0d4d7a63",
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
  "content_id": "670067a2-2540-4103-a177-49c317bb83e4",
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
  "content_id": "2fae4dbd-abda-40aa-b23a-24b17443249b",
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
  "content_id": "b83078cf-19a8-45b4-b8a2-f68686d9f066",
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
  "content_id": "285a31d9-1467-42b3-8239-d91f243e2c69",
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
  "content_id": "26f96e2c-36cb-42c5-a53b-79e9ead5bc18",
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
  "content_id": "d1f0f892-c6c2-4c72-ae9b-3851f9bebc14",
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
  "content_id": "c0786d53-a98f-4d64-ac8d-27b91128e718",
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
  "content_id": "976d2a44-1cbb-4f72-88b6-b1271b8cd77e",
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
  "content_id": "19439737-5923-49c4-b5ec-0bbbccee246c",
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
  "content_id": "f110040e-1f44-40f3-93b3-d3acac97968a",
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
  "content_id": "b500a080-f8c9-4e76-93fa-b100ff3b3d88",
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
  "content_id": "e875d857-7b71-4c7b-b2a6-902e24aad3e2",
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
  "content_id": "f0167621-eeaa-477a-8ce1-a43f88380697",
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
  "content_id": "700d6fa7-a31e-4618-9e19-d405b9dd1a43",
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
  "content_id": "b245433d-acd9-43c8-aa7c-469e3a7c9c2a",
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
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "420eb23c-23c1-441c-8eb8-80a70e6dfcb1",
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
  "content_id": "0f02ec88-c537-46d4-947a-1b9c42a6055d",
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
  "content_id": "4bef9404-1efc-4c2d-b0b0-df83834aa5f6",
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
  "content_id": "8c963c15-f9ab-4804-b1b5-5d2fe23f4a65",
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
  "content_id": "5449d23b-2282-4a33-a256-176c612c59b4",
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
  "content_id": "c6b1e9d6-43ce-45be-8cae-589dcd29105b",
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
