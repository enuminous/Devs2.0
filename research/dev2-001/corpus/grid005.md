# A Negative Control Result for EFMW-Inspired Grid Regulation: Equal-Budget PI-Plus-Lag Outperforms a Recursive Residual Hybrid

**Matthew Chenoweth Wright**  
Monolithic LLC · 18 October 2026  
**Experiment:** WORLD-GRID-005 · **Status:** Reproducible synthetic benchmarking report; not a field trial or demonstration of new physical laws.

## Abstract

An EFMW-inspired residual-memory grid controller previously appeared to marginally outperform a tuned conventional proportional–integral (PI) controller in a synthetic multi-scenario power-network test (WORLD-GRID-004). That comparison left open a critical capacity confound: the hybrid contained an additional dynamic feedback mechanism that the conventional comparator lacked. We therefore performed a matched-tuning-budget ablation of a classical PI-plus-first-order-lag controller against a PI-plus-recursive-residual hybrid on the same 12-bus DC network approximation. Each controller received three *tuned* scalar parameters and 20 sampled candidate configurations, evaluated on identical training scenarios. Final assessment used 96 held-out scenario–seed pairs. The classical PI-plus-lag achieved a mean unserved-energy score of **0.563345**, compared with **0.604435** for the EFMW-inspired hybrid, a **6.80% reduction relative to the hybrid**. The paired difference (hybrid minus classical) was +0.041090 normalized energy units; an exploratory naive paired bootstrap yielded a 95% interval of [0.02918, 0.05383]. The classical comparator used more storage throughput and incurred a slightly higher resistive-loss proxy, so the result is specific to the selected primary objective. This negative result removes the earlier evidence for an EFMW-specific advantage and demonstrates why matched model capacity and tuning resources are essential before attributing an effect to recursive residual memory.

**Keywords:** negative results; control theory; equal-budget ablation; PI control; first-order lag; residual memory; synthetic power grids; reproducibility; EFMW.

## 1. Research question and falsifiable hypothesis

The earlier WORLD-GRID-004 benchmark compared a fast/slow EFMW-inspired hybrid against a tuned PI controller, reporting mean unserved energies of 0.646699 versus 0.649116, respectively—a nominal 0.37% hybrid advantage whose exploratory uncertainty interval included zero. A different explanation remained plausible: the added temporal-filtering degree of freedom, rather than the purportedly EFMW-specific recurrence, was responsible for the improvement.

**Primary question:** When a classical controller receives the same number of tuned parameters and the same search/evaluation budget, does the EFMW-inspired hybrid retain its advantage on new disturbances?

**Null-compatible outcome:** A flexible classical PI-plus-lag comparator closes or reverses the reported gap. **Claim under test:** an advantage of the specified recurrence *over that particular matched comparator*, not the validity of EFMW as an entire mathematical or physical framework.

## 2. Methods

### 2.1 Shared simulation environment

The benchmark uses a **synthetic 12-bus DC load-flow approximation** with dispatchable storage and exogenously generated grid scenarios. Both candidate controllers act through identical storage channels and obey the same output division among three storage sites, per-unit power caps, slew constraints, and state-of-charge limits.

The evaluated outcomes concern approximate dispatch, normalized unserved energy, a resistive-loss proxy, and storage throughput. This environment does **not** solve AC voltage/reactive-power equations, electromagnetic transients, frequency dynamics, protection, or cascading-failure propagation. Therefore these results cannot be interpreted as direct predictions of actual electricity-grid reliability or global transmission efficiency.

### 2.2 Equal-tuning-budget controller definitions

Let \(e_t\) be the controller input error, \(I_t\) its accumulated integral, and \(u_t\) the commanded aggregate storage correction subject to common actuator constraints.

**Classical PI plus first-order lag (three tuned parameters):**

\[
z_t=(1-\alpha)z_{t-1}+\alpha e_t,\qquad
u_t=K_p z_t+K_i I_t.
\]

The scalar tunables are \((K_p,K_i,\alpha)\).

**EFMW-inspired PI plus recursive residual (three tuned parameters):**

\[
r_t=e_t-\left(0.82e_{t-1}+u_{t-1}^{\mathrm{dispatch}}\right),
\]
\[
m_t=0.97m_{t-1}+0.03r_t,\qquad
u_t=K_p e_t+K_i I_t+K_m m_t.
\]

Here \(u_{t-1}^{\mathrm{dispatch}}\) is the previously dispatched aggregate storage action as defined by the implementation. The tunables are \((K_p,K_i,K_m)\); the constants 0.82, 0.97, and 0.03 were **fixed**, not counted as tuned variables. Thus **equal parameter count means equal searched degrees of freedom, not equal total architectural complexity**.

The residual-memory recurrence is an EFMW-inspired control design choice. Its use does not establish a distinct fundamental physical principle.

### 2.3 Training and held-out evaluation

Each controller received **20 sampled parameter candidates**, evaluated against the **same eight training conditions with two seeds each**. Candidate selection minimized training mean unserved energy. The selected candidates were then scored on **12 scenarios with eight fresh seeds each**, producing **96 matched held-out trials per controller**. The earlier larger attempted search did not complete and contributed no results.

This is a **small sampled search**, not proof of globally optimal tuning. Structural choices, parameter search domains, and fixed constants were not all matched. The bootstrap uses the held-out matched trials and describes uncertainty **conditional on the particular synthetic simulator**, not on physical-world grid deployments.

