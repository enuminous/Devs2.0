# Reproduce the draft and prepare a future frozen run

**No experiment has run. Python infrastructure was developed with CPython 3.12.14.**
The package uses only the Python standard library and Git. No install step or
secret is needed for corpus reconstruction, planning, preparation or tests.

## 1. Checkout and offline verification

Clone `https://github.com/enuminous/Devs2.0.git` and check out the exact
package commit under study. This standalone repository bundles all ten original
corpus byte streams; a shallow clone is sufficient. Each still has its original
commit and SHA-256 in `CORPUS.json`. The source package came from `enuminous/papers`
at f1c8f5d15e873174bad25a018adadd71557cb659 (see root `IMPORT.json`).
From the repository root:

```bash
python --version
git --version
python -m unittest discover -s research/dev2-001/tests -v
python research/dev2-001/prepare.py --out /tmp/dev2-development-plan.json
python research/dev2-001/planning.py
```

`prepare.py` verifies SHA-256 of every source version and every gold quotation.
Its plan contains question IDs, text and the exact retrieved passages; gold,
tiers, curator notes and family IDs are excluded by an explicit allowlist.
The full private question ledger is never passed to the provider adapter.
Inspect representative retrieval coverage manually on development before tuning.

The tests include fabricated data with known outcomes. Those fixtures test
software, pairing and refusal paths only. They are not DEV2-001 observations.
The CI workflow executes only these local checks; it does not call any model.

## 2. Provider adapter contract

Create and audit a provider-specific adapter, commit its source and exact
dependency/environment lock, record its SHA-256 and model/tokenizer snapshot in
`CONFIG.json`, and test it **only on development**. This draft supplies the
orchestrator and contract; a live provider adapter remains an explicit integration
task. `adapters/gateway.py` supplies a working HTTPS JSON transport to an audited
backend, and `adapters/fixture.py` is explicitly software-only. Neither chooses
or validates a real model. Do not substitute a changing model alias for a snapshot or invent API usage.

The runner launches `python adapter.py`, writes one JSON request on stdin and
expects exactly one JSON object on stdout. Put diagnostics on private stderr;
never print API keys. Required operations:

```json
{
  "op": "count",
  "model": {"snapshot": "exact-snapshot", "tokenizer": "exact-tokenizer", "temperature": 0, "top_p": 1},
  "system": "rendered common and stage prompt",
  "input": {"question": "...", "context": [], "prior_stages": []},
  "seed": 73519,
  "stage": "answer"
}
```

Return `{"input_tokens": 123, "tokenizer": "exact-tokenizer"}` using the real
tokenizer, including message envelopes. Counting must not invoke answer generation.
`op: "generate"` carries the same request plus `max_output_tokens`. Return:

```json
{
  "model_snapshot": "exact-snapshot",
  "text": "{\"answer\":\"...\",\"citations\":[]}",
  "finish_reason": "stop",
  "usage": {"input_tokens": 123, "output_tokens": 45, "cached_input_tokens": 0}
}
```

`output_tokens` must include all generated/reasoning tokens, not only visible
text. Count cached tokens as part of input. Map truncation, refusal or incomplete
generation to a non-`stop` finish reason. Preserve raw provider records in the
adapter audit log with secrets removed. If exact preflight counting is impossible
for the chosen service, this adapter is not ready for this strict-budget protocol;
change and approve the accounting design prospectively rather than estimating
tokens and calling them measured. No auto-retries or hidden provider-side tools.
Record unsupported seed behavior and residual nondeterminism explicitly.

No model is selected here and no monetary cost is inferred from token counts.
Record dated input/output/cached prices, currency, source and any additional
fees before evaluation. The implemented model covers per-token charges; select a
service without unmodeled charges or extend and approve the cost code first.

## 3. Development run, after configuring a real adapter

```bash
python research/dev2-001/run.py --questions research/dev2-001/development/QUESTIONS.json --adapter research/dev2-001/adapters/provider.py --out /tmp/dev2-development-run
```

Output directory must not already exist. The runner writes the context plan,
every returned call, final responses, usage and a manifest. Development manifests
always say `official: false`. Partial and malformed responses remain recorded;
there is no automatic retry, replacement or primary-success credit.

The present development examples cover only answerable/absent candidates. A
complete three-tier development analysis requires independently audited conflict
examples; the analyzer deliberately rejects a missing tier or fewer than two
families in a contrast. Do not use fabricated examples as research evidence.

## 4. Freeze checklist and commit ordering

Complete all of these before any held-out generation:

