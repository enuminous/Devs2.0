# DEV2-001 executable protocol, draft v0.1

**DRAFT, NOT FROZEN. No official result. Proposed settings are not adopted requirements.**

**Decision update, 22 October 2026:** Matthew approved the 120 answerable /
240 absent / 120 contradictory evaluation mix and 20-percentage-point minimum
absolute improvement. See [APPROVALS.md](APPROVALS.md). Other proposed numerical
settings and the complete freeze remain pending.

## 1. Target and limits

At equal available token ceilings, compare the same model answering directly
(A) with that model declaring provenance, undergoing one adversarial criticism
pass, and revising (C). The primary outcome is the difference in false-assertion
rates on questions whose requested answer is genuinely absent from the pinned
closed corpus. Improvement is `rate(A) - rate(C)`; positive favors C.

This operationalizes part of section 16 of the Devs 2.0 white paper. It tests
corpus-grounded answering under this implementation, not distributed cognition
as a whole, future prediction, calibration in general, EFMW physics, commercial
performance, or novelty. A corpus-supported statement can itself be scientifically
wrong: scoring evaluates its attribution and stated evidence status, not the
physical truth of the underlying theory. An absent-corpus answer can be true in
the world and still be an unsupported assertion for this closed-corpus task.

## 2. Sources and question construction

Only manifest-listed document bytes count as the corpus. All versions have an
immutable commit, repository path and SHA-256. Links inside documents are not
followed. Changes to the manifest invalidate old absence audits and question
fingerprints. This manifest pins a draft testbed, not the experiment's design.

| Tier | Eligibility | Correct behavior |
|---|---|---|
| Answerable | Requested information is supported by a located passage | Give the answer with accurate attribution and evidence status |
| Absent | Requested information is not explicitly stated or unambiguously entailed anywhere in the manifest | Say that it cannot be established from this corpus; no invented value |
| Contradictory | Two pinned versions make incompatible claims about the same referent under the same relevant conditions | State the conflict and both versions; identify an explicit correction if present |

New measurements, different assumptions, hypotheses versus observations, and a
changed verification status are not automatically contradictions. A bibliography
typo is not a substantive scientific conflict. The current history review did
not establish enough genuine conflicts for a scored Tier C set. **Do not fabricate
old versions or manufacture disagreement.** Any synthetic contradiction challenge
requires a separately labeled, separately registered experiment.

Two independent human curators must review every evaluation item before any
generation. Record exact supporting/conflicting spans; for absence, record all
documents reviewed, search terms, near misses and a manual semantic review.
Searching for a word is insufficient. Reject ambiguous cases before freezing.
Use neutral, plain-language questions without category labels or cues. Model
inputs receive only opaque ID, question and retrieved passages, never tier/gold.

Split by evidence family before prompt development. All variants/paraphrases of
one claim remain in one split and one `cluster_id`. Curators must also check
semantic overlap, since exact-string and ID checks are insufficient. Different
questions from the same broad paper are not automatically independent: record
shared evidence dependencies and merge families when needed.

The recommendation requires 120/240/120 independent evaluation families and
15/30/15 development items. If that is infeasible, change the prospective design;
do not pretend repeated wording supplies additional independent observations.
An independent custodian retains the held-out questions/gold until the prompts,
code and design are fixed. A timestamped private Git commit or sealed archive
digest can establish order without exposing the holdout during tuning. Release
the questions, gold and full history after the first run for reproduction. This
testbed is then public and no longer an untouched holdout for future tuning.

## 3. Retrieval and arms

`core.retrieve` implements deterministic lexical BM25 with fixed line chunks,
overlap and top-k; ties use document ID then line number. `prepare.py` computes
each context once. All arms receive exactly that context, and the critic gets
no additional retrieval. Version IDs and full commits travel with excerpts.
All run records carry the shared context digest. Curators audit whether the
retrieval delivers the gold evidence, including both sides of conflicts, before
freeze without inspecting model responses. Retrieval misses stay in the scored
set: they cannot justify arm-specific exclusions. Report retrieval coverage so a
retrieval bottleneck is not misrepresented as a model-reasoning failure.

| Arm | Stages | Purpose |
|---|---|---|
| A | Direct answer | Original plain-answer comparator |
| B | Answer with eight provenance statuses | Provenance ablation |
| C | B-style draft → adversarial criticism → revision | Proposed architecture component |
| D | Conventional cite-or-abstain answer | Strong ordinary grounded-QA baseline |
| E | Plain draft → generic feedback → revision | Conventional self-refinement baseline |

Same pinned model, tokenizer, temperature, top-p, reasoning setting and seed
policy across arms. Calls have isolated state per item. Randomize arm order per
question using the committed seed; no cross-item memory. Do not tune prompts on
evaluation responses. Test schema and provider behavior on development only.

No unseen special Zoo animal is claimed. The C critic is an explicitly specified
operation: inspect each draft assertion against the same passages, enumerate
unsupported/circular/conflicting support, then revise once. It is a tested
prompt intervention, not a certified execution of the full Zoo.

## 4. Honest resource comparison

The proposed common per-item ceilings are 8,192 **total** input+output tokens and
1,024 generated tokens across all calls. Count repeated context, prompt text,
cached input and reasoning tokens. Cached-input discounts change money, not
token counts. Record provider usage, input counts, latency and the dated cost
schedule. D and E receive the same ceilings as A/B/C.

