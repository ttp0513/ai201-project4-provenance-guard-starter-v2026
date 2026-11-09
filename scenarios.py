"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

    "appeal"  one submission and the reason for appealing it. `run_eval.py`
              submits the text, appeals the returned content_id, and confirms
              that both entries appear in the audit log.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # These are ten pieces I wrote myself in different settings. Keeping
        # the original grammar and punctuation makes this a test of my actual
        # writing instead of polished versions of it.
        "texts": [
            """When I think about healthcare technology, I usually focus on electronic health records, clinical decision-making, or the growing use of AI. However, I had not given much thought to how different hospital systems communicate behind the scenes, even for something as routine as checking in for an appointment. This made me interested in understanding how Health Level Seven (HL7) standards support everyday healthcare operations.
HL7 plays an important role in exchanging information between healthcare systems, from admission, discharge, and transfer (ADT) notifications to laboratory results and appointment scheduling. Its widespread use is reflected in a report from the Office of the National Coordinator for Health Information Technology (ONC, 2024), which found that 90% of surveyed health information exchange organizations routinely received HL7v2 ADT messages. Similarly, Armson et al. (2025) highlighted the importance of data standards throughout laboratory workflows, from ordering tests to sharing results with providers and public health agencies.""",
            """One important distinction is that FHIR was not designed to simply eliminate older HL7 standards. Many healthcare organizations still depend on Version 2 interfaces, while FHIR provides additional opportunities for modern application integration and data access. The continued use of multiple HL7 standards demonstrates that interoperability is an ongoing process rather than a single technology upgrade.
Ultimately, understanding the differences between v2, v3, and FHIR is important for HIT professionals because healthcare organizations must often support legacy systems while adopting newer technologies. Knowing how these standards work together can help IT professionals make better integration decisions and improve the exchange of information across healthcare environments.""",
            """I was exploring the new map area and I finished exploring it in about two hours. IDK why but i feel like genshins map design is just getting sloppier and worse. The new area boring to explore, and many of the cool areas like the palace of glacial reflections being super empty. Im also sooo dissapointed with the old kitzegrad map too, just reptetive ruin exploration with nothing fun. I miss the fontaine days where the environment and the map design was actually unique and fun to explore, rather than the maps that we have now days.""",
            """I have c1 yae miko and c1 mizuki. Issue is I have neither of their weapons…. (I have an r3 widsith being traded back and forth)
Short story: I summoned for yae even though I was afraid they were going to replace her in the stellar team, because of that fear I didn’t try for her weapon. As for mizuki I knew I’d get her for free and I never thought they were going to make a standard character do decent damage much less meta damage so I thought her weapon would be a pointless upgrade.
QUESTION: is mitya weapon worth pulling for either mizuki or yae (obvious for stellar team)? I assume yae if either of them but I don’t know…. Can someone compare it to widsith and to their signature?? (Also I guess I have to ask would it be worth taking the chance with furina’s weapon being the other on the banner)
Thank you!!""",
            """I've been tracking job posts on companies' own career sites every day for a few weeks. A few checks that save a lot of wasted applications:

1. Find the job on the company's own careers page, not only on a job board. If it's gone from there, it's almost certainly gone.
2. Look at how long it's been up. About 37% of open jobs I see have been up 60+ days. Some are slow hires, some are ghosts, so weigh it, don't skip it automatically.
3. If a job you applied to disappears, search the company's page for the same title. Almost 1 in 5 jobs that come down get posted again, usually the same day, with a new date.
4. Apply in the first week. New posts are the ones that disappear fastest: of jobs posted in the past week, 36.5% were gone within two weeks.

What's your own rule for deciding a job is worth the time?""",
            """I’ve decided to add this statement at the top of all my writings.
“100% Human Written.”
Why? You ask.
Here’s why. I’m fully aware that most of what I read online these days is at the very least AI-assisted, if not entirely written by AI. Generally, I don’t mind. My main concern is whether what I’m reading is accurate or not. If I want to know how to operate my toaster, I don’t need to be assured that a human wrote the instructions. But when it comes to art and journalism, come on! With poetry, prose, etc., the whole point is the masterful placing of words in sentences, in paragraphs for the enjoyment and stirring of the reader.""",
            """Marketers spend a lot of time talking about optimization. We optimize campaigns, landing pages, bidding strategies, and budgets. The word promises an improvement, which makes it easy to agree with. But I think we often skip the question that gives it meaning: **optimize for what?**
A campaign that produces more conversions can earn less profit. A plan that improves return on ad spend (ROAS) can leave potential sales behind. Neither result automatically means the analysis failed. The answer depends on which outcome the analysis was asked to favor.""",
            """Let’s start with **Search** on its own, using an illustrative response curve. Revenue increases as spending rises, but each additional dollar produces a smaller increase. With a $60,000 spending limit, maximizing revenue means spending the full budget. Maximizing profit produces a different answer: about $21,700 a month. The next dollar explains the difference. Beyond the profit-maximizing point, each additional ad dollar brings back less than a dollar in contribution, which is revenue multiplied by margin. Revenue still grows, but profit falls. At the interior optimum shown here, marginal contribution equals one dollar per advertising dollar, so marginal profit is zero.""",
            """Whether it’s in the job requirements or in how the company describes itself, it’s clear that most companies hiring data scientists want to be seen as investing in AI.
And if we look deeper, in about half of all postings, **companies are clear that they expect their candidates to have AI skills or to work on AI projects**, many of them mentioning a specific skill like LLMs, RAG, or AI agents.
What’s important to notice is that most of these aren’t AI-specific roles. Only 13% of postings have “AI” in the job title, which means that for about half of the market, AI skills are simply just part of being a Data Scientist.""",
            """AI has been a steady part of **about half of all postings since February 2026**. What’s changing is which AI skills companies ask for.
On one side, AI agents, AI coding tools (like Claude Code, Cursor, or Copilot), and MCP show up in more postings this fall than they did earlier in the year.
“Evaluation” also rose, from about 20% to 25% of postings, making it the fastest-rising keyword I tracked. And with more companies building AI systems, my bet is that knowing how to evaluate them will only become more important.
On the other side, **PyTorch and TensorFlow dropped from about 16% to 11% of postings each**, which is the most consistent change in the entire dataset. Now, to be clear, that doesn’t necessarily mean people are using them less, just that a smaller share of postings list them.""",
        ],
    },
    {
        "name": "score spread - AI writing",
        "criterion": 2,
        # These ten samples were generated by AI for a known-origin comparison
        # with my ten human samples. Their topics and lengths are similar so
        # the comparison is not based only on subject or submission size.
        "texts": [
            """Healthcare organizations use many different systems to manage patient information, including electronic health records, laboratory platforms, scheduling tools, and billing applications. Interoperability standards allow these systems to exchange information without requiring every organization to build a completely unique connection. HL7 messages can support common activities such as patient admissions, laboratory orders, and discharge notifications. When these messages are implemented consistently, clinicians and administrative staff can access information more efficiently. However, technical standards alone do not guarantee successful communication. Organizations must also maintain accurate data mappings, monitor interfaces, and resolve differences in how systems interpret individual fields. Effective interoperability therefore depends on both shared standards and careful implementation.""",
            """FHIR provides healthcare developers with modern methods for accessing and exchanging clinical information. Its use of web-based technologies makes it suitable for mobile applications, patient portals, and services that need specific pieces of health data. However, adopting FHIR does not mean that organizations can immediately remove their existing HL7 Version 2 interfaces. Many hospitals continue to rely on older systems that support important workflows and cannot be replaced quickly. As a result, healthcare IT teams often manage several standards at the same time. They may use Version 2 for established hospital interfaces while introducing FHIR for new applications. Understanding how these standards complement each other helps organizations modernize without interrupting essential services.""",
            """I finished exploring the latest game region much faster than I expected, and the experience felt less memorable than earlier areas. The environment looked impressive from a distance, but many locations had little to discover once I reached them. Several large buildings appeared important but contained few rewards, characters, or useful interactions. The repeated ruins also made different parts of the map feel too similar. Older regions gave me more reasons to stop, explore side paths, and pay attention to environmental details. The new area is not completely bad, but it feels as though visual scale received more attention than meaningful exploration. I hope future updates make smaller locations feel more distinct and rewarding.""",
            """I am trying to decide whether a limited weapon is worth pulling for two characters on my account. Both characters can use the weapon, but I already have a strong four-star alternative that they currently share. The limited weapon would improve their damage, although getting it could require a large number of wishes. The second weapon on the banner is also not especially useful for my account, which makes the decision riskier. I am leaning toward saving because neither character requires the upgrade to clear the content I play. However, I would consider pulling if the improvement is significant for both characters instead of only being valuable in one specific team.""",
            """A job posting is more useful when it can be confirmed on the employer’s official careers page. Third-party job boards may continue displaying positions after the company has stopped accepting applications. The posting date also provides useful context, although an older listing is not automatically inactive. Some companies keep positions open during long hiring processes or while considering candidates for several teams. Applicants should also watch for jobs that disappear and return with a new identification number or posting date. This may indicate that the requirements changed or that the original search was restarted. Checking these details cannot guarantee a response, but it can help applicants spend more time on opportunities that appear active.""",
            """Adding a statement that says an article was written by a person may communicate the author’s values, but the statement cannot verify authorship by itself. Anyone can attach the same declaration to human, AI-assisted, or completely generated writing. Readers may care less about authorship when they need straightforward factual instructions, provided that the information is accurate and safe. Creative work presents a different concern because personal expression and deliberate language choices are part of its value. Even then, a simple label does not explain whether AI was used for brainstorming, editing, or drafting. Meaningful transparency requires more context about the writing process rather than an unsupported claim at the top of the page.""",
            """Marketing optimization begins with defining the outcome that matters to the organization. Increasing conversions may appear successful, but additional sales do not always produce additional profit. A campaign can attract customers through expensive discounts or advertising costs that exceed the value of the resulting purchases. Return on ad spend provides another useful measurement, although maximizing it may cause a company to avoid profitable opportunities with lower ratios. Analysts must therefore understand whether the goal is revenue, profit, customer acquisition, or long-term growth. The mathematical process can only optimize the objective it receives. If the business question is unclear, a technically correct model may still recommend a strategy that does not support the company’s actual priorities.""",
            """A response curve describes how advertising results change as spending increases. Early investments may produce strong returns because they reach the customers most likely to respond. As the budget grows, each additional dollar generally creates a smaller increase in revenue. A company focused only on revenue may continue spending until it reaches its full budget. Profit optimization can produce a lower spending level because advertising costs must be compared with the contribution generated by additional sales. The profit-maximizing point occurs when the expected contribution from the next advertising dollar equals its cost. Spending beyond that point can continue increasing total revenue while reducing profit. This distinction explains why different objectives can recommend different budgets using the same response curve.""",
            """Artificial intelligence skills increasingly appear in data-science job descriptions, even when the position title does not mention AI. Employers may expect candidates to understand language models, retrieval systems, model evaluation, or automated workflows alongside traditional statistical methods. This does not necessarily mean that every data scientist will build large AI models from the beginning. Some roles may focus on integrating existing services, measuring output quality, or preparing reliable data for AI applications. Job seekers should therefore read the responsibilities instead of relying only on the title. A general data-science position may include substantial AI work, while an AI-branded role may focus more heavily on software engineering, infrastructure, or product implementation.""",
            """The AI skills requested by employers can change as organizations move from experimentation to production. Early projects may emphasize model training and familiarity with deep-learning frameworks. Later projects often require evaluation, monitoring, retrieval, agent workflows, and tools that help developers build applications around existing models. A decrease in mentions of a particular framework does not necessarily mean that the technology is disappearing. It may instead indicate that employers consider the skill standard, use managed services, or are hiring for different stages of the AI lifecycle. Tracking job descriptions over time can reveal changes in stated demand, but those changes should be interpreted carefully. Posting frequency reflects employer language and priorities, not a complete measurement of actual workplace usage.""",
        ],
    },
    # A bad-input criterion looks like this. Uncomment and adjust if that's one
    # of your five — these are raw request bodies, sent exactly as written.
    #
    # {
    #     "name": "bad input",
    #     "criterion": 3,
    #     "bodies": [
    #         {"text": "", "creator_id": "eval_bad_empty"},
    #         {"creator_id": "eval_bad_missing"},          # no text field at all
    #         {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
    #         {"text": None, "creator_id": "eval_bad_null"},
    #     ],
    # },

    # TODO: add what your remaining criteria need.
    #
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
]

