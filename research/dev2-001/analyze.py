"""Paired evidence-family bootstrap; primary C vs A on absent questions.

No LLM grader, post-hoc threshold search, optional stopping, or success from fixture data.
"""
import argparse
import math
import random
from collections import defaultdict
from core import ROOT, digest, file_hash, package_hash, read, write


def quantile(values, p):
    s = sorted(values); x = (len(s)-1)*p
    lo, hi = math.floor(x), math.ceil(x)
    return s[lo] + (s[hi]-s[lo])*(x-lo)


def paired(rows, tier, first, second, field, positive, draws, seed):
    selected = [r for r in rows if r["tier"] == tier and r["arm"] in (first, second)]
    byq = defaultdict(dict)
    for r in selected:
        if r["arm"] in byq[r["question_id"]]:
            raise ValueError("duplicate pair")
        byq[r["question_id"]][r["arm"]] = r
    clusters = defaultdict(list)
    for qid, pair in sorted(byq.items()):
        if set(pair) != {first, second}:
            raise ValueError("unpaired/missing response: " + qid)
        a, b = pair[first], pair[second]
        if a["cluster_id"] != b["cluster_id"] or a["context_sha256"] != b["context_sha256"]:
            raise ValueError("paired cluster/retrieval differs")
        if a[field] not in (0, 1) or b[field] not in (0, 1):
            raise ValueError("missing binary score")
        clusters[a["cluster_id"]].append(positive*(a[field]-b[field]))
    if len(clusters) < 2:
        raise ValueError("at least two evidence families needed for interval")
    # Target is equal-weight evidence-family mean; paraphrases never inflate n.
    values = [sum(v)/len(v) for _, v in sorted(clusters.items())]
    effect = sum(values)/len(values)
    rng = random.Random(seed)
    boot = [sum(rng.choices(values, k=len(values)))/len(values) for _ in range(draws)]
    # Exploratory two-sided cluster sign-flip test; assumes sign exchangeability.
    extreme = sum(abs(sum(v*rng.choice((-1, 1)) for v in values)/len(values)) >= abs(effect)-1e-12
                  for _ in range(draws))
    return {"effect": effect, "ci95": [quantile(boot, .025), quantile(boot, .975)],
            "clusters": len(values), "questions": len(byq), "p_signflip": (extreme+1)/(draws+1)}


def holm(pvalues):
    result, last, n = {}, 0.0, len(pvalues)
    for i, (key, p) in enumerate(sorted(pvalues.items(), key=lambda kv: kv[1])):
        last = max(last, min(1.0, (n-i)*p)); result[key] = last
    return result


def macro_rate(rows, tier, arm, field):
    groups = defaultdict(list)
    for r in rows:
        if r["tier"] == tier and r["arm"] == arm:
            groups[r["cluster_id"]].append(r[field])
    if not groups:
        raise ValueError("missing arm/tier")
    return sum(sum(v)/len(v) for v in groups.values())/len(groups)


def verdict(effect, interval, ratio, quality, thresholds):
    if effect >= thresholds["pass_absolute_improvement"] and interval[0] > 0 and ratio <= thresholds["max_token_ratio"] and quality:
        return "PASS_PENDING_REPLICATION"
    if interval[1] <= thresholds["kill_upper_bound"]:
        return "DEAD_ON_THIS_TESTBED"
    if interval[0] > 0 and (ratio > thresholds["max_token_ratio"] or not quality):
        return "NARROWED"
    return "INCONCLUSIVE"


