#!/usr/bin/env python3
"""Purpose: the revised-climax check as ONE self-contained HTML file: 100-124 s of the new cut at 640 px CRF 30
(base64), the state evidence for "why does Hyper MICA turn jade after the hit", the pair shot's provenance, and
stills from the encoded file. Short on purpose; the full package was checkpoint 2.
Inputs: checkpoint3/climax-16x9.mp4 (+ .loudness.json, stingers.json, promo_kit-check.txt, overrun.json),
captures/e-lbz-boss-state, captures/d-lbz-pair. Origin: MICA & TALON promo redo 2026-11-12."""
import base64, csv, html, io, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

T = Path(__file__).resolve().parent.parent
C = T / 'checkpoint3'
FILM = C / 'climax-16x9.mp4'
BT = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]
esc = html.escape


def bt(n, beat=0.0):
    k = int(n)
    return BT[k] + (BT[k + 1] - BT[k]) * ((n - k) * 4 + beat) / 4


def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def jpg(im, q=86):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return b64(buf.getvalue(), 'image/jpeg')


def grab(t, w=640):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(FILM), '-frames:v', '1', '-vf', f'scale={w}:-2:flags=lanczos',
                        '-f', 'image2pipe', '-c:v', 'png', '-'], capture_output=True, check=True)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB')


F = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 15)


def strip(items, w=640, cols=3):
    ims = [(grab(t, w), lab) for t, lab in items]
    h = ims[0][0].height
    rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * w, rows * (h + 22)), (14, 18, 34))
    d = ImageDraw.Draw(S)
    for k, (im, lab) in enumerate(ims):
        x, y = (k % cols) * w, (k // cols) * (h + 22)
        S.paste(im, (x, y))
        d.text((x + 6, y + h + 2), lab, font=F, fill=(255, 220, 90))
    return S


# ---- excerpt
ex = C / 'climax-100-124-640.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '100', '-i', str(FILM), '-vf', 'scale=640:360:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow',
                '-crf', '30', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(ex)], check=True)

# ---- point 1: state evidence from the capture's own state.csv
BOSS = T / 'captures/e-lbz-boss-state'
rows = list(csv.DictReader(open(BOSS / 'state.csv')))
frames = sorted((BOSS / 'frames').glob('*.png'))
ref = list(csv.DictReader(open(T / 'captures/d-lbz-boss/state.csv')))
same = all((rows[i]['x'], rows[i]['y'], rows[i]['score']) == (ref[i]['x'], ref[i]['y'], ref[i]['score']) for i in range(len(ref)))


def colour(i):
    a = np.asarray(Image.open(frames[i]).convert('RGB')).astype(int)
    cx = int(rows[i]['x']) - int(rows[i]['cam_x']); cy = int(rows[i]['y']) - int(rows[i]['cam_y'])
    p = a[max(0, cy - 14):cy + 14, max(0, cx - 14):cx + 14].reshape(-1, 3)
    gold = int(((p[:, 0] > 200) & (p[:, 1] > 140) & (p[:, 2] < 130)).sum())
    jade = int(((p[:, 1] > p[:, 0] + 40) & (p[:, 1] > 110) & (p[:, 2] > 60) & (p[:, 0] < 120)).sum())
    return gold, jade


changes = [i for i in range(1, len(rows)) if (rows[i]['p1_super'], rows[i]['p1_state'], rows[i]['timer_paused']) !=
           (rows[i - 1]['p1_super'], rows[i - 1]['p1_state'], rows[i - 1]['timer_paused'])]
change_rows = ''.join(f"<tr><td>{i}</td><td>{rows[i]['p1_super']}</td><td>{rows[i]['p1_state']}</td><td>{rows[i]['p1_tier'] or '&ndash;'}</td>"
                      f"<td>{rows[i]['timer_paused']}</td><td>{int(rows[i]['score']):,}</td><td>{rows[i]['rings']}</td></tr>" for i in [0] + changes)
