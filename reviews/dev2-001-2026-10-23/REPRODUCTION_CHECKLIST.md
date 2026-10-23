# Independent reproduction-readiness checklist

Reviewer identity, affiliation, dates, baseline commit, independence disclosure:
**Unfilled.** For each row return READY / BLOCKED / NOT INSPECTED with evidence.

| Requirement | Preparation-time observation | Reviewer disposition |
|---|---|---|
| Source and corpus reconstruction | Pinned baseline; hashes and ten corpus snapshots supplied | Unfilled |
| Complete reviewed question set | 12 unreviewed public development items; evaluation ledger empty | Unfilled |
| Authentic conflict families | None established by the bounded screen | Unfilled |
| Family independence and split custody | Requires human semantic review and sealed holdout | Unfilled |
| Retrieval evidence coverage | Deterministic code exists; blind coverage review missing | Unfilled |
| Model/tokenizer snapshot and availability | Unpinned | Unfilled |
| Provider adapter and dependency lock | Contract and fixture/gateway exist; audited live adapter unpinned | Unfilled |
| Exact token accounting, seed/reasoning policy | Resource/context policy specified; provider behavior unresolved | Unfilled |
| Costs and access | Dated price schedule and any API expense cap unset | Unfilled |
| Complete decision-rule approval and freeze | Partial parameter decisions recorded; package remains draft | Unfilled |
| Separate operator and scoring custodian | Unassigned | Unfilled |
| Blinded human raters and adjudicator | Unassigned; no primary annotations completed | Unfilled |
| Complete raw evidence release | No generation run yet; expected artifacts specified in reproduction guide | Unfilled |
| Deterministic analysis replay | Code/tests supplied; no real scored run to reproduce | Unfilled |
| Independent new generation and scoring | Future separately agreed stage; cannot presently be attested | Unfilled |
| Both-run gates and 12-point effect agreement | Criteria specified; no observed effects | Unfilled |
| Signed result review | Cannot certify an unproduced result | Unfilled |

After a real run exists, obtain the freeze and results commits; full question/gold
ledger; corpus, prompts and model/adapter/environment pins; retrieval plans and
coverage review; every raw request/response and provider usage record; randomized
order/seeds; failures and deviations; both original human votes and rationales;
adjudication and blinding diagnostics; analysis outputs; cost/latency accounting;
and role/custody records with secrets removed. The independent operator reruns
generation; different independent raters score it; both runs retain negative and
inconclusive results. An unavailable model snapshot blocks full reproduction.