# Criterion 2 compares the same ten personal samples with the ten AI samples.
# Reusing the list keeps the human half identical to Criterion 1 without
# copying the writing a second time in this file.
SCENARIOS.insert(1, {
    "name": "score spread - human writing",
    "criterion": 2,
    "texts": SCENARIOS[0]["texts"],
})

# Criterion 3 uses three human samples followed by three AI samples. The
# samples cover formal, casual, instructional, and analytical writing styles.
SCENARIOS.append({
    "name": "label coverage",
    "criterion": 3,
    "texts": [
        SCENARIOS[0]["texts"][0],  # human: formal healthcare writing
        SCENARIOS[0]["texts"][2],  # human: casual gaming criticism
        SCENARIOS[0]["texts"][4],  # human: numbered job-post advice
        SCENARIOS[2]["texts"][0],  # AI: formal healthcare explanation
        SCENARIOS[2]["texts"][2],  # AI: polished gaming criticism
        SCENARIOS[2]["texts"][6],  # AI: marketing optimization
    ],
})

# Criterion 4 needs a real content_id, so the evaluator must submit the text
# before it can appeal. Each trial creates a new decision and checks that the
# original decision and the new appeal both remain in the audit log.
SCENARIOS.append({
    "name": "appeal path",
    "criterion": 4,
    "appeal": {
        "text": SCENARIOS[0]["texts"][0],
        "reasoning": "I wrote this submission and request a human review.",
    },
})

# Criterion 5 sends the four invalid request bodies named in criteria.md. The
# evaluator also confirms that every rejection reaches the audit log and that
# the service remains healthy after each trial.
SCENARIOS.append({
    "name": "bad input",
    "criterion": 5,
    "bodies": [
        {"creator_id": "eval_bad_missing"},
        {"text": "", "creator_id": "eval_bad_empty"},
        {"text": None, "creator_id": "eval_bad_null"},
        {"text": "word " * 50_000, "creator_id": "eval_bad_huge"},
    ],
    "check_rejection_log": True,
    "check_health": True,
})


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")
        appeal = scenario.get("appeal")

        if sum(bool(value) for value in (texts, bodies, appeal)) > 1:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has more than one "
                "scenario type — pick texts, bodies, or appeal"
            )
            continue

        if appeal:
            if not isinstance(appeal, dict):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}') appeal is not a dict"
                )
                continue
            if not isinstance(appeal.get("text"), str) or not appeal["text"].strip():
                problems.append(f"scenario {i} appeal has no usable text")
            if (
                not isinstance(appeal.get("reasoning"), str)
                or not appeal["reasoning"].strip()
            ):
                problems.append(f"scenario {i} appeal has no usable reasoning")
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
