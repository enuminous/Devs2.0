"""DEV2-001 infrastructure. Standard library only; no model calls on import."""
import hashlib
import json
import math
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
TIERS = ("answerable", "absent", "contradictory")
STATUSES = ("proposed", "derived", "simulated", "observed", "replicated",
            "contradicted", "superseded", "unknown")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args]).decode().strip()


def corpus(manifest=None):
    manifest = manifest or read(ROOT / "CORPUS.json")
    docs = {}
    for entry in manifest["documents"]:
        if not re.fullmatch(r"[0-9a-f]{40}", entry["commit"]):
            raise ValueError("corpus requires full immutable commits")
        # The standalone companion vendors the exact upstream bytes. Keep the
        # original manifest unchanged so existing question digests stay valid.
        local = ROOT / "corpus" / (entry["id"] + ".md")
        if not re.fullmatch(r"[a-z0-9-]+", entry["id"]):
            raise ValueError("invalid corpus ID")
        raw = local.read_bytes() if local.exists() else subprocess.check_output(
            ["git", "-C", str(REPO), "show", entry["commit"] + ":" + entry["path"]])
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError("corpus digest mismatch: " + entry["id"])
        if entry["id"] in docs:
            raise ValueError("duplicate document ID")
        docs[entry["id"]] = dict(entry, lines=raw.decode("utf-8").splitlines())
    return docs


def passage_ok(passage, docs):
    try:
        doc = docs[passage["doc_id"]]
        start, end = passage["start_line"], passage["end_line"]
        return (type(start) is int and type(end) is int and 1 <= start <= end <= len(doc["lines"])
                and isinstance(passage["quote"], str) and bool(passage["quote"].strip())
                and passage["quote"] in "\n".join(doc["lines"][start-1:end]))
    except (KeyError, TypeError):
        return False


def validate_questions(data, docs, development=None, confirmatory=False):
    ids, texts, clusters = set(), set(), set()
    split = data["split"]
    if split not in ("development", "evaluation"):
        raise ValueError("invalid split")
    for q in data["questions"]:
        if q["split"] != split or q["tier"] not in TIERS:
            raise ValueError("invalid question tier or split")
        if not q["id"] or q["id"] in ids:
            raise ValueError("duplicate/missing question ID")
        text = " ".join(q["text"].lower().split())
        if not text or text in texts or not q["cluster_id"]:
            raise ValueError("duplicate/empty question or missing cluster")
        if q["corpus_manifest_sha256"] != file_hash(ROOT / "CORPUS.json"):
            raise ValueError("question targets a different corpus manifest")
        if q["corpus_commit"] != read(ROOT / "CORPUS.json")["anchor_commit"]:
            raise ValueError("question corpus commit mismatch")
        if not q["gold"]["expected_behavior"]:
            raise ValueError("missing scoring gold")
        evidence = q["gold"]["evidence"]
        if not all(passage_ok(e, docs) for e in evidence):
            raise ValueError("invalid gold citation: " + q["id"])
        if q["tier"] == "answerable" and not evidence:
            raise ValueError("answerable question needs evidence")
        if q["tier"] == "contradictory":
            versions = {docs[e["doc_id"]]["commit"] for e in evidence}
            if len(versions) < 2 or not q["gold"]["conflict_explanation"]:
                raise ValueError("contradictory item needs two versions and a semantic conflict")
        if q["tier"] == "absent" and not q["gold"]["absence_audit"]:
            raise ValueError("absent item needs a whole-corpus absence audit")
        if confirmatory:
            reviews = q["review"]["reviewers"]
            if len(set(reviews)) < 2 or not all(isinstance(x, str) and x.strip() for x in reviews):
                raise ValueError("two independent human question reviewers required")
            if not q["review"]["approved"] or not q["review"]["independent_humans"]:
                raise ValueError("unreviewed evaluation item")
            if not q["review"]["no_category_cues"] or not q["review"]["semantic_split_checked"]:
                raise ValueError("cue/leakage review incomplete")
            if q["tier"] == "absent":
                a = q["gold"]["absence_audit"]
                if set(a["documents_reviewed"]) != set(docs) or not a["manual_semantic_review"]:
                    raise ValueError("absence not checked against every pinned document")
        ids.add(q["id"]); texts.add(text); clusters.add(q["cluster_id"])
    if development:
        dq = development["questions"]
        if ids & {q["id"] for q in dq} or clusters & {q["cluster_id"] for q in dq}:
            raise ValueError("development/evaluation ID or evidence-family overlap")
        if texts & {" ".join(q["text"].lower().split()) for q in dq}:
            raise ValueError("development/evaluation text overlap")
    return Counter(q["tier"] for q in data["questions"])


