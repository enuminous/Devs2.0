# DEV2-001 design decision record

**22 October 2026 · Two parameters approved · Experiment remains DRAFT, NOT FROZEN**

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

## Scope and remaining work

This records approval of the **question counts and minimum absolute improvement**.
It does not represent approval of every other proposed parameter or establish
that the evaluation questions already exist. The additional failure rule, resource
limits, utility guardrails, family-count minima and reproduction tolerances retain
their separately identified proposed status. The original requirements for
independence, equal-budget comparisons and reproducibility remain in force.

The full-protocol approval fields in `THRESHOLDS.json` remain unset and
`recommendation_only` remains true for that complete rule package; the new
`parameter_approvals` object identifies the two approved selections precisely.
Both `CONFIG.json` and `THRESHOLDS.json` remain `DRAFT_NOT_FROZEN`.

Before freeze, complete independently reviewed held-out questions, an authentic
conflict inventory, pinned model/tokenizer/adapter, resource and price settings,
retrieval review, human scoring arrangements and the remaining design decisions.
If the corpus cannot supply the approved category counts, document that finding
and obtain a revised mix rather than silently reallocating or fabricating items.

No model experiment, success verdict or validation of EFMW physics follows from
this approval record.
