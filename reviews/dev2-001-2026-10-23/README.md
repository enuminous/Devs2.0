# DEV2-001 initial methods-review packet

**23 October 2026 · DRAFT_NOT_FROZEN · no confirmatory model result**

This packet makes the bounded initial review request concrete. It does not record
an accepted engagement, an endorsement, a fee agreement, or independent human work.
The reviewed benchmark baseline is [Devs2.0 `f6a4f30`](https://github.com/enuminous/Devs2.0/tree/f6a4f30c55190e1eff0026ea3f1f004ec34b363a/research/dev2-001),
the same snapshot named in the already-sent request. New packet files are outside
the benchmark corpus; the ten-version corpus, prompts, thresholds and empty holdout
are unchanged.

## Reviewer handoff

1. Read [scope and deliverables](SCOPE.md), then the pinned protocol, scoring manual,
   design brief, configuration, thresholds, approvals and reproduction guide.
2. Review the 12 public development examples in [the worksheet](QUESTION_REVIEW_WORKSHEET.json).
   The proposed gold is included for curation review. Both human-review columns are blank.
3. Examine [conflict screening](CONFLICT_SCREENING.md) and its exact-source ledger.
   **No eligible authentic conflict has been established.** Four historical amendments
   were screened; they are not four independent conflict families. A smaller initial
   review is appropriate unless new authentic candidates are supplied.
4. Address [the statistical and independence questions](METHODS_REVIEW.md) and return
   [a reproduction-readiness checklist](REPRODUCTION_CHECKLIST.md).
5. Resolve [availability, independence and commercial terms](ENGAGEMENT_QUESTIONS.md)
   before any service commitment or paid work.

## Materials included and requested outputs

| Material | Purpose |
|---|---|
| [Baseline manifest](BASELINE_MANIFEST.json) | Exact hashes of all benchmark sources and the 10-version corpus |
| [Question worksheet](QUESTION_REVIEW_WORKSHEET.json) | Existing question/gold, evidence and absence audits, dependency leads, blank independent judgments |
| [History census](HISTORY_CENSUS.json) and [screening ledger](CONFLICT_SCREENING.json) | Bounded source-history search with immutable versions, quotes and dispositions |
| `evidence/` | Review-only snapshots; explicitly excluded from model retrieval and the closed corpus |
| [Planning output](PLANNING_OUTPUT.json) | Reproduced analytic assumptions, not performance observations |
| [Readiness snapshot](READINESS_SNAPSHOT.json) | Machine-reported blockers at preparation time |
| [Scoring work order](HUMAN_SCORING.md) | Separate blinded human annotation scope and workload |

Return (a) an annotated worksheet, (b) a short methods memo with blocking issues and
suggested prospective amendments, and (c) a reproduction-readiness checklist.
Reviewing these public examples does not replace two-person review of all 480
proposed evaluation items. Do not turn any packet example into an untouched holdout.

From the repository root, verify the handoff without model calls:

```sh
python3 reviews/dev2-001-2026-10-23/verify_packet.py
python3 bench.py doctor
python3 bench.py doctor --require-frozen
```

The last command must still refuse this draft. The packet is AI-assisted preparation;
all independent reviewer decisions, curator attestations, raters and signatures remain
unfilled. A later reviewer can assess a produced result only after generation, scoring,
analysis and independent reproduction evidence exists.

The packet verifier is an explicit check against this historical baseline. Later
benchmark edits should report baseline drift; prepare a new review snapshot when
needed. This historical draft check is not installed as a permanent gate that
would prevent a legitimately completed future freeze.