ev = []
for i in (641, 642, 645, 647, 648, 649, 650, 651, 655, 660, 661, 662, 663, 670, 684, 690):
    g, j = colour(i)
    look = 'gold' if g > 100 and j < 40 else 'jade' if j > 90 and g < 40 else 'mixed / fading'
    note = {642: 'strike pressed: jade strike palette', 648: 'the kill: score +1000, timer stops, form ends', 651: 'still drawn gold', 661: 'fading',
            663: 'jade from here on', 685: 'lands'}.get(i, '')
    ev.append(f"<tr class='{'k' if i == 648 else ''}'><td>{i}</td><td>{rows[i]['p1_super']}</td><td>{rows[i]['p1_tier'] or '&ndash;'}</td><td>{rows[i]['timer_paused']}</td>"
              f"<td>{int(rows[i]['score']):,}</td><td>{g}</td><td>{j}</td><td>{look}</td><td>{note}</td></tr>")
idx = [641, 645, 648, 651, 656, 660, 662, 664, 672, 688]
S = Image.new('RGB', (len(idx) * 192, 144 + 20), (14, 18, 34))
d = ImageDraw.Draw(S)
for k, i in enumerate(idx):
    cx = int(rows[i]['x']) - int(rows[i]['cam_x']); cy = int(rows[i]['y']) - int(rows[i]['cam_y'])
    x0 = max(0, min(320 - 64, cx - 40)); y0 = max(0, min(224 - 48, cy - 26))
    S.paste(Image.open(frames[i]).convert('RGB').crop((x0, y0, x0 + 64, y0 + 48)).resize((192, 144), Image.NEAREST), (k * 192, 0))
    d.text((k * 192 + 4, 146), f"#{i}  super={rows[i]['p1_super']}", font=F, fill=(255, 220, 90))
revert_strip = S

# ---- pair provenance
PAIR = T / 'captures/d-lbz-pair'
prov = json.load(open(PAIR / 'provenance.json'))
pr = list(csv.DictReader(open(PAIR / 'state.csv')))
pchg = [i for i in range(1, len(pr)) if (pr[i]['p1_super'], pr[i]['p1_state'], pr[i]['sk_super'], pr[i]['sk_state']) !=
        (pr[i - 1]['p1_super'], pr[i - 1]['p1_state'], pr[i - 1]['sk_super'], pr[i - 1]['sk_state'])]
pair_rows = ''.join(f"<tr><td>{i}</td><td>{pr[i]['p1_state']}</td><td>{pr[i]['p1_tier'] or '&ndash;'}</td><td>{pr[i]['sk_state']}</td><td>{pr[i]['sk_tier'] or '&ndash;'}</td>"
                    f"<td>{pr[i]['rings']}</td><td>{int(pr[i]['score']):,}</td><td>{pr[i]['timer_paused']}</td></tr>" for i in [0] + pchg + [388])
carry = [i for i in range(len(pr)) if pr[i]['sk_x'] and abs(int(pr[i]['x']) - int(pr[i]['sk_x'])) <= 2 and 20 <= int(pr[i]['y']) - int(pr[i]['sk_y']) <= 36 and pr[i]['air'] == '1']
hurt = sum(x['hurt'] == '1' for x in pr)
tf = int(prov['props']['promo.timer'])
cmd = ' '.join(str(c) for c in prov['command'])
cmd = cmd.replace(str(T), '$TASK').replace(prov['checkout'], '$CHECKOUT')
P0 = 70 - round((bt(80, 1) - bt(80)) * 60)

loud = json.load(open(C / 'climax-16x9.loudness.json'))
sting = json.load(open(C / 'stingers.json'))
over = json.load(open(C / 'overrun.json'))
check = (C / 'promo_kit-check.txt').read_text().strip()
probe = loud['ffprobe']
new_st = [s for s in sting if s['t'] >= bt(78)]
NAMES = {'s3k-sfx-4a': 'S3K Grab', 's3k-sfx-b4': 'S3K Explode', 's3k-sfx-b3': 'S3K Big Ring', 's3k-sfx-9f': 'S3K Super Transform', 's3k-sfx-6e': 'S3K Boss Hit'}
st_rows = ''.join(f"<tr><td>{s['t']:.2f}</td><td>{NAMES.get(s['sfx'], s['sfx'])}</td><td>{s['under_bed_db']:+.1f}</td></tr>" for s in new_st)

