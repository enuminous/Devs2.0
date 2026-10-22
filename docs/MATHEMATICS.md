# Mathematical companion to Devs 2.0

**Scope:** architectural models, not a physical theory. The September paper is a conceptual proposal, not a complete system of equations. The definitions below are new, explicit operationalizations using conventional set theory, likelihood updating, graph order, filtering, and paired statistics. They do not establish novelty. Each theorem is visible in [`theorems.json`](theorems.json), the desktop, and the corresponding Lean source.

## Possibilities and CollapseΩ

For a universe X, let Ω be a predicate X → Prop and E an externally supplied evidence constraint. Define

\[
U(\Omega,E)(x)=\Omega(x)\land E(x),\qquad
A(\Omega,N)(x)=\Omega(x)\lor N(x).
\]

Intersection cannot add a possibility, satisfies E, is idempotent, and commutes with another fixed constraint. Inconsistent constraints may empty the space. Expansion can admit new hypotheses explicitly. These are theorems in [`Possibility.lean`](../Devs/Possibility.lean). They do not establish that E is reliable or complete. “Collapse” here is an operational restriction, not quantum measurement. Revision of a mistaken constraint may enlarge the viable space; monotonic narrowing is not a universal model of learning.

## Uncertainty and likelihood

For nonnegative weights and likelihoods,

\[
w'_i=w_iL_i,\qquad Z=\sum_iw'_i,\qquad p'_i=w'_i/Z\quad (Z>0).
\]

The browser uses finite floating-point numbers, validates nonnegative priors and likelihoods in [0,1], and refuses Z=0. It displays Shannon entropy H(p)=−Σ pᵢ log₂pᵢ. A surprising observation can increase entropy. A zero prior stays zero, so new possibilities require expansion rather than multiplication alone.

[`Uncertainty.lean`](../Devs/Uncertainty.lean) proves the unnormalized **natural-number** support laws, positivity, neutral evidence, and composition/commutation of supplied likelihoods. It does not formalize real normalization, floating-point error, conditional independence, calibration, or entropy. Sequential multiplication is a numerical rule; interpreting separate likelihood factors as Bayesian evidence requires an appropriate joint/conditional model. The UI's tests are computational checks and are not a refinement proof from JavaScript to Lean.

## Provenance and noncircular support

A citation records document, immutable revision, and line range. A claim has one of eight explicit statuses. The formal definition of observed evidence requires an observed/replicated status and a well-formed citation; proposed, simulated, and derived statuses do not satisfy it. This proves a type-level distinction, not that a reference is true, entailed, independently observed, or even present on a real server.

For dependency edge u → v, impose rank(u) < rank(v). Every nonempty path strictly increases rank, so no directed cycle can exist. [`Provenance.lean`](../Devs/Provenance.lean) proves this induction. Whether the rank assignment describes the real dependency graph is an external obligation. Repeated agreement or a circular chain of references supplies no independent experiment.

## Criticism and its limit

For a list S and Boolean acceptance rule c, define F(S,c)=filter(c,S). A survivor belonged to S and satisfies c; repeating the same filter is idempotent. If one separately establishes ∀x, c(x)=true → TrueClaim(x), survivors are true. The soundness premise is explicit and is not obtained by calling the rule a “critic.”

[`Criticism.lean`](../Devs/Criticism.lean) also proves a counterexample: filtering [true,false] by negation leaves [false]. Another example preserves a false claim under unanimous acceptance. There is no theorem that arbitrary criticism improves accuracy. DEV2-001 tests that empirical question for specific prompts, model, corpus, and budget. Its generative revision can introduce new claims; the no-invention theorem applies only to the **filter model**, not to arbitrary LLM revision.

## Human authorization

A proposal contains an action identifier and revision. An authorized value contains proof of an external permission predicate for that exact proposal; execution requires that value. [`Agency.lean`](../Devs/Agency.lean) proves permission is required and an approval for a different revision does not match. The permission predicate, identity, credential checks, and enforcement in a real service are external to this model. The desktop does not execute privileged actions and is not a deployed authorization kernel.

## Resource accounting

For each stage s, Tₛ=Iₛ+Oₛ and 0≤Cₛ≤Iₛ, where C is cached input. Total spend is ΣTₛ. Cached input is still input, even if its monetary price differs. Generated reasoning tokens must be included in O. [`Budget.lean`](../Devs/Budget.lean) proves monotonic spending, a bounded next step when spent≤cap, and equality of the 256+256+512 and 1024 output pools. Correct provider tokenization and complete accounting remain empirical/interface obligations.

All arms have the same **available** 8192-token total ceiling and 1024-token generation pool. They need not consume identical totals. The proposed efficiency ratio is C's total observed tokens divided by A's on the same complete roster. Median/p95 usage and cached totals are additionally reported. A 1.5× ceiling does not establish strict equal consumption; a separate 1.0× sensitivity is reported.

## Paired benchmark estimand

Let Y_A,Y_C be independently human-scored false-assertion indicators on an absent question, and D=Y_A−Y_C∈{−1,0,1}. The target is the equal-weight mean of family-level mean D values. With one independent item per family, δ=E[D], q=P(D≠0), and Var(D)=q−δ². The planning standard error is √((q−δ²)/n). The production analysis resamples **paired evidence families**, not individual arms or paraphrases.

At n=240, δ=.20, q=.50, the normal planning half-width is about 8.6 percentage points. The browser calculator is an explicitly illustrative normal interval; the Python analysis uses the prespecified seeded percentile bootstrap. Neither has an exact finite-sample coverage proof here. A point estimate ≥.20 plus an interval above zero does **not** establish that the true effect is ≥.20. Baseline error below .20 leaves insufficient headroom.

[`Benchmark.lean`](../Devs/Benchmark.lean) uses integer basis points for arithmetic and logical implications. It proves headroom, the paired difference identity, sample and margin arithmetic, draft/replication gates, and pass/kill disjointness **assuming the point estimate is no higher than its upper interval endpoint**. A percentile interval does not automatically satisfy that assumption for every statistic. This file is a transparent companion model, not a formally verified implementation of the analyzer or bootstrap.

## Proof obligations and evidence status

| Claim | Status and remaining obligation |
|---|---|
| Listed Lean implications | Kernel-checked in pinned Lean; standard logical foundation remains trusted |
| Public source bytes | Verified against ten SHA-256 entries and original Git revisions |
| Citation entailment / corpus absence | Requires semantic review by people |
| Browser/Python matches every formal definition | Tested examples; no translation/refinement theorem |
| Criticism reduces false assertions | Unmeasured; needs frozen matched-model evaluation |
| Independent replication | Not performed |
| Physical prediction, EFMW validity, novelty | Not established by this package |

These distinctions are part of the result, not qualifications to remove when presenting it.
