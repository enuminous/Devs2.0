#!/usr/bin/env python3
"""Verify the pinned SciFact archive and build a public development candidate set.

This never creates a confirmatory holdout and makes no model calls.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import tarfile
import urllib.request
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "data.tar.gz"
ARCHIVE_URL = "https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz"
EXPECTED_SHA256 = "11c621288d41ac144d29b13b0f8503b3820b7d6e8b1f6ff24dff335c196d76be"
SEED = "DEV2-SCIFACT-PUBLIC-DEV-2026-11-08"
TARGETS = {"SUPPORT": 120, "NOINFO": 240, "CONTRADICT": 120}
ALLOWED_MEMBERS = {
    "data/claims_train.jsonl",
    "data/claims_dev.jsonl",
    "data/claims_test.jsonl",
    "data/corpus.jsonl",
}


def read_jsonl(raw: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]


def source_class(row: dict[str, Any]) -> str:
    labels = {
        item["label"]
        for items in (row.get("evidence") or {}).values()
        for item in items
    }
    if not labels:
        return "NOINFO"
    if labels == {"SUPPORT"}:
        return "SUPPORT"
    if labels == {"CONTRADICT"}:
        return "CONTRADICT"
    return "MIXED"


def family_key(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(str(doc_id) for doc_id in row.get("cited_doc_ids", [])))


def stable_key(text: str) -> str:
    return hashlib.sha256((SEED + "\0" + text).encode("utf-8")).hexdigest()


def load_archive() -> dict[str, bytes]:
    if ARCHIVE.is_file():
        raw = ARCHIVE.read_bytes()
    else:
        with urllib.request.urlopen(ARCHIVE_URL, timeout=60) as response:
            raw = response.read()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_SHA256:
        raise SystemExit(f"archive SHA-256 mismatch: {actual}")
    files: dict[str, bytes] = {}
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        names = {member.name for member in archive.getmembers() if member.isfile()}
        if not ALLOWED_MEMBERS.issubset(names):
            raise SystemExit(f"archive missing required data files: {sorted(ALLOWED_MEMBERS - names)}")
        for member in archive.getmembers():
            if not member.isfile():
                continue
            if member.name not in ALLOWED_MEMBERS:
                continue
            if member.name.startswith("/") or ".." in Path(member.name).parts:
                raise SystemExit(f"unsafe archive path: {member.name}")
            stream = archive.extractfile(member)
            if stream is None:
                raise SystemExit(f"cannot read archive member: {member.name}")
            files[member.name] = stream.read()
    return files


def canonical_rows(rows: list[dict[str, Any]]) -> dict[tuple[str, ...], list[dict[str, Any]]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        tier = source_class(row)
        key = family_key(row)
        if tier in TARGETS and key:
            groups[key].append(row)
    return groups


def select(groups: dict[tuple[str, ...], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Choose exact mix with no repeated cited-document set across tiers.

    Candidate family independence across *overlapping* citation sets still needs
    human review. This deduplicates exact sets only.
    """
    by_tier: dict[str, dict[tuple[str, ...], list[dict[str, Any]]]] = {
        tier: collections.defaultdict(list) for tier in TARGETS
    }
    for key, rows in groups.items():
        for row in rows:
            tier = source_class(row)
            if tier in TARGETS:
                by_tier[tier][key].append(row)

    selected: list[dict[str, Any]] = []
    used: set[tuple[str, ...]] = set()
    for tier in ("NOINFO", "CONTRADICT", "SUPPORT"):
        candidates = []
        for key, rows in by_tier[tier].items():
            if key in used:
                continue
            row = sorted(rows, key=lambda r: (r.get("split", ""), r["id"]))[0]
            candidates.append((stable_key(tier + ":" + "|".join(key)), key, row))
        candidates.sort()
        need = TARGETS[tier]
        if len(candidates) < need:
            raise SystemExit(
                f"not enough unique cited-document sets for {tier}: "
                f"{len(candidates)} available, {need} required"
            )
        chosen = candidates[:need]
        for _, key, row in chosen:
            used.add(key)
            selected.append(make_candidate(row, tier, key))
    return selected


