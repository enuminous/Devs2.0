# EFMW Zoo R-001: A Finite-Curvature Primordial Recursion Boundary and the Limits of Rotational Inheritance

**Matthew Chenoweth Wright**  
Monolithic LLC · 17 October 2026  
**Status:** Analytic toy-model audit; not a validated cosmological solution or independently executed Lean/Zoo build.

## Abstract

We examine a proposed nonsingular cosmological transition, termed a *primordial recursion event*, as a candidate replacement for a singular boundary within an exploratory EFMW cosmology. We prescribe the spatially flat FLRW scale factor
\[
a(t)=a_{\min}\sqrt{1+(t/\tau)^2},\quad a_{\min},\tau>0,
\]
and test curvature regularity, a phenomenological rotational-amplitude scaling, and consistency with the Einstein equations. The Ricci and Kretschmann scalars are finite for all finite real times; the supplied rotational amplitude propagates continuously across the bounce but is not dynamically generated. In spatially flat general relativity the bounce requires violation of the null energy condition by its effective stress-energy source. A putative recursion mapping remains unspecified; therefore neither EFMW Prime nor the tested ansatz establishes the existence of a cosmological recursion event or intrinsic cosmic rotation. We provide explicit proof obligations and a falsifiable numerical program. All displayed results are analytic calculations of an imposed toy geometry; a fully coupled EFMW simulation, a Lean verification, and observational fitting remain outstanding.

## 1. Scope and hypotheses

EFMW Prime is provisionally written as
\[
\nabla^2\phi-c^{-2}\partial_t^2\phi=4\pi c^{-2}(E+Pc).
\]
Its physical source definitions, dimensional conventions, generally covariant completion, stress-energy tensor, and coupling to gravity require specification before it can act as a complete cosmological evolution law. A constant source-free \(\phi\) solves EFMW Prime, so the scalar equation alone does **not** require nonzero rotation.

**R-001 tests only** whether a chosen nonsingular FLRW geometry is regular, whether a specified rotational mode remains finite through its boundary, and what dynamical matter requirements follow in standard GR. A *recursion event* is an interpretation of the \(t=0\) matching surface, not an independently established physical process.

## 2. Model and geometric invariants

Use
\[
ds^2=-c^2dt^2+a(t)^2(dx^2+dy^2+dz^2),\qquad
x=t/\tau,\qquad a(t)=a_{\min}\sqrt{1+x^2}.
\]
The Hubble parameter and its derivative are
\[
H=\frac{t}{t^2+\tau^2},\qquad
\dot H=\frac{\tau^2-t^2}{(t^2+\tau^2)^2}.
\]
For a spatially flat FLRW geometry, the Ricci scalar and Kretschmann scalar, in units where the time coordinate is \(ct\), are
\[
R=\frac{6}{c^2}(\dot H+2H^2)
=\frac{6(\tau^2+t^2)}{c^2(t^2+\tau^2)^2}
=\frac{6}{c^2(t^2+\tau^2)},
\]
\[
K=\frac{12}{c^4}\left[(\dot H+H^2)^2+H^4\right]
=\frac{12(\tau^4+t^4)}{c^4(t^2+\tau^2)^4}.
\]
**At the boundary:**
\[
a(0)=a_{\min},\quad H(0)=0,\quad \dot H(0)=\tau^{-2},
\quad R(0)=6/(c^2\tau^2),\quad K(0)=12/(c^4\tau^4).
\]
Thus no divergence of these curvature scalars occurs at \(t=0\), and both remain bounded for all real \(t\). This is a local regularity result, not by itself a proof of geodesic completeness or physical stability.

**Correction to an earlier informal session report:** the expression \(R=6(1+3t^2)/(1+t^2)^2\) was an algebraic error. With \(a=\sqrt{1+t^2}\) and \(c=\tau=1\), the correct Ricci scalar is \(R=6/(1+t^2)\). Boundary values previously given as \(R(0)=6\), \(K(0)=12\) remain correct.

## 3. Rotational-amplitude ansatz

