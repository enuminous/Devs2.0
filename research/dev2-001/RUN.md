# DEV2-001 run report template

**TEMPLATE — NO RUN, NO RESULT, DRAFT NOT FROZEN**

Copy into a run directory. Replace placeholders only with recorded evidence.
Never present this template or synthetic test outputs as a completed experiment.

## Identity and provenance

- Run ID, date, operator: NOT RUN
- Parameter approval: 120 / 240 / 120 questions and 20-point margin approved by Matthew on 22 October 2026; see [APPROVALS.md](APPROVALS.md) in the package root. Full-protocol approval and freeze: PENDING.
- Freeze commit / result commit / result parent: NOT CREATED
- Package, corpus manifest, questions and adapter digests: NOT RECORDED
- Model snapshot, tokenizer, Python/Git and adapter environment: NOT SELECTED
- Corpus scope and held-out custody/exposure record: INCOMPLETE
- Question and independent family counts per tier: NOT CURATED
- Retrieval evidence coverage, including both conflicting versions: NOT AUDITED
- Price schedule, currency, pricing source/date: NOT SET

## Completion and scoring

- Planned / completed / invalid responses by arm: NO RUN
- Every failed/truncated call and reset decision: NONE RECORDED
- Independent rater IDs and independence evidence: NOT ASSIGNED
- Blinding method and arm-guess diagnostic: NOT ASSESSED
- Agreement, primary disagreements, third ratings and adjudication: NOT SCORED
- Mechanical citation failures versus human entailment failures: NOT SCORED

## Results (complete only from released analysis)

| Arm | Absent false assertion | Answerable success | Conflict report | Mean total tokens | Mean cost |
|---|---|---|---|---|---|
| A plain | — | — | — | — | — |
| B status | — | — | — | — | — |
| C status + critic | — | — | — | — | — |
| D cite/abstain | — | — | — | — | — |
| E generic self-refinement | — | — | — | — | — |

- Primary paired gain and 95% family-bootstrap interval: NOT ESTIMATED
- Paired outcome counts, family sizes and sparse/degenerate interval limitations: NOT ESTIMATED
- Prespecified margin, utility and cost gates: NOT EVALUATED
- Actual C/A token ratio and strict 1.0× sensitivity: NOT EVALUATED
- Five exploratory contrasts and Holm-adjusted p-values: NOT ESTIMATED
- Unsupported claims/citations; confidence coverage/Brier if present: NOT ESTIMATED
- Missing-data, leakage, drift or deviations: NOT ASSESSED

## Interpretation and independent reproduction

Verdict: **UNVERIFIED — no model experiment**.

Record the independent replay and generation-replication artifacts, operators,
raters, original/replication effect difference, gate outcomes and reviewer signoff.
No `SUPPORTED` verdict without that evidence. If the kill rule is met, report:
“The tested architecture claim loses on this testbed,” with exact scope and data.

Any eventual result concerns this model, corpus, retrieval, prompt, question
distribution and resource budget. It is **not evidence validating EFMW physics**,
industrial performance, or novelty. If D/E match or outperform C, report that
ordinary methods account for the observed benefit.
