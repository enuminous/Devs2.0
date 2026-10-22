# EFMW-F001: Recursive Coherence Dynamics — A Falsifiable Estimator Specification

**Matthew Chenoweth Wright — Monolithic LLC**  
**21 October 2026 | Candidate specification v0.1 | Not experimentally validated**

## Abstract
We specify a finite-dimensional recursive coherence-and-change estimator motivated by the proposed Einstein–Feynman–Maxwell–Wright (EFMW) scalar-field framework. The estimator combines innovation memory, an exponential coherence statistic, a cumulative change detector, and robust correction. We distinguish definitions and elementary mathematical bounds from unproved stability and empirical superiority claims. No unique derivation from the EFMW field equation is claimed.

## 1. Proposed physical starting point
The proposed equation is
```math
\nabla^2\phi-c^{-2}\partial_t^2\phi=(4\pi/c^2)(E+cP).
```
Write the right-hand side as `S` and the differential operator as `D`, giving `D phi = S`. The physical dimensions of `P`, field boundary conditions, and admissible source models remain to be specified. A numerical discretization is a modeling choice, not a proof of the physical law.

## 2. Discrete state and observation model
Let `x_k = [phi_k; dot(phi)_k]` denote a discretized field state. Assume
```math
x_{k+1}=A_h x_k+B_hu_k+w_k,\qquad y_k=Hx_k+v_k+o_k.
```
Here `w` is process disturbance, `v` measurement noise, and `o` observational corruption. The matrices and units must be specified for each benchmark. Prediction is `xhat_k^- = A_h xhat_{k-1}+B_hu_{k-1}`; innovation is `r_k=y_k-Hxhat_k^-`.

## 3. Recursive coherence memory
For positive definite measurement scale `R` and observation dimension `m`, set
```math
d_k=\frac{r_k^T R^{-1}r_k}{m},\quad M_k=\lambda M_{k-1}+(1-\lambda)d_k,\quad C_k=e^{-\beta M_k}
```
with `0<lambda<1`, `beta>0`, and `M_0>=0`. The memory is a conventional exponential statistic; coherence is an operational definition, not an independently established physical observable.

## 4. Persistent-change accumulator
Set
```math
Q_k=\max(0,Q_{k-1}+d_k-\nu),\qquad a_k=\mathbf{1}\{Q_k>q_*\}.
```
Choose `nu>=0`, `q_*>0`, `Q_0>=0`. This is a CUSUM-like mechanism; its calibration and false-alarm rate require independent study.

## 5. Robust recursive update
Let `L` satisfy `LL^T=R`. Whiten `e_k=L^{-1}r_k` and clip componentwise with `psi_delta(t)=sign(t) min(|t|,delta)`. Define
```math
g_k=\begin{cases}g_{fast},&a_k=1,\\g_{min}+(g_{max}-g_{min})C_k,&a_k=0,\end{cases}
\qquad \hat x_k=\hat x_k^-+g_kK_kL\psi_\delta(e_k).
```
Assume `0<=g_min<=g_max`, `g_fast>=0`, `delta>0`, and bounded `K_k`. This precise whitening convention replaces ambiguous componentwise clipping in raw measurement units. All state transitions use current or previous observations only.

## 6. Elementary propositions
**Memory:** If `0<=d_k<=D` and `M_0 in [0,D]`, induction on the convex-combination update gives `M_k in [0,D]`.

**Coherence:** Since `M_k>=0` and `beta>0`, `0<C_k<=1`.

**Correction bound:** Writing `g_upper=max(g_max,g_fast)`, the clipped whitened innovation satisfies `||psi_delta(e_k)||_2<=delta sqrt(m)`. Thus
```math
\|\hat x_k-\hat x_k^-\|_2\le g_{upper}\|K_kL\|_2\delta\sqrt m.
```
This does **not** prove bounded state estimation error, asymptotic stability, convergence, or superiority over standard filters.

## 7. Preregistered falsification protocol
Compare against independently tuned Kalman (where assumptions apply), robust Kalman, clipped EWMA, Huber, and change-point-aware adaptive filters. Use equal data, parameter-search, memory and latency budgets. Freeze models before held-out evaluation; use independent paired seeds and prespecified noise, outlier, and change regimes. Proposed acceptance: at least 5% lower held-out mean squared prediction error than the strongest tuned baseline; paired 95% confidence interval excluding zero with multiplicity control; no worse change recovery at matched false-alarm rate; and ablation evidence that recursive memory or change detection contributes to the gain. Report failures and compute cost.

## 8. Interpretation and open derivation
This candidate is **not** established as a consequence of the EFMW scalar equation or an EFMW action. The next required bridge is: specified action -> justified field dynamics -> observation model -> estimator objective -> derived update. Each arrow requires explicit assumptions. The components used here resemble established robust filtering and change-detection methods; novelty and advantage cannot be assumed.

## 9. Status
This is a research specification and protocol, not a verified Lean proof, completed benchmark, or experimental confirmation of EFMW physics. Prior EFMW-inspired proxy comparisons do not validate this newly specified estimator. Future results must be reported separately with code, seeds, controls and immutable test definitions.