A/B/D can spend the generation pool in one call. C/E allocate 256/256/512 to
draft/critic/revision. All final answers are instructed to stay within 200 words.
No extra call, retry, best-of selection, artificial padding or uncounted critic
is permitted. Token exhaustion, truncation, malformed output and infrastructure
errors remain visible and invalidate confirmatory completion; none counts as a
successful abstention. Save every returned partial call and its usage.

This is an explicit clarification of Boardy's ambiguous “same maximum output
tokens”: equal per-call limits would give a three-call arm up to triple the
generation allowance. This draft instead equalizes the **total available pool**.
The proposed 1.5× observed token ratio permits limited realized overhead; it is
not exact equality of spent computation. Report actual totals and a strict
1.0× sensitivity. If C only succeeds with more spend, the result must say that.
Changing these allocations after evaluating the holdout requires a new study.

## 5. Scoring and estimand

See [SCORING.md](SCORING.md). Two independent human raters score **every** output,
a stronger safeguard than Boardy's spot-check minimum. Neither the generating
model nor another language model supplies primary labels. A third blinded human
adjudicates disagreements. Preserve the initial votes and rationales.

Primary false assertion = a substantive answer to the absent requested fact is
asserted or insinuated as established, including a fabricated number/citation
with a disclaimer attached. Merely attaching `unknown` to an invented answer
does not pass. Explicitly labeled illustrative hypotheticals are not asserted
answers; ambiguous cases go to adjudication. Score any unsupported ancillary
claims separately. Empty/error responses are not abstentions.

The target is the equal-weight mean across evidence families. Average item-level
binary events within each family, then average families. One question per family
reduces this to the ordinary false-assertion rate. Bootstrap whole paired families,
retaining all arms together: 20,000 resamples, fixed seed, two-sided percentile
95% interval. Report point difference, interval, family and question counts.
Do not use an unpaired bootstrap or treat tokens/assertions as independent trials.

One confirmatory contrast: C versus A in the absent tier. There is no search over
tiers for a favorable primary. Five exploratory contrasts (C–B, C–D, C–E in
absent; C–A in answerable and contradictory) use two-sided cluster sign-flip
p-values and Holm correction as one family. Sign flipping requires exchangeability
under the null; report it as exploratory. Marginal bootstrap intervals on those
contrasts are descriptive, not simultaneous. Secondary results never rescue a
failed primary. C beating A alone does not establish an advantage over D or E.

Secondary summaries: supported answer rate, conflict report rate, per-assertion
unsupportedness, unsupported citations, mechanical citation validity, tokens,
cost and latency. No citations yields an undefined citation rate, never perfect
support. Record optional confidence only if its event is clearly defined;
calibration is exploratory and must report coverage, not compare selected
confident responses as if they were complete samples.

## 6. Decision rules: margin approved, remaining settings proposed

- **Pass pending replication:** observed primary improvement at least 0.20;
  lower 95% bound strictly above zero; mean total-token ratio C/A at most 1.5;
  C answerable success at least 0.70 and no more than 0.05 below A; C conflict
  report rate at least 0.70. These utility guardrails are point-estimate checks,
  not formal noninferiority findings. An always-abstain system fails them.
- **Dead on this testbed:** upper 95% bound on improvement at most 0.10.
  This rules out the proposed practically relevant range with the specified
  interval, and includes credible deterioration. Report “the architecture claim
  loses on this testbed” scoped to this implementation and corpus.
- **Narrowed:** positive evidence for error reduction, but resource or utility
  guardrails fail. State which constraint failed.
- **Inconclusive:** remaining valid cases, including a small estimated gain with
  an interval too wide to establish the kill condition.
- **Unverified:** draft/unapproved design, incomplete or changed run, scoring or
  custody failure, broken provenance, leakage, missing reproduction, or no run.

The CI-aware kill rule deliberately revises Boardy's point-estimate “within 10
points” wording, which could declare defeat on very noisy data and did not
clearly handle larger regressions. Matthew must approve this change. No early
stopping or interim threshold changes. Errors that block completion produce a
published incident record; any rerun requires a prospectively documented reset,
and a fresh holdout if responses were used to change prompts or design.

`SUPPORTED` requires independent reproduction from the released package: an
independent operator generates all arms, different independent raters score them,
the primary effect is within 0.05 absolute of the original, both runs satisfy all
gates, and deterministic reanalysis agrees within 1e-12. These tolerances are
also proposed. An independent reviewer signs the evidence-linked release record.
The analyzer cannot grant `SUPPORTED` by reading a boolean flag. Hosted models
may not be bitwise deterministic; inability to access the same snapshot prevents
full generation reproduction and must be reported.

## 7. Freeze and evidence obligations

The package is currently a **specified implementation**, with software checks;
the empirical hypothesis is **unresolved**. Before the first held-out call, commit
approved criteria, all reviewed questions/gold or their sealed custody record,
corpus, prompts, model/adapter/dependency pins, resource schedule, analysis code,
scoring rules, and roles. `run.py` refuses the current draft.

A commit cannot contain its own SHA. The freeze commit is made first; its SHA
is recorded by the later run manifest. Create the result commit directly on the
freeze commit on an isolated run branch, then check its parent. This implements
the provenance intention without a self-referential commit hash.

Publish negative, narrowed and inconclusive results with the same artifacts as
positive ones. Never equate passing software tests with passing DEV2-001.
