# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1. False positives - Limit false AI classifications

Of 10 pieces of writing that I wrote myself, no more than 2 may be labelled
high-confidence AI in each of three trials.

**Why this target:**

Human and AI writing can share similar patterns, so I do not expect the system
to classify every piece correctly. However, more than 2 false classifications
out of 10 would make the system too unreliable. A high-confidence AI result
should trigger a human investigation, where reviewers can examine drafts,
writing progress, and other evidence instead of treating the score as proof.

---

## 2. Clear human and AI samples have separated scores

Across 10 human-written and 10 AI-generated calibration samples, the average
human score must be no higher than `0.35`, and the average AI score must be no
lower than `0.65` in each of three trials.

**Why this target:**

Clearly human and clearly AI samples should not produce nearly identical
scores. These targets place the average human sample in the human range and the
average AI sample in the AI range, creating a minimum average separation of
`0.30`. Individual mistakes are still possible and are evaluated separately
by the false-positive criterion.


---

## 3. All three labels are reachable

When three human-written and three AI-generated calibration samples with
different writing styles are tested, the results must collectively include at
least one `human`, one `unsure`, and one `AI` label in each of three trials.

**Why this target:**

Although the true origin is either human or AI, the system needs an `unsure`
label when its evidence is inconclusive. If one label is never produced, the
thresholds or scoring rule may not represent the full range of confidence.


---

## 4. Every valid appeal is recorded

In each of three trials, create a valid submission and appeal its `content_id`.
All 3 appeals must return an `under_review` status and append a matching appeal
entry to the audit log. The original decisions must remain in the log.

**Why this target:**

An appeal is the writer's protection against an incorrect classification. If
an appeal is lost or not recorded, a human reviewer may never investigate the
decision. Therefore, valid appeals need a 100% success rate.

---
## 5. Invalid submissions do not crash the service

In each of three trials, test four invalid submissions: missing text, empty
text, `null` text, and a 50,000-word submission. All 12 requests must return an
appropriate `4xx` response, never a `500`. Every rejection must be recorded in
the audit log, and `/health` must continue returning `200` after each trial.

**Why this target:**

Invalid input should produce a clear client error without crashing the service.
The four cases represent different validation failures supplied by the starter:
an absent value, an empty value, an invalid value, and an excessively large
value. Logging every rejection supports investigation, while the health check
confirms that the service remains available.


<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
