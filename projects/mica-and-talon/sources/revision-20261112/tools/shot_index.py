#!/usr/bin/env python3
"""Purpose: out/shot-index.csv: every capture the final cuts put on screen, with its entry kind, declared setup
(position, time, rings, score, emeralds, cast), build commit, source frames used in each cut and the command.
Inputs: out/usage-16x9.json, out/usage-9x16.json (tools/usage.py), captures/*/provenance.json.
Origin: MICA & TALON promo redo 2026-11-12."""
import csv, json, os
from pathlib import Path
T = Path(__file__).resolve().parent.parent
CAP = T / os.environ.get('MT_CAPTURES', 'captures')
H = json.load(open(T / 'out/usage-16x9.json'))['captures']
V = json.load(open(T / 'out/usage-9x16.json'))['captures']
ENTRY = {'tool': 'positioned start (GameplayCaptureTool --x/--y)', 'title': 'cold title-first production boot',
         'host': 'positioned start (PromoCapture host)'}
rows = []
for name in sorted(set(H) | set(V)):
    p = json.load(open(CAP / name / 'provenance.json'))
    pr = p.get('props', {})
    kind = p.get('kind', 'tool')
    entry = ENTRY[kind]
    if kind == 'host':
        entry = {'declared': 'positioned start, solo MICA (declared host)', 'positioned': 'positioned start with declared score (positioned host)',
                 'powered': 'positioned start with declared score and powered-state log (powered host)',
                 'starpost': 'debug ROM-starpost component entry into the special stage (starpost host)',
                 'original': 'debug presentation component entry (original host)'}[p['host']]
    if 'x' not in p and kind == 'tool':
        entry = "the act's own start position"
    if name == 'scz-chain':
        entry = "the act's own start position (positioned host, solo MICA; the game puts TALON in the cockpit)"
    if p.get('stock'):
        entry += '; stock control, no mod'
    tf = p.get('timer', pr.get('promo.timer'))
    cast_main = p.get('main', pr.get('promo.main', 'sonic' if p.get('stock') else 'mica'))
    cast_side = p.get('sidekick', pr.get('promo.sidekick', ''))
    if kind == 'title':
        cast_side = 'tails' if p.get('stock') else 'talon'
    if kind == 'host' and p['host'] in ('starpost', 'original'):
        cast_side = 'talon'
    cmd = ' '.join(str(c) for c in p['command']).replace(str(T), '$TASK').replace(p['checkout'], '$CHECKOUT')
    rows.append(dict(capture=name, game=p['game'], zone=p['zone'], act=p.get('act', 1), entry=entry, x=p.get('x', ''), y=p.get('y', ''),
                     declared_time=f'{int(tf) // 3600}:{int(tf) // 60 % 60:02d}' if tf not in (None, '') else '',
                     declared_rings=p.get('rings', pr.get('promo.rings', '')), declared_score=pr.get('promo.score', ''),
                     emeralds=p.get('emeralds', pr.get('promo.emeralds', '')), main=cast_main, sidekick=cast_side or '',
                     frames=H.get(name, V.get(name))['capture_frames'],
                     used_16x9=f"{H[name]['src_min']}-{H[name]['src_max']}" if name in H else '',
                     used_9x16=f"{V[name]['src_min']}-{V[name]['src_max']}" if name in V else '',
                     first_on_screen_s=min(d[name]['first_s'] for d in (H, V) if name in d),
                     build_commit=p.get('build_commit', p['commit'])[:10], mod_commit=p.get('mod_commit', '')[:10], develop_commit=p.get('develop_commit', '')[:10],
                     jar_sha256=p['jar_sha256'][:12], audio=p.get('audio_stem') or 'silent', note=p.get('note', ''), command=cmd))
with open(T / 'out/shot-index.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(sorted(rows, key=lambda r: r['first_on_screen_s']))
print(len(rows), 'captures;', 'only in 16:9:', sorted(set(H) - set(V)), 'only in 9:16:', sorted(set(V) - set(H)))