1. The mix and margin decision is recorded in `APPROVALS.md` and
   `THRESHOLDS.json.parameter_approvals`. Complete the approval record for the
   accompanying failure, budget, utility and reproduction rules.
   The top-level approval fields and `recommendation_only` concern the complete
   rule package; set `recommendation_only: false` only after full approval. Check that pass and kill
   boundaries do not overlap if changing margins.
2. Curate the complete holdout with two human reviewers, evidence spans, whole-
   corpus absence audits, neutral wording, genuine conflict explanations, and
   development/evaluation evidence-family separation. Re-pin the corpus if it
   must expand; redo all affected audits. Do not re-use the public dev examples.
3. Fix prompts/retrieval, perform a blind evidence-coverage review, and record
   model snapshot, tokenizer, exact settings, seed support, adapter source/hash,
   environment lock, prices, operator and a distinct scoring custodian.
4. Have the independent custodian attest that the holdout was sealed before
   generation and never used for tuning. Commit full questions/gold in a private
   controlled checkout or branch if public exposure would contaminate tuning.
   A separate digest can be published before disclosure; this runner needs the
   full reviewed ledger in the actual freeze checkout.
5. Set status in both `CONFIG.json` and `THRESHOLDS.json` to `FROZEN` only when all substantive approvals and inputs exist.
   Run the gate and tests, then commit the entire package. Do not run generation
   while `git status --porcelain` shows changes.

```bash
python research/dev2-001/prepare.py --questions research/dev2-001/QUESTIONS.json --check-freeze --out /tmp/dev2-evaluation-plan.json
python -m unittest discover -s research/dev2-001/tests -v
```

The current draft fails the gate as intended. A successful gate is necessary,
not proof that human attestations or absence judgments are true; inspect them.

Create a dedicated run branch **at the freeze commit**. The manifest records that
commit after it exists; do not attempt to embed a commit's own SHA in itself.
Write runs under `research/dev2-001/runs/<run-id>/` or an external output directory.
Do not edit the package's `RUN.md` template during execution; copy it into the run
directory. No prompts, code, gold or thresholds change after freezing.

## 5. Generate, blind, score, analyze

Commands below assume a real frozen checkout and approved inputs:

```bash
python research/dev2-001/run.py --questions research/dev2-001/QUESTIONS.json --adapter research/dev2-001/adapters/provider.py --out research/dev2-001/runs/run-001
python research/dev2-001/score.py blind --run research/dev2-001/runs/run-001 --questions research/dev2-001/QUESTIONS.json --out /tmp/dev2-human-scoring
```

The custodian privately distributes the two blank rating forms and packets.
After both humans finish, a third independently judges every disputed response.
Do not fill these forms with an LLM, infer raters' approval, or expose the key.

```bash
python research/dev2-001/score.py combine --run research/dev2-001/runs/run-001 --questions research/dev2-001/QUESTIONS.json --key /tmp/dev2-human-scoring/PRIVATE-key.json --first /tmp/dev2-human-scoring/rater-1.json --second /tmp/dev2-human-scoring/rater-2.json --adjudication /tmp/dev2-human-scoring/adjudication.json --out research/dev2-001/runs/run-001/scored.json
python research/dev2-001/analyze.py --scored research/dev2-001/runs/run-001/scored.json --out research/dev2-001/runs/run-001/analysis.json
```

Omit `--adjudication` only if there are no disagreements. Neither script imputes
missing scores or silently excludes bad outcomes. Review recorded costs, counts,
conflicts and all gates. `analyze.py` reports `UNVERIFIED` for development or an
unfrozen/mismatched package regardless of attractive diagnostic numbers.

## 6. Publish and independently reproduce

After scoring is locked, release the run manifest, all raw calls, context plan,
questions/gold, rater votes/rationales, key, adjudication and report with secrets
removed and scoring identities pseudonymized consistently if needed. Preserve
independence evidence under controlled access. Release a negative/inconclusive
run with the same completeness. Force-add only the intended files from ignored
run directories; never add credentials or unreviewed private adapter logs.

Make the results commit directly on the freeze commit and verify its parent with
`git rev-parse HEAD^`. The report names both hashes. If integrating elsewhere,
preserve that run-branch history. Hashes, Python/Git versions and exact adapter
environment belong in the report. The corpus stays pinned even if `main` moves.

An independent operator must rebuild from the package alone, re-run generation
and obtain fresh independent human ratings. Replaying the original responses
checks analysis reproducibility only. Reproduce the deterministic analysis
within 1e-12; the proposed generation replication requires primary effects within
5 points, the same direction and all original gates in **both** runs. Document
who is independent of whom, artifacts and commands. The signed release review,
not a boolean command-line switch, determines whether `SUPPORTED` is justified.
If reproduction is missing, unavailable or disagrees, retain `UNVERIFIED`/failed
replication and state exactly what was reproduced.
