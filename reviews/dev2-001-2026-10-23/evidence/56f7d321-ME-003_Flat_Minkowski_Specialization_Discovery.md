# ME-003 in Flat Minkowski Spacetime

## A Formal Discovery Paper on the Scalar d’Alembertian

**Matthew Chenoweth Wright** · Monolithic LLC / eNuminous  
15 October 2026 · Formal discovery paper · Version 1.0

**Formal artifact:** [enuminous/Monolithic-102-Zoo-Lean4](https://github.com/enuminous/Monolithic-102-Zoo-Lean4), commit [01f51acb0b0e564105dcf7f14cc55998d41b91ce](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/commit/01f51acb0b0e564105dcf7f14cc55998d41b91ce).  
**Verification:** Lean 4.28.0, pinned Mathlib dependency, successful GitHub Actions run [38793976970](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/actions/runs/38793976970).

## Abstract

This paper records a formal mathematical-physics result for ME-003, the scalar d’Alembertian written as a covariant metric contraction. In four-dimensional Cartesian Minkowski coordinates with physical time \(t\), the inverse metric is fixed to \(\operatorname{diag}(1/c^2,-1,-1,-1)\), the connection coefficients are fixed to zero, and the field is a real \(C^2\) scalar. The Lean theorem MonolithicAnalysis.FlatScalar.minkowski_specialization_eq_box proves that the resulting contraction equals the existing ME-004 operator,
\[
\Box\phi = \frac{1}{c^2}\frac{\partial^2\phi}{\partial t^2}-\nabla^2\phi,
\]
under \(c\ne 0\). The formalization uses actual Fréchet coordinate derivatives and preserves the catalogue’s \((+---)\) sign convention.

The result is a **partial flat-Minkowski specialization**. The canonical ME-003 equation remains unchanged, and its general covariant formalization remains open. The identity is standard mathematical physics; the contribution reported here is an auditable Lean formalization in the catalogue’s existing conventions, not a new wave law or experimental finding. No observations, fitted data, or empirical validation are claimed.

## 1. Frozen target and scope

The frozen canonical entry is ME-003:
\[
\Box\phi = g^{\mu\nu}\nabla_\mu\nabla_\nu\phi.
\]
The adjacent catalogue entry ME-004 gives the flat-spacetime expansion:
\[
\Box\phi = \frac{1}{c^2}\frac{\partial^2\phi}{\partial t^2}-\nabla^2\phi.
\]

These two statements are preserved in the canonical source. Its digest, recorded by the analysis ledger, is **d534be8e0664fd523bd0bbbd82e98b8acda29e23f0941690be96573661080268**. The new result does not edit or replace either formula.

The model uses coordinates \(x=(t,x^1,x^2,x^3)\), with coordinate 0 representing physical time. For a nonzero real parameter \(c\), set
\[
g_{\mu\nu}=\operatorname{diag}(c^2,-1,-1,-1),
\qquad
g^{\mu\nu}=\operatorname{diag}(1/c^2,-1,-1,-1).
\]
This is the \((+---)\) Minkowski convention written with \(t\), rather than \(ct\), as the time coordinate. The connection is specified to vanish in these Cartesian coordinates. A real scalar field is modeled as a function \(\phi:\mathbb{R}^4\to\mathbb{R}\), with the theorem stated for \(C^2\) fields.

This is physical mathematical structure: it includes spacetime, a scalar field, a propagation-speed parameter, a Lorentzian metric, covariant differentiation, and the wave operator. The formal claim is about the exact operator identity in this declared model.

## 2. Explicit specialization

In the implementation, spacetime is Fin 4 → ℝ. The coordinate derivative partialD i f x is defined by evaluating the Fréchet derivative of \(f\) at \(x\) in the \(i\)-th coordinate direction. Thus the partial derivatives are not uninterpreted symbols.

The scalar covariant Hessian is represented by
\[
H_{\mu\nu}(x)
=
\partial_\mu(\partial_\nu\phi)(x)
-
\sum_{\lambda=0}^{3}\Gamma^\lambda_{\mu\nu}\,\partial_\lambda\phi(x).
\]
The specialization sets every Cartesian Minkowski Christoffel coefficient \(\Gamma^\lambda_{\mu\nu}\) to zero and defines the full contraction
\[
\Box_M\phi(x)
=
\sum_{\mu=0}^{3}\sum_{\nu=0}^{3}
g^{\mu\nu}H_{\mu\nu}(x).
\]

Because the inverse metric is diagonal, all off-diagonal terms vanish. Because the connection is zero, the Hessian components reduce to the corresponding iterated coordinate partials. Consequently,
\[
\Box_M\phi
=
\frac{1}{c^2}\partial_0\partial_0\phi
-\partial_1\partial_1\phi
-\partial_2\partial_2\phi
-\partial_3\partial_3\phi
=
\frac{1}{c^2}\partial_t^2\phi-\nabla^2\phi.
\]

The repository states this equality as
\[
\mathrm{minkowskiCovariantBox}\ c\ f\ x
=
\mathrm{box}\ c\ f\ x
\]
for \(c\ne0\) and ContDiff ℝ 2 f. The proof unfolds the explicit metric, Hessian, and connection definitions, simplifies the finite sums, and closes the remaining real-algebra identity. It does not exchange derivative order or prove an existence theorem for wave solutions.

## 3. Discovery and verification record

| Check | Input and criterion | Result |
|---|---|---|
| Frozen-source check | Preserve the canonical ME-003 and ME-004 formulas and their sign convention. | **Pass.** The source is unchanged; its digest is recorded in the ledger. |
| Model construction | Use the declared physical-time coordinates, inverse metric, zero connection, real scalar field, and \(c\ne0\). | **Pass.** Each component is explicit in the Lean definitions. |
| Operator correspondence | Prove the full ME-003 contraction equals the existing ME-004 operator. | **Demonstrated.** minkowski_specialization_eq_box proves the equality under its stated hypotheses. |
| Source and coverage audit | Check the analytic declarations against canonical source entries and record the scope. | **Pass.** The ledger labels ME-003 partial_specialization and keeps general_covariant_status open. |
| Build and axiom audit | Build both Lean packages; run source-correspondence checks, strict axiom audits, audit rejection controls, and dependency-pin checks. | **Pass.** Both jobs in workflow run 38793976970 completed successfully. |
| Novelty screen | Compare the flat operator with standard mathematical-physics formulations. | **Equivalent / reparameterized.** The flat d’Alembertian with this signature is established; novelty is not claimed. |

No Zoo-animal sweep or empirical study is reported in this paper. The evidence is a proof-checked symbolic identity and its repository verification record. The standard flat expression is given, for example, in the TU Delft *Introduction to Quantum Mechanics*, section 6.1.2, equation 6.13, with the same mostly-negative spatial signs and the \(c\)-scaled time derivative. The broader theory of wave operators on Lorentzian manifolds is treated by Bär, Ginoux, and Pfäffle [5].

## 4. What the proof establishes—and what it does not

The demonstrated result is the equality of two explicitly defined real-valued operators on the declared flat model. The hypotheses are visible: a four-coordinate real domain, a \(C^2\) scalar, a nonzero real \(c\), the \((+---)\) inverse metric, physical-time Cartesian coordinates, and zero connection coefficients.

The code **specifies** the connection to be zero; it does not derive Christoffel symbols from a general metric or construct a Lorentzian manifold. The result therefore does not prove ME-003 for arbitrary curved spacetime, arbitrary coordinates, or a dynamical metric. It also does not derive ME-004 from an action, identify the scalar with a measured physical field, establish existence or stability of solutions, or test a prediction against observations.

The evidence status is:

- **Demonstrated:** equality of the flat metric contraction and the ME-004 operator in Lean.
- **Supported but incomplete:** ME-003 has a concrete flat-space realization under the declared conventions.
- **Unresolved:** a general curved-spacetime formalization, including a metric-derived connection and explicit geometric assumptions.
- **Not assessed:** experimental adequacy or the physical interpretation of the catalogue’s scalar field.

The repository coverage report records this distinction directly: ME-003 has a partial flat-Minkowski specialization, while its complete covariant formalization remains open. The package currently contains 15 analytic models among the 49 catalogue-only entries; ME-003’s partial specialization is tracked separately from those models.

## 5. Reproducibility

The proof and coverage change are in the pinned formal artifact at commit 01f51acb0b0e564105dcf7f14cc55998d41b91ce. The GitHub Actions run for that commit passed:

1. The root Lean build, project axiom audit, and audit rejection controls.
2. The analysis package build, source-to-coverage correspondence check, analytic declaration axiom audit, rejection controls, and dependency-pin check.

The artifact includes the theorem in analysis/CatalogueAnalysis.lean, the machine-readable entry in analysis/coverage.json, the scope summary in analysis/COVERAGE.md, and a README description. The exact workflow result is [run 38793976970](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/actions/runs/38793976970).

## 6. Next proof obligation

A justified next mathematical step would define a curved-spacetime model with an explicit Lorentzian metric and a metric-compatible connection, then prove a coordinate expression for the scalar wave operator under stated regularity and chart assumptions. A successful result would need to derive or constrain the connection from the metric and preserve the frozen sign convention. A missing geometric definition, a sign mismatch, or a theorem that merely assumes the desired coordinate identity would fail that criterion. No such curved-space result is claimed here.

## References

1. eNuminous, [Monolithic 102 canonical source](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/blob/01f51acb0b0e564105dcf7f14cc55998d41b91ce/canonical/CANONICAL_102.md), especially ME-003 and ME-004; [canonical checksums](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/tree/01f51acb0b0e564105dcf7f14cc55998d41b91ce/canonical).
2. eNuminous, [Lean analysis implementation](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/blob/01f51acb0b0e564105dcf7f14cc55998d41b91ce/analysis/CatalogueAnalysis.lean), theorem MonolithicAnalysis.FlatScalar.minkowski_specialization_eq_box.
3. eNuminous, [coverage report](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/blob/01f51acb0b0e564105dcf7f14cc55998d41b91ce/analysis/COVERAGE.md) and [machine-readable ledger](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/blob/01f51acb0b0e564105dcf7f14cc55998d41b91ce/analysis/coverage.json).
4. eNuminous, [Lean verification workflow run 38793976970](https://github.com/enuminous/Monolithic-102-Zoo-Lean4/actions/runs/38793976970).
5. C. Bär, N. Ginoux, and F. Pfäffle, *Wave Equations on Lorentzian Manifolds and Quantization*, European Mathematical Society, 2007; [arXiv:0806.1036](https://arxiv.org/abs/0806.1036).
6. Delft University of Technology, *Introduction to Quantum Mechanics*, section 6.1.2, equation 6.13, [“Four-vectors”](https://interactivetextbooks.tudelft.nl/introduction-to-quantum-mechanics/content/relativisticquantummechanics.html).
