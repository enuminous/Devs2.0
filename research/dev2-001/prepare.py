"""Validate pinned corpus and create an arm-neutral, gold-free retrieval plan."""
import argparse
import random
from core import ROOT, corpus, digest, freeze_errors, read, retrieve, validate_questions, write


def prepare(data, docs, config):
    # Explicit allowlist: no tier, cluster, gold, or review metadata reaches model.
    items = [{"id": q["id"], "question": q["text"],
              "context": retrieve(q["text"], docs, config["retrieval"])} for q in data["questions"]]
    random.Random(config["order_seed"]).shuffle(items)
    return {"split": data["split"], "questions_sha256": digest(data), "items": items}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--questions", default=str(ROOT/"development/QUESTIONS.json"))
    p.add_argument("--out", required=True)
    p.add_argument("--check-freeze", action="store_true")
    args = p.parse_args()
    data, config, docs = read(args.questions), read(ROOT/"CONFIG.json"), corpus()
    validate_questions(data, docs, read(ROOT/"development/QUESTIONS.json") if data["split"] == "evaluation" else None)
    if args.check_freeze or data["split"] == "evaluation":
        errors = freeze_errors(config, read(ROOT/"THRESHOLDS.json"), data, docs)
        if errors:
            raise SystemExit("NOT READY TO FREEZE:\n- " + "\n- ".join(errors))
    write(args.out, prepare(data, docs, config))
    print("Prepared", len(data["questions"]), data["split"], "items; no generation performed.")