def retrieve(text, docs, config):
    """Fixed lexical BM25 over overlapping line chunks; labels/gold never used."""
    tokens = lambda s: re.findall(r"[a-z0-9]+", s.lower())
    chunks = []
    width, overlap = config["chunk_lines"], config["overlap_lines"]
    if not (0 <= overlap < width):
        raise ValueError("invalid chunk overlap")
    for key, doc in sorted(docs.items()):
        for start in range(0, len(doc["lines"]), width-overlap):
            end = min(start+width, len(doc["lines"]))
            body = "\n".join(doc["lines"][start:end])
            chunks.append(dict(doc_id=key, commit=doc["commit"], path=doc["path"],
                               start_line=start+1, end_line=end, text=body))
    counts = [Counter(tokens(c["text"])) for c in chunks]
    lengths = [sum(c.values()) for c in counts]
    avg = sum(lengths)/max(1, len(lengths))
    df = Counter(t for c in counts for t in c)
    terms = set(tokens(text))
    scores = []
    for i, c in enumerate(counts):
        score = 0.0
        for term in terms:
            tf = c[term]
            if tf:
                idf = math.log(1+(len(counts)-df[term]+0.5)/(df[term]+0.5))
                score += idf*tf*2.2/(tf+1.2*(0.25+0.75*lengths[i]/avg))
        scores.append(score)
    order = sorted(range(len(chunks)), key=lambda i: (-scores[i], chunks[i]["doc_id"], chunks[i]["start_line"]))
    return [chunks[i] for i in order[:config["top_k"]]]


def package_hash():
    """Digest only tracked-to-be source inputs; excludes runs and local caches."""
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".py", ".json", ".txt", ".md")
                   and not any(x in p.relative_to(ROOT).parts for x in ("runs", "__pycache__", "private")))
    return digest({str(p.relative_to(ROOT)): file_hash(p) for p in files})


def freeze_errors(config, thresholds, questions, docs):
    errors = []
    if (thresholds["status"] != "FROZEN" or not thresholds["approved_by"] or not thresholds["approval_reference"]
            or not thresholds["approved_at"] or thresholds["recommendation_only"]):
        errors.append("design is DRAFT; Matthew's approval and frozen thresholds are required")
    if config["status"] != "FROZEN":
        errors.append("configuration remains DRAFT")
    if not (0 <= thresholds["kill_upper_bound"] < thresholds["pass_absolute_improvement"] <= 1):
        errors.append("kill/pass margins must be ordered within [0,1]")
    if thresholds["bootstrap_draws"] < 1000 or thresholds["max_token_ratio"] <= 0:
        errors.append("invalid analysis or cost gate")
    for key in ("min_answerable_success", "max_answerable_drop", "min_conflict_report"):
        if not 0 <= thresholds[key] <= 1:
            errors.append("invalid utility threshold: " + key)
    if set(config["arms"]) != set("ABCDE"):
        errors.append("all three original arms and both conventional baselines are required")
    if config["budget"]["generated_tokens"] <= 0 or config["budget"]["total_tokens"] <= config["budget"]["generated_tokens"]:
        errors.append("invalid common token budget")
    for arm, stages in config["arms"].items():
        if any(s["output_cap"] <= 0 for s in stages) or sum(s["output_cap"] for s in stages) != config["budget"]["generated_tokens"]:
            errors.append("unequal allocated generation pool: " + arm)
    if not config["model"]["snapshot"] or not config["model"]["tokenizer"]:
        errors.append("model snapshot/tokenizer unpinned")
    if not config["adapter"]["sha256"]:
        errors.append("model adapter unpinned")
    if not config["adapter"].get("environment_lock"):
        errors.append("adapter dependency/environment lock missing")
    if type(config["model"]["seed_supported"]) is not bool or not config["model"]["reasoning_setting"]:
        errors.append("seed support and reasoning setting must be explicitly resolved")
    if not config["operator"] or not config["scoring_custodian"] or config["operator"] == config["scoring_custodian"]:
        errors.append("distinct operator and scoring custodian required")
    if any(config["cost"][k] is None for k in ("input_per_million", "output_per_million", "cached_input_per_million")):
        errors.append("cost schedule unset")
    elif any(config["cost"][k] < 0 for k in ("input_per_million", "output_per_million", "cached_input_per_million")):
        errors.append("negative price")
    if not config["cost"]["source"] or not config["cost"]["as_of"]:
        errors.append("cost schedule provenance missing")
    try:
        counts = validate_questions(questions, docs, read(ROOT/"development/QUESTIONS.json"), True)
        if dict(counts) != thresholds["evaluation_counts"]:
            errors.append("held-out counts do not match approved design")
        for tier, minimum in thresholds["minimum_clusters"].items():
            if len({q["cluster_id"] for q in questions["questions"] if q["tier"] == tier}) < minimum:
                errors.append("insufficient independent evidence families: " + tier)
    except (ValueError, KeyError) as exc:
        errors.append(str(exc))
    if not config["holdout"]["custodian_attestation"] or not config["holdout"]["sealed_before_run"]:
        errors.append("held-out custody/exposure attestation missing")
    if not config["retrieval"]["coverage_review"]:
        errors.append("blind retrieval coverage review missing")
    return errors