Consider a small, phenomenologically imposed rotational amplitude
\[
\omega(t)=\omega_0\left[\frac{a(0)}{a(t)}\right]^2
=\frac{\omega_0}{1+(t/\tau)^2}.
\]
For normalized \(\omega_0=\tau=1\):

| \(t/\tau\) | -3 | -2 | -1 | 0 | 1 | 2 | 3 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| \(\omega/\omega_0\) | 0.1 | 0.2 | 0.5 | 1 | 0.5 | 0.2 | 0.1 |

The amplitude is continuous and finite across the boundary if \(\omega_0\) is finite. However \(\omega_0=0\) yields \(\omega(t)=0\) everywhere. The ansatz inherits but does not create rotation. Moreover, an exact isotropic FLRW cosmology has zero vorticity for its fundamental comoving fluid congruence; the nonzero \(\omega\) above must be interpreted as a **test perturbation** or a separate field quantity until a self-consistent anisotropic metric and stress tensor are supplied. It is not an exact globally rotating FLRW solution.

## 4. Dynamical consistency in standard general relativity

With spatial curvature \(k=0\), the Friedmann/Raychaudhuri relation reads
\[
\dot H=-4\pi G(\rho+p/c^2)
\]
for mass density \(\rho\) and pressure \(p\). Because \(\dot H(0)=1/\tau^2>0\), the effective source must satisfy
\[
\boxed{\rho+p/c^2=-1/(4\pi G\tau^2)<0\quad\text{at }t=0.}
\]
This violates the null energy condition (NEC) for the effective matter source in unmodified flat-spatial-section GR. A cosmological constant alone does not remove this conclusion because \(\rho_\Lambda+p_\Lambda/c^2=0\). A viable extension must specify modified gravity, a consistent effective source, or different geometric assumptions, while checking stability and constraints. Prescribing a(t) alone does not derive such a source from EFMW.

## 5. What “recursion” would have to mean

A proposed matching law
\[
X(0^+)=\mathcal R[X(0^-)],
\quad X=\{g_{\mu\nu},T_{\mu\nu},\phi,\Pi_\phi,\omega_{\mu\nu}\}
\]
does not become a new physical process until \(\mathcal R\) is defined, is compatible with gravitational constraint equations, and demonstrably follows from a valid action or justified effective boundary theory. The smooth even-in-time toy scale factor is consistent with continuous matching, but provides no novel recursion map.

Note also that \(\omega/H\) is **undefined at the bounce** because \(H(0)=0\); it cannot be used as a finite boundary diagnostic there. Instead use finite local invariants, the bounded amplitude \(\omega\), or dimensionless ratios involving a nonzero regular reference scale such as \(\omega\tau\).

## 6. Falsifiable follow-up experiment

1. Freeze an explicit covariant EFMW action, fields, source dimensions, and variational principle; derive field equations and \(T_{\mu\nu}\).
2. Determine whether its coupled equations admit a regular bouncing solution without silently imposing the desired scale factor.
3. Construct an anisotropic or perturbative cosmological treatment with a gauge-invariant vorticity observable, and evolve the full Einstein/EFMW constraints.
4. Test zero-vorticity initial data as a negative control. If an asserted spontaneous-generation mechanism exists, identify the symmetry breaking and source terms.
5. Run ensembles over explicitly fixed initial conditions and resolution, checking convergence and conservation residuals.
6. Predict CMB multipoles and polarization with a declared likelihood against standard cosmology; do not infer a global axis merely from local spins or post-hoc apparent alignments.
7. For the historical 100,000-primordial-black-hole EFMW Monte Carlo claim, recover code, random seeds, physical units, maps, preregistered alignment statistic, and independent isotropic-null realizations before reporting any match to the CMB “Axis of Evil.”

## 7. Zoo disposition

