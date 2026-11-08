# Devs 2.0 equation set

**Status: complete operational equation ledger for the paper's architectural claims; not a uniquely derivable physical theory.** The September 2026 white paper is conceptual. It does not specify a domain state space, transition kernel, observation model, utilities, or system parameters, so no unique numerical or physical equation set follows from it. This document makes the paper's possibility, distributed-knowledge, prediction, evidence, criticism, uncertainty, feedback, scientific-update, and human-agency claims explicit as a mathematical architecture. It distinguishes repository-backed Lean models from new operational definitions. The equations use conventional mathematics and make no novelty claim.

## Frozen target and scope

The target is the architecture described in [Devs2.0-EFMW.md](../Devs2.0-EFMW.md), especially sections 2–10 and 14–16, together with the mathematical companion in [MATHEMATICS.md](MATHEMATICS.md) and the explicit DEV2-001 protocol. This set describes an evidence-bounded decision-support system. It does not derive an EFMW field equation, a physical law, a deterministic future, or empirical forecasting accuracy.

A label below has one of four meanings:

- **Existing formal model:** the equation or property is represented in the Lean companion.
- **Derived identity:** follows mathematically from stated definitions and assumptions.
- **Operational definition:** a proposed mathematical encoding of a prose requirement.
- **Empirical question:** mathematics alone cannot decide whether the system helps.

## Symbols

| Symbol | Meaning |
|---|---|
| \(\mathcal X\) | State or outcome space under a fixed model family |
| \(x\) | A candidate state or future |
| \(h_t\) | Information available by time \(t\), with source revisions attached |
| \(E_t(x)\) | A hard evidence constraint; true only when \(x\) is compatible with that constraint |
| \(\Omega_t\subseteq\mathcal X\) | States still admitted by the current model and constraints |
| \(p_t(x)\) | A normalized probability over \(\mathcal X\), when one is justified |
| \(m\in\mathcal M\) | One explicit candidate model |
| \(c\) | A claim with provenance and an evidence status |
| \(a\) | An action or intervention |
| \(Y\) | A forecast outcome |

## 1. Possibilities and evidence

### E01 — Current possibility set

\[
\Omega_t
=
\{x\in\mathcal X : M_t(x)\land C_t(x)\}.
\]

Here \(M_t\) is the current model’s admissibility predicate and \(C_t\) is the conjunction of constraints accepted by time \(t\). This is a definition: it makes the paper’s “structured representation of possible futures” explicit without asserting that the chosen model captures reality.

### E02 — Hard-evidence update (existing formal model)

\[
\Omega_{t+1}
=
\Omega_t\cap\{x:E_{t+1}(x)\}.
\]

Membership in the updated set entails both prior admissibility and compatibility with the new constraint. Therefore \(\Omega_{t+1}\subseteq\Omega_t\). Reapplying the same fixed constraint is idempotent, and applying two fixed constraints commutes. These set identities are proved in [Possibility.lean](../Devs/Possibility.lean).

This operation is a logical restriction. “Collapse” is the paper’s computational metaphor here; no quantum-measurement claim follows.

### E03 — Explicit model expansion (existing formal model)

\[
\Omega_{t+1}
=
\bigl(\Omega_t\cap\{x:E_{t+1}(x)\}\bigr)\cup N_{t+1},
\]

where \(N_{t+1}\) is a separately recorded set of newly proposed alternatives. The union can reopen possibilities rejected by an earlier constraint. The new alternatives remain hypotheses until supported; expansion is not evidence. The Lean companion proves only the set inclusion facts in [Possibility.lean](../Devs/Possibility.lean).

### E04 — Inconsistent hard constraints

\[
\Omega_t\cap\{x:E_{t+1}(x)\}=\varnothing
\quad\Longrightarrow\quad
\text{model–evidence conflict}.
\]

The empty set is a diagnostic, not permission to silently discard evidence or normalize zero mass. Resolution requires checking source interpretation, assumptions, and model scope; until then the result is **UNRESOLVED**.

## 2. Probabilistic forecasts and uncertainty