h = bt(79)
climax = strip([(h - 0.05, 'the strike, 0.05 s before the hit (jade strike palette)'), (h + 0.07, 'hit + 0.07 s: flash; the card slams in; she is gold'),
                (h + 0.35, 'hit + 0.35 s: ONE HIT.; the machine breaking up'), (h + 0.9, 'hit + 0.9 s: pieces flying'),
                (bt(80) + 0.24, 'bar 80 + 0.24 s: white clears onto the twin silhouettes'), (bt(80, 1) + 0.03, 'beat 2: both snap open'),
                (bt(80) + (125 - P0) / 60 + 0.05, 'the catch'), (bt(81, 2), 'bar 81: name tags'), (bt(82) + 0.9, 'bar 82.6: her jade flash (0.35 s), tag beside her'),
                (bt(83), 'bar 83'), (bt(84) - 0.06, 'last frame of the shot: gold and flame'), (bt(85, 2), 'end card: the same take playing on')])
weak = strip([(bt(53), 'grid, bars 52-55 (one bar shorter)'), (bt(57) + 0.4, 'ending pose, bars 56.5-58.5'), (bt(59), 'new: normal MICA runs Hydrocity'),
              (bt(60) - 0.15, 'wind-up'), (bt(60) + 0.05, 'gold reveal ON bar 60'), (bt(62), 'Gilded dash')])

