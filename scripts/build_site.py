"""Generate a self-contained index.html from the tracked, audited sources."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / 'research/dev2-001'
sys.path.insert(0, str(BENCH))
from core import corpus, read, freeze_errors


def catalog():
    descriptions = {
        'Possibility': 'Ordinary predicate intersection or explicit expansion; constraints are supplied, not inferred.',
        'Provenance': 'Typed status or dependency-rank invariant. Correct source interpretation and rank assignment are assumptions.',
        'Uncertainty': 'Natural-number weight update. Positive mass and correctly specified likelihoods are separate obligations.',
        'Criticism': 'Filtering invariant or counterexample. Critic soundness is not established by this theorem.',
        'Agency': 'Authorization bound to an exact action and revision. Real-world identity and UI enforcement remain outside the proof.',
        'Budget': 'Natural-number accounting invariant. Accurate provider usage is an external obligation.',
        'Benchmark': 'Arithmetic or logical property of explicitly stated gates. No statistical coverage or empirical superiority theorem.'
    }
    result = []
    for name in descriptions:
        file = ROOT / 'Devs' / (name + '.lean')
        text = file.read_text()
        matches = list(re.finditer(r'^theorem\s+(\w+)', text, re.M))
        for i, m in enumerate(matches):
            end = matches[i+1].start() if i+1 < len(matches) else text.rfind('\nend ')
            code = text[m.start():end].split('/--')[0].strip()
            result.append(dict(module=name, name=m.group(1), qualified=f'Devs.{name}.{m.group(1)}',
                               file=str(file.relative_to(ROOT)), line=text[:m.start()].count('\n')+1,
                               description=descriptions[name], code=code))
    return result


def build():
    documents = list(corpus().values())
    for d in documents:
        d['title'] = next((s.lstrip('# ').strip() for s in d['lines'] if s.startswith('# ')), d['path'])
    config, thresholds = read(BENCH/'CONFIG.json'), read(BENCH/'THRESHOLDS.json')
    answers = [
        dict(question='What does Devs 2.0 actually predict?',short='Prediction, without prophecy',
             heading='A map of possibilities, with conditions.',
             summary='The paper proposes bounded foresight: an evolving account of possible outcomes, assumptions, and uncertainty. It does not claim to recover one inevitable future.',
             doc='devs',anchor='## 7. Prediction Without Prophecy',
             quote='Given these observations, assumptions and models, these outcomes currently occupy this range of possibilities.'),
        dict(question='Does this validate EFMW physics?',short='Does this validate physics?',
             heading='The architecture has its own empirical test.',
             summary='Section 16 explicitly separates architectural evaluation from the correctness of EFMW physics. DEV2-001 has not run; neither the site nor its Lean proofs validate a physical theory.',
             doc='devs',anchor='## 16. The EFMW Proposition',
             quote='The strongest interpretation of Devs 2.0 does not require EFMW physics to be correct.'),
        dict(question='Who authorizes an action?',short='Who stays in control?',
             heading='Prediction and authorization are distinct operations.',
             summary='The human-agency section separates prediction, recommendation, authorization, and action. The formal companion models permission for a particular action revision; it does not execute external actions.',
             doc='devs',anchor='## 8. Human Agency',
             quote='Prediction must not silently become authority.'),
        dict(question='What does the critic guarantee?',short='What does criticism guarantee?',
             heading='A testable hypothesis, not automatic correctness.',
             summary='The paper calls for mechanisms that challenge assumptions and conclusions. Whether criticism improves answers is an empirical question. The formal companion includes a counterexample in which a bad critic keeps only a false claim.',
             doc='devs',anchor='## 6. The Zoo as an Internal Scientific Immune System',
             quote='The Zoo should not exist to confirm EFMW.\n\nIt should attack EFMW.')
    ]
    for a in answers:
        d=next(d for d in documents if d['id']==a['doc'])
        assert a['quote'].replace('**','') in '\n'.join(d['lines']).replace('**',''), a['question']
        start=next(i for i,line in enumerate(d['lines']) if a['quote'].split('\n')[0] in line.replace('**',''))
        a['start']=start+1
        a['end']=min(start+max(8,len(a['quote'].split('\n'))),len(d['lines']))
        assert a['quote'] in '\n'.join(d['lines'][start:a['end']]).replace('**','')
    proofs=catalog()
    data=dict(documents=documents,config=config,thresholds=thresholds,proofs=proofs,
              sourceCorrections=json.loads((ROOT/'web/source-corrections.json').read_text()),
              blockers=freeze_errors(config,thresholds,read(BENCH/'QUESTIONS.json'),{d['id']:d for d in documents}),
              answers=answers,paper=(ROOT/'Devs2.0-EFMW.md').read_text(),
              prompts={p.name:p.read_text() for p in sorted((BENCH/'arms').glob('*.txt'))})
    html=(ROOT/'web/template.html').read_text()
    html=html.replace('/*__STYLE__*/',(ROOT/'web/style.css').read_text())
    html=html.replace('/*__DATA__*/','window.DEVS_DATA='+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+';')
    html=html.replace('/*__ENGINE__*/',(ROOT/'web/engine.js').read_text().replace('export ',''))
    html=html.replace('/*__APP__*/',(ROOT/'web/app.js').read_text())
    (ROOT/'index.html').write_text(html)
    (ROOT/'_site').mkdir(exist_ok=True)
    (ROOT/'_site/index.html').write_text(html)
    (ROOT/'_site/.nojekyll').write_text('')
    (ROOT/'docs').mkdir(exist_ok=True)
    (ROOT/'docs/theorems.json').write_text(json.dumps(proofs,indent=2)+'\n')
    audit='import Devs\n\n'+'\n'.join('#print axioms '+p['qualified'] for p in proofs)+'\n'
    (ROOT/'Devs/Audit.lean').write_text(audit)
    print(f'Built self-contained index.html: {len(html.encode()):,} bytes; {len(proofs)} formal statements; {len(documents)} corpus versions.')
    return data


if __name__=='__main__': build()
