"""Verify the pinned methods handoff; no model calls or human approvals."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BENCH = REPO / 'research/dev2-001'


def read(path):
    return json.loads(path.read_text())


def check():
    manifest = read(HERE/'BASELINE_MANIFEST.json')
    for path, expected in manifest['sha256'].items():
        actual = hashlib.sha256((REPO/path).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit('Baseline drift: ' + path)
    for path, source in manifest['review_only_version_snapshots'].items():
        if hashlib.sha256((HERE/path).read_bytes()).hexdigest() != source['sha256']:
            raise SystemExit('Review evidence drift: ' + path)
    originals = {q['id']: q for q in read(BENCH/'development/QUESTIONS.json')['questions']}
    worksheet = read(HERE/'QUESTION_REVIEW_WORKSHEET.json')
    if len(worksheet['items']) != 12 or {q['id'] for q in worksheet['items']} != set(originals):
        raise SystemExit('Worksheet roster mismatch')
    for q in worksheet['items']:
        original = originals[q['id']]
        if (q['question'] != original['text'] or q['proposed_gold_from_existing_package'] != original['gold']
                or q['existing_cluster_id'] != original['cluster_id'] or q['proposed_tier'] != original['tier']):
            raise SystemExit('Worksheet source mismatch: ' + q['id'])
        if q['eligible_for_holdout'] or q['final_curator_resolution'] is not None:
            raise SystemExit('Public preparation worksheet cannot grant holdout eligibility')
        for reviewer in ('reviewer_1', 'reviewer_2'):
            if any(v is not None for v in q[reviewer].values()):
                raise SystemExit('Published preparation worksheet must not invent reviewer judgments')
    screening = read(HERE/'CONFLICT_SCREENING.json')
    if screening['eligible_authentic_conflicts_established'] != 0 or len(screening['items']) != 4:
        raise SystemExit('Screening summary mismatch')
    for item in screening['items']:
        if item['independent_human_review'] or item['final_decision'] is not None:
            raise SystemExit('Preparation cannot impersonate independent review')
        for side in ('before','after'):
            evidence = item[side]
            text = (HERE/evidence['packet_path']).read_text().splitlines()
            quote = '\n'.join(text[evidence['start_line']-1:evidence['end_line']])
            if quote != evidence['quote']:
                raise SystemExit('Source quotation mismatch: ' + item['id'])
    census = read(HERE/'HISTORY_CENSUS.json')
    if len(census['paths']) != 8 or sum(c['change_kind']=='revision' for p in census['paths'] for c in p['changes']) != 4:
        raise SystemExit('Bounded history census mismatch')
    if read(BENCH/'CONFIG.json')['status'] != 'DRAFT_NOT_FROZEN' or read(BENCH/'QUESTIONS.json')['questions']:
        raise SystemExit('This handoff describes a draft with an empty evaluation ledger')
    for path in HERE.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#') and not (path.parent/link.split('#')[0]).exists():
                raise SystemExit('Broken packet link: ' + link)
    print(f"REVIEW_PACKET_PASS: {len(manifest['sha256'])} baseline files; 12 development items; 4 screened amendments; 0 eligible conflicts; all human-review fields blank")


if __name__ == '__main__':
    check()
