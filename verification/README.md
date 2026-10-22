# Verification evidence and scope

The verification workflow distinguishes three kinds of evidence:

- **Software:** Python corpus/split/budget/scoring/analysis tests, gateway transport checks, JavaScript numerical/retrieval/import tests, and deterministic site regeneration.
- **Formal:** `lake build`, 45 theorem declarations checked by Lean 4.28.0, and `#print axioms` for every listed theorem. The audit accepts only Lean's standard `propext`, `Quot.sound`, and `Classical.choice` foundation, and rejects `sorryAx` or any new axiom. Current declarations use at most `propext` and `Quot.sound`. A declaration count is not a count of scientific discoveries.
- **Integration:** 12 public development fixtures across five arms, 60 final responses / 108 generated stages, blinded packet creation, and no human scores. This is labeled `SOFTWARE_SMOKE_ONLY`, with no LLM calls and no experimental verdict.

`python3 scripts/check_lean.py` saves the actual compiler audit and computed executable output under ignored `verification/local/`. The CI workflow uploads these logs and the software-only smoke record as a verification artifact. Logs can be matched to the workflow's exact commit; no hardcoded passing badge substitutes for them.

During initial development, the managed container did not expose the running Lean executable's `/proc/.../exe` path correctly. A scratch-only launcher shim supplied the official executable path so the unmodified Lean 4.28.0 binary could locate its own libraries. It did not modify theorem source, the kernel, or dependencies. The portable project does not require or include that shim; hosted CI runs the official archive in an ordinary Ubuntu environment as an independent execution check.

The browser review checks workbench retrieval, unknown-query handling, citation inspection, criticism, notes, possibility updating and zero-mass refusal, benchmark controls, proof search and the paper. Numerical UI examples are illustrative; uploaded reports are displayed as unverified local files. No experimental run, independent human scoring, independent research replication, or physical validation has occurred.