| Obligation | Result |
|---|---|
| Positive finite scale factor | PASS, by construction |
| Finite Ricci and Kretschmann invariants | PASS, analytic |
| Finite assigned rotation through boundary | PASS, conditional on nonzero parameter |
| Rotation generated from zero | FAIL for tested ansatz |
| NEC-compatible flat GR effective source at bounce | FAIL |
| Self-consistent globally rotating spacetime | NOT DEMONSTRATED |
| EFMW action-derived bounce | OPEN |
| Defined physical recursion operator | OPEN |
| Lean kernel audit and independent numerical build | NOT PERFORMED |
| Historical primordial-black-hole empirical alignment | NOT VERIFIED; see the distinct observational companion below |

## 8. Conclusion

The R-001 candidate is a mathematically regular, prescribed bouncing geometry supporting a continuous phenomenological rotational amplitude. This does **not** establish that EFMW produces a recursion event, that the universe globally rotates, or that primordial rotational motion is unavoidable. The constructive contribution of this test is the explicit separation of geometric regularity, dynamical admissibility, rotational inheritance, and observational confirmation. The next decisive result must be a constrained solution of specified equations of motion that produces a measurable rotational signature without inserting it by assumption.

## 9. Observational follow-up: 18 October 2026

The [CMB alignment reproducibility companion](research/cmb-alignment/README.md) now supplies a provenance ledger, frozen isotropic-null code, saved numerical products and an independently extracted WMAP measurement. It does not repeat or validate this paper's bouncing-geometry calculation.

A January 23, 2025 archived article explicitly describes the 100,000-object simulation, so a matching historical **narrative** is now identified. Its executable, original seed, complete physical parameters, outputs and generated sky maps remain unrecovered. The separate October 18 Universe 003 toy ensemble is reproducible but is not that historical simulation.

For the specified WMAP nine-year ILC map with leading Doppler-quadrupole subtraction, the quadrupole and octopole dispersion axes are 5.85464 degrees apart. The ideal preselected single-pair isotropic-Gaussian probability is 0.521611%; the frozen Monte Carlo maximum-over-36-pairs test for multipoles 2–10 gives 17.17283%. This declared comparison family is not a reconstruction of the full historical search. Instrumental and foreground uncertainties are not fully marginalized.

Thus a particular CMB alignment is reproducible, while its attribution to primordial black holes, EFMW dynamics or global cosmic rotation remains unestablished. Statistical anisotropy, a preferred observational axis and physical vorticity remain distinct claims.

A subsequent [conditional nonzero-vorticity derivation](research/cmb-alignment/nonzero-vorticity/v1/DERIVATION.md) supplies an explicit local solution in a fixed-background, two-scalar specialization of the parent C1 action. Its combined Landau energy flow develops nonzero vorticity from zero initial flow, while each scalar flow remains irrotational. Symbolic identities, independent stress-tensor numerics, ablations and frozen orientation controls verify that result. Spatially varying initial scalar momenta are supplied, and no Einstein-constraint solution or cosmological axis is derived. This distinct local mechanism does not alter the R-001 ansatz's failure to generate its assigned rotational amplitude, and does not establish a bounce or the historical PBH interpretation.

## Related work and background

- [Wright, *From Big Bang to Great Recursion*](great-recursion-primordial-rotation.md) — earlier EFMW oriented-rotation hypothesis and curvature/rotation identifiability issues.
- [Wright, *Two Paths to Rotation*](Two-Paths-to-Rotation.md) — mathematical comparison with Clifford-algebra formalism.
- [EFMW-Lagrangian repository](https://github.com/enuminous/EFMW-Lagrangian) — candidate action/verification program; not assumed validated here.
- [Planck Collaboration, *Planck 2015 results. XVIII. Background geometry and topology of the Universe*](https://arxiv.org/abs/1502.01593) — background cosmological constraints.
- [Saadeh et al., *How Isotropic is the Universe?* (2016)](https://arxiv.org/abs/1605.07178) — stringent anisotropic cosmology constraints.

**Disclosure:** Sections 1–8 are a theoretical toy-model analysis based on symbolic identities and tabulated evaluations. No external dataset, source-code simulation or formal theorem-prover run established the physical validity of that geometry. The separate section 9 companion executes statistical controls, a recovered toy ensemble and a public CMB-map measurement; none establishes the proposed bounce or EFMW cosmology.