doc = f"""<!doctype html><html lang=en><meta charset=utf-8><title>MICA &amp; TALON promo redo: revised climax check</title>
<style>
body{{background:#0e1222;color:#e8ecf6;font:16px/1.5 system-ui,sans-serif;max-width:1400px;margin:0 auto;padding:28px}}
h1{{font-size:28px;margin:0 0 4px}}h2{{margin:40px 0 10px;font-size:22px;border-bottom:2px solid #2449db;padding-bottom:6px}}
table{{border-collapse:collapse;font-size:14px}}td,th{{border:1px solid #2a3355;padding:5px 9px;vertical-align:top;text-align:left}}
th{{background:#18203d}}tr.k td{{background:#3a2a12;font-weight:600}}
img,video{{max-width:100%;display:block;border:1px solid #2a3355}}
.box{{background:#151b33;border-left:4px solid #ffdc5a;padding:12px 16px;margin:12px 0}}.warn{{border-left-color:#ff7a7a}}
code{{background:#1b2342;padding:1px 5px;border-radius:3px;font-size:13px}}li{{margin:5px 0}}.dim{{color:#aab3cf}}pre{{background:#151b33;padding:12px;overflow:auto;font-size:12.5px;white-space:pre-wrap}}
</style>
<h1>MICA &amp; TALON promo redo: revised climax check</h1>
<p class=dim>Full-size file: <code>~/scratch/agent-tmp/mt-promo-redo-20261111/checkpoint3/climax-16x9.mp4</code> (whole film, {float(probe['format']['duration']):.2f} s). Edit: <code>edit/edit.py</code>;
the checkpoint 2 cut is kept as <code>edit/edit-draft-checkpoint2.py</code>. Worktree still clean at <code>1e0faac123</code>.</p>

<h2>100&ndash;124 s</h2>
<video controls preload=metadata src="{b64(ex.read_bytes(), 'video/mp4')}"></video>
<p class=dim>640&times;360, CRF 30. Starts on the powered triptych; Hyper reveal at 6.4 s, the hit at 10.65 s, the pair at 12.07 s, end card at 17.7 s (file times).</p>
<img src="{jpg(climax)}">

<h2>Point 1. It is (a): the game ends her Hyper form on the kill frame</h2>
<div class=box>The capture's own state says so. At frame 648 of the boss take, in one step: the score goes up 1,000, the level timer stops, and her Super flag clears. That is the game's rule, not a palette phase: a Super form ends when the HUD timer stops, and Sonic 3 &amp; K stops it when this mini-boss dies. Engine source: <code>SuperStateController.runSuperFrameWork</code> ("ROM: Sonic_Super checks Update_HUD_timer == 0 every frame").</div>
<p>Evidence is <code>captures/e-lbz-boss-state/state.csv</code>: the boss take re-run on the same inputs with extra state columns (<code>hosts/powered/PromoCapture.java</code>). Its positions and score match the film's take <code>d-lbz-boss</code> on all {len(ref)} frames: <b>{same}</b>.</p>
<table><tr><th>Frame</th><th>Super flag</th><th>State</th><th>Tier</th><th>Timer stopped</th><th>Score</th><th>Rings</th></tr>{change_rows}</table>
<p class=dim>Every change of state in the take. Nothing else changes between frame 76 and frame 648.</p>
<table><tr><th>Frame</th><th>Super flag</th><th>Tier</th><th>Timer stopped</th><th>Score</th><th>Gold px</th><th>Jade px</th><th>She looks</th><th></th></tr>{''.join(ev)}</table>
<p class=dim>Gold and jade pixel counts in a 28&times;28 box on her centre, from the capture's frames.</p>
<img src="{jpg(revert_strip, 90)}">
<p>So she is drawn in her jade strike colours for the strike (642&ndash;650), gold for ten frames after the kill (651&ndash;660), and normal jade from frame 663. The form really is off from 648; the gold frames are its colours fading.</p>
<p><b>What the film does.</b> You said to cut before the revert. The revert is on the kill frame itself, so a cut there would remove the boss breaking apart. Instead:</p>
<ul>
<li>The hit is still on bar 79. On that frame the "ONE HIT." card slams in from the right and covers the columns she is in (native x &ge; 202 at her height). It is fully in by frame 655, while she is still gold.</li>
<li>The machine breaks apart beside the card for the rest of the bar. On the frames after 660 the only jade left of the card is a few ember pixels of the strike trail next to the machine.</li>
<li>Bar 80 cuts to the pair. The signpost and results tally are gone.</li>
</ul>
<div class="box warn"><b>Your call.</b> The card hides something the game really does: her form ends at the moment of victory. I have written it down as such for the README. If you would rather not cover it, the alternative is a hard cut to the pair 12 frames after the hit, while she is still gold. That loses most of the machine breaking apart.</div>

<h2>Point 2. The pair shot (bars 80&ndash;84)</h2>
<ul>
<li><b>What it is:</b> Launch Base 1 at the last starpost, outside the mini-boss corridor. The cut on bar 80 is a white flash that clears onto the two as white silhouettes; they snap open together on beat 2 as Hyper MICA and Solar TALON. TALON walks over, hops, catches her and carries her up past the towers. It is the cold open's carry again, with both of them powered.</li>
<li><b>Her jade flash is in it, twice,</b> for 0.35 s each (source frames 139&ndash;159 and 265&ndash;285). That is the Prism Gilt cycle itself: Super flag 1 and tier HYPER on every frame from 45 to the end. The "HYPER MICA" tag is beside her both times. The shot ends on frame 388, three frames before the next jade phase, so its last image is gold and flame.</li>
<li><b>She is carried, so she sheds no after-images here.</b> Those are in the Death Egg shot just before (bars 76&ndash;78). TALON's flaps shed embers throughout.</li>
<li><b>End card:</b> the same take plays on behind it in soft focus (columns right of the HUD: sky, towers, the pair still climbing).</li>
<li><b>Tried and dropped:</b> the two running side by side (the corridor is 240 px away and Hyper MICA outruns him within a second); the same carry in Death Egg (busier background); a powered carry in Angel Island (he missed the catch).</li>
</ul>
<h3 style="color:#ffdc5a">Provenance: <code>captures/d-lbz-pair</code></h3>
<table>
<tr><th>Source kind</th><td>{esc(prov['source_kind'])}; 60 Hz, every frame, silent, surfaceless EGL, no trace input</td></tr>
<tr><th>Build</th><td>commit <code>{prov['commit'][:10]}</code>, worktree dirty: {prov['worktree_dirty']}; jar sha256 <code>{prov['jar_sha256'][:16]}&hellip;</code></td></tr>
<tr><th>Start</th><td>Sonic 3 &amp; K, Launch Base act 1, positioned at x {prov['x']}, y {prov['y']} (the act's last starpost is at 15552, 488)</td></tr>
<tr><th>Declared</th><td>time {tf // 3600}:{tf // 60 % 60:02d}, {prov['props']['promo.rings']} rings, score {int(prov['props']['promo.score']):,}, emeralds <code>{prov['props']['promo.emeralds']}</code> (all seven Super Emeralds, as for Death Egg)</td></tr>
<tr><th>Cast</th><td>MICA leads on controller 1; TALON is the sidekick, driven from controller 2</td></tr>
<tr><th>Input script</th><td><code>{esc(prov['script'])}</code></td></tr>
<tr><th>Host</th><td><code>hosts/powered/PromoCapture.java</code>, sha256 <code>{prov['capture_host_sha256'][:16]}&hellip;</code>: the positioned host plus powered-state columns in <code>state.csv</code></td></tr>
<tr><th>Command</th><td><code>{esc(cmd)}</code></td></tr>
</table>
<p>State through the take (every change, plus the last frame the film uses):</p>
<table><tr><th>Frame</th><th>MICA state</th><th>MICA tier</th><th>TALON state</th><th>TALON tier</th><th>Rings</th><th>Score</th><th>Timer stopped</th></tr>{pair_rows}</table>
<p class=dim>Carry (TALON exactly above her, 28 px, both airborne): frames {carry[0]}&ndash;{carry[-1]}. Hurt frames: {hurt}. The film uses frames {P0}&ndash;388; the end card continues from 389. Frames {P0}&ndash;57, where the two are still in normal colours at the start of their wind-up, are under the white flash.</p>
<p class=dim>Two things a careful viewer could spot: the pair take's HUD reads 2:41 and 283,200 straight after the boss take's 3:10 and 284,900 (it is a separate take at the starpost before the arena), and TALON only transforms because a second controller asks him to.</p>

<h2>Point 3. The grid and the bar it freed</h2>
<p>The grid is one bar shorter (bars 52&ndash;55). The ending moves up a bar. The freed bar goes to the front of the Gilded shot: normal MICA now runs Hydrocity for a bar and a half before she jumps and transforms, and the gold reveal is still exactly on bar 60. New capture <code>d-hcz1-gilded-runin</code> (same declared 1:40, 66 rings, 41,900).</p>
<img src="{jpg(weak)}">

<h2>Numbers</h2>
<ul>
<li>Whole film on the encoded AAC: <b>{loud['integrated_lufs']:.1f} LUFS, true peak {loud['true_peak_dbtp']:.1f} dBTP</b>, range {loud['lra_lu']:.1f} LU; full decode exit {loud['full_decode_exit']}.</li>
<li><code>promo_kit.py check</code>: <code>{esc(check)}</code></li>
<li>Sources outlived (my audit, every {over['step']}nd frame): {len(over['overruns'])}.</li>
<li>Stingers from bar 78 on, each on its event frame, dB under the music: <table><tr><th>Time (s)</th><th>Sound</th><th>dB under the bed</th></tr>{st_rows}</table></li>
<li>Sound was checked by measurement only.</li>
</ul>
<p class=dim>After your reply: final 16:9, the 9:16 cut, README, contact sheets and the local archive.</p>
</html>"""
out = C / 'climax-check.html'
out.write_text(doc)
print(out, f'{out.stat().st_size / 1e6:.1f} MB', 'excerpt', f'{ex.stat().st_size / 1e6:.1f} MB', 'same', same, 'P0', P0, 'carry', carry[0], carry[-1], 'hurt', hurt)
