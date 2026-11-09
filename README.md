# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 - THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps - this is the trace you wrote in Milestone 1. -->

Provenance Guard is a web service that looks at submitted writing and estimates
whether it looks human-written or AI-generated. It cannot prove who wrote the
text. It uses two signals and returns `unsure` when they do not give a clear
answer.

When someone submits writing:

1. The app receives the text and the writer's creator ID.
2. It checks that the submission contains valid text.
3. A model signal measures how predictable the writing is.
4. A style signal examines sentence structure, vocabulary, and punctuation.
5. The app combines both signals into one score.
6. The score becomes a `human`, `unsure`, or `AI` label.
7. The app returns the result and records the decision in an audit log.

If the writer believes the result is incorrect, they can appeal it. The app
records the appeal and marks the submission as `under_review`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet - and unit 8's attack set is built out of blind spots. -->

### Signal one - the model signal

**What it measures:**

The model signal asks GPT-2 how easy the next words were to predict. This is
called perplexity. Text that is easier to predict gets a higher AI score, and
text that is more surprising gets a lower AI score.

**Why that might differ between human and AI writing:**

AI often chooses likely next words, so its writing can be easier for another
model to predict. Human writing may include more personal details, unusual
words, or sudden changes.

**What it can't see:**

This signal does not know who wrote the text. A person writing in a second
language, a younger writer, or anyone using simple words may get a high AI
score. AI text with rare words may also get a human-like score.

### Signal two - the style signal

**What it measures:**

The style signal looks at the shape of the writing, not its meaning. It checks
sentence-length changes, the amount of unique words, and punctuation. A higher
result means the style looks more AI-like.

Within the style score, sentence-length variation contributes 50%, vocabulary
variety contributes 35%, and punctuation density contributes 15%. Punctuation
has the smallest influence because it is especially easy to add or remove.

**Why that might differ between human and AI writing:**

AI writing may repeat words or follow more regular patterns. It can also use
sentences that are very short or longer than needed. These are only clues
because current AI writing can look a lot like human writing.

**What it can't see:**

The style signal cannot tell if ideas connect well or if a phrase is needed. It
also cannot identify the real writer. Someone can change the score by adding
typos, splitting sentences, or changing punctuation without changing the main
message. Text length can also change the vocabulary score.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

I average the model score and style score. A higher result means more AI-like.
If the signals disagree, the average moves closer to `unsure` instead of
letting one signal decide everything.

**The numbers:**