Hard constraints and probabilistic evidence are different operations. A system must say which it is using.

### E05 — Bayesian update on a finite state space (operational definition)

Given a prior \(p_t\) and likelihood \(\ell_{t+1}(x)=P(e_{t+1}\mid x,h_t)\),

\[
Z_{t+1}=\sum_{x\in\mathcal X}p_t(x)\ell_{t+1}(x),
\qquad
p_{t+1}(x)=
\frac{p_t(x)\ell_{t+1}(x)}{Z_{t+1}}
\quad\text{only if }Z_{t+1}>0.
\]

The update is normalized because summing the right-hand side over \(x\) gives \(Z_{t+1}/Z_{t+1}=1\). If \(Z_{t+1}=0\), the stated model and likelihood assign zero probability to the evidence; the posterior is undefined. The system should report that conflict or expand/revise the model explicitly. It must not add an arbitrary epsilon and present the result as a neutral update.

The current Lean result in [Uncertainty.lean](../Devs/Uncertainty.lean) covers natural-number weights and support behavior. It does **not** prove real-valued normalization, numerical stability, likelihood correctness, calibration, or entropy reduction.

### E06 — Sequential evidence and the independence warning

For evidence \(e_1,\ldots,e_t\),

\[
p(x\mid e_{1:t})
\propto
p(x)\prod_{k=1}^{t}P(e_k\mid x,e_{1:k-1}).
\]

Replacing the conditional factors with \(\prod_k P(e_k\mid x)\) requires conditional independence given \(x\). Repeated reports copied from one underlying source are not independent observations. The algebraic commutation of supplied likelihood factors in the Lean natural-weight model does not establish empirical independence.

### E07 — Combining explicit models

If model weights \(\pi_t(m)\) are justified and sum to one,

\[
P(Y\mid h_t)
=
\sum_{m\in\mathcal M}\pi_t(m)P(Y\mid h_t,m).
\]

When defensible model weights are unavailable, a safer report is the model envelope

\[
\underline p_t(y)=\min_{m\in\mathcal M}P(y\mid h_t,m),
\qquad
\overline p_t(y)=\max_{m\in\mathcal M}P(y\mid h_t,m).
\]

The mixture is a probability model; the envelope is a sensitivity summary. Neither creates evidence for omitted models.

### E08 — Forecast uncertainty

For a finite outcome distribution,

\[
H(Y\mid h_t)=-\sum_{y}P(y\mid h_t)\log_2 P(y\mid h_t).
\]

Entropy can rise or fall after evidence. A surprising observation may increase uncertainty. A point estimate or a low entropy is not evidence that the model is correct.

### E09 — Within-model and between-model uncertainty

When \(M\) is a discrete model index and the moments exist,

\[
\operatorname{Var}(Y\mid h_t)
=
\mathbb E_M[\operatorname{Var}(Y\mid h_t,M)]
+
\operatorname{Var}_M(\mathbb E[Y\mid h_t,M]).
\]

The first term describes variation inside models; the second describes disagreement among their expected outcomes. This is the law of total variance, not a Devs-specific law. Reporting only the first term can hide model uncertainty.

### E10 — Forecast object and interval

A bounded forecast is a record, not a bare number:

\[
F_t=(P(Y\mid h_t),\,C_{1-\alpha},\,A_t,\,\tau_t,\,R_t,\,V_t),
\]

where \(A_t\) lists assumptions, \(\tau_t\) the horizon, \(R_t\) the source revisions, and \(V_t\) the conditions that would trigger revision. For discrete outcomes, a credible set can be defined by

\[
C_{1-\alpha}
=
\arg\min_{S\subseteq\mathcal Y}|S|
\quad\text{subject to}\quad
P(Y\in S\mid h_t)\ge 1-\alpha,
\]

with a prespecified tie rule. This is a model-based interval; empirical coverage must be measured prospectively.

## 3. Claims, provenance, and criticism

### E11 — Claim record (operational definition)

\[
c_i=(\varphi_i,s_i,r_i,\ell_i,\operatorname{parents}_i),
\]

