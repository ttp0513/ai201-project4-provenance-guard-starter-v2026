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

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

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
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

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

### Signal two — the style signal

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

AI helped me move faster, but I stayed responsible for the requirements,
design choices, testing, and final explanation.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

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
differently — one script can look like a thousand callers, and one household
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

## Attack Run — Before

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
| MF01 | malformed | whitespace only | 400 | — | — | HELD |
| MF02 | malformed | single character | 400 | — | — | HELD |
| MF03 | malformed | control characters | 200 | human | 0.250 | BROKE |
| MF04 | malformed | punctuation only | 200 | unsure | 0.431 | BROKE |
| MF05 | malformed | very long single word | 200 | ai | 0.824 | BROKE |
| MF06 | malformed | emoji only | 200 | ai | 0.923 | BROKE |
| MF07 | malformed | right-to-left script | 200 | ai | 0.944 | BROKE |
| MF08 | malformed | 60,000 characters | 200 | ai | 0.797 | BROKE |
| RQ01 | malformed request | no text field | 400 | — | — | HELD |
| RQ02 | malformed request | no creator ID | 400 | — | — | HELD |
| RQ03 | malformed request | text is a number | 400 | — | — | HELD |
| RQ04 | malformed request | text is a list | 400 | — | — | HELD |
| RQ05 | malformed request | text is null | 400 | — | — | HELD |
| RQ06 | malformed request | creator ID is an object | 400 | — | — | HELD |
| RQ07 | malformed request | body is a JSON array | 400 | — | — | HELD |
| RQ08 | malformed request | unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed request | empty body | 400 | — | — | HELD |
| RQ10 | malformed request | form-encoded body | 400 | — | — | HELD |
| RQ11 | malformed request | JSON sent as plain text | 429 | — | — | HELD |
| RQ12 | malformed request | deeply nested JSON | 400 | — | — | HELD |
| FL01_01 | flood | request 1 from one creator | 200 | human | 0.322 | HELD |
| FL01_02 | flood | request 2 from one creator | 200 | human | 0.322 | HELD |
| FL01_03 | flood | request 3 from one creator | 200 | human | 0.322 | HELD |
| FL01_04 | flood | request 4 from one creator | 200 | human | 0.322 | HELD |
| FL01_05 | flood | request 5 from one creator | 200 | human | 0.322 | HELD |
| FL01_06 | flood | request 6 from one creator | 200 | human | 0.322 | HELD |
| FL01_07 | flood | request 7 from one creator | 429 | — | — | HELD |
| FL01_08 | flood | request 8 from one creator | 429 | — | — | HELD |
| FL01_09 | flood | request 9 from one creator | 429 | — | — | HELD |
| FL01_10 | flood | request 10 from one creator | 429 | — | — | HELD |
| FL01_11 | flood | request 11 from one creator | 429 | — | — | HELD |
| FL01_12 | flood | request 12 from one creator | 429 | — | — | HELD |

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

**The single worst outcome** — the one I'd least want to explain to a writer
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
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

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
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