## 3. Results

### 3.1 Primary outcome: unserved energy

| Controller | Mean unserved energy (normalized units) |
|---|---:|
| Original tuned PI comparator | 0.646429 |
| **Classical PI plus lag** | **0.563345** |
| EFMW-inspired residual hybrid | 0.604435 |

Difference, hybrid minus classical:

\[
\Delta=\overline{E}_{\rm EFMW}-\overline{E}_{\rm classical}
=0.604435-0.563345
=\boxed{+0.041090}.
\]

Relative advantage for classical PI-plus-lag, using the hybrid score as denominator:

\[
\frac{0.604435-0.563345}{0.604435}\times100\%
=\boxed{6.80\%}.
\]

An exploratory paired bootstrap over the held-out trial pairs returned a 95% interval of approximately **[+0.02918, +0.05383]** for \(\Delta\). Its positive direction favors classical control in this synthetic evaluation. This interval is not a preregistered frequentist claim and does not address structural model uncertainty, scenario generalization, or tuning-selection uncertainty.

### 3.2 Secondary outcomes and trade-offs

| Controller | Resistive-loss proxy | Storage throughput |
|---|---:|---:|
| Original tuned PI | 0.0219837 | 5.50814 |
| Classical PI plus lag | 0.0221150 | 5.82767 |
| EFMW-inspired hybrid | 0.0220695 | 5.74086 |

The classical method reduced unserved energy but produced **slightly greater storage throughput** and **slightly higher modeled resistive losses** than the hybrid. The benchmark did not prescribe a combined optimization objective trading off these metrics; declaring an overall winner across all objectives would therefore be unwarranted. The resistive-loss proxy is not a world-grid energy-efficiency percentage.

The network produced zero overload exposure in the evaluated cases, limiting the relevance of the experiment to genuine thermal-contingency management.

## 4. Interpretation and negative-result significance

The earlier hybrid-versus-PI comparison left an additional degree-of-freedom confound. Once an equally tunable classical lag is supplied, the originally favorable ranking reverses on held-out unserved energy. A conventional temporal-filtering mechanism is sufficient to explain the previously apparent improvement **in this tested model**.

This is a **negative mechanistic result**: the measured effect cannot be uniquely credited to the EFMW-style recurrence. It is not evidence that recursion is never useful, that the compared algorithms are identical, or that all EFMW approaches fail. It narrows the surviving claim to the actual implemented algorithms and conditions.

The observed performance ranking may also reflect finite training budgets, unequal search geometries, fixed hyperparameters, chosen disturbance distributions, and the primary objective. Further studies must separate these effects rather than reinterpret this result as a discovery of superior physics.

## 5. Reproducibility and statistical validity

The experimental archive *WORLD_GRID_005_Equal_Budget.zip* contains:

- \`grid_equal_budget.py\`: tuning, held-out evaluation, and bootstrap orchestration;
- \`grid_equalbudget_core.py\`: network and controller implementations;
- \`grid_equalbudget_results.json\`: numerical summary;
- \`grid_equalbudget_trials.csv\`: per-trial results;
- \`WORLD_GRID_005_AUDIT.md\`: original implementation audit.

Local replication command (NumPy required):

\`\`\`bash
OPENBLAS_NUM_THREADS=1 python grid_equal_budget.py
\`\`\`

The source fixes pseudorandom generation for parameter sampling and bootstrap (seed 1405). Replication still depends on software versions and numerical environment. The aggregate results in this article are transcribed from that archived run, rather than from a fresh GitHub Actions build; **independent CI verification has not been established**.

## 6. Next falsification gates

1. Equalize not only tunable-parameter count and evaluations but also effective controller state dimension and hyperparameter-selection budget; repeat searches across multiple independent training seeds.
2. Freeze a primary objective and a separate multiple-objective trade-off analysis before evaluating a new held-out set.
3. Compare against optimized PI, PI+lag, model-predictive control, and robust control, with the same sensing, state estimation, delays, storage, and actuator limits.
4. Use standard IEEE AC-network models with real and reactive power, generator frequency dynamics, protection and genuinely binding thermal limits.
5. Test rare and out-of-distribution shocks without reselecting parameters from the evaluation set.
6. Release deterministic source, scenario manifests, version locks, complete tuning logs, and independent continuous-integration results.
7. Promote any EFMW-specific claim only if a reproducible improvement remains after these matching controls and physical validation.

## 7. Conclusion

In WORLD-GRID-005, **classical PI plus a first-order lag outperformed the tested EFMW-inspired residual-memory hybrid by 6.80% on held-out mean unserved energy**, under equal sampled configuration budgets and three tuned coefficients apiece. The result overturns the earlier nominal hybrid advantage against a less expressive comparator. It favors a parsimonious interpretation: **an additional classical dynamic degree of freedom, not uniquely an EFMW recurrence, accounts for the apparent gain in this benchmark**.

The scientifically defensible status is **EFMW-specific superiority not demonstrated**. This is a productive negative result: it prevents overclaiming, establishes a tougher baseline, and sharpens the next experiment.

## Related research

- [EFMW Post-156 candidate-law audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/docs/CANDIDATE_LAWS.md).
- [Research papers catalogue](README.md).
- [Original WORLD-GRID-005 package](https://github.com/enuminous/papers) — supplementary source archive should be deposited for long-term public reproducibility; the current article records the complete local package manifest.