where \(\varphi_i\) is the proposition, \(s_i\) its status, \(r_i\) an immutable source revision, \(\ell_i\) a source span, and \(\operatorname{parents}_i\) the claims or observations used in its derivation.

The current status vocabulary is **proposed, derived, simulated, observed, replicated, contradicted, superseded, unknown**. Status labels are claims to justify, not evidence by themselves.

A modeled observation predicate is

\[
\operatorname{ObservedEvidence}(c)
\iff
s_i\in\{\text{observed},\text{replicated}\}
\land
\exists r\in\operatorname{references}(c):\operatorname{Valid}(r).
\]

This type-level rule is in [Provenance.lean](../Devs/Provenance.lean). It checks that a reference exists and has a revision and line range; it does not prove that a source is truthful, the span entails the claim, or the observation was independent.

### E12 — Acyclic support dependencies (existing formal model)

For every dependency edge \(u\to v\), require

\[
\rho(u)<\rho(v).
\]

Along any nonempty path, rank strictly increases; a directed cycle would require \(\rho(u)<\rho(u)\), which is impossible. [Provenance.lean](../Devs/Provenance.lean) proves this conditional result. Correctness of a real dependency graph and its rank assignment still need audit.

### E13 — Mechanical criticism as filtering (existing formal model)

For a claim set \(S\) and fixed Boolean criterion \(k\),

\[
K_k(S)=\{c\in S:k(c)=1\}.
\]

By construction, \(K_k(S)\subseteq S\), and \(K_k(K_k(S))=K_k(S)\). If the separate soundness premise

\[
\forall c,\ k(c)=1\Rightarrow \operatorname{True}(c)
\]

is established, every survivor is true. The premise is not proved by naming \(k\) a critic. The Lean companion also contains counterexamples showing that a bad criterion can retain only a false claim and that agreement can preserve an error; see [Criticism.lean](../Devs/Criticism.lean).

### E14 — Generative criticism workflow (operational definition)

\[
d_0=\operatorname{Draft}(q,R),\qquad
z=\operatorname{Critic}(q,R,d_0),\qquad
d_1=\operatorname{Revise}(q,R,d_0,z).
\]

Here \(q\) is a query and \(R\) the retrieved evidence. Unlike E13, revision may add claims not present in \(d_0\). Therefore no “does not invent claims” theorem follows. The resulting assertions and citations require independent scoring. DEV2-001 is an empirical test of particular prompts, a model, a corpus, and a token budget; it does not prove that recursive criticism generally improves accuracy.

## 4. Observers, interventions, and human agency

### E15 — World and policy transition (operational definition)

\[
X_{t+1}\sim P(\,\cdot\mid X_t,A_t,\eta_t),
\qquad
F_t=G(h_t),
\qquad
A_t\sim\pi(\,\cdot\mid h_t,F_t).
\]

The first expression models state evolution, the second generates a forecast, and the third models a person or institution responding to the forecast. This formalizes the paper’s “observer inside the model” idea. The transition law, response policy, and disturbance distribution must be identified for a real application.

### E16 — Forecast disclosure can create a fixed-point problem

If a forecast changes the response policy, a self-consistent forecast may need to satisfy

\[
F=G\bigl(h_t,\pi(F)\bigr).
\]

A solution need not exist or be unique for arbitrary \(G\) and \(\pi\). Thus a forecast made while assuming the forecast is hidden is not automatically valid after disclosure. This is a structural warning, not a claim that all social forecasts have fixed points.

### E17 — Observation versus intervention

\[
P(Y\mid A=a,h_t)
\ne
P(Y\mid \operatorname{do}(A=a),h_t)
\quad\text{in general}.
\]

Equality requires additional causal assumptions. Predictive correlations alone do not identify intervention effects. A Devs 2.0 system should label whether it reports an observational forecast or a causal intervention estimate.

### E18 — Recommendation is separate from authorization

If a causal outcome distribution and utility function are available,

\[
EU(a\mid h_t)
=
\sum_y U(y,a)P(y\mid h_t,\operatorname{do}(a)),
\qquad
A^\star=\arg\max_{a\in\mathcal A}EU(a\mid h_t).
\]

