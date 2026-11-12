#!/usr/bin/env python3
"""Purpose: out/verification.json for the two final masters (run with MT_CAPTURES naming the capture folder), all measured on the ENCODED files: ffprobe, chapter
count, full decode, integrated loudness / true peak / range (ffmpeg ebur128=peak=true, from tools/finish.py's
report), loudness per film section, black and frozen stretches, plus the edit's own checks (promo_kit check in
both modes, stinger levels against the bed, captures outlived).
Inputs: out/master-16x9.mp4, out/master-9x16.mp4 and their .loudness.json; out/usage-*.json.
Origin: MICA & TALON promo redo 2026-11-12."""
import json, os, re, subprocess, sys
from pathlib import Path
T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
PY = sys.executable
BT = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]
SECT = [('Cold open', 0, BT[10]), ('Title drop', BT[10], BT[14]), ('MICA', BT[14], BT[28]), ('TALON', BT[28], BT[36]),
        ('Every screen', BT[36], BT[52]), ('At speed', BT[52], BT[60]), ('Powered up (chorus)', BT[60], BT[76]),
        ('Hyper, boss and the pair (lift)', BT[76], BT[84]), ('End card (fade)', BT[84], 124.0)]
rep = {}
for tag in ('16x9', '9x16'):
    f = T / f'out/master-{tag}.mp4'
    L = json.load(open(f.with_suffix('.loudness.json')))
    st = {s['codec_name']: s for s in L['ffprobe']['streams']}
    ch = subprocess.run(['ffprobe', '-v', 'error', '-show_chapters', '-of', 'json', str(f)], capture_output=True, text=True).stdout.count('"start_time"')
    sect = []
    for name, a, b in SECT:
        e = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', str(f), '-map', '0:a:0', '-af',
                            'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
        s = e[e.rindex('Summary:'):]
        sect.append(dict(section=name, t0=round(a, 2), t1=round(b, 2), lufs=float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1)),
                         true_peak_dbtp=float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1))))
    d = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-vf', 'blackdetect=d=0.2:pix_th=0.06,freezedetect=n=-60dB:d=0.5', '-an',
                        '-f', 'null', '-'], capture_output=True, text=True).stderr
    still = [re.sub(r'^\[.*?\] ', '', l).replace('lavfi.freezedetect.', '') for l in d.splitlines() if 'black_start' in l or 'freeze_start' in l or 'freeze_duration' in l]
    env = dict(os.environ, **({'MT_VERTICAL': '1'} if tag == '9x16' else {}))
    chk = subprocess.run([PY, str(ROOT / 'tools/media/promo_kit.py'), 'check', str(T / 'edit/edit.py')], capture_output=True, text=True, env=env).stdout.strip()
    use = json.load(open(T / f'out/usage-{tag}.json'))
    rep[tag] = dict(file=f'out/master-{tag}.mp4', bytes=f.stat().st_size, duration_s=float(L['ffprobe']['format']['duration']),
                    video=dict(codec=st['h264']['codec_name'], profile=st['h264']['profile'], pix_fmt=st['h264']['pix_fmt'], width=st['h264']['width'],
                               height=st['h264']['height'], fps=st['h264']['avg_frame_rate'], bit_rate=int(st['h264']['bit_rate'])),
                    audio=dict(codec='aac', bit_rate=int(st['aac']['bit_rate']), sample_rate=48000), chapters=ch, full_decode_exit=L['full_decode_exit'],
                    integrated_lufs=L['integrated_lufs'], true_peak_dbtp=L['true_peak_dbtp'], loudness_range_lu=L['lra_lu'],
                    loudness_method='ffmpeg ebur128=peak=true on the encoded AAC; two-pass linear loudnorm, extra gain %.2f dB' % L['extra_gain_db'],
                    sections=sect, black_and_frozen=still, promo_kit_check=chk,
                    captures_used=len(use['captures']), captures_outlived=use['overruns'], usage_sample_step=use['step'])
# game sound: every on-screen hit's captured SFX against the bed (tools/mixcheck.py); there are no placed stingers
subprocess.run([PY, str(T / 'tools/mixcheck.py'), str(T / 'out/sfx-levels.json')], capture_output=True, text=True, check=True)
mix = json.load(open(T / 'out/sfx-levels.json'))
rep['game_sound'] = dict(mix['summary'], source='each take\'s own SFX-only stem (music volume 0 at capture), cut to the frames on screen', placed_stingers=0,
                         note='the two cuts share one sound track; levels are before mastering, relative to the bed')
rep['sound_checked_by'] = 'measurement only; nobody listened to these files'
json.dump(rep, open(T / 'out/verification.json', 'w'), indent=1)
(T / 'out/promo_kit-check.txt').write_text('16:9\n' + rep['16x9']['promo_kit_check'] + '\n\n9:16\n' + rep['9x16']['promo_kit_check'] + '\n')
for tag in ('16x9', '9x16'):
    r = rep[tag]
    print(tag, r['duration_s'], 's', r['integrated_lufs'], 'LUFS', r['true_peak_dbtp'], 'dBTP', 'LRA', r['loudness_range_lu'], 'chapters', r['chapters'], 'decode', r['full_decode_exit'],
          'outlived', r['captures_outlived'], '|', r['promo_kit_check'].splitlines()[-1][:120])
    print('   sections', [(s['lufs'], s['true_peak_dbtp']) for s in r['sections']])
    print('   still', r['black_and_frozen'])
print('game sound', json.dumps(rep['game_sound'])[:400])
