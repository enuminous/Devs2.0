# Design comparison and approval status

**Matthew approved the 120 / 240 / 120 mix and 20-point minimum improvement on 22 October 2026. The follow-up implementation selects the resource/context policy and a 12-point replication tolerance; the experiment is not frozen.**

## Question allocation

Keep development and evaluation separate. A useful development target is 60
items (15 answerable, 30 absent, 15 contradictory), with no evidence-family
overlap with evaluation. Twelve initial development examples are supplied;
they are not independently reviewed or a completed development set.

For a fixed evaluation total of 480 independent evidence families:

| Design | Answerable / absent / contradictory | Approximate primary 95% half-width | Tradeoff |
|---|---:|---:|---|
| Balanced | 160 / 160 / 160 | 10.5 percentage points | Best coverage of all three categories; weakest primary precision of these choices |
| **Selected by Matthew** | **120 / 240 / 120** | **8.6 points** | Half the sample addresses the primary claim while retaining substantial utility checks |
| Primary-heavy | 60 / 360 / 60 | 7.0 points | Tighter primary estimate; poor precision for answerability and conflict safeguards |

These are planning approximations, not power guarantees. For paired binary
outcomes let `D = false_A - false_C`, true gain `delta = E[D]`, and discordance
`q = P(D != 0)`. Then `Var(D) = q - delta^2` and approximate standard error is
`sqrt((q-delta^2)/n)`. The table assumes `delta=0.20`, `q=0.50`, independent
families and one item per family. `planning.py` reproduces it. With 240 absent
families and discordance 0.25/0.50/0.75, the approximate half-widths are
5.8/8.6/10.7 points. Actual precision depends on the joint paired outcomes.

For the secondary categories, worst-case single-arm binomial half-widths are
about 7.7 points at n=160, 8.9 at n=120 and 12.7 at n=60. A 5-point answerability
guardrail is therefore an operational point-estimate screen; this design does
not establish 5-point noninferiority with high precision. A formal noninferiority
claim would need a separately powered, registered analysis.

If questions are correlated, nominal question count overstates information.
For example, four related variants per family at intrafamily correlation 0.5
give a design-effect approximation of `1+(4-1)*0.5=2.5`: 240 rows contain roughly
96 independent-item equivalents under that heuristic. The implemented bootstrap
resamples whole evidence families, and the recommended freeze gate requires
240 **distinct absent families**, not just 240 differently worded questions.
Dependence across families remains a limitation to audit, not something a
bootstrap can automatically repair.

The current ten-version corpus may be too small for 120 substantive conflict
families. Matthew has selected that target, but an evidence inventory must still
establish feasibility before freeze. Options are to expand the pinned corpus with
authentic versions, or obtain approval for a revised sample mix and acknowledge
weaker Tier C precision. This is a curation problem, not a
reason to synthesize conflicts and call them historical facts.

## Pass margin

| Absolute margin | Example baseline 40% → C at threshold | Interpretation |
|---|---|---|
| 10 points | 40% → 30% | Detects a modest gain; change the proposed 10-point kill boundary to avoid an overlapping pass/kill definition |
| **20 points — selected by Matthew** | **40% → 20%** | Meaningful reduction in unsupported answers; adopts Boardy's suggested margin |
| 30 points | 40% → 10% | Demands a large effect and makes floor effects more likely |

All choices should also require a 95% paired interval excluding zero, resource
compliance and usefulness. A 20-point absolute improvement is not a 20% relative
reduction: 40% to 20% is a 50% relative reduction. If baseline error is below
20%, a 20-point improvement is unattainable. A strong ordinary baseline may
already handle absence well; that is an informative result, not a reason to
weaken it. Development-only estimates can inform a revised design **before**
freezing; never select the threshold after examining held-out outcomes.