The model signal contributes 50% and the style signal contributes 50%. Scores
from `0.00` through `0.35` are labelled human, scores above `0.35` and below
`0.65` are unsure, and scores from `0.65` through `1.00` are labelled AI.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A plain human paragraph beginning "I went to the store" got a model score of
`0.7858` and a style score of `0.4798`. The final score was `0.6328`, so the
result was `unsure` instead of AI. This is what I wanted when the signals do not
agree.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00-0.35, inclusive | This writing appears likely to have been written by a person, but this result is not proof of authorship. |
| unsure | above 0.35 and below 0.65 | The signals are inconclusive, so we cannot determine whether this writing was produced by a person or AI. |
| high-confidence AI | 0.65-1.00, inclusive | This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I used this wording because the system does not have a clear answer. It avoids
accusing the writer when the signals are uncertain.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"Meet the RoamCup: a double-wall insulated travel mug that actually keeps up with your day. Coffee stays piping hot during morning commutes, while the leak-proof lid and ergonomic grip mean fewer spills and more sips. Toss it in your bag and go.","creator_id":"john_human"}'
```

```json
{
  "confidence": 0.2667,
  "content_id": "7a32d5fd-60ac-4ae3-b705-bd2b5bf1b613",
  "guess": "human",
  "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
  "model_score": 0.3403,
  "style_score": 0.1931
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"7a32d5fd-60ac-4ae3-b705-bd2b5bf1b613","reasoning":"I wrote this sample and want a person to review the result."}'
```

```json
{
  "content_id": "7a32d5fd-60ac-4ae3-b705-bd2b5bf1b613",
  "message": "Your appeal was recorded and is awaiting human review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.2667,
      "content_id": "7a32d5fd-60ac-4ae3-b705-bd2b5bf1b613",
      "creator_id": "john_human",
      "guess": "human",
      "label": "This writing appears likely to have been written by a person, but this result is not proof of authorship.",
      "model_score": 0.3403,
      "status": "decided",
      "style_score": 0.1931,
      "timestamp": "2026-11-01T23:03:38+00:00"
    },
    {
      "content_id": "7a32d5fd-60ac-4ae3-b705-bd2b5bf1b613",
      "creator_id": "john_human",
      "event": "appeal",
      "reasoning": "I wrote this sample and want a person to review the result.",
      "status": "under_review",
      "timestamp": "2026-11-01T23:03:53+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I used AI as an instructor and requirements reviewer. I
  asked it to explain the request flow, identify fairness risks, and help turn
  my goals into five measurable acceptance criteria.
- *What came back:* It explained the two signals, suggested test targets, and
  showed how false positives, score spread, appeals, labels, and bad input
  could be measured.
- *What I changed:* I did not accept every suggestion. I questioned arbitrary
  targets, caught that AUC measures ranking rather than score distance, and
  tied my final numbers to the required three trials, label thresholds, and
  test cases already provided by the starter. This helped me use AI output as
  a draft to evaluate instead of an answer to copy.

**Moment 2**

- *What I asked for:* I used AI as a pair programmer for the Flask routes,
  stylometry functions, scoring rule, labels, audit logging, and appeal flow. I
  also asked for beginner-friendly comments and tests for each stage.
- *What came back:* It produced implementation drafts, edge-case checks, test
  commands, and explanations of how the files connect.
- *What I changed:* I made punctuation only 15% of the style score because it
  is easy to manipulate, and I used equal signal weights so disagreement moves
  toward `unsure`. I tested the signals separately, checked all three label
  boundaries, ran real API requests, inspected the audit log, and kept the
  commits separated by milestone. My own AI-labelled sample returned `unsure`,
  which showed me why model output needs human review instead of blind trust.

**Moment 3**

- *What I asked for:* In Unit 8, I used AI as a testing coach. I asked it to
  help automate the three trials, connect each appeal to its real content ID,
  calculate the human and AI score averages, and explain why so many results
  were `unsure`.
- *What came back:* It helped organize the attack verdicts and showed that the
  model signal ranked my AI samples below my human samples, while the style
  signal moved in the intended direction. It also suggested several possible
  fixes, including changing weights, thresholds, or input validation.
- *What I changed:* I supplied and approved all ten human writing samples,
  checked the verdict policy, and kept the missed criteria instead of changing
  samples or thresholds to make them pass. I chose input validation because it
  fixed a measured route problem without increasing false accusations. I then
  compared the same attack and evaluation sets before and after the change.

AI helped me move faster, but I stayed responsible for the requirements,
design choices, testing, and final explanation.

<!-- ═══════════════════════ UNIT 8 - THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 6 submissions per minute, 100 submissions per day

**Why those numbers and not others:**
I assumed that each `creator_id` represents one individual writer. Six
submissions per minute gives a writer room to correct and resubmit their work,
but it slows down a script that sends many versions quickly to study the
detector. A limit of 100 per day still allows frequent use while preventing one
creator from sending hundreds or thousands of submissions. In a real system, I
would review normal usage data and adjust these limits if legitimate users were
being blocked.

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently - one script can look like a thousand callers, and one household
can look like one. -->

The service counts each creator_id as one caller and uses the IP address when a valid ID is missing. I chose creator_id because different writers may share the same household or school network, and an IP-only limit could block them together. However, the service does not verify the ID, so an attacker can avoid the limit by changing it. In a real system, I would use an authenticated account or API key and combine per-account and per-IP limits.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
>> python run_attacks.py --flood 15
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 429 429 429 429 429 429 429 429 429
============================================================

9 of 15 were rate limited.

```

---

## Attack Run - Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

I treated `unsure` as a cautious result rather than an accusation or a claim
that the text was human. With that rule, 42 attacks were held and 14 broke the
system. The complete raw report is in
`results/attack_run_2026-11-04_1947_before.md`.

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | typos raise word variety | 200 | human | 0.324 | BROKE |
| EV02 | evasion | broken-up sentences raise length spread | 200 | human | 0.350 | BROKE |
| EV03 | evasion | a pasted quotation changes the shape | 200 | unsure | 0.449 | HELD |
| EV04 | evasion | unusual words raise perplexity | 200 | unsure | 0.541 | HELD |
| EV05 | evasion | heavy human editing pass | 200 | human | 0.223 | BROKE |
| EV06 | evasion | one very long sentence and one very short | 200 | unsure | 0.375 | HELD |
| EV07 | evasion | padding with punctuation | 200 | unsure | 0.603 | HELD |
| EV08 | evasion | text below the token window | 200 | human | 0.301 | BROKE |
| EV09 | evasion | AI text with a human opening paragraph | 200 | unsure | 0.460 | HELD |
| EV10 | evasion | repeated stanza structure | 200 | ai | 0.820 | HELD |
| FP01 | false positive | plain human writing | 200 | unsure | 0.471 | HELD |
| FP02 | false positive | formal human writing | 200 | unsure | 0.623 | HELD |
| FP03 | false positive | non-native English speaker | 200 | unsure | 0.614 | HELD |
| FP04 | false positive | student essay written to a rubric | 200 | unsure | 0.570 | HELD |
| FP05 | false positive | human technical documentation | 200 | ai | 0.696 | BROKE |
| FP06 | false positive | person imitating a formal template | 200 | unsure | 0.564 | HELD |
| FP07 | false positive | deliberate phrase repetition | 200 | ai | 0.662 | BROKE |
| FP08 | false positive | short genuine human submission | 200 | human | 0.231 | HELD |
| PI01 | prompt injection | instruction to ignore the check | 200 | human | 0.292 | BROKE |
| PI02 | prompt injection | disguised system message | 200 | human | 0.148 | BROKE |
| PI03 | prompt injection | instruction in writer's voice | 200 | unsure | 0.462 | HELD |
| PI04 | prompt injection | hostile label text | 200 | unsure | 0.352 | HELD |
| PI05 | prompt injection | audit-log injection | 200 | unsure | 0.374 | HELD |
| PI06 | prompt injection | instruction plus human text | 200 | unsure | 0.447 | HELD |
| MF01 | malformed | whitespace only | 400 | - | - | HELD |
| MF02 | malformed | single character | 400 | - | - | HELD |
| MF03 | malformed | control characters | 200 | human | 0.250 | BROKE |
| MF04 | malformed | punctuation only | 200 | unsure | 0.431 | BROKE |
| MF05 | malformed | very long single word | 200 | ai | 0.824 | BROKE |
| MF06 | malformed | emoji only | 200 | ai | 0.923 | BROKE |
| MF07 | malformed | right-to-left script | 200 | ai | 0.944 | BROKE |
| MF08 | malformed | 60,000 characters | 200 | ai | 0.797 | BROKE |
| RQ01 | malformed request | no text field | 400 | - | - | HELD |
| RQ02 | malformed request | no creator ID | 400 | - | - | HELD |
| RQ03 | malformed request | text is a number | 400 | - | - | HELD |
| RQ04 | malformed request | text is a list | 400 | - | - | HELD |
| RQ05 | malformed request | text is null | 400 | - | - | HELD |
| RQ06 | malformed request | creator ID is an object | 400 | - | - | HELD |
| RQ07 | malformed request | body is a JSON array | 400 | - | - | HELD |
| RQ08 | malformed request | unparseable JSON | 400 | - | - | HELD |
| RQ09 | malformed request | empty body | 400 | - | - | HELD |
| RQ10 | malformed request | form-encoded body | 400 | - | - | HELD |
| RQ11 | malformed request | JSON sent as plain text | 429 | - | - | HELD |
| RQ12 | malformed request | deeply nested JSON | 400 | - | - | HELD |
| FL01_01 | flood | request 1 from one creator | 200 | human | 0.322 | HELD |
| FL01_02 | flood | request 2 from one creator | 200 | human | 0.322 | HELD |
| FL01_03 | flood | request 3 from one creator | 200 | human | 0.322 | HELD |
| FL01_04 | flood | request 4 from one creator | 200 | human | 0.322 | HELD |
| FL01_05 | flood | request 5 from one creator | 200 | human | 0.322 | HELD |
| FL01_06 | flood | request 6 from one creator | 200 | human | 0.322 | HELD |
| FL01_07 | flood | request 7 from one creator | 429 | - | - | HELD |
| FL01_08 | flood | request 8 from one creator | 429 | - | - | HELD |
| FL01_09 | flood | request 9 from one creator | 429 | - | - | HELD |
| FL01_10 | flood | request 10 from one creator | 429 | - | - | HELD |
| FL01_11 | flood | request 11 from one creator | 429 | - | - | HELD |
| FL01_12 | flood | request 12 from one creator | 429 | - | - | HELD |

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp":"2026-11-05T00:46:59+00:00","content_id":"f17a44ef-089c-4a2e-b789-35c2eded0098","creator_id":"attacker_EV01","guess":"human","model_score":0.1635,"style_score":0.4848,"combined_score":0.3241,"label":"This writing appears likely to have been written by a person, but this result is not proof of authorship.","status":"decided"}
{"timestamp":"2026-11-05T00:47:01+00:00","content_id":"52b0e158-08a8-4873-b8f2-596e05cd1d4a","creator_id":"attacker_FP05","guess":"ai","model_score":0.8005,"style_score":0.5906,"combined_score":0.6956,"label":"This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.","status":"decided"}
{"timestamp":"2026-11-05T00:47:01+00:00","content_id":"9e26a5a2-9ad8-4fbf-b8e7-d5534e106288","creator_id":"attacker_FP07","guess":"ai","model_score":0.8816,"style_score":0.442,"combined_score":0.6618,"label":"This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.","status":"decided"}
{"timestamp":"2026-11-05T00:47:01+00:00","content_id":"984e9cef-9a6f-40a5-987a-fb16b16bebc6","creator_id":"attacker_MF03","guess":"human","model_score":0.0,"style_score":0.5,"combined_score":0.25,"label":"This writing appears likely to have been written by a person, but this result is not proof of authorship.","status":"decided"}
{"timestamp":"2026-11-05T00:47:02+00:00","content_id":"2601dc22-5625-4f7b-82a1-de8a5e31f2d3","creator_id":"attacker_MF06","guess":"ai","model_score":0.9969,"style_score":0.85,"combined_score":0.9234,"label":"This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.","status":"decided"}
{"timestamp":"2026-11-05T00:47:02+00:00","content_id":"d9583911-36b9-4c27-8fbb-db1f65a8506c","creator_id":"attacker_MF07","guess":"ai","model_score":0.9064,"style_score":0.9822,"combined_score":0.9443,"label":"This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.","status":"decided"}
{"timestamp":"2026-11-05T00:47:02+00:00","content_id":"1e6f8b9b-c34b-48d3-83b6-4d86e9c414b4","creator_id":"attacker_MF08","guess":"ai","model_score":0.9876,"style_score":0.6074,"combined_score":0.7975,"label":"This writing shows patterns associated with AI-generated text. This result is not proof and should be reviewed by a person.","status":"decided"}
{"timestamp":"2026-11-05T00:47:01+00:00","content_id":"389c1e55-43f9-495b-9e5f-d02014b3eb12","creator_id":"attacker_PI01","guess":"human","model_score":0.4625,"style_score":0.1207,"combined_score":0.2916,"label":"This writing appears likely to have been written by a person, but this result is not proof of authorship.","status":"decided"}
{"timestamp":"2026-11-05T00:47:03+00:00","content_id":"cbce3a07-9ea5-47da-82ee-524ff0a8a097","creator_id":"attacker_flood","guess":"human","model_score":0.0287,"style_score":0.6159,"combined_score":0.3223,"label":"This writing appears likely to have been written by a person, but this result is not proof of authorship.","status":"decided"}
{"timestamp":"2026-11-05T00:47:03+00:00","creator_id":"attacker_flood","event":"rejected","status":"rejected","reason":"rate_limited","limit":"6 per 1 minute"}
```

**The single worst outcome** - the one I'd least want to explain to a writer
whose work got caught by it:

My worst result was FP05. The system labelled human-written technical
documentation as AI with a score of 0.6956. Technical instructions naturally
use short commands and repeated sentence patterns, so the detector confused a
clear writing style with AI authorship. I would not want a real writer to be
questioned only because their work was direct and structured.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | At most 2 of 10 human samples labelled `ai` | 0 of 10 | 0 of 10 | 0 of 10 | MET |
| 2. Score separation | Human average ≤ 0.35 and AI average ≥ 0.65 | H 0.3947 / AI 0.4309 | H 0.3947 / AI 0.4309 | H 0.3947 / AI 0.4309 | MISSED |
| 3. Label coverage | At least one `human`, `unsure`, and `ai` | 1 / 5 / 0 | 1 / 5 / 0 | 1 / 5 / 0 | MISSED |
| 4. Appeal path | Appeal is `under_review`, logged, and original remains | All checks passed | All checks passed | All checks passed | MET |
| 5. Bad input | Four logged 4xx responses and health 200 | 4 of 4; health 200 | 4 of 4; health 200 | 4 of 4; health 200 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json
{
  "source_file": "results/run_2026-11-08_2213_before.md",
  "producer": "run_eval.py::main",
  "trial": 1,
  "criterion_1_guesses": [
    "unsure", "unsure", "unsure", "human", "unsure",
    "unsure", "human", "human", "unsure", "unsure"
  ],
  "criterion_2_human_combined_scores": [
    0.4170, 0.5016, 0.3689, 0.3183, 0.4113,
    0.4099, 0.2626, 0.3279, 0.5016, 0.4279
  ],
  "criterion_2_ai_combined_scores": [
    0.4140, 0.4519, 0.4093, 0.5272, 0.4545,
    0.3826, 0.3307, 0.4895, 0.4579, 0.3915
  ],
  "criterion_3_guesses": [
    "unsure", "unsure", "unsure", "unsure", "unsure", "human"
  ],
  "criterion_4": {
    "submit_status": 200,
    "appeal_http_status": 200,
    "appeal_status": "under_review",
    "original_decision_preserved": true,
    "appeal_logged": true
  },
  "criterion_5": {
    "responses": [
      {"status": 400, "error": "missing_text", "rejection_logged": true},
      {"status": 400, "error": "empty_text", "rejection_logged": true},
      {"status": 400, "error": "invalid_text", "rejection_logged": true},
      {"status": 413, "error": "text_too_large", "rejection_logged": true}
    ],
    "health_after_trial": {"status": 200, "ok": true}
  }
}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety - so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

1. **False positives - MET.** I counted the `ai` labels across my ten human
   samples. Every trial had three `human`, seven `unsure`, and zero `ai`, so it
   stayed below my limit of two false AI classifications.

2. **Score separation - MISSED.** The human average was `0.3947`, above my
   `0.35` target, while the AI average was only `0.4309`, below my `0.65`
   target. The failure started in **signal one**: its human average was `0.4700`
   but its AI average was lower at `0.3951`, the opposite of the intended
   direction. **Signal two** moved in the expected direction (`0.3194` human
   and `0.4667` AI), but the equal-weight **combining rule** let the two signals
   cancel. The final averages were separated by only `0.0362`.

3. **Label coverage - MISSED.** Each trial returned one `human`, five
   `unsure`, and no `ai`. This was not a bug in the **label mapping** because
   none of the six combined scores reached the `0.65` AI threshold. The same
   signal-one reversal and equal-weight cancellation from Criterion 2 kept all
   six scores between `0.3307` and `0.4170`.

4. **Appeal path - MET.** In all three trials, `/appeal` returned `200` with
   `under_review`. Reading `/log` showed both the original `decided` entry and
   the matching appeal entry, so the append-only history was preserved.

5. **Bad input - MET.** The missing, empty, and null text requests returned
   `400`, while the 50,000-word request returned `413`. All twelve rejections
   were logged, and `/health` returned `200` after every trial.

The 14 broken attacks also formed four patterns:

- **EV01, EV02, EV05, and EV08 - signals and combining rule.** Typos, changed
  sentence breaks, heavy editing, and short text changed the measurements
  without changing the AI origin. Their combined scores fell into the human
  range, showing that both signals can be changed by surface edits.
- **FP05 and FP07 - signal one.** Human technical instructions and deliberate
  repetition were very predictable to the language model. Signal one gave
  them `0.8005` and `0.8816`, and the combined scores crossed the AI threshold.
- **PI01 and PI02 - signals, not instruction following.** The service did not
  execute the injected instructions, but the added command-like text changed
  its predictability and style enough to produce the requested `human` label.
- **MF03 through MF08 - route validation.** The route rejected missing or
  incorrectly typed fields, but it accepted control characters, punctuation,
  a giant word, emoji, unsupported script, and 60,000 characters as scorable
  text. MF08 also bypassed the size check because the route counts words while
  that attack was large in characters.


---

## The Improvement

**What I changed:**
I added supported-input validation before either signal runs. The route now
rejects text over 50,000 characters, unsafe control characters, and text with
fewer than two supported Latin-alphabet words. Rejections still go through
`audit.log_rejection`, so the new checks do not create gaps in the log.

**Which diagnosis pointed at it:**
MF03 through MF08 all reached the signals even though they contained control
characters, punctuation, one giant token, emoji, unsupported script, or 60,000
characters. The route only checked whether `text` was a non-empty string and
whether it had 50,000 words, so it produced authorship labels for input the
English detector could not meaningfully evaluate.

### Attack Run - After

<!-- Same format. `run_attacks.py --label after` -->

Full evidence: `results/attack_run_2026-11-08_2239_after.md`.

| ID | Status | Guess | Verdict |
|---|---:|---|---|
| EV01 | 200 | human | BROKE |
| EV02 | 200 | human | BROKE |
| EV03 | 200 | unsure | HELD |
| EV04 | 200 | unsure | HELD |
| EV05 | 200 | human | BROKE |
| EV06 | 200 | unsure | HELD |
| EV07 | 200 | unsure | HELD |
| EV08 | 200 | human | BROKE |
| EV09 | 200 | unsure | HELD |
| EV10 | 200 | ai | HELD |
| FP01 | 200 | unsure | HELD |
| FP02 | 200 | unsure | HELD |
| FP03 | 200 | unsure | HELD |
| FP04 | 200 | unsure | HELD |
| FP05 | 200 | ai | BROKE |
| FP06 | 200 | unsure | HELD |
| FP07 | 200 | ai | BROKE |
| FP08 | 200 | human | HELD |
| PI01 | 200 | human | BROKE |
| PI02 | 200 | human | BROKE |
| PI03 | 200 | unsure | HELD |
| PI04 | 200 | unsure | HELD |
| PI05 | 200 | unsure | HELD |
| PI06 | 200 | unsure | HELD |
| MF01 | 400 | — | HELD |
| MF02 | 400 | — | HELD |
| MF03 | 400 | — | HELD |
| MF04 | 400 | — | HELD |
| MF05 | 400 | — | HELD |
| MF06 | 400 | — | HELD |
| MF07 | 400 | — | HELD |
| MF08 | 413 | — | HELD |
| RQ01 | 400 | — | HELD |
| RQ02 | 400 | — | HELD |
| RQ03 | 400 | — | HELD |
| RQ04 | 400 | — | HELD |
| RQ05 | 400 | — | HELD |
| RQ06 | 400 | — | HELD |
| RQ07 | 400 | — | HELD |
| RQ08 | 400 | — | HELD |
| RQ09 | 400 | — | HELD |
| RQ10 | 400 | — | HELD |
| RQ11 | 429 | — | HELD |
| RQ12 | 400 | — | HELD |
| FL01_01 | 200 | human | HELD |
| FL01_02 | 200 | human | HELD |
| FL01_03 | 200 | human | HELD |
| FL01_04 | 200 | human | HELD |
| FL01_05 | 200 | human | HELD |
| FL01_06 | 200 | human | HELD |
| FL01_07 | 429 | — | HELD |
| FL01_08 | 429 | — | HELD |
| FL01_09 | 429 | — | HELD |
| FL01_10 | 429 | — | HELD |
| FL01_11 | 429 | — | HELD |
| FL01_12 | 429 | — | HELD |

| Family | BROKE before | BROKE after | Change |
|---|---:|---:|---:|
| Evasion | 4 | 4 | 0 |
| False positive | 2 | 2 | 0 |
| Prompt injection | 2 | 2 | 0 |
| Malformed | 6 | 0 | -6 |
| Flood | 0 | 0 | 0 |
| **Total** | **14** | **8** | **-6** |

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Yes, for the problem I changed. Broken malformed attacks fell from six to zero,
and total broken attacks fell from 14 to 8. MF03 through MF07 now return `400`
and MF08 returns `413` instead of receiving misleading authorship scores. The
five acceptance-criteria verdicts stayed the same, which makes sense because I
did not change either signal, the combining rule, or the label thresholds. The
full criteria evidence is in `results/run_2026-11-08_2240_after.md`.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

Eight attacks still broke the system after my improvement:

- **EV01, EV02, EV05, and EV08:** AI text still received a `human` label after
  typos, changed sentence breaks, heavy editing, or a short input changed the
  two text signals. I would build a larger set of contemporary AI text and the
  edited versions of that same text, then calibrate or replace the signals on
  separate training and test sets.
- **FP05 and FP07:** Human technical writing and deliberate repetition still
  received an `ai` label. In a real system I would require human review and
  supporting evidence such as drafts or revision history before taking action.
  I would also select thresholds using a measured false-positive limit rather
  than treating the detector score as proof.
- **PI01 and PI02:** Adding instruction-like text still produced the requested
  `human` result. The GPT-2 signal is not actually following the instruction;
  the added words change predictability and style. I would add these variants
  to an adversarial calibration set instead of blocking every sentence that
  looks like an instruction, because legitimate writing can quote commands.

Criteria 2 and 3 also remain missed. The human average is `0.3947`, the AI
average is `0.4309`, and their separation is only `0.0362`. No selected
label-coverage sample reaches the `0.65` AI threshold. My next improvement
would be to recalibrate the two signals with a larger held-out dataset because
signal one ran in the wrong direction on this small set. I stopped because
Unit 8 asks for one measured change at a time, and changing weights using the
same 20 samples would overfit the test instead of proving better
classification.

The route also rejects writing without at least two Latin-alphabet words. This
is safer than giving unsupported writing a misleading AI score, but it excludes
some legitimate languages. A production version would route those requests to
a multilingual model. The rate limiter also trusts an unverified `creator_id`
and stores counts only in memory, so changing IDs or restarting the service can
bypass it.


**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I would accept more AI writing getting through in order to reduce false
accusations against real writers. The site would pay through more manual review
and some missed AI text, rather than making a writer pay for an unreliable
automated decision.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST - unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted - WRITE IT DOWN

     SUBMISSION CHECKLIST - unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack - stage AND mechanism
       [ ] One improvement, with Attack Run - After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
