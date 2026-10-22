"""Fabricated fixtures verify mechanics only. No empirical model or human result."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core import corpus, digest, file_hash, freeze_errors, passage_ok, read, validate_questions, write
from prepare import prepare
from run import generate_item, run
from score import blind, combine, FIELDS
from analyze import analyze, holm, paired, verdict


def synthetic_scores():
    rows = []
    for tier in ("answerable", "absent", "contradictory"):
        for i in range(4):
            for arm in "ABCDE":
                rows.append(dict(question_id=f"{tier}-{i}", cluster_id=f"{tier}-{i}", tier=tier, arm=arm,
                                 false_assertion=int(arm in "AB") if tier == "absent" else None,
                                 answerable_success=1 if tier == "answerable" else None,
                                 conflict_report=1 if tier == "contradictory" else None,
                                 claim_count=1, unsupported_claim_count=0, citation_count=1,
                                 unsupported_citation_count=0, mechanical_invalid_citations=0,
                                 input_tokens=100, output_tokens=50, cached_input_tokens=0,
                                 latency_seconds=.1, context_sha256="same-context", confidence=None))
    return {"manifest": {"official": False, "split": "development", "complete": True},
            "rows": rows, "scoring": {"disagreement_count": 0}}


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = corpus()
        cls.data = read(ROOT/"development/QUESTIONS.json")
        cls.config = read(ROOT/"CONFIG.json")

    def test_all_pinned_bytes_and_development_evidence(self):
        counts = validate_questions(self.data, self.docs)
        self.assertEqual(sum(counts.values()), 12)
        self.assertEqual(len(self.docs), 10)

    def test_corrupted_corpus_is_rejected(self):
        manifest = read(ROOT/"CORPUS.json")
        manifest["documents"][0]["sha256"] = "0"*64
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            corpus(manifest)

    def test_missing_quote_and_invalid_range(self):
        p = copy.deepcopy(self.data["questions"][0]["gold"]["evidence"][0])
        self.assertTrue(passage_ok(p, self.docs))
        p["quote"] = "THIS DOES NOT EXIST IN THE PINNED PASSAGE"
        self.assertFalse(passage_ok(p, self.docs))
        p["start_line"] = 0
        self.assertFalse(passage_ok(p, self.docs))

    def test_duplicates_rejected(self):
        data = copy.deepcopy(self.data)
        data["questions"].append(data["questions"][0])
        with self.assertRaises(ValueError):
            validate_questions(data, self.docs)

    def test_family_leakage_rejected(self):
        data = copy.deepcopy(self.data); data["split"] = "evaluation"
        for q in data["questions"]:
            q["split"] = "evaluation"; q["id"] = "eval-"+q["id"]; q["text"] += " Please explain."
        with self.assertRaisesRegex(ValueError, "overlap"):
            validate_questions(data, self.docs, self.data)

    def test_gold_never_enters_plan(self):
        plan = prepare(self.data, self.docs, self.config)
        for item in plan["items"]:
            self.assertEqual(set(item), {"id", "question", "context"})
        self.assertEqual(plan, prepare(self.data, self.docs, self.config))

    def test_empty_holdout_draft_cannot_freeze(self):
        thresholds = read(ROOT/"THRESHOLDS.json"); thresholds["status"] = "DRAFT_NOT_FROZEN"
        data = {"split": "evaluation", "questions": []}
        errors = freeze_errors(self.config, thresholds, data, self.docs)
        self.assertTrue(any("DRAFT" in e for e in errors))
        self.assertTrue(any("held-out counts" in e for e in errors))

    def test_absence_needs_human_semantic_review(self):
        data = copy.deepcopy(self.data); data["split"] = "evaluation"
        for q in data["questions"]:
            q["split"] = "evaluation"
            q["review"] = dict(approved=True, reviewers=["fixture-1", "fixture-2"], independent_humans=True,
                               no_category_cues=True, semantic_split_checked=True)
        with self.assertRaisesRegex(ValueError, "absence not checked"):
            validate_questions(data, self.docs, confirmatory=True)

    def test_unapproved_eval_runner_refuses_before_adapter(self):
        with tempfile.TemporaryDirectory() as t:
            adapter = Path(t)/"adapter.py"; adapter.write_text("raise Exception('must never run')")
            with patch("run.freeze_errors", return_value=["DRAFT_NOT_FROZEN"]), self.assertRaisesRegex(ValueError, "NOT FROZEN"):
                run(read(ROOT/"QUESTIONS.json"), self.config, adapter, Path(t)/"out")


class BudgetTests(unittest.TestCase):
    def config(self):
        c = read(ROOT/"CONFIG.json"); c["model"]["snapshot"] = "FIXTURE"; c["model"]["tokenizer"] = "FIXTURE"
        return c

    def fake(self, adapter, request):
        if request["op"] == "count":
            return {"input_tokens": 100, "tokenizer": "FIXTURE"}
        return {"model_snapshot": "FIXTURE", "text": '{"answer":"Synthetic fixture only","citations":[]}',
                "finish_reason": "stop", "usage": {"input_tokens": 100, "output_tokens": 20, "cached_input_tokens": 10}}

    def test_all_critic_calls_count(self):
        with patch("run.invoke", self.fake):
            result = generate_item({"question": "fixture", "context": []}, "C", self.config(), None)
        self.assertEqual(len(result["calls"]), 3)
        self.assertEqual((result["input_tokens"], result["output_tokens"], result["cached_input_tokens"]), (300,60,30))

    def test_total_budget_blocks_extra_call(self):
        c = self.config(); c["budget"]["total_tokens"] = 150
        with patch("run.invoke", self.fake), self.assertRaisesRegex(ValueError, "exhausted"):
            generate_item({"question": "fixture", "context": []}, "C", c, None)

    def test_provider_overrun_and_partial_trace_retained(self):
        def overrun(adapter, request):
            result = self.fake(adapter, request)
            if request["op"] == "generate": result["usage"]["output_tokens"] = 9000
            return result
        calls = []
        with patch("run.invoke", overrun), self.assertRaisesRegex(ValueError, "violated"):
            generate_item({"question": "fixture", "context": []}, "C", self.config(), None, calls)
        self.assertEqual(len(calls), 1)

    def test_model_drift_rejected(self):
        def drift(adapter, request):
            result = self.fake(adapter, request)
            if request["op"] == "generate": result["model_snapshot"] = "CHANGED"
            return result
        with patch("run.invoke", drift), self.assertRaisesRegex(ValueError, "snapshot"):
            generate_item({"question": "fixture", "context": []}, "A", self.config(), None)

    def test_truncation_not_credited_as_abstention(self):
        def truncated(adapter, request):
            result = self.fake(adapter, request)
            if request["op"] == "generate": result["finish_reason"] = "length"
            return result
        with patch("run.invoke", truncated), self.assertRaisesRegex(ValueError, "truncated"):
            generate_item({"question": "fixture", "context": []}, "A", self.config(), None)

    def test_subprocess_adapter_to_manifest_integration(self):
        with tempfile.TemporaryDirectory() as t:
            adapter=Path(t)/"fixture_adapter.py"
            adapter.write_text('''import json, sys
r=json.load(sys.stdin)
if r["op"]=="count":
 print(json.dumps({"input_tokens":100,"tokenizer":"FIXTURE"}))
else:
 print(json.dumps({"model_snapshot":"FIXTURE","text":'{"answer":"Synthetic fixture only","citations":[]}',"finish_reason":"stop","usage":{"input_tokens":100,"output_tokens":20,"cached_input_tokens":0}}))
''')
            data=read(ROOT/"development/QUESTIONS.json");data["questions"]=data["questions"][:1]
            c=self.config();c["operator"]="fixture-operator"
            manifest=run(data,c,adapter,Path(t)/"run")
            self.assertTrue(manifest["complete"])
            self.assertFalse(manifest["official"])
            records=read(Path(t)/"run/responses.json")
            self.assertEqual(len(records),5)
            self.assertEqual(sum(len(r["calls"]) for r in records),9)


class AnalysisTests(unittest.TestCase):
    def test_paired_effect_orientation_and_reproducibility(self):
        rows = synthetic_scores()["rows"]
        r = paired(rows, "absent", "A", "C", "false_assertion", 1, 200, 42)
        self.assertEqual(r["effect"], 1)
        self.assertEqual(r["ci95"], [1,1])
        self.assertEqual(r, paired(rows, "absent", "A", "C", "false_assertion", 1, 200, 42))

    def test_paraphrases_not_independent_samples(self):
        rows=[]
        for i in range(9):
            for arm in "AC":
                rows.append(dict(question_id=str(i), tier="absent", arm=arm,
                                 cluster_id="large" if i < 8 else "small", context_sha256="x",
                                 false_assertion=int(i < 8 and arm == "A")))
        r = paired(rows, "absent", "A", "C", "false_assertion", 1, 100, 1)
        self.assertEqual(r["effect"], .5)
        self.assertEqual(r["clusters"], 2)

    def test_missing_pair_and_context_mismatch_rejected(self):
        rows=synthetic_scores()["rows"]
        rows=[r for r in rows if not(r["question_id"] == "absent-0" and r["arm"] == "C")]
        with self.assertRaisesRegex(ValueError, "unpaired"):
            paired(rows,"absent","A","C","false_assertion",1,100,1)
        rows=synthetic_scores()["rows"]
        next(r for r in rows if r["tier"] == "absent" and r["arm"] == "C")["context_sha256"]="other"
        with self.assertRaisesRegex(ValueError, "retrieval differs"):
            paired(rows,"absent","A","C","false_assertion",1,100,1)

    def test_holm_hand_calculation(self):
        self.assertEqual(holm({"a": .01,"b": .04,"c": .03}), {"a":.03,"c":.06,"b":.06})

    def test_pass_kill_inconclusive_and_utility_failure(self):
        t=read(ROOT/"THRESHOLDS.json")
        self.assertEqual(verdict(.2,[.01,.4],1.5,True,t),"PASS_PENDING_REPLICATION")
        self.assertEqual(verdict(-.2,[-.3,-.1],1,True,t),"DEAD_ON_THIS_TESTBED")
        self.assertEqual(verdict(.08,[-.1,.3],1,True,t),"INCONCLUSIVE")
        self.assertEqual(verdict(.3,[.1,.5],1,False,t),"NARROWED")
        self.assertEqual(verdict(.3,[.1,.5],1.6,True,t),"NARROWED")

    def test_draft_can_never_be_supported(self):
        t=read(ROOT/"THRESHOLDS.json");t["bootstrap_draws"]=100
        result=analyze(synthetic_scores(),read(ROOT/"CONFIG.json"),t)
        self.assertEqual(result["verdict"],"UNVERIFIED")
        self.assertEqual(result["diagnostic_rule_outcome"],"PASS_PENDING_REPLICATION")
        self.assertFalse(result["physics_validation"])
        self.assertEqual(len(result["secondary_exploratory"]),5)

    def test_missing_arms_rejected(self):
        scored=synthetic_scores();scored["rows"].pop()
        with self.assertRaisesRegex(ValueError,"missing or duplicate"):
            analyze(scored,read(ROOT/"CONFIG.json"),read(ROOT/"THRESHOLDS.json"))

    def test_no_citations_is_undefined_not_perfect(self):
        scored=synthetic_scores()
        for r in scored["rows"]:r["citation_count"]=0
        t=read(ROOT/"THRESHOLDS.json");t["bootstrap_draws"]=100
        result=analyze(scored,read(ROOT/"CONFIG.json"),t)
        self.assertIsNone(result["arms"]["A"]["answerable_unsupported_citation_rate"])


class HumanScoringTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name);self.rundir=self.path/"run";self.rundir.mkdir()
        self.q=read(ROOT/"development/QUESTIONS.json");self.q["questions"]=self.q["questions"][:1]
        self.responses=[dict(question_id="d001",arm=a,status="ok",final={"answer":"Fixture only", "citations":[]},
                             input_tokens=100,output_tokens=30,cached_input_tokens=0,latency_seconds=.1,context_sha256="same") for a in "ABCDE"]
        self.manifest=dict(complete=True,official=False,split="development",operator="fixture-operator",
                           responses_sha256=digest(self.responses),questions_sha256=digest(self.q))
        write(self.rundir/"responses.json",self.responses);write(self.rundir/"manifest.json",self.manifest)
        blind(self.rundir,self.q,self.path/"blind")
        self.key=read(self.path/"blind/PRIVATE-key.json")
        self.a=read(self.path/"blind/rater-1.json");self.b=read(self.path/"blind/rater-2.json")
        for idx, form in enumerate((self.a,self.b)):
            form.update(rater_id=f"fixture-human-{idx}",human=True,independent=True,scored_without_key_or_other_ratings=True)
            for rating in form["ratings"]:
                rating.update(false_assertion=None,answerable_success=0,conflict_report=None,claim_count=1,
                              unsupported_claim_count=1,citation_count=0,unsupported_citation_count=0,rationale="Fabricated software fixture, not human evidence.")

    def test_blinded_export_hides_metadata_and_combines(self):
        packets=read(self.path/"blind/packets.json")
        for packet in packets:
            self.assertNotIn("arm",packet);self.assertNotIn("input_tokens",packet)
        result=combine(self.rundir,self.q,self.key,self.a,self.b)
        self.assertEqual(len(result["rows"]),5)
        self.assertEqual(result["scoring"]["disagreement_count"],0)

    def test_nonhuman_same_rater_and_missing_scores_rejected(self):
        self.a["human"]=False
        with self.assertRaises(ValueError):combine(self.rundir,self.q,self.key,self.a,self.b)
        self.a["human"]=True;self.b["rater_id"]=self.a["rater_id"]
        with self.assertRaises(ValueError):combine(self.rundir,self.q,self.key,self.a,self.b)
        self.b["rater_id"]="other";self.b["ratings"].pop()
        with self.assertRaises(ValueError):combine(self.rundir,self.q,self.key,self.a,self.b)

    def test_disagreement_requires_third_independent_vote(self):
        bid=self.a["ratings"][0]["blind_id"]
        next(r for r in self.b["ratings"] if r["blind_id"]==bid)["answerable_success"]=1
        with self.assertRaisesRegex(ValueError,"unresolved"):
            combine(self.rundir,self.q,self.key,self.a,self.b)
        adj=dict(rater_id="fixture-third-human",human=True,independent=True,scored_without_key_or_other_ratings=True,
                 ratings=[copy.deepcopy(self.a["ratings"][0])])
        result=combine(self.rundir,self.q,self.key,self.a,self.b,adj)
        self.assertEqual(result["scoring"]["disagreement_count"],1)

    def test_modified_response_digest_rejected(self):
        self.responses[0]["final"]["answer"]="changed";write(self.rundir/"responses.json",self.responses)
        with self.assertRaisesRegex(ValueError,"modified"):
            combine(self.rundir,self.q,self.key,self.a,self.b)

    def test_incomplete_run_not_scored_as_abstention(self):
        self.manifest["complete"]=False;write(self.rundir/"manifest.json",self.manifest)
        with self.assertRaisesRegex(ValueError,"incomplete"):
            blind(self.rundir,self.q,self.path/"new-blind")


if __name__ == "__main__":
    unittest.main()
