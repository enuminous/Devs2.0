"""Convenient entrypoint. No paid API calls occur in doctor, prepare or smoke."""
import argparse
import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BENCH=ROOT/'research/dev2-001'
sys.path.insert(0,str(BENCH))
from core import corpus,read,freeze_errors,write

def doctor():
    docs=corpus()
    return {'experiment':'DEV2-001','status':'DRAFT_NOT_FROZEN',
            'corpus_versions_verified':len(docs),
            'development_questions':len(read(BENCH/'development/QUESTIONS.json')['questions']),
            'heldout_questions':len(read(BENCH/'QUESTIONS.json')['questions']),
            'blockers':freeze_errors(read(BENCH/'CONFIG.json'),read(BENCH/'THRESHOLDS.json'),read(BENCH/'QUESTIONS.json'),docs),
            'model_experiment_executed':False,'physics_validated':False}

def smoke(out):
    from run import run
    from score import blind
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    config=copy.deepcopy(read(BENCH/'CONFIG.json'))
    config['model'].update(snapshot='SOFTWARE_FIXTURE_ONLY',tokenizer='fixture_chars_128_v1')
    config['operator']='SOFTWARE_FIXTURE_NO_HUMAN_OPERATOR'
    data=read(BENCH/'development/QUESTIONS.json')
    manifest=run(data,config,BENCH/'adapters/fixture.py',out/'generation')
    blind(out/'generation',data,out/'blank-scoring-packets')
    report={'kind':'SOFTWARE_SMOKE_ONLY','official':False,'complete':manifest['complete'],
            'questions':len(data['questions']),'responses':len(read(out/'generation/responses.json')),
            'human_scoring':'NOT PERFORMED; blank templates only','experimental_verdict':'UNVERIFIED',
            'model_calls':0,'physics_validation':False}
    write(out/'SMOKE.json',report)
    return report

if __name__=='__main__':
    forwarded = ('prepare','run','score','analyze','planning')
    if len(sys.argv)>1 and sys.argv[1] in forwarded:
        sys.exit(subprocess.call([sys.executable,str(BENCH/(sys.argv[1]+'.py')),*sys.argv[2:]]))
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    d=sub.add_parser('doctor');d.add_argument('--require-frozen',action='store_true')
    s=sub.add_parser('smoke');s.add_argument('--out',required=True)
    for name in forwarded:
        sub.add_parser(name,add_help=False)
    args=p.parse_args()
    if args.command=='doctor':
        result=doctor();print(json.dumps(result,indent=2));sys.exit(1 if args.require_frozen and result['blockers'] else 0)
    elif args.command=='smoke': print(json.dumps(smoke(args.out),indent=2))
