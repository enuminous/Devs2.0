"""Provider-neutral runner. Requires an explicitly supplied, auditable adapter.

Adapter subprocess JSON stdin/stdout: op=count or op=generate. See REPRODUCIBILITY.md.
Never retries or silently drops failed items. Evaluation refuses an unfrozen package.
"""
import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path
from core import ROOT, corpus, digest, file_hash, freeze_errors, git, package_hash, read, validate_questions, write
from prepare import prepare


def invoke(adapter, request):
    proc = subprocess.run([sys.executable, str(adapter)], input=json.dumps(request),
                          capture_output=True, text=True, timeout=180)
    if proc.returncode:
        # Do not print provider stderr: it may include credentials.
        raise ValueError("adapter failed (exit %s); inspect private provider log" % proc.returncode)
    return json.loads(proc.stdout)


def generate_item(item, arm, config, adapter, calls=None):
    history = []
    calls = [] if calls is None else calls
    budget = config["budget"]
    total_in = total_out = 0
    for stage in config["arms"][arm]:
        system = (ROOT/"arms/common.txt").read_text() + "\n" + (ROOT/"arms"/stage["prompt"]).read_text()
        payload = {"question": item["question"], "context": item["context"], "prior_stages": history}
        request = {"model": config["model"], "system": system, "input": payload,
                   "seed": config["generation_seed"], "stage": stage["name"]}
        counted = invoke(adapter, dict(request, op="count"))
        if counted["tokenizer"] != config["model"]["tokenizer"] or type(counted["input_tokens"]) is not int:
            raise ValueError("tokenizer/count mismatch")
        n_in = counted["input_tokens"]
        if n_in < 0:
            raise ValueError("negative token count")
        cap = min(stage["output_cap"], budget["generated_tokens"]-total_out,
                  budget["total_tokens"]-total_in-total_out-n_in)
        if cap <= 0:
            raise ValueError("common total token budget exhausted before completion")
        request.update(op="generate", max_output_tokens=cap)
        response = invoke(adapter, request)
        # Journal before validation so failed/truncated calls retain usage and text.
        calls.append({"request": request, "response": response})
        if response["model_snapshot"] != config["model"]["snapshot"]:
            raise ValueError("provider model snapshot mismatch")
        usage = response["usage"]
        if any(type(usage[k]) is not int or usage[k] < 0 for k in ("input_tokens", "output_tokens", "cached_input_tokens")):
            raise ValueError("invalid usage")
        if usage["input_tokens"] != n_in or usage["output_tokens"] > cap or usage["cached_input_tokens"] > n_in:
            raise ValueError("token budget/count violated")
        total_in += n_in; total_out += usage["output_tokens"]
        if response["finish_reason"] != "stop" or not response["text"].strip():
            raise ValueError("truncated, refused, or empty stage; no retry permitted")
        history.append({"stage": stage["name"], "text": response["text"]})
    final = json.loads(history[-1]["text"])
    if not isinstance(final.get("answer"), str) or not final["answer"].strip() or not isinstance(final.get("citations"), list):
        raise ValueError("invalid final response schema")
    return {"final": final, "calls": calls, "input_tokens": total_in, "output_tokens": total_out,
            "cached_input_tokens": sum(c["response"]["usage"]["cached_input_tokens"] for c in calls)}


def run(data, config, adapter, out):
    docs = corpus()
    validate_questions(data, docs)
    confirmatory = data["split"] == "evaluation"
    if confirmatory:
        errors = freeze_errors(config, read(ROOT/"THRESHOLDS.json"), data, docs)
        if digest(config) != digest(read(ROOT/"CONFIG.json")) or digest(data) != digest(read(ROOT/"QUESTIONS.json")):
            errors.append("evaluation config/questions must be the committed canonical files")
        if git("status", "--porcelain"):
            errors.append("evaluation must start from a clean committed checkout")
        if file_hash(adapter) != config["adapter"]["sha256"]:
            errors.append("adapter digest differs from frozen configuration")
        if errors:
            raise ValueError("NOT FROZEN: " + "; ".join(errors))
    elif not config["model"]["snapshot"] or not config["model"]["tokenizer"]:
        raise ValueError("configure an exact model and tokenizer before any live development run")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    plan = prepare(data, docs, config)
    write(out/"plan.json", plan)
    manifest = {"experiment": "DEV2-001", "split": data["split"], "official": confirmatory,
                "freeze_commit": git("rev-parse", "HEAD") if confirmatory else None,
                "source_commit": git("rev-parse", "HEAD"), "package_sha256": package_hash(),
                "questions_sha256": digest(data), "config_sha256": digest(config),
                "thresholds_sha256": file_hash(ROOT/"THRESHOLDS.json"),
                "adapter_sha256": file_hash(adapter), "operator": config["operator"],
                "model": config["model"], "started_utc_unix": time.time(), "complete": False}
    write(out/"manifest.json", manifest)
    rng = random.Random(config["order_seed"])
    records = []
    for item in plan["items"]:
        arms = list(config["arms"])
        rng.shuffle(arms)
        for arm in arms:
            record = {"question_id": item["id"], "arm": arm, "context_sha256": digest(item["context"]), "calls": []}
            t0 = time.monotonic()
            try:
                record.update(generate_item(item, arm, config, adapter, record["calls"]), status="ok")
            except (ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
                record.update(status="invalid", error=type(exc).__name__ + ": " + str(exc))
            record["latency_seconds"] = time.monotonic()-t0
            records.append(record)
            write(out/"responses.json", records)
    manifest.update(complete=all(r["status"] == "ok" for r in records),
                    responses_sha256=digest(records), finished_utc_unix=time.time())
    write(out/"manifest.json", manifest)
    return manifest


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--questions", default=str(ROOT/"development/QUESTIONS.json"))
    p.add_argument("--config", default=str(ROOT/"CONFIG.json"))
    p.add_argument("--adapter", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    print(json.dumps(run(read(args.questions), read(args.config), Path(args.adapter), args.out), indent=2))
