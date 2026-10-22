"""Blind export and human-only scoring. Never infers truth from a model's status label."""
import argparse
import json
import random
import secrets
from pathlib import Path
from core import ROOT, corpus, digest, read, passage_ok, write

FIELDS = ("false_assertion", "answerable_success", "conflict_report", "claim_count",
          "unsupported_claim_count", "citation_count", "unsupported_citation_count")


def blind(run_dir, questions, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    run_dir = Path(run_dir)
    responses, manifest = read(run_dir/"responses.json"), read(run_dir/"manifest.json")
    if digest(responses) != manifest["responses_sha256"] or digest(questions) != manifest["questions_sha256"]:
        raise ValueError("run/question digest mismatch")
    if not manifest["complete"] or any(r["status"] != "ok" for r in responses):
        raise ValueError("incomplete run: preserve as UNVERIFIED; do not count failures as abstentions")
    gold = {q["id"]: q for q in questions["questions"]}
    packets, key, rating = [], {}, []
    for r in responses:
        bid = secrets.token_hex(12)
        q = gold[r["question_id"]]
        key[bid] = {"question_id": q["id"], "arm": r["arm"]}
        packets.append({"blind_id": bid, "question": q["text"], "tier": q["tier"],
                        "gold": q["gold"], "response": r["final"]})
        rating.append(dict(blind_id=bid, **{f: None for f in FIELDS}, rationale="", arm_guess="unknown"))
    random.SystemRandom().shuffle(packets)
    random.SystemRandom().shuffle(rating)
    write(out/"packets.json", packets)
    write(out/"PRIVATE-key.json", {"run_responses_sha256": digest(responses), "map": key})
    for rater in ("rater-1", "rater-2"):
        write(out/(rater+".json"), {"rater_id": "", "human": True, "independent": False,
                                   "scored_without_key_or_other_ratings": False, "ratings": rating})
    write(out/"adjudication-template.json", {"rater_id": "", "human": True, "independent": False,
                                             "scored_without_key_or_other_ratings": False, "ratings": []})


def rating_index(form, ids, tier_for):
    if not form["rater_id"] or form["human"] is not True or form["independent"] is not True:
        raise ValueError("independent identified human raters required")
    if form["scored_without_key_or_other_ratings"] is not True:
        raise ValueError("blinded independent initial judgment attestation required")
    result = {}
    for r in form["ratings"]:
        if r["blind_id"] in result or r["blind_id"] not in ids:
            raise ValueError("duplicate/unknown rating")
        tier = tier_for[r["blind_id"]]
        active = {"absent": "false_assertion", "answerable": "answerable_success",
                  "contradictory": "conflict_report"}[tier]
        for f in FIELDS:
            v = r[f]
            if f in ("false_assertion", "answerable_success", "conflict_report"):
                if f == active and (type(v) is not int or v not in (0, 1)):
                    raise ValueError("binary human judgment missing")
                if f != active and v is not None:
                    raise ValueError("non-applicable primary/tier fields must be null")
            elif type(v) is not int or v < 0:
                raise ValueError("nonnegative claim/citation counts required")
        if r["unsupported_claim_count"] > r["claim_count"] or r["unsupported_citation_count"] > r["citation_count"]:
            raise ValueError("impossible claim/citation counts")
        if not r["rationale"].strip():
            raise ValueError("each human rating requires an evidence rationale")
        result[r["blind_id"]] = r
    return result


def combine(run_dir, questions, keyfile, first, second, adjudication=None):
    run_dir = Path(run_dir)
    manifest, responses = read(run_dir/"manifest.json"), read(run_dir/"responses.json")
    key = keyfile["map"]
    if not manifest["complete"] or digest(responses) != manifest["responses_sha256"]:
        raise ValueError("incomplete or modified run")
    if digest(questions) != manifest["questions_sha256"] or keyfile["run_responses_sha256"] != digest(responses):
        raise ValueError("scoring inputs are not tied to this run")
    qs = {q["id"]: q for q in questions["questions"]}
    rs = {(r["question_id"], r["arm"]): r for r in responses}
    if len(rs) != len(responses) or {(v["question_id"], v["arm"]) for v in key.values()} != set(rs) or len(key) != len(rs):
        raise ValueError("blinding key is not a one-to-one map of responses")
    tiers = {bid: qs[v["question_id"]]["tier"] for bid, v in key.items()}
    a, b = rating_index(first, set(key), tiers), rating_index(second, set(key), tiers)
    if set(a) != set(key) or set(b) != set(key):
        raise ValueError("every response needs two independent ratings")
    if first["rater_id"] == second["rater_id"] or manifest["operator"] in (first["rater_id"], second["rater_id"]):
        raise ValueError("raters must differ from each other and the model operator")
    disagreements = [bid for bid in key if any(a[bid][f] != b[bid][f] for f in FIELDS)]
    adjudicated = {}
    if disagreements:
        if not adjudication:
            raise ValueError("unresolved disagreements: " + ", ".join(disagreements))
        if adjudication["rater_id"] in (first["rater_id"], second["rater_id"], manifest["operator"]):
            raise ValueError("a third independent human must adjudicate")
        adjudicated = rating_index(adjudication, set(disagreements), tiers)
        if set(adjudicated) != set(disagreements):
            raise ValueError("adjudication must cover exactly the disagreements")
    docs, rows = corpus(), []
    for bid, v in key.items():
        q, r = qs[v["question_id"]], rs[(v["question_id"], v["arm"])]
        rating = adjudicated.get(bid, a[bid])
        cites = r["final"]["citations"]
        conf = r["final"].get("confidence")
        event = r["final"].get("confidence_event")
        if not (type(conf) in (int, float) and 0 <= conf <= 1 and event == "response_correctness"):
            conf = None
        rows.append(dict(question_id=q["id"], cluster_id=q["cluster_id"], tier=q["tier"], arm=v["arm"],
                         **{f: rating[f] for f in FIELDS}, input_tokens=r["input_tokens"],
                         output_tokens=r["output_tokens"], cached_input_tokens=r["cached_input_tokens"],
                         latency_seconds=r["latency_seconds"],
                         mechanical_invalid_citations=sum(not passage_ok(c, docs) for c in cites),
                         confidence=conf,
                         context_sha256=r["context_sha256"]))
    # Preserve all original judgments; never average disagreement into a half-error.
    primary_disagreements = sum(a[bid]["false_assertion"] != b[bid]["false_assertion"]
                                for bid in key if tiers[bid] == "absent")
    return {"manifest": manifest, "rows": rows, "scoring": {
        "rater_ids": [first["rater_id"], second["rater_id"]],
        "adjudicator_id": adjudication["rater_id"] if disagreements else None,
        "disagreement_count": len(disagreements), "response_count": len(key),
        "absent_primary_disagreements": primary_disagreements,
        "raw_agreement": 1-len(disagreements)/len(key),
        "first": first, "second": second, "adjudication": adjudication,
        "disagreement_blind_ids": disagreements}}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("blind", "combine"):
        sp = sub.add_parser(name); sp.add_argument("--run", required=True)
        sp.add_argument("--questions", required=True); sp.add_argument("--out", required=True)
        if name == "combine":
            for flag in ("key", "first", "second"):
                sp.add_argument("--"+flag, required=True)
            sp.add_argument("--adjudication")
    args = p.parse_args()
    if args.command == "blind":
        blind(args.run, read(args.questions), args.out)
    else:
        write(args.out, combine(args.run, read(args.questions), read(args.key), read(args.first), read(args.second),
                                read(args.adjudication) if args.adjudication else None))