def analyze(scored, config, thresholds):
    from core import TOKEN_RATIO_DENOMINATOR
    if config["budget"].get("token_ratio_denominator") != TOKEN_RATIO_DENOMINATOR:
        raise ValueError("unsupported or unpinned token ratio denominator")
    rows, manifest = scored["rows"], scored["manifest"]
    expected_arms = set(config["arms"])
    byq = defaultdict(list)
    for r in rows:
        byq[r["question_id"]].append(r)
    for q, group in byq.items():
        if len(group) != len(expected_arms) or {r["arm"] for r in group} != expected_arms:
            raise ValueError("missing or duplicate arms: " + q)
        if len({r["tier"] for r in group}) != 1 or len({r["cluster_id"] for r in group}) != 1 or len({r["context_sha256"] for r in group}) != 1:
            raise ValueError("paired metadata mismatch")
        for r in group:
            if r["input_tokens"]+r["output_tokens"] > config["budget"]["total_tokens"] or r["output_tokens"] > config["budget"]["generated_tokens"]:
                raise ValueError("equal available budget violated")
    if manifest["official"]:
        canonical = read(ROOT/"QUESTIONS.json")
        expected = {q["id"]: q for q in canonical["questions"]}
        if digest(canonical) != manifest["questions_sha256"] or set(byq) != set(expected):
            raise ValueError("scored set does not match frozen evaluation roster")
        for qid, group in byq.items():
            if any(r["tier"] != expected[qid]["tier"] or r["cluster_id"] != expected[qid]["cluster_id"] for r in group):
                raise ValueError("scored labels differ from frozen gold")
    draws, seed = thresholds["bootstrap_draws"], thresholds["analysis_seed"]
    primary = paired(rows, "absent", "A", "C", "false_assertion", 1, draws, seed)
    stats = {}
    for arm in sorted(expected_arms):
        rr = [r for r in rows if r["arm"] == arm]
        if not rr:
            raise ValueError("empty arm")
        cost = config["cost"]
        priced = all(cost[k] is not None for k in ("input_per_million", "output_per_million", "cached_input_per_million"))
        denom = sum(r["citation_count"] for r in rr if r["tier"] == "answerable")
        claims = sum(r["claim_count"] for r in rr)
        confident = [r for r in rr if r.get("confidence") is not None]
        def correct(r):
            return 1-r["false_assertion"] if r["tier"] == "absent" else r["answerable_success"] if r["tier"] == "answerable" else r["conflict_report"]
        stats[arm] = {"false_assertion_rate": macro_rate(rows, "absent", arm, "false_assertion"),
                      "answerable_success": macro_rate(rows, "answerable", arm, "answerable_success"),
                      "conflict_report_rate": macro_rate(rows, "contradictory", arm, "conflict_report"),
                      "mean_tokens": sum(r["input_tokens"]+r["output_tokens"] for r in rr)/len(rr),
                      "median_tokens": quantile([r["input_tokens"]+r["output_tokens"] for r in rr], .5),
                      "p95_tokens": quantile([r["input_tokens"]+r["output_tokens"] for r in rr], .95),
                      "total_input_tokens": sum(r["input_tokens"] for r in rr),
                      "total_output_tokens": sum(r["output_tokens"] for r in rr),
                      "total_cached_input_tokens": sum(r["cached_input_tokens"] for r in rr),
                      "mean_latency_seconds": sum(r["latency_seconds"] for r in rr)/len(rr),
                      "answerable_unsupported_citation_rate": sum(r["unsupported_citation_count"] for r in rr if r["tier"] == "answerable")/denom if denom else None,
                      "mechanical_invalid_citations": sum(r["mechanical_invalid_citations"] for r in rr),
                      "unsupported_claim_rate": sum(r["unsupported_claim_count"] for r in rr)/claims if claims else None,
                      "confidence_coverage": len(confident)/len(rr),
                      "selective_brier_score": sum((r["confidence"]-correct(r))**2 for r in confident)/len(confident) if confident else None,
                      "mean_cost": sum(((r["input_tokens"]-r["cached_input_tokens"])*cost["input_per_million"] + r["cached_input_tokens"]*cost["cached_input_per_million"] + r["output_tokens"]*cost["output_per_million"])/1e6 for r in rr)/len(rr) if priced else None}
    denominator = stats["A"]["mean_tokens"]
    if denominator <= 0:
        raise ValueError("zero baseline token denominator")
    ratio = stats["C"]["mean_tokens"]/denominator
    quality = (stats["C"]["answerable_success"] >= thresholds["min_answerable_success"]
               and stats["A"]["answerable_success"]-stats["C"]["answerable_success"] <= thresholds["max_answerable_drop"] + 1e-12
               and stats["C"]["conflict_report_rate"] >= thresholds["min_conflict_report"])
    secondary = {}
    for comparator in ("B", "D", "E"):
        key = "absent_C_vs_"+comparator
        secondary[key] = paired(rows, "absent", comparator, "C", "false_assertion", 1, draws, seed+1)
    for tier, field in (("answerable", "answerable_success"), ("contradictory", "conflict_report")):
        secondary[tier+"_C_vs_A"] = paired(rows, tier, "C", "A", field, 1, draws, seed+2)
    adjusted = holm({key: val["p_signflip"] for key, val in secondary.items()})
    for key in secondary:
        secondary[key]["p_holm"] = adjusted[key]
    official = (manifest["official"] and manifest["split"] == "evaluation" and thresholds["status"] == "FROZEN" and config["status"] == "FROZEN"
                and manifest["complete"] and manifest["config_sha256"] == digest(config)
                and manifest["thresholds_sha256"] == file_hash(ROOT/"THRESHOLDS.json")
                and manifest["package_sha256"] == package_hash())
    decision = verdict(primary["effect"], primary["ci95"], ratio, quality, thresholds)
    # Independent generation+scoring is deliberately a separate human release gate.
    # This script NEVER automatically prints SUPPORTED, even for passing numbers.
    return {"experiment": "DEV2-001", "official_eligible": official,
            "verdict": decision if official else "UNVERIFIED",
            "diagnostic_rule_outcome": decision, "primary": primary, "arms": stats,
            "token_ratio_C_over_A": ratio, "strict_equal_spend_sensitivity": ratio <= 1.0,
            "token_ratio_denominator": config["budget"]["token_ratio_denominator"],
            "quality_guardrails_pass": quality, "secondary_exploratory": secondary,
            "primary_scope": "one prespecified paired contrast; no multiple-primary selection",
            "scoring_disagreement_count": scored["scoring"]["disagreement_count"],
            "independent_replication": "NOT ESTABLISHED BY THIS SCRIPT",
            "replication_criteria": {
                "max_absolute_effect_difference": thresholds["replication_effect_tolerance"],
                "same_positive_direction": True, "all_original_gates_in_both_runs": True,
                "deterministic_analysis_tolerance": thresholds["deterministic_analysis_tolerance"],
                "independent_generation_scoring_and_signed_review_required": True},
            "physics_validation": False,
            "scored_sha256": digest(scored)}


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--scored", required=True)
    p.add_argument("--out", required=True); args = p.parse_args()
    write(args.out, analyze(read(args.scored), read(ROOT/"CONFIG.json"), read(ROOT/"THRESHOLDS.json")))
