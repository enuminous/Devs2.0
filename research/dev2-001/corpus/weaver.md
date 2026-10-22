# External Formalization of an EFMW Inspired Residual Core in Weaver OS

## A Pinned Source and Evidence Audit

**Matthew Chenoweth Wright** · Monolithic LLC / eNuminous

22 October 2026 · Technical preprint · Version 1.0

**Artifact reviewed:** [`ryansctt1994-sudo/Weaver_Os`, pull request 57](https://github.com/ryansctt1994-sudo/Weaver_Os/pull/57), at commit [`740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52`](https://github.com/ryansctt1994-sudo/Weaver_Os/commit/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52).

**Evidence cutoff:** 22 October 2026. The pull request was open and unmerged at inspection.

## Abstract

An external repository has produced a small, inspectable formalization explicitly attributed to the Einstein–Feynman–Maxwell–Wright framework. Weaver OS pull request 57 contains seventeen Lean theorem declarations: twelve concerning a conventional exponentially weighted moving average over the real numbers and five concerning its composition with a modeled authorization boundary. This paper reconstructs the mathematical content, checks the declarations against their assumptions, and examines the associated continuous-integration record. The recurrence preserves intervals and uniform bounds, forgets initial conditions geometrically, converges under constant input when the memory coefficient lies in $[0,1)$, and satisfies a finite-horizon disturbance bound. The monitor ingestion operation leaves protected state, grants, and history unchanged by construction; without stored grants, subsequent modeled execution remains ineligible and preserves protected state. A successful GitHub Actions run records compilation and axiom output for all seventeen declarations. That hosted record was inspected, not independently rerun for this paper. The artifact establishes substantive, attributed external engagement with a bounded mathematical slice of EFMW. It does not establish new EWMA mathematics, empirical superiority, deployed-system safety, or the physical claims of the broader framework. Its significance is the conversion of an attributed idea into explicit definitions, conditional proofs, and a reproducible target whose limitations remain visible.

**Keywords:** EFMW; Lean; exponentially weighted moving average; formal verification; authorization; provenance; reproducibility.

## 1. The contribution being documented

External engagement with a research program can take several forms: a citation, an implementation, a formal proof, an empirical comparison, or deployment. These forms support different conclusions. This case concerns an attributed formal artifact and its recorded build, rather than a completed adoption or validation of EFMW as a physical theory.

The public repository `ryansctt1994-sudo/Weaver_Os` describes an execution substrate for bounded AI. Pull request 57, titled “Formalize EFMW residual core and monitor authority boundary,” was created on 1 October 2026 and last updated on 6 October. At the evidence cutoff it remained open, targeted `codex/integrated-formal-closure`, and was explicitly described as stacked on pull request 56. The account and repository are outside the `enuminous` namespace; GitHub reports the repository as non-fork. These facts establish a distinct repository provenance. They do not establish the full interpersonal, institutional, or methodological independence of its contributors. [1, 2]

The formalization's README credits Matthew Chenoweth Wright for EFMW and its physical interpretations, while treating the implemented recurrence as conventional EWMA mathematics. Its source expressly excludes those physical interpretations from the proof assumptions. Attribution is therefore directly documented. Neither appropriation nor endorsement of the broader theory should be inferred from the artifact. [3, 4]

I write as the originator credited by the external project. This is a source-based technical assessment from that perspective, not a disinterested replication study or a joint publication with the Weaver OS maintainers. The external formalization remains their contribution; this paper supplies its mathematical exposition and evidence classification.

## 2. Frozen target and review method

The target is the `formal/efmw-core` package at the commit above, together with its imported `WNSKernel.Core` and its verification workflow. The review compared theorem statements, proof bodies, the seventeen-entry audit file, package configuration, and the hosted job log. Mutable pull-request metadata was inspected separately to establish status at the cutoff. No local Lean rebuild, deployment test, or empirical benchmark was performed for this paper.

The evidence is organized around four questions:

1. What objects and assumptions occur in the formal statements?
2. What does the recorded build establish about those particular statements?
3. Which scientific or engineering conclusions would require an additional bridge?
4. What bounded next test could supply that bridge or falsify the stronger claim?

This method prevents the theorem count, the EFMW name, and a successful build from serving as evidence for claims they do not express. It also separates definitional invariants from substantive properties of unmodeled software.

### 2.1 Provenance record

| Evidence item | Frozen or observed value |
|---|---|
| Reviewed head commit | `740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52` |
| Recorded CI checkout | `0f66cdf31442df6481f1ec51e2c4969cdbdd3533`, a synthetic PR merge |
| Recorded base commit | `44bbfd1af4c687e5f9780f5247051a11e24a5d6e` |
| Lean version | `4.19.0` |
| Mathlib revision | `c44e0c8ee63ca166450922a373c7409c5d26b00b` |
| Successful workflow run | `36926483410`, 1 October 2026 |
| Inspected job | `110584966954`, named `efmw` |
| Theorem source Git blob | `1631c98c9af6e26be1225b5df5df7a25dfb70000` |

The workflow run identifies the PR head, but the checkout log shows that execution used GitHub's synthetic merge commit. Direct comparison found identical Git blob hashes and file contents at head and merge for `EFMW.lean`, `Audit.lean`, the package README, `lakefile.toml`, `lean-toolchain`, `WNSKernel/Core.lean`, and the EFMW workflow. This connects the inspected formal sources and configuration to the recorded build without confusing a test merge with an accepted merge into the repository. [4–8]

## 3. The mathematical object

Let $\lambda\in\mathbb R$ be fixed, $a\in\mathbb R$ an initial memory, and $r:\mathbb N\to\mathbb R$ an arbitrary residual stream. The package defines

$$
U_\lambda(m,r)=\lambda m+(1-\lambda)r,
\qquad
T_\lambda(a,r)_0=a,
\qquad
T_\lambda(a,r)_{n+1}=U_\lambda(T_\lambda(a,r)_n,r_n).
$$

These correspond to `update` and `track`. All arithmetic is over Lean's real numbers, within a `noncomputable` section. No probability distribution, measurement model, alarm threshold, physical field, or interpretation of residual generation appears in these definitions. [4]

The recurrence is the standard exponentially weighted moving average under a change of parameter convention. Writing NIST's new-observation coefficient as $\alpha$ rather than its original $\lambda$, the previous statistic receives weight $1-\alpha$. Here the old memory receives $\lambda$, so $\alpha=1-\lambda$, with a one-step indexing adjustment. The boundary $\lambda=1$ additionally permits a frozen memory that ignores observations. This equivalence is enough to reject novelty of the recurrence itself. It says nothing about whether a particular application or formal integration is useful. [9]

The scalar type alone does not enforce physical units. Any physical application must assign compatible units to $m$ and $r$ and a dimensionless coefficient to $\lambda$. This dimensional interpretation is an additional modeling obligation, not a theorem of the package.

### 3.1 Preservation of bounds

If $0\leq\lambda\leq1$ and both $m$ and $r$ lie in $[L,H]$, their convex combination does too:

$$
L\leq U_\lambda(m,r)\leq H.
$$

Taking $L=-B$ and $H=B$ yields the absolute-value bound. Induction then gives

$$
|a|\leq B,\quad \forall k\;|r_k|\leq B
\quad\Longrightarrow\quad
\forall n\;|T_\lambda(a,r)_n|\leq B.
$$

The code proves these as `update_interval`, `update_bounded`, and `track_bounded`. Boundedness of the residual stream is a hypothesis, not a property supplied by the monitor. The premises already imply $B\geq0$; a separate nonnegativity premise is unnecessary. [4]

### 3.2 Forgetting and constant input

For two initial conditions driven by the same stream,

$$
T_\lambda(a,r)_n-T_\lambda(b,r)_n=\lambda^n(a-b).
$$

The identity holds for every real $\lambda$. If $\lambda\geq0$, taking absolute values gives $\lambda^n|a-b|$. When $0\leq\lambda<1$, the difference tends to zero even if the common residual stream is unbounded or nonconvergent. This is convergence of the difference, not convergence of either trajectory.

For a constant input $r_n=c$,

$$
T_\lambda(a,c)_n-c=\lambda^n(a-c),
$$

and therefore $T_\lambda(a,c)_n\to c$ for $0\leq\lambda<1$. The Lean proofs obtain both identities by induction and the limits from Mathlib's geometric-power limit theorem. [4]

The strict upper bound matters. At $\lambda=1$, $T_1(a,r)_n=a$ for every $n$; forgetting and constant-input convergence generally fail. At $\lambda=0$, $T_0(a,r)_{n+1}=r_n$, so a bounded alternating input gives a bounded nonconvergent trajectory. These direct consequences of the definitions rule out an interpretation of the package as proving unconditional stabilization of arbitrary signals.

### 3.3 Disturbance bound

For two potentially different input streams, suppose

$$
0\leq\lambda\leq1,\qquad |a-b|\leq D,
\qquad \forall k\;|r_k-s_k|\leq E.
$$

The formal theorem `disturbance_bound` establishes

$$
\left|T_\lambda(a,r)_n-T_\lambda(b,s)_n\right|
\leq \lambda^nD+(1-\lambda^n)E.
$$

Writing $d_n=T_\lambda(a,r)_n-T_\lambda(b,s)_n$, the update identity gives

$$
d_{n+1}=\lambda d_n+(1-\lambda)(r_n-s_n).
$$

The triangle inequality, the nonnegative weights, and induction produce the claimed bound. No individual bound on either stream is needed, only a uniform bound on their difference. [4]

For $\lambda<1$, the right-hand side approaches $E$, not necessarily zero. Thus bounded persistent input discrepancy produces a bounded output discrepancy. It does not prove calibration, accurate prediction, or advance detection of a failure. The constant $E$ must come from a separately justified input model or measurement guarantee.

## 4. Complete inventory of the seventeen declarations

All names below lie in `WNSKernel.EFMW`. Let $T_a^r(n)=T_\lambda(a,r)_n$. Each statement was checked against the pinned source and its entry in `Audit.lean`. The rows are declarations, not seventeen independent discoveries. [4, 5]

| No. | Declaration | Claim and required assumptions |
|---:|---|---|
| 1 | `update_difference` | $U_\lambda(a,r)-U_\lambda(b,r)=\lambda(a-b)$; arbitrary reals. |
| 2 | `update_constant_error` | $U_\lambda(m,r)-r=\lambda(m-r)$; arbitrary reals. |
| 3 | `update_interval` | Interval preservation when $0\leq\lambda\leq1$ and both inputs lie in that interval. |
| 4 | `update_bounded` | Absolute bound $B$ preserved by one update under the same coefficient restriction and bounds on both inputs. |
| 5 | `track_bounded` | Bound $B$ preserved for all times when $0\leq\lambda\leq1$ and the initial value and every residual satisfy it. |
| 6 | `initial_difference` | $T_a^r(n)-T_b^r(n)=\lambda^n(a-b)$; no coefficient restriction. |
| 7 | `initial_distance` | $\lvert T_a^r(n)-T_b^r(n)\rvert=\lambda^n\lvert a-b\rvert$ for $\lambda\geq0$. |
| 8 | `constant_error` | $T_a^c(n)-c=\lambda^n(a-c)$ for constant input; no coefficient restriction. |
| 9 | `constant_distance` | $\lvert T_a^c(n)-c\rvert=\lambda^n\lvert a-c\rvert$ for $\lambda\geq0$. |
| 10 | `constant_converges` | Constant-input trajectory tends to $c$ for $0\leq\lambda<1$. |
| 11 | `initial_difference_converges` | Same-stream trajectory difference tends to zero for $0\leq\lambda<1$. |
| 12 | `disturbance_bound` | The bound in Section 3.3 under its initial-gap and pointwise stream-gap assumptions. |
| 13 | `monitor_preserves_protected` | Ingestion preserves the protected-state field; no restriction on real monitor parameters. |
| 14 | `monitor_preserves_grants` | Ingestion preserves the stored grant list; same unrestricted parameters. |
| 15 | `monitor_preserves_history` | Ingestion preserves the history list; same unrestricted parameters. |
| 16 | `warning_without_grant_denied` | After ingestion, eligibility is false if the original grant list is empty. |
| 17 | `warning_without_grant_preserves` | A subsequent modeled `step` preserves protected state under that empty-grant premise. |

Rows 1–12 are conventional real-valued recurrence mathematics. Rows 13–17 specialize a modeled authorization interface. This distinction is more informative than the aggregate theorem count.

## 5. What the authority boundary proves

The imported kernel models a state as protected data, a list of grants, and a history of receipts. Eligibility requires a stored grant, a recognized issuer, matching subject and action scope, a valid time interval, no revocation, and three Boolean proposal conditions. Its `step` applies the requested action only when eligibility holds; otherwise it retains the protected data. Both outcomes append a receipt to history. [6]

Monitor ingestion is defined by

$$
\operatorname{ingest}(S,\lambda,m,r)=(S,U_\lambda(m,r)).
$$

The returned state is literally the input state. Consequently, preservation of protected data, grants, and history follows by definitional equality; the three proofs use `rfl`. These are valid interface invariants. Their force comes from the operation's deliberately restricted definition, rather than from analysis of an arbitrary monitor implementation. [4]

The last two declarations compose this operation with the kernel. An empty grant list makes eligibility impossible because membership in that list is required. The rejection theorem then preserves protected state. The theorem names use “warning,” but the formal operation contains neither a warning threshold nor an alarm event. Its conclusion holds independently of the memory value or residual.

Two boundaries are important. First, ingestion preserves history, but a rejected execution step records a receipt; the final theorem does not say that the entire state remains unchanged. Second, the monitored real value is not an input to eligibility at all. The package therefore documents a separation between observation and authority within this model. It does not prove that a deployed program has no other write path, that Boolean evidence flags reflect genuine evidence, or that runtime grants are authentic.

This is a useful specification pattern: a diagnostic quantity cannot grant itself execution permission through the defined interface. Establishing the corresponding property in running software requires a refinement argument and a threat model covering the actual paths to protected state.

## 6. Interpretation of the build and axiom audit

The inspected GitHub Actions run reports success. Its job log identifies Lean 4.19.0, resolution of the pinned Mathlib revision, compilation of `WNSKernel.Core` and `EFMW`, and execution of `lake env lean Audit.lean`. All seventeen printed dependency lists contain exactly `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` or additional named axiom occurs in those lists. [7, 8]

This supports the claim that Lean accepted the seventeen declarations in the recorded environment under the listed foundational dependencies. It does not make the proofs axiom-free. Nor is a dependency audit a check that a definition captures a real-world phenomenon: a mathematically sound theorem can concern an intentionally simplified model.

The workflow uses `set -o pipefail`, builds the package, prints theorem dependencies, and rejects matching `sorryAx` or lines beginning with `axiom `. The explicit dependency lists are more informative than that grep alone. The grep is not a general allowlist check for every possible custom axiom name printed inside a dependency list. This review therefore inspected the actual seventeen outputs rather than treating the workflow's success badge as sufficient evidence. [5, 7, 8]

The log also records an uploaded evidence archive and its SHA-256 digest, `883b1ad1bcf59f8568ab21d8e6ea67ee7d44cf1e7453375530dcf5354b36116c`. This paper reports that recorded digest; it does not claim an independent download and hash verification of the archive. The recorded build used cached Mathlib artifacts. A fresh rebuild and separate compiled-proof replay would supply additional reproducibility evidence, but neither was performed here.

## 7. Evidence classification and significance

| Claim | Status at the cutoff | Basis or missing obligation |
|---|---|---|
| The external package explicitly attributes EFMW to Wright. | Demonstrated | Pinned README and source comments. |
| The package formalizes twelve recurrence results and five modeled boundary results. | Demonstrated within the formal model | Source inspection plus the recorded successful build and audit. |
| The project engaged substantively with an EFMW-inspired idea. | Supported | Definitions, proofs, configuration, and CI exceed a passing mention; social independence remains unestablished. |
| The recurrence is new mathematics. | Rejected for this recurrence | Equivalent to conventional EWMA under $\alpha=1-\lambda$. |
| The PR has been merged or the feature deployed. | Not established | PR remained open and unmerged; no deployment evidence reviewed. |
| The artifact validates broader EFMW physics or ontology. | Not established | No such premises, predictions, or experimental comparison occur in the package. |
| The monitor improves detection or warning lead time. | Unresolved | No detector definition, benchmark, or calibrated performance result supplied by these proofs. |
| The modeled boundary guarantees runtime safety. | Unresolved | No runtime refinement or complete implementation threat model established. |
| A preceding WNS EFMW v0.2 pilot failed validation and retained a sealed holdout. | Maintainer-reported | Stated in the README and PR; underlying experimental records were not verified in this review. |

The defensible significance is external technical uptake of a carefully limited component. The source preserves attribution while declining to import the full interpretive framework into its theorem assumptions. That makes the result easier to inspect, challenge, and reuse.

The formal package also exposes a productive division of labor. Conventional mathematics supplies the recurrence guarantees. The project-specific contribution is the particular formal packaging and its composition with the WNS state interface. The present paper documents that composition and the provenance of its evidence; it makes no priority claim for EWMA and no claim that this is the first external EFMW engagement.

The reported v0.2 failure must remain separate from the proof result. A valid bound on a recurrence can coexist with an ineffective detector or an unsuccessful experiment. In the absence of the underlying protocol and data, the appropriate record is that the maintainers report a failed validation gate, not that this paper independently reproduced that failure or that the later formalization reversed it. [1, 3]

## 8. Minimal next tests

The remaining questions should be addressed by distinct tests with criteria fixed before results are inspected.

1. **Reproduce the formal artifact.** Check out the pinned commit in a fresh environment, record toolchain and resolved dependency hashes, run the documented build and audit, and preserve logs. Success requires all seventeen declarations to build and all axiom dependencies to match an explicit allowed set. Failure includes a missing dependency, an unreviewed axiom, or a source mismatch. This reproduces the formal result, not its physical interpretation.

2. **Connect real arithmetic to a numerical implementation.** Specify the number format, evaluation order, overflow and non-finite-value behavior, input range, and admissible $\lambda$. Prove an implementation-to-real relation with an explicit error budget. Boundary and adversarial tests should include coefficients near one and long input sequences. Success requires a verified error bound under those conditions; finite sampling alone does not prove universal refinement.

3. **Test the actual authorization interface.** Identify every implementation path from monitor output to protected data and grants, and define its relation to `ingest` and `step`. A formal refinement must preserve the relevant state projection. Adversarial tests should attempt to turn arbitrary residual values into authorization. An unauthorized protected-state change is a decisive failure; absence of such changes in a finite test suite is supporting evidence, not a universal guarantee.

4. **Evaluate any detector claim separately.** Freeze residual construction, thresholds, tuning budget, data splits, baseline implementations, and the primary metric before opening held-out data. Include the mathematically equivalent EWMA as a matched baseline: identical input, initialization, coefficient, and threshold should give identical real-arithmetic outputs. Any proposed advantage must arise from a separately identified component. Success requires the preregistered held-out criterion; an unsuccessful comparison must remain visible rather than being replaced by the proof count.

5. **Recover the earlier pilot record.** Locate the v0.2 protocol, validation decision, and permissible provenance records without opening a holdout merely to explain a failure. Until those materials are available, preserve the distinction between a documented maintainer statement and an independently assessed experimental outcome.

No physical-theory test is implied by the recurrence alone. Such a test would first need a distinct EFMW prediction, a measurement procedure, and a comparison that separates it from established alternatives.

## 9. Conclusion

Weaver OS provides a concrete example of attributed external engagement with an EFMW-inspired mathematical component. The inspected artifact contains a complete seventeen-declaration Lean package and a successful hosted build record. Its real-valued recurrence has explicit boundedness, forgetting, convergence, and disturbance guarantees. Its monitor operation preserves authority-bearing state by construction and composes with empty-grant rejection in a small kernel model.

Those results deserve to be recorded at their actual scale. They offer a reusable formal target and a clear boundary between monitoring and authorization. Broader scientific validation, empirical advantage, numerical fidelity, and deployed safety remain separate questions. Preserving these distinctions makes the external contribution more credible and the next research obligations more precise.

## Attribution and assistance

The formalization and its CI workflow are credited to the Weaver OS project and the account under which the reviewed contribution appears, `ryansctt1994-sudo`. No external contributor is listed as a coauthor, and no review, consent, or endorsement by the project's maintainers is implied. EFMW attribution follows the project's explicit source notice.

An OpenAI assistant assisted with source retrieval, theorem-statement comparison, mathematical exposition, and manuscript preparation. This assistance is not an independent Lean execution or an experimental replication.

## References

1. Weaver OS. [Pull request 57, Formalize EFMW residual core and monitor authority boundary](https://github.com/ryansctt1994-sudo/Weaver_Os/pull/57). Created 1 October 2026; status inspected 22 October 2026.
2. Weaver OS. [Repository metadata](https://api.github.com/repos/ryansctt1994-sudo/Weaver_Os), including owner and non-fork status. Inspected 22 October 2026.
3. Weaver OS. [EFMW Residual Core v0.1 README](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52/formal/efmw-core/README.md). Pinned attribution, reproduction instructions, and boundaries.
4. Weaver OS. [EFMW.lean](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52/formal/efmw-core/EFMW.lean). Definitions and all seventeen theorem declarations.
5. Weaver OS. [Audit.lean](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52/formal/efmw-core/Audit.lean). Explicit theorem dependency audit.
6. Weaver OS. [WNSKernel/Core.lean](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52/formal/wns-kernel/WNSKernel/Core.lean). State, eligibility, execution, and rejection definitions.
7. Weaver OS. [EFMW verification workflow](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52/.github/workflows/efmw-residual-core.yml), [package configuration](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52/formal/efmw-core/lakefile.toml), and [Lean toolchain](https://github.com/ryansctt1994-sudo/Weaver_Os/blob/740bfbe7925f278a60d0c3f6ef9ed3bc470f3c52/formal/efmw-core/lean-toolchain).
8. Weaver OS. [GitHub Actions run 36926483410](https://github.com/ryansctt1994-sudo/Weaver_Os/actions/runs/36926483410), [job 110584966954](https://github.com/ryansctt1994-sudo/Weaver_Os/actions/runs/36926483410/job/110584966954), and [recorded evidence artifact](https://github.com/ryansctt1994-sudo/Weaver_Os/actions/runs/36926483410/artifacts/11193214202). Executed 1 October 2026; job log inspected 22 October 2026.
9. NIST/SEMATECH. [e-Handbook of Statistical Methods, Section 6.3.2.4, EWMA Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm). Conventional recurrence and parameter convention; accessed 22 October 2026.