def make_candidate(
    row: dict[str, Any], tier: str, key: tuple[str, ...]
) -> dict[str, Any]:
    source_labels = {
        "SUPPORT": "SUPPORTED",
        "CONTRADICT": "CONTRADICTED",
        "NOINFO": "NOT_ESTABLISHED_IN_CITED_ABSTRACTS",
    }
    family_digest = hashlib.sha256("\0".join(key).encode("utf-8")).hexdigest()[:20]
    doc_evidence = []
    for doc_id, items in sorted((row.get("evidence") or {}).items()):
        for item in items:
            doc_evidence.append({
                "doc_id": str(doc_id),
                "label": item["label"],
                "sentence_indices_zero_based": item["sentences"],
            })
    claim = row["claim"]
    return {
        "record_id": f"scifact-{row.get('split','train')}-{row['id']}",
        "split": "public_development_candidate",
        "tier": {"SUPPORT": "answerable", "NOINFO": "absent", "CONTRADICT": "contradictory"}[tier],
        "source_label": tier,
        "expected_behavior": source_labels[tier],
        "question": (
            "Using only the cited abstracts for this record, classify whether the "
            "claim is supported, contradicted, or not established by those abstracts. "
            "Do not use outside knowledge. Claim: " + claim
        ),
        "claim_text": claim,
        "source_split": row.get("split"),
        "source_claim_id": row["id"],
        "cited_doc_ids": list(key),
        "gold_evidence": doc_evidence,
        "evidence_family_candidate": family_digest,
        "family_status": "PROVISIONAL_EXACT_CITATION_SET; overlapping source dependencies require human review",
        "label_source": "SciFact public train/dev annotation; never treat this row as sealed evaluation data",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=HERE)
    args = parser.parse_args()
    files = load_archive()
    train = [dict(row, split="train") for row in read_jsonl(files["data/claims_train.jsonl"])]
    dev = [dict(row, split="dev") for row in read_jsonl(files["data/claims_dev.jsonl"])]
    test = [dict(row, split="test") for row in read_jsonl(files["data/claims_test.jsonl"])]
    corpus = read_jsonl(files["data/corpus.jsonl"])
    labeled = train + dev

    counts = collections.Counter(source_class(row) for row in labeled)
    groups = canonical_rows(labeled)
    family_counts = {
        tier: len({key for key, rows in groups.items() if any(source_class(r) == tier for r in rows)})
        for tier in TARGETS
    }
    candidates = select(groups)
    candidate_counts = collections.Counter(item["source_label"] for item in candidates)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "development_candidates_480.jsonl").open("w", encoding="utf-8") as f:
        for row in candidates:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    # The official test split has no released labels or cited-document IDs.
    # Keep it as an unlabeled human-curation pool; never infer its class.
    test_pool = [
        {
            "record_id": f"scifact-test-{row['id']}",
            "split": "unlabeled_test_candidate_pool",
            "source_claim_id": row["id"],
            "claim_text": row["claim"],
            "gold": None,
            "label_status": "NOT_RELEASED_BY_SOURCE",
        }
        for row in test
    ]
    with (args.out_dir / "unlabeled_test_pool_300.jsonl").open("w", encoding="utf-8") as f:
        for row in test_pool:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    audit = {
        "dataset": "SciFact",
        "archive_sha256": EXPECTED_SHA256,
        "counts": {
            "corpus_abstracts": len(corpus),
            "train_claims": len(train),
            "dev_claims": len(dev),
            "unlabeled_test_claims": len(test),
            "train_dev_labels": dict(sorted(counts.items())),
            "train_dev_unique_citation_sets_by_label": dict(sorted(family_counts.items())),
            "development_candidate_mix": dict(sorted(candidate_counts.items())),
            "unlabeled_test_pool": len(test_pool),
        },
        "candidate_selection": {
            "seed": SEED,
            "targets": TARGETS,
            "exact_citation_set_reuse_across_selected_rows": 0,
            "semantic_independence": "NOT ESTABLISHED; overlapping source-document dependencies require two human reviewers",
            "use": "development / public diagnostic only; source labels are public",
        },
        "limitations": [
            "The SciFact claim-verification task differs from the original corpus-QA task.",
            "NOINFO means no evidence was annotated in the cited abstracts; scope is limited to those abstracts.",
            "The 300 test claims are unlabeled and have no cited_doc_ids in the release.",
            "Public train/dev claims and labels are not an untouched holdout.",
            "No user/model calls, ratings, or confirmatory experiment are performed by this script.",
        ],
    }
    (args.out_dir / "audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(audit, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

