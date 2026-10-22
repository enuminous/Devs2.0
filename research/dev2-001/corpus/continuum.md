# From Finite Certificates to Continuum Scalar Dynamics

## A Verified Bridge for the Frozen EFMW C1 Action

**Matthew Chenoweth Wright** · Monolithic LLC / eNuminous

14 October 2026 · Technical preprint · Version 1.0

**Formal artifact:** [enuminous/EFMW-Lagrangian](https://github.com/enuminous/EFMW-Lagrangian), commit [`053043b8ccd44e55d9f73000cb078f31c74052a9`](https://github.com/enuminous/EFMW-Lagrangian/commit/053043b8ccd44e55d9f73000cb078f31c74052a9).

**Frozen mathematical target:** EFMW-LAGRANGIAN-C1, version 1.0.0.

**Verification:** Lean 4.28.0; pinned Mathlib; successful finite and continuum GitHub Actions runs on `main`.

## Abstract

The frozen EFMW C1 action was previously accompanied by an exhaustive classification of 585 FieldSpace statements and finite Lean certificates for 360 scalar interaction magnitudes. These certificates established exact polynomial identities under declared coefficient identifications, but did not establish that the formal derivative represented differentiation of a real-valued function or that the resulting expressions followed from a continuum action. This paper reports a formal bridge across those boundaries. First, the existing polynomial normalizer is proved to preserve evaluation under every real assignment, and its formal derivative is proved to compute the ordinary real derivative of the represented polynomial. Second, the resulting potential derivative is incorporated into a scalar action on fixed Minkowski spacetime. Under explicit differentiability, integrability, and domination hypotheses, Lean verifies differentiation under the action integral and integration by parts. Stationarity against every smooth compactly supported test then implies the scalar Euler–Lagrange equation almost everywhere; continuity of the residual gives a pointwise equation. All 360 original magnitude certificates are instantiated as real-derivative and action-variation theorems. Independent execution in a conventional GitHub-hosted environment passes source checks, compilation, axiom audits, compiled-proof replay, and rejection controls. The frozen candidate remains unchanged. The result is a conditional scalar variational theorem, with curved metric and gauge variation, solution existence, stability, source interpretation, and empirical validation remaining separate obligations.

**Keywords:** formal verification; Lean 4; scalar field theory; calculus of variations; polynomial semantics; reproducibility; EFMW.

## 1. The two gaps addressed

A finite symbolic certificate and a continuum field equation are different mathematical objects. A computation over integer coefficients and lists can certify that a polynomial differentiation procedure produces a specified expression. Additional theorems are needed to identify that procedure with real differentiation and to justify moving from pointwise derivatives to the variation of an integral.

The original C1 audit supplied the finite layer. It classified all 585 displayed statements in the 165-triplet FieldSpace catalogue. For each of the 360 scalar statements, it provided one derivative-magnitude identity and one formal nonidentity recording the potential-sign discrepancy. The resulting 720 explicit scalar certificates did not constitute 720 independent physical laws. Nor did catalogue coverage mean that all 585 statements followed literally from C1. [1, 2]

A separate reproducibility gap concerned execution. The authoring environment used an explicit-path Lean launcher because its standard launcher could not locate its application normally. A successful local record established a result in that environment, but did not demonstrate a build through a conventional hosted environment. A Pages deployment checked publication rather than the mathematical verification pipeline.

The work reported here addresses both gaps. The existing finite pipeline now runs in GitHub Actions with the standard upstream toolchain. A separate `continuum/` package proves real semantics and a conditional scalar action theorem, with its own verification workflow. The candidate action, its convention lock, historical source files, and original finite certificate sources are preserved.

## 2. Frozen target and scope

C1 uses signature $(-,+,+,+)$ and natural units $c=\hbar=1$ for its master action. Its field content comprises a metric, two Abelian gauge potentials, and eight real neutral scalar fields. Its interaction family includes quadratic scalar terms and pair and triple products of the declared sector invariants, with spacetime-constant coefficients. Directional source coefficients are compared with this common potential only under the recorded reciprocity identifications. [1]

The present formalization varies one active scalar at a time in a restricted C1 potential. All other field and coefficient atoms are held fixed during that variation. Spacetime is the real vector space

$$
M=\mathbb R^4,
\qquad
\sigma=(-1,1,1,1),
\qquad
\Box\varphi=\sum_{\mu=0}^{3}\sigma_\mu\partial_\mu\partial_\mu\varphi.
$$

In Lean, `Spacetime` is `Fin 4 → ℝ`. A coordinate partial derivative is a genuine Fréchet derivative evaluated on the corresponding coordinate direction. Integration uses Lebesgue measure. The Lorentzian signature enters through the fixed kinetic coefficients; the implementation does not construct a curved Lorentzian manifold. [4]

For generality, the theorem permits real atom assignments that depend on spacetime. C1's constant couplings are a specialization. To interpret the specialization as actual Minkowski geometry, the Ricci-scalar atom must be assigned zero. Allowing an arbitrary prescribed function in that atom does not prove a theorem about a dynamical curved metric.

The frozen triplet rule deletes couplings involving inactive sectors before variation. Consequently, the certificates concern a family of restricted actions. They do not establish that every solution of a restricted triplet extends to a solution of the unrestricted theory. Other terms independent of the selected scalar have zero variation when their action contributions are well defined; the formalized integral is the selected scalar kinetic term together with the restricted potential.

## 3. Real semantics for the original certificates

### 3.1 Polynomial representation

The finite syntax represents a polynomial by a list of terms. Each term consists of an integer coefficient and a list of atom indices. Repeated indices represent repeated factors. For a real assignment $a:\mathbb N\to\mathbb R$, define

$$
\operatorname{ev}_a(p)
=\sum_{(c,m)\text{ in }p} c\prod_{j\text{ in }m}a(j),
$$

where sums and products preserve list multiplicities. Let $N$ denote the existing normalizer and $D_v$ the existing formal derivative with respect to atom $v$. These are the original finite operations, rather than replacements chosen for the continuum proof. [3]

**Theorem 1 — Normalization preserves real evaluation.** For every polynomial list $p$ and every assignment $a$,

$$
\operatorname{ev}_a(N(p))=\operatorname{ev}_a(p).
$$

The Lean theorem `normalize_sound` proves this by establishing evaluation preservation for monomial sorting, term insertion and combination, zero-coefficient removal, and term sorting. It follows that a certificate $N(p)=N(q)$ implies equality of the unnormalized real evaluations.

**Theorem 2 — Formal differentiation computes the real derivative.** For every $p$, $v$, and $a$,

$$
\left.\frac{d}{dz}\operatorname{ev}_{a[v\mapsto z]}(p)\right|_{z=a(v)}
=\operatorname{ev}_a(D_vp).
$$

The Lean statement is a `HasDerivAt` proposition, so it establishes differentiability with the stated derivative. The proof handles repeated monomial factors and then proceeds through the term list using the real product and sum rules. It does not infer analytic correctness merely from agreement on the 360 catalogue instances.

### 3.2 Transporting a frozen certificate

The finite audit uses doubled potentials to represent half-integer normalizations with integer coefficients. For a particular scalar certificate, let $p$ be the doubled restricted potential and $q$ its certified doubled scalar source magnitude. The old theorem supplies

$$
N(D_vp)=N(q).
$$

Theorems 1 and 2 therefore give

$$
\left.\frac{d}{dz}\frac12\operatorname{ev}_{a[v\mapsto z]}(p)\right|_{z=a(v)}
=\frac12\operatorname{ev}_a(q).
$$

This is `certified_potential_hasDerivAt`. The generator instantiates it for all 360 scalar magnitude certificates, recording the original theorem, source line, active atom, and new theorem name in `continuum/certificate_index.json`. The new instances consume the old certificates as proof inputs. [3, 5]

The result concerns equality of real functions and their derivatives. A different logical question is whether a formal polynomial nonidentity forces unequal values at every real assignment. It does not: special assignments, including vanishing couplings, can make a nonzero formal discrepancy evaluate to zero. The original sign findings retain their meaning as generic symbolic nonidentities.

## 4. The scalar action theorem

### 4.1 The actual variation

Let $a:M\to(\mathbb N\to\mathbb R)$ assign values to atoms at each spacetime point, and write $\varphi(x)=a(x)(v)$. For a test field $\eta$, define

$$
a_\epsilon(x)=a(x)[v\mapsto\varphi(x)+\epsilon\eta(x)],
\qquad
f(x)=\frac12\operatorname{ev}_{a(x)}(q).
$$

The varied density and one-parameter action are

$$
\rho_\epsilon(x)
=-\frac12\sum_{\mu=0}^{3}\sigma_\mu
\bigl(\partial_\mu\varphi(x)+\epsilon\partial_\mu\eta(x)\bigr)^2
-\frac12\operatorname{ev}_{a_\epsilon(x)}(p),
\qquad
S_\eta(\epsilon)=\int_M\rho_\epsilon(x)\,d^4x.
$$

Theorem `partial_variation` proves the derivative identity

$$
\partial_\mu(\varphi+\epsilon\eta)
=\partial_\mu\varphi+\epsilon\partial_\mu\eta
$$

under the stated differentiability hypotheses. Theorem `actionAlong_eq_varied_action` then identifies the jet expression above with the action evaluated on the genuinely varied scalar field. This prevents the jet variables from being treated as unrelated formal placeholders. [4]

Using the transported potential derivative, `densityAlong_hasDerivAt` proves

$$
\left.\frac{d\rho_\epsilon(x)}{d\epsilon}\right|_{\epsilon=0}
=-\sum_{\mu=0}^{3}\sigma_\mu
\partial_\mu\varphi(x)\partial_\mu\eta(x)-f(x)\eta(x).
$$

### 4.2 Analytic hypotheses

Two explicit structures supply the hypotheses for passage from the density to the action. They contain regularity, measurability, and integrability conditions; neither contains the desired Euler–Lagrange identity as an assumed field.

| Structure | Required conditions |
|---|---|
| `IBPConditions` | Differentiability of $\varphi$ and $\eta$; differentiability of each $\partial_\mu\varphi$; integrability of $(\partial_\mu\partial_\mu\varphi)\eta$, $(\partial_\mu\varphi)(\partial_\mu\eta)$, and $(\partial_\mu\varphi)\eta$ for every $\mu$; integrability of $f\eta$. |
| `DominatedVariation` | A common neighborhood of $\epsilon=0$; almost-everywhere strong measurability of $\rho_\epsilon$ for parameters sufficiently near zero; integrability of $\rho_0$; almost-everywhere strong measurability of the first-variation density; an integrable bound controlling the density's local Lipschitz dependence on $\epsilon$. |

Concretely, the last condition supplies an integrable nonnegative bound $B(x)$ such that, almost everywhere in $x$ and for $\epsilon,\epsilon'$ in one common neighborhood,

$$
|\rho_\epsilon(x)-\rho_{\epsilon'}(x)|
\le B(x)|\epsilon-\epsilon'|.
$$

Mathlib's parameter-integral theorem then justifies differentiation under the integral. Its integration-by-parts theorem applies to the listed product integrability and differentiability hypotheses. These are existing analysis theorems in the pinned library. [6]

The assumptions specify a sufficient finite-action class. Compact support of the test field alone does not establish integrability of an arbitrary unperturbed density over all of $\mathbb R^4$. Nondecaying backgrounds can require a relative-action construction, and the present package does not automatically discharge its hypotheses from a general-purpose definition of admissible fields.

### 4.3 First variation and stationarity

**Theorem 3 — Scalar action variation.** Suppose $N(D_vp)=N(q)$ and the two analytic structures above are supplied. Then

$$
S_\eta'(0)
=\int_M\bigl(\Box\varphi(x)-f(x)\bigr)\eta(x)\,d^4x.
$$

**Proof outline.** Real differentiation gives the pointwise density derivative. Dominated differentiation identifies the derivative of the action with its integral. For each coordinate direction, integration by parts gives

$$
\int_M(\partial_\mu\varphi)(\partial_\mu\eta)\,d^4x
=-\int_M(\partial_\mu\partial_\mu\varphi)\eta\,d^4x.
$$

Summing with the signature coefficients yields the displayed residual. The corresponding Lean theorems are `firstVariation_eq_residual` and `actionAlong_hasDerivAt`. The generator supplies 360 `action_derivative_*` instances. This is an ordinary derivative along a specified scalar variation; Fréchet differentiability of an action functional on a normed space of fields is a further question. [4, 5]

**Theorem 4 — Stationarity implies the scalar equation.** Assume additionally that the residual $r=\Box\varphi-f$ is locally integrable; that **every** smooth compactly supported $\eta$ satisfies the required admissibility hypotheses; and that $S_\eta'(0)=0$ for every such test. Then

$$
\Box\varphi=f\quad\text{almost everywhere on }M.
$$

The proof uses uniqueness of the real derivative to obtain $\int_M r\eta=0$ for all smooth compactly supported tests. Mathlib's test-function theorem then implies $r=0$ almost everywhere. The statement is formalized as `stationary_action_implies_scalar_equation`. Merely checking a selected subset of tests is not its premise. [4, 6]

**Corollary — Pointwise equation.** If the residual is also continuous, it vanishes everywhere. The theorem `continuous_residual_eq_zero` supplies this upgrade using the positive measure of nonempty open sets.

Stationarity is a variational premise. The proof does not assume the scalar equation to derive itself, and it does not construct a stationary field or prove that one exists.

## 5. Preserved signs and negative results

For the frozen signature and kinetic sign, the equation is

$$
\Box\varphi-\frac{\partial U}{\partial\varphi}=0.
$$

The bridge therefore supports the C1 minus-sign equation. It does not convert the historical catalogue's generic plus-sign equations into valid consequences of the action. As a sign check, a free scalar potential $U=\tfrac12m^2\varphi^2$ gives $\Box\varphi-m^2\varphi=0$ under the declared convention. The formal bridge preserves that convention throughout. [1–4]

The original audit also records 88 incompatible neutral-scalar gauge-current expressions, two unresolved gauge-current equations, 45 gravitational statements with underdefined stress identification, and 90 Bianchi statements requiring explicit index repair. The scalar extension does not change those classifications. It does not formalize the complete gauge or metric variation. [2]

Global stability remains a separate issue with an explicit counterexample inside the allowed family. For three unit-mass scalar fields, zero pair couplings, and unit cubic coupling, setting all three fields equal to $t$ gives

$$
U(t)=\frac32t^2+t^3\longrightarrow-\infty
\qquad(t\longrightarrow-\infty).
$$

Deriving the field equation correctly does not remove this unbounded direction. Adding stabilizing interactions would change the frozen candidate and require an explicitly versioned extension. Restricting coefficients or the domain of an effective theory would require separately stated assumptions and proofs. [9]

## 6. Verification and reproducibility

### 6.1 Pinned environment and successful runs

The verified source is commit `053043b8ccd44e55d9f73000cb078f31c74052a9`. Both packages pin `leanprover/lean4:v4.28.0`. The continuum package pins Mathlib commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`, with transitive revisions recorded in its Lake manifest. The workflows use GitHub-hosted Ubuntu 24.04, Python 3.12, and elan 4.2.4 with an installer checksum. Actions are pinned by commit. [7, 8]

| Workflow on `main` | Run | Result, 14 October 2026 |
|---|---|---|
| Verify candidate and Lean certificates | [38636651859](https://github.com/enuminous/EFMW-Lagrangian/actions/runs/38636651859) | Success: frozen-input/source checks, Python regressions, Lean compilation, axiom audit, compiled-proof replay, negative checks, and deterministic regeneration. |
| Verify real and scalar continuum bridge | [38636651794](https://github.com/enuminous/EFMW-Lagrangian/actions/runs/38636651794) | Success: C1/source checks, bridge regeneration, pinned dependency retrieval, compilation, axiom and coverage audit, sequential `leanchecker` replay, and rejection controls. |

Both runs check the same commit using the standard upstream launcher. The continuum run had no GitHub dependency-cache hit and successfully fetched the pinned dependencies and upstream compiled Mathlib cache. This is evidence of hosted reproducibility; it is not a claim that Mathlib was rebuilt entirely from source.

The continuum axiom audit inspected 802 safe declarations and confirmed exactly 360 `real_derivative_*` and 360 `action_derivative_*` theorems. Its transitive dependency union used only `propext`, `Classical.choice`, and `Quot.sound`. The 802 figure includes definitions and supporting declarations. The 720 generated bridge instances are applications of general theorems, not a count of independent discoveries.

Rejection controls confirmed failure for an introduced public axiom, a private axiom, a `sorry` placeholder, a native reduction oracle, and a false derivative claiming that the derivative of the square function at one equals one. Such probes check that safeguards are active; they do not establish that every possible defect has been excluded.

### 6.2 What the checks trust

`leanchecker` replays compiled declarations through Lean's kernel against their imported environment. It is useful for detecting invalid compiled environments, but it is not a second independently implemented proof kernel. The continuum runner checks all 16 bridge modules with declarations in separate processes and verifies that the root module contains only imports. Sequential execution avoids the memory multiplication observed when the namespace-wide checker launched all modules concurrently. [8, 10]

The trust boundary includes Lean's implementation, the permitted foundational axioms, imported library artifacts, and the correspondence between the formal definitions and the intended mathematical objects. The historical text parser and its translation into finite propositions remain outside the Lean proof. Source hashes, fail-closed parsing, regression tests, and deterministic regeneration make that boundary inspectable without eliminating it.

The committed `verification/build_status.json` is the historical authoring record. Fresh hosted-run logs are retained as CI artifacts, configured for 90 days. The successful run links above identify the independent execution environment and exact checked-out source; they should be distinguished from the repository's Pages deployment.

### 6.3 Reproduction

With Git, Python 3.12, and elan available, check out the exact revision and run the finite pipeline followed by the continuum layer:

```sh
git clone https://github.com/enuminous/EFMW-Lagrangian.git
cd EFMW-Lagrangian
git checkout --detach 053043b8ccd44e55d9f73000cb078f31c74052a9
elan toolchain install leanprover/lean4:v4.28.0
python3 scripts/verify.py --clean
python3 continuum/generate.py
git diff --exit-code -- candidate sources src audit \
  Audit.lean EFMWLagrangian.lean EFMWLagrangian \
  lean-toolchain lakefile.toml lake-manifest.json \
  continuum/EFMWContinuum continuum/EFMWContinuum.lean \
  continuum/certificate_index.json
cd continuum
lake exe cache get \
  Mathlib.Analysis.Calculus.Deriv.Mul \
  Mathlib.Analysis.Calculus.Deriv.Add \
  Mathlib.Analysis.Calculus.Deriv.Comp \
  Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts \
  Mathlib.Analysis.Calculus.ParametricIntegral \
  Mathlib.Analysis.Distribution.AEEqOfIntegralContDiff \
  Mathlib.Tactic.Ring Mathlib.Tactic.Linarith Mathlib.Tactic.Convert
git diff --exit-code -- lake-manifest.json lean-toolchain
lake build
lake env lean Audit.lean
python3 recheck.py
python3 negative_checks.py
```

The workflow files provide the full installer and environment setup. Reproduction requires each command to succeed, including the expected rejection of invalid probes; a successful rendering or deployment alone is insufficient.

## 7. Contribution and evidence status

The analysis uses standard differentiation, integration by parts, and the test-function characterization of a vanishing locally integrable function. These operations already exist in Mathlib. The candidate-specific contribution is a checked connection from the unchanged finite polynomial syntax and all its scalar magnitude certificates to an actual action variation, together with reproducible execution of that connection. No worldwide priority claim or new physical law is inferred from this engineering result. [3–6]

| Claim | Evidence status | Boundary |
|---|---|---|
| Real semantics of the normalizer and formal derivative | **Demonstrated** | General Lean theorems for real atom assignments and the original list-polynomial syntax. |
| Scalar action variation and stationarity-to-equation implication | **Demonstrated, conditional** | Fixed Minkowski spacetime; explicit analytic hypotheses; one scalar varied at a time. |
| Conventional hosted reproduction at the cited revision | **Demonstrated** | Successful standard-toolchain CI runs; imported dependency trust remains. |
| Correspondence from historical source text to formal propositions | **Supported but incomplete** | Auditable parser and regeneration pipeline; no parser-correctness theorem in Lean. |
| Literal equivalence of the full historical catalogue to C1 | **Rejected as a general identity claim** | Sign, current, stress, and index findings are retained. |
| Global stability for the unrestricted allowed C1 coefficient family | **Rejected as a universal guarantee** | An allowed cubic specialization is unbounded below. |
| Curved coupled dynamics, PDE existence, uniqueness, and hyperbolicity | **Unresolved** | Outside the scalar theorem and its verification scope. |
| EFMW field interpretation and agreement with measurements | **Hypothesis / unresolved** | No empirical dataset or physical validation is supplied by this work. |

Anti-circularity is enforced at two central points. The potential derivative is derived from the finite certificate through proved semantics, rather than postulated as an analytic bridge. The Euler–Lagrange identity is derived through analysis, rather than placed inside an admissibility structure. Stationarity remains an explicit premise of the final implication. Independent hosted execution is execution-level reproduction of the same artifact, not independent empirical evidence or a second research derivation.

## 8. Next proof obligations

The immediate analytic task is to supply a useful field class that discharges `IBPConditions` and `DominatedVariation` for every smooth compactly supported test. A suitable next target is a precisely specified class of smooth fields with sufficient decay, together with a relative-action formulation for backgrounds whose absolute action is infinite. Its acceptance condition should be a Lean theorem deriving the existing hypotheses from the proposed field-class definition, plus a nontrivial admissible example. Reintroducing the desired action identity as an assumption would fail that condition.

Beyond that task, curved-space scalar variation requires a metric-dependent volume form and covariant integration by parts. Gauge and metric variation require their own functional analysis and boundary treatment. A consistent-truncation theorem must account for equations of omitted fields. PDE existence, uniqueness, hyperbolicity, and energy estimates require coefficient and background domains fixed in advance; the existing instability example must remain visible when those domains are selected.

Physical evaluation requires independently defined observables, units, source dynamics, and measurements. In particular, the rotational source used elsewhere in EFMW is not identified physically by the present scalar formalization. A preregistered empirical prediction and comparator would supply a different kind of evidence from the mathematical and software checks reported here.

## 9. Conclusion

The published bridge establishes a continuous chain of mathematical implications: an unchanged finite certificate determines the derivative of a real polynomial potential; that derivative enters a rigorously varied Minkowski scalar action; and stationarity against all smooth compactly supported tests yields the scalar equation under explicit analytic conditions. Conventional GitHub Actions execution verifies the implementation at an identified commit.

This advances the formal status of the scalar sector while preserving C1's conventions, the catalogue discrepancies, and the limits of the evidence. The result provides a checked foundation for further continuum work. It does not establish the complete curved coupled theory, stable solutions, or a physical law of nature.

## Reproducibility and assistance statement

The source, generated instance index, workflows, and verification logs are public. This manuscript and the associated formalization and build work were prepared with OpenAI Codex assistance. The cited kernel checks and CI runs provide the computational evidence; human review of the formal-to-physical interpretation remains a separate task. No new empirical measurements are reported.

## References and primary artifacts

All project source links below refer to the verified revision. Library links refer to pinned upstream revisions. Run results were checked on 14 October 2026.

1. **Frozen candidate and conventions.** [CANDIDATE.md](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/candidate/CANDIDATE.md), [conventions.json](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/candidate/conventions.json), and [FREEZE.json](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/candidate/FREEZE.json).
2. **Finite catalogue audit.** [FULL_AUDIT.md](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/audit/FULL_AUDIT.md) and [original scalar certificate index](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/audit/lean_certificate_index.json). Its historical continuum-scope statements should be read alongside the new bridge in references 3–5.
3. **Real polynomial semantics.** [Realization.lean](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/EFMWContinuum/Realization.lean).
4. **Scalar continuum theorem.** [ScalarVariation.lean](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/EFMWContinuum/ScalarVariation.lean) and [scope documentation](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/docs/CONTINUUM_BRIDGE.md).
5. **Instantiation and traceability.** [Bridge generator](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/generate.py), [bridge certificate index](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/certificate_index.json), and [dependency manifest](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/lake-manifest.json).
6. **Mathlib analysis dependencies**, commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`: [ParametricIntegral.lean](https://github.com/leanprover-community/mathlib4/blob/8f9d9cff6bd728b17a24e163c9402775d9e6a365/Mathlib/Analysis/Calculus/ParametricIntegral.lean), [IntegrationByParts.lean](https://github.com/leanprover-community/mathlib4/blob/8f9d9cff6bd728b17a24e163c9402775d9e6a365/Mathlib/Analysis/Calculus/LineDeriv/IntegrationByParts.lean), and [AEEqOfIntegralContDiff.lean](https://github.com/leanprover-community/mathlib4/blob/8f9d9cff6bd728b17a24e163c9402775d9e6a365/Mathlib/Analysis/Distribution/AEEqOfIntegralContDiff.lean).
7. **Finite verification workflow and result.** [verify.yml](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/.github/workflows/verify.yml) and [successful main-branch run 38636651859](https://github.com/enuminous/EFMW-Lagrangian/actions/runs/38636651859).
8. **Continuum verification workflow and controls.** [continuum.yml](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/.github/workflows/continuum.yml), [Audit.lean](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/Audit.lean), [recheck.py](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/recheck.py), [negative_checks.py](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/continuum/negative_checks.py), and [successful main-branch run 38636651794](https://github.com/enuminous/EFMW-Lagrangian/actions/runs/38636651794).
9. **Physical obligations and instability example.** [PHYSICAL_OBLIGATIONS.md](https://github.com/enuminous/EFMW-Lagrangian/blob/053043b8ccd44e55d9f73000cb078f31c74052a9/docs/PHYSICAL_OBLIGATIONS.md).
10. **Lean compiled-environment checker.** [LeanChecker.lean](https://github.com/leanprover/lean4/blob/7e01a1bf5c70fc6167d49c345d3bf80596e9a79b/src/LeanChecker.lean), Lean 4.28.0 source.
