# SciFact corpus extension

**Role:** public development source and held-out candidate pool for research on evidence-grounded claim verification. This extension does not replace the ten-version DEV2-001 corpus or freeze an experiment.

## Source pin

The official SciFact release endpoint is maintained by the Allen Institute for AI. The builder downloads the archive into memory when `data.tar.gz` is absent beside the script; a supplied local archive is used when present. In either case it refuses any bytes whose SHA-256 differs from the pinned digest. The 3.1 MB upstream archive is not included in this repository.

- Archive: [official data release](https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz)
- SHA-256: **11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be**
- Source repository: [allenai/scifact](https://github.com/allenai/scifact)
- Dataset and schema documentation: [README](https://github.com/allenai/scifact/blob/master/README.md), [data schema](https://github.com/allenai/scifact/blob/master/doc/data.md), [license](https://github.com/allenai/scifact/blob/master/LICENSE.md)
- Paper: Wadden et al., [“Fact or Fiction: Verifying Scientific Claims”](https://aclanthology.org/2020.emnlp-main.609/), EMNLP 2020.

The source archive contains 5,183 scientific abstracts, 809 labeled training claims, 300 labeled development claims, and 300 test claims without released labels or cited-document IDs. Among train and development claims, the source labels comprise 456 SUPPORT, 237 CONTRADICT, and 416 with no annotated evidence. These are source-data counts, not results for Devs 2.0.

## Reproducible candidate material

Run with Python 3.12 or newer:

~~~bash
python research/dev2-001/expansion/scifact/make_candidates.py
~~~

The script verifies the archive digest, checks the expected source files, and writes:

- development_candidates_480.jsonl: a deterministic 120 / 240 / 120 sample from the public labeled train/development records. It uses one record per exact cited-document set and does not reuse an exact set across tiers.
- unlabeled_test_pool_300.jsonl: the official unlabeled test claims, preserving the absence of labels.
- audit.json: source counts, selection rules, and limitations.

The development sample uses this explicit mapping:

| SciFact source label | DEV2 candidate tier | Narrow meaning |
|---|---|---|
| SUPPORT | answerable | Cited abstracts support the claim |
| NOINFO | absent | The cited abstracts do not establish the claim |
| CONTRADICT | contradictory | At least one cited abstract contains evidence labeled as contradicting the claim |

Here, **absent** is scoped to a claim’s cited abstracts. It does not mean that no relevant information exists anywhere in the world or across every paper. The candidate question asks whether the cited abstracts support, contradict, or fail to establish the provided scientific claim. That is a claim-verification task and differs from the current DEV2-001 closed-corpus question-answering task.

## Evidence boundary

The 480-row sample is **public labeled development material**, not a sealed evaluation set. Its source annotations and claims are public, and model-training exposure cannot be ruled out. It is suitable for workflow development, prompt debugging, reviewer training, or a clearly labeled public diagnostic. It cannot support an untouched-holdout claim.

The script deduplicates identical cited-document sets, but different sets can share abstracts or derive from related studies. The candidate family IDs are provisional. Two independent human curators must review semantic overlap, evidence-family independence, wording, cited passages, and labels before any confirmatory use. A separate scoring team and frozen model/runtime configuration are still required.

The 300 official test claims have no released gold labels or cited-document IDs. They are a useful independent annotation pool, but their class distribution is unknown and the pool alone cannot be assumed to satisfy the approved 120 / 240 / 120 counts. New independently reviewed items or a separately approved sample design may be needed.

**No SciFact item has been merged into the canonical research/dev2-001/CORPUS.json or QUESTIONS.json.** Using SciFact for the original experiment requires an explicit protocol amendment because its task and contradiction definition differ. The public development sample does not clear the existing freeze gate.

## Attribution and licensing

SciFact identifies the claim text and evidence annotations as CC BY 4.0, and the abstract corpus as part of Semantic Scholar S2ORC under ODC-By 1.0. The project archive is not committed here. Generated candidate rows contain adapted claim text and annotation metadata, but no abstract text. The SciFact code is Apache 2.0; this extension does not copy it.

Citation:

> David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh Hajishirzi. “Fact or Fiction: Verifying Scientific Claims.” EMNLP 2020.

Attribution for the adapted claim/evidence records: David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh Hajishirzi, “Fact or Fiction: Verifying Scientific Claims,” EMNLP 2020; SciFact dataset from the Allen Institute for AI. Changes made here: deterministic subset selection, label-to-tier mapping, and task-prompt formatting. This attribution does not imply endorsement.

The builder's 480-row file is a selected and reformatted derivative of the public claim/evidence annotations: it maps labels into candidate tiers, adds a task-specific prompt, and retains source claim IDs, cited-document IDs, and gold sentence indices. It does not copy S2ORC abstract text into the generated candidate files. The archive is verified against the exact SHA-256 above before any rows are produced.

