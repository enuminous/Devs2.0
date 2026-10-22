"""Audit every theorem and check computed examples against protocol constants."""
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification/local'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    audit=subprocess.run(['lake','env','lean','Devs/Audit.lean'],cwd=ROOT,text=True,capture_output=True,check=True).stdout
    (OUT/'lean-axioms.txt').write_text(audit)
    expected={p['qualified'] for p in json.loads((ROOT/'docs/theorems.json').read_text())}
    seen=set()
    for line in audit.splitlines():
        m=re.fullmatch(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*)\])",line)
        if not m: raise SystemExit('Unexpected axiom audit output: '+line)
        seen.add(m[1])
        axioms={s.strip() for s in (m[3] or '').split(',') if s.strip()}
        if not axioms <= {'propext','Quot.sound','Classical.choice'}:
            raise SystemExit('Unexpected axiom dependency: '+line)
    if seen != expected: raise SystemExit('Theorem catalog/audit mismatch')
    raw=subprocess.check_output(['lake','exe','devs-check'],cwd=ROOT,text=True)
    actual=json.loads(raw)
    cfg=json.loads((ROOT/'research/dev2-001/CONFIG.json').read_text())
    th=json.loads((ROOT/'research/dev2-001/THRESHOLDS.json').read_text())
    expected_values={'sample_total':sum(th['evaluation_counts'].values()),
                     'critic_output_pool':sum(s['output_cap'] for s in cfg['arms']['C']),
                     'margin_basis_points':round(th['pass_absolute_improvement']*10000),
                     'bad_critic_keeps_false':True,'physics_validation':False}
    if actual != expected_values: raise SystemExit('Computed Lean example/protocol mismatch')
    (OUT/'lean-examples.json').write_text(json.dumps(actual,indent=2)+'\n')
    (OUT/'formal-verification.json').write_text(json.dumps({'kind':'FORMAL_SOFTWARE_CHECK_ONLY','theorems':len(seen),'toolchain':(ROOT/'lean-toolchain').read_text().strip(),'computed_examples':actual,'empirical_result':False},indent=2)+'\n')
    print(f'Lean audit passed: {len(seen)} theorems, standard foundation only; computed examples match protocol constants.')

if __name__=='__main__': main()
