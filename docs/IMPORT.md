# Reuse and source provenance

The implementation reuses DEV2-001 from `enuminous/papers` at **f1c8f5d15e873174bad25a018adadd71557cb659**. `IMPORT.json` records all imported paths and original Git blob IDs. The initial import commit preserves this lineage. `Devs2.0-EFMW.md` and `DEVS2-Protocol.md` retain the original text and attribution.

The current corpus anchor is **c4e9d7cf4a2dbf6646aaf45f39d75593fa674331**; two historical revisions have their own exact commits in `research/dev2-001/CORPUS.json`. All ten original document byte streams are bundled under `research/dev2-001/corpus/`, with the unchanged SHA-256 manifest. A fresh or shallow clone of this repository can therefore verify the corpus without needing the papers repository's Git objects. Verification fails closed on a hash mismatch. The original Git-object fallback remains available for use in the source repository.

Changes from the imported package: bundled-corpus loading; deterministic fixture and HTTPS gateway transports; median/p95 and component usage reporting; integration tests; root CLI; documentation for this standalone repository; and the application/formal companion. These changes are visible in Git history. Original approval and question-split records remain intact. No new design approval, human annotation, model identity, or empirical outcome was invented during import.

The browser contains copies of already public research, not private Boardy correspondence. Public methodological suggestions are assessed in `DESIGN_REVIEW.md` without publishing email threads or financial discussions.
