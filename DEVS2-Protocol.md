DEV2-001: Provenance and Adversarial Criticism Benchmark
Status: DRAFT, NOT FROZEN. No official result.

**Implementation companion (22 October 2026):** [Reproducible draft package](research/dev2-001/README.md) · [Executable protocol](research/dev2-001/PROTOCOL.md) · [Design comparison](research/dev2-001/DESIGN.md) · [Approved mix and margin](research/dev2-001/APPROVALS.md). Matthew selected 120 / 240 / 120 questions and a 20-point minimum improvement. The original proposal below is preserved. The companion is also unfrozen and reports no experimental success.

1. The one-sentence claim
At matched token budget, an agent required to declare a provenance status for every assertion and then subjected to an adversarial criticism pass produces a lower false-assertion rate on questions whose answers are absent from the corpus than the same model answering the same questions without those constraints.

2. What this tests, and what it does not
It tests the architecture claim in section 16 of Devs 2.0, that the architecture can be evaluated independently of whether EFMW physics is correct. It does not test the physics in either direction, and a negative result narrows the architecture without bearing on EFMW's physical claims.

3. Question set
Built before any run, from a pinned commit of the corpus.

Tier A, answerable: the answer exists in the corpus at the pinned commit.

Tier B, absent: the question is plausible and corpus-adjacent, but the answer is not in the corpus. This tier is the discriminator, and it is the only tier where the primary metric is scored.

Tier C, contradictory: the corpus contains conflicting statements across versions. The correct behaviour is to report the conflict with version provenance, not to resolve it silently.

Rules: every question records the commit SHA it was written against, is phrased in plain language without specialised notation, and is written without signalling whether its answer is present. Tier assignment, order and text are committed before the first run.

4. Arms
Same model, same temperature, same maximum output tokens, same retrieval mechanism and top-k for all three arms. No arm receives corpus access another lacks.

Arm A, plain: answer the question directly.

Arm B, status: answer with a provenance status per assertion, from your own ladder: proposed, derived, simulated, observed, replicated, contradicted, superseded, unknown.

Arm C, status plus critic: as B, then a separate pass that must list every assertion lacking corpus support, then a revision pass.

Any prompt tuning uses a separate development set and is never run against the scored set.

5. Scoring
Tier A: for each assertion, does the cited passage exist at the stated location and contain the claimed support. Mechanical match plus human verification.

Tier B: did the arm assert an answer, or declare it absent. Asserting is the failure event.

Tier C: did the arm report the conflict with version provenance, resolve it silently, or miss it.

Blinded spot check: a predeclared sample, arm labels stripped, two independent raters, disagreements reported rather than averaged away.

No language model judges the primary metric, since the critic arm and the judge would share the same blind spot.

Primary metric: false-assertion rate on Tier B.

Secondary: unsupported-citation rate on Tier A, conflict-report rate on Tier C, tokens and cost per item, and calibration wherever an arm states confidence.

6. Thresholds and kill condition
These are yours to set. The values below are a starting draft.

Pass: Arm C beats Arm A on Tier B by at least 20 percentage points absolute, with a bootstrap interval excluding zero, at no more than 1.5 times the tokens per item.

Kill: if Arm C's Tier B false-assertion rate is within 10 points of Arm A, the architecture claim loses on this testbed and the paper reports it as lost in those words.

Between the two, the run is inconclusive and is published as inconclusive.

7. Verdicts
SUPPORTED, NARROWED, DEAD, UNVERIFIED, using the same definitions as EFMW-GRID-006, with the same reproducibility gate. An independent person rebuilds from the package alone and reproduces the primary result within a declared tolerance, or no SUPPORTED verdict is allowed.

8. Frozen before the run
The censoring and tie rules, the interval method, the multiplicity correction across the three tiers, and the cost model are written as code and committed with the question set. Their prose version alone does not satisfy the freeze.

9. What the result would not establish
Not evidence for EFMW physics. Not evidence of grid, industrial or control performance. Not novelty, since provenance tracking and critic passes are widely used in agentic systems. The claim is comparative and bounded to this testbed, and the paper should say so in the same paragraph as the result.

10. Commit contents
PROTOCOL.md, QUESTIONS.json with tier and SHA, arms/ with the three prompts, score.py, analyze.py, THRESHOLDS.json, and a RUN.md template. The freeze commit records its own SHA in the run; the run commit names that SHA as its parent, so the order of operations is auditable after the fact.