This computes a recommendation under the stated model and utility; it does not authorize execution. The Lean interface binds authorization to an exact proposal revision:

\[
\operatorname{Execute}(p,a)\ \text{is defined only with}\ 
\operatorname{Authorized}(p,a,\operatorname{revision}).
\]

[Agency.lean](../Devs/Agency.lean) proves properties of this abstract type. Real identity checks, human consent, appeal, and enforcement are outside that proof.

## 5. Scientific updating and evaluation

### E19 — Hypothesis revision after an observation

\[
\mathcal H_{t+1}
=
\operatorname{Revise}(\mathcal H_t,o_{t+1},\mathcal M_t).
\]

This is an interface definition: revision depends on the registered method and the acquired observation. A generated hypothesis, simulation, or elegant derivation is not \(o_{t+1}\). Provenance and status must distinguish the input evidence types.

### E20 — Proper scores for prospective forecasts

For a binary event with forecast probability \(p_i\) and outcome \(y_i\in\{0,1\}\),

\[
\operatorname{Brier}
=
\frac1N\sum_{i=1}^N(p_i-y_i)^2,
\qquad
\operatorname{LogLoss}
=
-\frac1N\sum_{i=1}^N
\bigl[y_i\log p_i+(1-y_i)\log(1-p_i)\bigr].
\]

These scores assess probabilistic forecasts over a prespecified set. They require forecasts to be timestamped before outcomes and evaluated against a named baseline. They do not replace checks of source accuracy, calibration, or decision impact.

### E21 — DEV2-001 paired estimand (current draft)

For item \(i\), let \(Y_{i,A}\) and \(Y_{i,C}\) be the blinded human false-assertion indicators for direct-answer arm A and critic/revision arm C. Then

\[
D_i=Y_{i,A}-Y_{i,C}\in\{-1,0,1\},
\qquad
\widehat\delta=\frac1J\sum_{j=1}^{J}
\left(\frac1{n_j}\sum_{i\in j}D_i\right).
\]

Here \(j\) indexes independently reviewed evidence families; families receive equal weight. Positive \(\widehat\delta\) favors C on the absent tier. If items are independent and \(q=P(D_i\ne0)\), then

\[
\operatorname{Var}(D_i)
=
\mathbb E[D_i^2]-\mathbb E[D_i]^2
=
q-\delta^2.
\]

The planning standard error \(\sqrt{(q-\delta^2)/n}\) is an approximation, not the production analysis. The draft analysis resamples paired evidence families. Scoring rules and gates remain subject to the incomplete freeze record in [THRESHOLDS.json](../research/dev2-001/THRESHOLDS.json).

### E22 — Resource accounting

For call stage \(s\), let \(I_s\) be all input tokens, \(O_s\) all generated tokens including reasoning, and \(C_s\le I_s\) cached input tokens:

\[
T_s=I_s+O_s,\qquad
T_{\rm run}=\sum_sT_s,\qquad
C_s\text{ remains part of }I_s.
\]

If per-million prices are \(r_{\rm in},r_{\rm cache},r_{\rm out}\), the token charge is

\[
\operatorname{Cost}
=
\frac1{10^6}\sum_s\left[
(I_s-C_s)r_{\rm in}+C_sr_{\rm cache}+O_sr_{\rm out}
\right].
\]

The current proposed ceilings are 8,192 total tokens and 1,024 generated tokens per item; the staged 256+256+512 allocation sums to 1,024. The software proves arithmetic properties of this accounting model in [Budget.lean](../Devs/Budget.lean). Correct provider token counts and a dated price schedule remain interface obligations.

### E23 — Draft decision rule, not a result

The recorded primary target is a 20-percentage-point reduction in absent-tier false assertions. A draft pass rule adds a positive paired 95% interval and resource and utility guardrails; independent reproduction allows at most 12 percentage points of absolute effect difference, while both runs must pass the same gates. Several guardrails and the complete decision package remain unapproved, and no holdout run exists. The exact operational state is **DRAFT_NOT_FROZEN**. These equations describe proposed decision logic; they do not license a verdict.

