# Source, reuse and evidence audit

**22 October 2026 · DRAFT_NOT_FROZEN**

## Existing work located

- Boardy's 20 October DEV2-001 email was read directly. Its body says draft/not
  frozen despite the subject referring to a frozen spec. The public copy already
  exists at [`DEVS2-Protocol.md`](../../DEVS2-Protocol.md), introduced in commit
  `8c81477c6538af11ac692f33903e98a3d3511a42`. This package extends it rather than
  replacing its original text. Private mail headers and unrelated correspondence
  are not republished.
- [`Devs2.0-EFMW.md`](../../Devs2.0-EFMW.md) was read at the source. Sections 5,
  6 and 16 motivate provenance, adversarial criticism and independent evaluation
  of architecture. The paper explicitly separates that evaluation from physics.
- The local repository, all three fetched remote branches, commit history,
  bounded owner-scoped code and issue searches, and current open-PR listing
  disclosed the existing prose protocol but no executable DEV2-001 package.
  Indexed code search initially missed even the prose file; this is why the
  repository-tree inspection was necessary. This is a bounded search, not a
  guarantee about every private or unpushed project.
- At the initial draft's source check, available newer email and prior-decision context did not disclose approval of
  the question mix, performance margin, model, token budget, sample size or freeze.
  At that point Boardy's 20-point and 1.5× figures remained suggestions. Matthew
  subsequently selected the question mix and 20-point margin in this conversation;
  see [APPROVALS.md](APPROVALS.md). The 1.5× cap remains a proposal.

## Source pin and history limitations

The repository main head used to construct the draft is
`c4e9d7cf4a2dbf6646aaf45f39d75593fa674331`. `CORPUS.json` pins eight current
research documents and two authentic older versions. Only those ten versions
count toward question answerability. The DEV2 protocol, gold answers, unrelated
documents and links outside the manifest do not count.

Historical inspection found additions to R-001 and a bibliography correction to
ME-003. These are not, by themselves, an independently verified bank of scientific
contradictions. Tier C is therefore an explicit remaining curation obligation.
The current development set has six answerable and six candidate absent items;
all await independent review. No held-out questions have been invented or run.

## Evidence status

| Claim or obligation | Status |
|---|---|
| Existing white paper and Boardy protocol found | Demonstrated by direct source read |
| Corpus bytes and development evidence spans can be reconstructed | Computationally checked against pinned Git objects |
| Scoring, pairing, budgets and refusal of unfrozen evaluation | Software checks; see test suite and CI |
| Development absent labels are semantically correct | Supported only as draft candidates; independent review unresolved |
| Sufficient genuine contradictory version families | Unresolved |
| Matthew approved question mix and minimum improvement | Recorded: 120 / 240 / 120 and 20 percentage points; see APPROVALS.md |
| Matthew approved the full decision-rule package and freeze | Not recorded; remains pending |
| Provenance plus criticism reduces false assertions | Hypothesis; no model experiment executed |
| Architecture outperforms conventional D/E baselines | Unresolved |
| Novel architecture or new EFMW physics is established | Not established by this task or benchmark |

The skill's anti-circularity principles are implemented as separation of gold
from model inputs, no model primary grader, fixed pre-run criteria, family-level
split checks, preserved negative outcomes and an independent reproduction gate.
No full Zoo-animal certification or mathematical proof is asserted.

## Explicit additions to Boardy's proposal

These are proposed implementation choices, not undocumented prior agreements:
two conventional baselines; all-output double human scoring; total-token rather
than per-call budgeting; family-level pairing; one primary plus Holm-controlled
exploratory comparisons; utility guardrails; an interval-aware kill rule;
independent-replication tolerances; and executable refusal of an unfrozen run.
The linked [decision brief](DESIGN.md) explains the material changes.

Boardy refers to EFMW-GRID-006 verdict definitions. That external verdict text
was not established by the scoped source inspection. This package states its
own complete proposed decision rules instead of assuming unseen definitions.
