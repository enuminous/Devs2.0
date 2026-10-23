# Methods questions for independent review

Use the pinned `PROTOCOL.md`, `DESIGN.md`, `CONFIG.json`, `THRESHOLDS.json`,
`analyze.py`, `core.py`, `SCORING.md` and `APPROVALS.md` together. Return a short memo
classifying each item as acceptable, blocking, amendment proposed, or not inspected.
No entry below is a reviewer conclusion.

## Question validity and dependence

- Can the closed corpus support the selected 120 answerable / 240 absent / 120
  contradictory evaluation items with the proposed independent-family minima?
  The holdout is empty. Public development has six answerable and six absent
  candidates, and no eligible conflict is established.
- Do the absence audits establish semantic absence across all ten versions, rather
  than failure to find a keyword? Are near misses or questions with ambiguous
  requested referents excluded prospectively?
- The development set uses 12 unique cluster IDs, but six items share the Devs
  paper, three F001, two the grid study, and one R-001. These are dependency leads,
  not certified independent families or an instruction to merge every paper's
  claims. Examine common premises, source passages, calibration choices and
  experiments. Preserve related variants in one split; do not pad sample counts.
- Review stylistic category cues, selection bias from a largely single-author
  corpus, scope of generalization, and evidence-family exposure during prompt tuning.
- Check that deterministic BM25 supplies both relevant versions for conflict
  candidates. Retrieval misses must remain visible under the common scoring rules.

## Statistical validity

- Confirm the primary estimand: equal-weight evidence-family mean of absent-tier
  false-assertion differences A minus C. The code retains paired arms when resampling
  whole families (20,000 draws). Assess residual cross-family dependence, sparse
  discordance, percentile-interval coverage and potential degeneracy before freeze.
- The selected 20-point gain is an observed threshold plus an interval above zero;
  it is not a lower confidence bound above 20 points. Baseline error below 20%
  makes that gain unattainable. Examine development-only headroom without tuning
  the held-out benchmark to force a pass.
- `PLANNING_OUTPUT.json` is generated from the existing planning code. With 240
  independent absent families, assumed gain .20 and discordance .50, the normal
  approximate 95% half-width is 8.6 points and the chance of meeting a cutoff at
  the true effect is about 50%. These are assumptions, not empirical power results.
- Assess the five exploratory contrasts, their cluster sign-flip exchangeability
  assumption and joint Holm correction. No secondary comparison rescues a failed
  primary. C versus A alone does not demonstrate advantage over ordinary D/E controls.
- Utility gates (70% answerability/conflict success and at most five-point
  answerability loss) are proposed point-estimate screens, not a powered
  noninferiority claim. The CI-aware kill rule, 1.5× resource cap and full rule
  package still require the decisions recorded as pending in `APPROVALS.md`.
- Check actual input/output/reasoning and repeated-context accounting, the observed
  A denominator, no retries, fixed C/E stage allocations, and the 1.0× sensitivity.
  Equal available ceilings do not mean equal realized expenditure.
- Review the selected 12-point replication agreement rule and both-run pass gates.
  Same questions, model/provider drift and new raters induce dependencies not
  captured by the illustrative independent-normal calculation. Agreement within
  tolerance does not by itself establish equivalence or adequate precision.
- Confirm handling of malformed/truncated/error outputs, incomplete rosters,
  missing labels, custody failure and resets: no imputation, response-selected
  exclusions, optional stopping or automatic `SUPPORTED` classification.

## Independent reproduction and reviewer independence

Distinguish environment reconstruction, deterministic analysis replay (tolerance
1e-12), and a new full generation run with fresh blinded human scoring. Record any
work that prevents the reviewer from later being described as independent of that
component. If substantial design/code authorship occurs, document it and arrange
an additional independent release review where needed. KALEI automation may assist
secondary checks but cannot replace the specified primary human judgments.