## 6. Integrated Devs 2.0 architecture

The following equations collect the preceding pieces into one distributed system and its evidence loop. They are interface definitions: an application must still supply its domain-specific state, dynamics, observation process, model family, and update method.

### E24 — Distributed, versioned knowledge state (operational definition)

Let \(\mathcal R_t\) be the set of participating repositories, papers, people, models, and instruments at time \(t\), and let \(\mathcal K_t^{(r)}\) be the records held by component \(r\). The accessible record set is

\[
\mathcal K_t=\bigcup_{r\in\mathcal R_t}\mathcal K_t^{(r)},
\qquad
G_t=(V_t,E_t),
\]

where \(G_t\) is the provenance and dependency graph over those records. A record used to support a claim must retain its source identity, immutable revision, source span, status, and dependency links as in E11–E12. The union describes availability, not corroboration: copied claims, shared upstream papers, and dependent reports do not become independent evidence because multiple components store them.

### E25 — Complete Devs 2.0 application state (operational definition)

For a chosen application, define its reviewable state as

\[
S_t=(\mathcal K_t,G_t,\mathcal H_t,\Omega_t,p_t,F_t,\mathcal U_t,\mathcal P_t),
\]

where \(\mathcal H_t\) is the explicit model/hypothesis family, \(\Omega_t\) the admitted possibilities, \(p_t\) an optional justified probability distribution, \(F_t\) the bounded forecast object, \(\mathcal U_t\) the declared decision objective, and \(\mathcal P_t\) the proposed-action and authorization record. A component may be unknown or omitted only with that status made explicit; absence of a probability model is not a license to report an invented probability.

### E26 — The recursive evidence loop (operational definition)

\[
\begin{aligned}
F_t &= \operatorname{Forecast}(S_t;\tau_t),\\
A_t &= \operatorname{Recommend}(F_t,\mathcal U_t)\quad\text{(optional)},\\
o_{t+1} &= \operatorname{Observe}(W_{t+1},A_t),\\
S_{t+1} &= \operatorname{Update}(S_t,o_{t+1};\theta_t).
\end{aligned}
\]

Here \(W_{t+1}\) is the relevant external process and \(\theta_t\) records the frozen or versioned update procedure. The forecast may affect action, and action may affect what is later observed, so E15–E17 govern this loop. Only sourced observations with the required status may enter the observation update; generated hypotheses and simulations remain separately typed. The update may restrict \(\Omega_t\), expand it with explicit alternatives, revise \(\mathcal H_t\), or leave uncertainty unresolved. This is the paper's “Know → Predict → Criticize → Test → Observe → Update → Know” cycle expressed as a software interface, not a universal law of nature.

The state schema is complete at the architectural level of the white paper. It is deliberately not a closed executable model: an implementation must instantiate the domain-specific functions, assumptions, data, and authorization rules, then validate those choices against external observations.

## Evidence and derivation audit

| Claim | Status | What would change the status |
|---|---|---|
| Set restriction, expansion, natural-weight support laws, rank acyclicity, finite filtering, exact-revision authorization, token arithmetic | **Existing formal model** | Audit model assumptions and prove any implementation refinement separately |
| Bayesian normalization, total-variance identity, proper-score definitions | **Derived identities** under their stated probability assumptions | Pin distributions, likelihoods, and scoring conventions in a concrete run |
| Distributed knowledge state, recursive feedback loop, causal recommendations, structured forecast object | **Operational definitions** | Freeze target domain, state variables, response model, evidence policy, and intervention assumptions |
| Criticism reduces false assertions | **Empirical question** | Complete and replicate a frozen, human-scored benchmark |
| Devs 2.0 predicts physical futures or validates EFMW physics | **Not established** by this equation set | Separate physical theory, dimensional analysis, falsifiable predictions, and independent data tests |

The audit does not treat repeated agreement as independent evidence, uses no benchmark outcome to select equations, and keeps generated hypotheses separate from observations. The full prediction architecture remains a specification with unresolved empirical performance.

