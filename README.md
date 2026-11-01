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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



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
