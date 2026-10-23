# DEV2-001 design decision record

**Decisions and follow-up implementation · Experiment remains DRAFT, NOT FROZEN**

## Decision 2026-10-22: evaluation mix and minimum improvement

Matthew Chenoweth Wright explicitly selected the following values in the
continuing DEV2-001 conversation, responding to the two design-choice questions:

| Parameter | Approved value | Meaning |
|---|---|---|
| `evaluation_counts` | 120 answerable / 240 absent / 120 contradictory | 480 evaluation questions total |
| `pass_absolute_improvement` | 0.20 | At least 20 percentage points absolute reduction in absent-tier false assertions, C versus A |

His responses were:

> 120 / 240 / 120 — recommended

> 20 percentage points — recommended

Source: Matthew's explicit reply to the published draft's design-choice questions
in this conversation. The record uses the session date in America/Los_Angeles;
no precise approval time or external message identifier is asserted.

The alternatives in `DESIGN.md` remain documented but were not selected. The
approved numerical values already matched the draft configuration, so this
change records their approval without changing those values.

## Follow-up: resource policy and replication

Matthew subsequently instructed implementation of Boardy's suggested fixes:
pin A's token budget, choose full transcript or fixed state for critic stages,
widen replication tolerance to around 12–15 points, then freeze and tag.
This authorizes the fixes and a valid freeze; no extra generic permission is
needed. It does not supply missing questions, model pins or human assignments.

The implementation records these choices on 2026-10-23 UTC:

| Choice | Recorded implementation |
|---|---|
| Arm A | Retain one ordinary-answer call, output cap 1,024; common total input/output cap 8,192 |
| Efficiency denominator | A's observed total tokens on the identical complete roster |
| Critic context | `full_prior_outputs_v1` for both C and E: same question/evidence plus all earlier outputs; common/current stage instructions only |
| Replication agreement | At most 0.12 absolute effect difference (12 percentage points), same positive direction and all original gates in both runs |

Twelve points was selected during implementation as the stricter end of the
requested range. It is not represented as an explicit exact-number reply from
Matthew. The 5/12/15-point precision comparison is in `DESIGN.md`. The 20-point
minimum gain is unchanged. No evaluation outcome informed these choices.

The stage-history journal also required a correction: earlier request records
shared a mutable list with later completions. Actual adapter inputs were correct,
but their retained logs could acquire future outputs. Each call now retains its
own prior-output snapshot, verified against the actual serialized-call boundary.

## Scope and remaining work

The original numerical approvals and follow-up choices are distinct from sealing
an executable experiment. The evaluation file still has zero questions; the
model/tokenizer/adapter, prices, custody and independent scoring roles are unset.
The original independence, equal-budget and reproducibility requirements remain
in force. The remaining proposed guardrails must be included in the final sealed
record; changing them or the approved mix requires a prospective decision.

The full-protocol approval fields in `THRESHOLDS.json` remain unset and
`recommendation_only` remains true for the incomplete package.
`parameter_approvals` identifies the original two selections; `design_followup`
records the later authorization and implementation choices without inventing
approvals for inputs that do not exist.
Both `CONFIG.json` and `THRESHOLDS.json` remain `DRAFT_NOT_FROZEN`.

Freeze was requested but **cannot pass the readiness checks**. The tag
`dev2-001-v0.2-draft` identifies only this tested design/software checkpoint.

Before freeze, complete independently reviewed held-out questions, an authentic
conflict inventory, pinned model/tokenizer/adapter, resource and price settings,
retrieval review, human scoring arrangements and the remaining design decisions.
If the corpus cannot supply the approved category counts, document that finding
and obtain a revised mix rather than silently reallocating or fabricating items.

No model experiment, success verdict or validation of EFMW physics follows from
this approval record.