The draft combines the approved margin with an uncertainty condition:
**observed gain >=20 points and interval above zero**. The margin approval alone
does not finalize the full decision rule.
It is not “the true gain is at least 20 points.” To substantiate that stronger
claim the lower bound would have to exceed 20 points. Under a symmetric normal
approximation, an experiment whose true gain is exactly 20 points has roughly
50% probability of meeting an observed 20-point cutoff, even with a precise
positive interval. Increasing n cannot make a boundary effect exceed its own
cutoff with 80–90% probability. At n=240, q=0.5, approximate probabilities of
meeting the numerical 20-point/positive-CI rule are 1.3%, 50%, and 99.2% for true
gains of 10, 20, and 30 points. Utility, cost and replication gates can only reduce
those probabilities. These calculations are not observations of this model.

The percentile bootstrap is a pragmatic specified method, not exact finite-sample
coverage. Sparse discordant families and boundary rates can yield degenerate
intervals; publish the paired counts and those limitations. Do not switch interval
methods after seeing which one passes.

## Failure rule and efficiency

Recommend a **CI-aware kill boundary**: upper 95% bound <=10 points. This can
support a conclusion that the proposed practically meaningful advantage failed
on this testbed. An observed gain <=10 with a wide interval is inconclusive.
Boardy's original “within 10 points” rule used a point estimate and was ambiguous
about larger negative effects. This modification is explicit and unapproved.

Recommend keeping the proposed **1.5× observed total-token cap** for the limited
overhead claim, with equal available ceilings and all calls counted. Also report
the strict 1.0× result. A 1.5× cap cannot support wording that actual consumption
was equal. The conventional E arm matches the critic arm's number of calls and
stage allocation; D tests whether a simple cite-or-abstain instruction does the
work. Passing C versus A while tying D or E supplies no EFMW-specific advantage.

Recommended additional guardrails, also unapproved: answerable success >=70%,
no more than a 5-point drop versus A, and conflict reporting >=70%. These prevent
success by universal refusal. The follow-up selects a **12-point absolute
independent-replication tolerance**, the stricter edge of Matthew's requested
12–15-point range, replacing the original 5-point proposal. With n=240 independent
absent families, effect .20 and discordance .50, one estimate has planning
SE=sqrt((.50-.20²)/240)=4.38 points. Assuming independent estimates, their
difference has SE=6.19 points. A normal approximation puts about 58%, 95% and
98% of differences inside ±5, ±12 and ±15 points respectively. These are
illustrations, not measured reproducibility rates; dependence between repeated
runs on the same items changes the calculation. Family clustering, provider
variability and rater variation also matter. Twelve points allows plausible
sampling variation while being stricter than fifteen. Both runs must still pass
the original 20-point, interval, utility and cost gates with the same positive
direction. This agreement rule does not prove equivalence or interval coverage.

## Known-method comparison

The benchmark combines established ideas; no novelty claim follows from naming
them EFMW. [Rajpurkar, Jia and Liang (ACL 2018)](https://aclanthology.org/P18-2124/)
use plausible unanswerable questions to test abstention. [Gao et al. (EMNLP
2023)](https://aclanthology.org/2023.emnlp-main.398/) evaluate generated answers
and citation quality in ALCE. [Madaan et al., Self-Refine
(2023)](https://arxiv.org/abs/2303.17651v2) study feedback and revision by the same
model. These are adjacent methodological precedents, not evidence that this
implementation works. D and E are simple conventional comparators inspired by
these general methods, not claimed reproductions of those papers' full systems.

## Decision record

Matthew's explicit selections on 22 October 2026 are recorded in
[`APPROVALS.md`](APPROVALS.md) and `THRESHOLDS.json.parameter_approvals`:
120 answerable / 240 absent / 120 contradictory questions, and a 20-percentage-point
minimum absolute improvement. The alternatives above were not selected. The
follow-up instruction authorizes the resource/context fixes and widening the
replication tolerance; their exact implementation is recorded in `APPROVALS.md`.
Matthew also requested freeze and tagging, but the reviewed holdout and runtime/
scoring pins do not yet exist. Publish a draft checkpoint, not a fictitious freeze.
Do not change `status` to
`FROZEN` until the remaining decisions and every gate in `REPRODUCIBILITY.md`
are complete. Any later parameter revision needs its own prospective record.
