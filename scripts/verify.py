"""Portable software verification. Run `lake build` separately for Lean."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(cmd): subprocess.run(cmd,cwd=ROOT,check=True)

def main():
    run([sys.executable,'-m','unittest','discover','-s','research/dev2-001/tests','-v'])
    run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py','-v'])
    run(['node','--test','tests/engine.test.mjs'])
    run([sys.executable,'scripts/build_site.py'])
    run([sys.executable,'bench.py','doctor'])
    cfg=json.loads((ROOT/'research/dev2-001/CONFIG.json').read_text())
    if cfg['status'] != 'FROZEN':
        refused=subprocess.run([sys.executable,'bench.py','doctor','--require-frozen'],cwd=ROOT,capture_output=True).returncode
        if refused==0: raise SystemExit('Draft unexpectedly passed freeze gate')
    sources=list((ROOT/'Devs').glob('*.lean'))+[ROOT/'Devs.lean',ROOT/'Main.lean']
    # Source hygiene complements (and never substitutes for) Lean compilation.
    for p in sources:
        if re.search(r'\b(sorry|admit|axiom)\b',p.read_text()):
            raise SystemExit('Forbidden proof placeholder/declaration: '+str(p))
    print('Software checks passed. Compile and audit Lean independently; no experimental result.')

if __name__=='__main__': main()
