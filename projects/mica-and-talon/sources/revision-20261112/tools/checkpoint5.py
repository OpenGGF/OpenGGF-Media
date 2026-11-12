#!/usr/bin/env python3
"""Purpose: checkpoint 5, the stage B probe report, as ONE self-contained HTML file plus a PNG under 512 KB:
the build the probes ran on, the SFX-only audio check of every capture host, the six re-stages (confirmed or
switched to fallback) with stills from the probe that will be re-shot as the final take, and the beat offsets
after the input tunes. No final captures: every picture is a probe on the build without the art branch.
Inputs: probes-b/* (tools/probes_b.py, tools/capture.py --dest probes-b), work/beat-track.json.
Outputs: checkpoint5/probes.html, checkpoint5/probes.png, checkpoint5/probes.json.
Origin: MICA & TALON promo redo, stage B, 2026-11-12."""
import base64, csv, html, io, json, math, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

T = Path(__file__).resolve().parent.parent
C = T / 'checkpoint5'
C.mkdir(exist_ok=True)
P = T / 'probes-b'
R = Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f')
BT = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]
esc = html.escape


def bf(n, beat=1):
    n = n + (beat - 1) / 4
    k = int(n)
    return int(round((BT[k] + (BT[k + 1] - BT[k]) * (n - k)) * 60))


BEATS = [bf(b, k) for b in range(0, 89) for k in (1, 2, 3, 4)]


def near(f):
    j = min(range(len(BEATS)), key=lambda i: abs(BEATS[i] - f))
    return j // 4, j % 4 + 1, f - BEATS[j]


def rows(name):
    return list(csv.DictReader(open(P / name / 'state.csv')))


def num(r, k):
    try:
        return float(r[k])
    except (KeyError, ValueError, TypeError):
        return 0.0


def speed(name, a, b, events=()):
    r = rows(name)
    v = [max(math.hypot(num(r[i], 'xvel'), num(r[i], 'yvel')), min(6400.0, 256 * math.hypot(num(r[i], 'x') - num(r[i - 1], 'x'), num(r[i], 'y') - num(r[i - 1], 'y')))) for i in range(max(1, a), min(len(r), b))]
    g = [abs(num(r[i], 'gspeed')) for i in range(max(1, a), min(len(r), b))]
    idle = sum(1 for i, x in zip(range(max(1, a), min(len(r), b)), v) if x < 384 and not any(abs(i - e) <= 30 for e in events))
    return round(sum(g) / len(g)), round(sum(v) / len(v) / 256, 1), round(idle / 60, 2)


def place(b0, anchors):
    """Shot starting on bar b0; anchors = [(label, src_frame, bar, beat)]; the first one fixes the window."""
    f0 = bf(b0)
    lab, src, bar, beat = anchors[0]
    src0 = src - (bf(bar, beat) - f0)
    out = []
    for lab, src, bar, beat in anchors:
        b, k, dev = near(f0 + src - src0)
        out.append(dict(event=lab, src=src, bar=b, beat=k, dev=dev))
    return src0, out


F13 = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Regular.ttf', 13)
F13B = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 13)
F22B = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 22)


def frame(name, i):
    fr = sorted((P / name / 'frames').glob('*.png'))
    idx = [int(f.stem) for f in fr]
    j = min(range(len(idx)), key=lambda k: abs(idx[k] - i))
    return Image.open(fr[j]).convert('RGB'), idx[j]


def strip(name, picks, w=176):
    h = round(w * 224 / 320)
    s = Image.new('RGB', (len(picks) * (w + 3) - 3, h + 15), (14, 18, 34))
    d = ImageDraw.Draw(s)
    for k, i in enumerate(picks):
        im, real = frame(name, i)
        s.paste(im.resize((w, h), Image.BOX), (k * (w + 3), 0))
        d.text((k * (w + 3) + 2, h + 1), f'#{real}', font=F13, fill=(255, 220, 90))
    return s


def jpg(im, q=82):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def audio(name):
    with wave.open(str(P / name / 'audio.wav')) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(np.float64).reshape(-1, 2) / 32768
    n = len(x) // 800
    db = [20 * math.log10(max(1e-9, math.sqrt(float((x[i * 800:(i + 1) * 800] ** 2).mean())))) for i in range(n)]
    loud = [v for v in db if v > -90]
    nz = np.nonzero(np.abs(x).max(axis=1) > 2e-4)[0]
    return dict(frames=n, silent_frames=sum(v <= -100 for v in db), loudest_frame_db=round(max(db), 1), mean_loud_db=round(sum(loud) / len(loud), 1) if loud else None,
                first_sound_frame=round(float(nz[0]) / 800, 2) if len(nz) else None)


# ---- the six re-stages: (key, bars, title, status, probe with pictures, picks, anchors, what, script note, limit)
RESTAGE = [
    ('R1', '2-4', 'Launch Base 1 duo from a run-up', 'confirmed, with a limit', 'r1-final-look', [74, 100, 130, 160, 190, 215, 224, 236],
     (2, [('spring', 218, 3, 4)]),
     'Start at x 14300 on the lower bridge (the storyboard guessed 13500-14000; a wall stands at 14100). Both run right; MICA reaches top speed (|gspeed| 1536) at #139 and holds it to the spring at #218.',
     'positioned host, MICA + TALON, start (14300, 1470), script "20 -; 250 R"',
     'The bridge is 836 px long, so top speed lasts 79 frames, not the whole shot: the shot opens at 2.7 px/f and is at 6 px/f for its second bar. It ends 21 frames after the spring, before the machine on the upper deck comes into view.'),
    ('R2', '4-6', 'Angel Island 1 carry swoop', 'confirmed', 'r2-look-s75-j40', [88, 100, 112, 120, 126, 130, 160, 200, 250],
     (4, [('catch', 128, 4, 3)]),
     'TALON runs ahead, hops and hovers; MICA runs toward him, jumps (#115) and he catches her in the air 13 frames later; they fly on over the hill and the canopy at 2.3 px/f, climbing.',
     'positioned host, MICA on pad 1, TALON on pad 2: TALON "50 R; R+A; 7 -; A", then Right with a flap every 8 frames from #150; MICA waits to #75, runs, jumps #115 (A held 12)',
     'The carry itself flies at 2.3 px/f plus the climb, under the 3 px/f the storyboard asked for; that is the game\'s carry speed.'),
    ('R3', '34-36', 'Aquatic Ruin 1: TALON divebombs a Whisp', 'confirmed in part: one kill, not two', 'r3-look-t150-d14-x3', [130, 150, 164, 176, 186, 192, 198, 215, 240],
     (34, [('kill', 191, 35, 1)]),
     'TALON solo runs the ruins, jumps at #150 and dives; the third dive press finds a Whisp and kills it at #191 (native 100). Twenty-three probes found no second Whisp in reach after it.',
     'positioned host, TALON solo, start (8300, 860), script "20 -; 130 R; R+A; 13 R; D+A; 11 R; D+A; 9 R; D+A; 100 R"',
     'One kill on bar 35 instead of kills on bar 34 beat 3 and bar 35. Still his Sonic 2 hit, which the fallback (the Launch Base flight) did not have.'),
    ('R4', '67.5-70', 'Solar TALON: reveal straight into a divebomb kill', 'confirmed', 'r4-look-x6900-dh12', [70, 86, 98, 106, 125, 150, 180, 190, 215, 250],
     (67.5, [('reveal', 104, 68, 1), ('kill', 188, 69, 1)]),
     'He jumps, winds up in the air (#79), the flame reveal is at #104; eight flaps across the clearing, the dive, and the Rhinobot dies at #188: exactly one bar after the reveal.',
     'powered host, TALON solo, 7 emeralds, start (6900, 900), script "30 -; A; 20 -; A; 27 -; R+A; 20 R; repeat 8 { R+A; 8 R }; 12 D+R; D+A; 150 R"',
     'After the reveal he is on screen in flight for 1.2 s before the dive, then 1.4 s after the kill, so the Solar design has 3.9 s in all to be read.'),
    ('R5', '78-80', 'Launch Base 1 mini-boss: run-in strike', 'confirmed', 'r5-look2-t560-r590-h618-s8', [549, 565, 580, 597, 610, 621, 630, 636, 648, 669],
     (78, [('boss hit', 632, 79, 1)]),
     'With the arena camera locked she backs off left (#560), turns, runs in (#590), hops (#618) and strikes once (#626): boss hit +1000 at #632. She stands for 12 frames of the shot instead of 84.',
     'powered host, Hyper MICA, the old script to the arena, then "338 -; 30 L; 28 R; R+A; 7 R; R+A"',
     'The game still ends her Hyper form on the hit frame (p1_state NORMAL at #632). After the hit she travels right, so the ONE HIT. card stays on the right; its edge moves from x 208 to about x 200 so she is under it 5 frames before she is drawn jade. To be checked on the final take.'),
    ('R6', '80-84', 'The pair: nobody stands, the carry travels', 'confirmed, moved to the lower bridge', 'r6-final-look-b20k10', [66, 78, 87, 100, 114, 123, 129, 150, 190, 250, 330, 399],
     (80, [('reveal', 86, 80, 2), ('catch', 128, 80, 4)]),
     'Moved from the starpost deck (350 px long, a wall 180 px to the right) to the lower bridge, the one the opening duo shot runs across: open sky above and room to fly. Twin transformation, reveal at #86, they land, TALON hops at #113 and catches her at #128; they drift up and to the right across the domes for the rest of the shot (about 1.3 px/f across and 1 px/f up, the flight climb limit of the game).',
     'powered host, both pads, Super Emeralds, start (14350, 1470): "40 -; A / A; 20 -; A / A", TALON "R+A" at #113, flap, Right held 20 frames after the catch then tapped one frame in ten, a flap every 9 frames',
     'The catch is on beat 4 of bar 80, two beats earlier than the storyboard\'s bar 81: waiting for bar 81 would put 22 frames of standing back in. Both are on screen in their powered forms for 0.7 s before the catch and for the whole carry. Flight tires after 8 s (#593), so the end card backdrop is ping-ponged before that, as in the delivered cut. The carried flight cannot climb faster than 1 px/f, so the pair moves at about 1.7 px/f in all and my slow-frame measure still counts 3 s of it; the camera travels the whole time.'),
]

# ---- tunes: (bars, title, before events, after events (probe, events), anchors, note)
TUNES = [
    ('14-16', 'Marble Garden chain', [('kill 100', 65), ('kill 200', 82), ('kill 500', 104)], 't1-mgz-84-105', [('kill 100', 65), ('kill 200', 85), ('kill 500', 107)], (14, 14, 4),
     'second and third strike presses moved from #80, #103 to #84, #105'),
    ('48-50', 'Sky Chase chain', [('kill', 259), ('kill', 319), ('kill', 358)], 't2-scz-320-363', [('kill', 259), ('kill', 321), ('kill', 364)], (48, 48, 2),
     'the strike presses at #317 and #357 moved to #320 and #363'),
    ('75.5-78', 'Hyper reveal and kill (Death Egg)', [('reveal', 96), ('kill', 185)], 't4-dez-w47', [('reveal', 96), ('kill', 182)], (75.5, 76, 1),
     'the wait after the transform press cut from 50 frames to 47 (46 misses the badnik)'),
    ('26-28', 'Casino Night bumpers', [('bumper', 196), ('bumper', 211), ('bumper', 261), ('bumper', 276)], 't3-cnz-j270', [('bumper', 196), ('bumper', 211), ('bumper', 261), ('bumper', 276)], None,
     'cannot be tuned: the leap comes after the bumpers, and the gaps between them (15, 50, 15 frames) are the game\'s physics. The window is placed for the smallest worst offset.'),
]


def tune_rows():
    out = []
    for bars, title, before, probe, after, anc, note in TUNES:
        b0 = float(bars.split('-')[0])
        f0 = bf(b0)
        if anc:
            _, bar, beat = anc
            def devs(ev):
                src0 = ev[0][1] - (bf(bar, beat) - f0)
                return src0, [near(f0 + s - src0) for _, s in ev]
            s0b, db = devs(before); s0a, da = devs(after)
        else:
            best = None
            for src0 in range(150, 200):
                d = [near(f0 + s - src0) for _, s in after]
                m = max(abs(x[2]) for x in d)
                if best is None or m < best[0]:
                    best = (m, src0, d)
            s0a, da = best[1], best[2]; s0b, db = s0a, da
        r = rows(probe)
        ok = all(any(abs(i - s) <= 0 and (num(r[i], 'score') - num(r[i - 1], 'score')) > 0 for i in range(s, s + 1)) or lab == 'reveal' for lab, s in after)
        out.append(dict(bars=bars, title=title, probe=probe, note=note, src0=s0a, verified_in_probe=ok,
                        before=[dict(event=l, src=s, bar=b, beat=k, dev=d) for (l, s), (b, k, d) in zip(before, db)],
                        after=[dict(event=l, src=s, bar=b, beat=k, dev=d) for (l, s), (b, k, d) in zip(after, da)]))
    return out


def main():
    head = subprocess.check_output(['git', 'log', '--oneline', '-1'], cwd=R, text=True).strip()
    jar = subprocess.check_output(['sha256sum', str(R / 'target/mica-and-talon/mica-and-talon.jar')], text=True).split()[0]
    # audio check
    hosts = [('positioned', 'rms-positioned', 'jump pressed #30', 31), ('powered', 'rms-powered', 'starpost at spawn, jumps #24 and #45', 1),
             ('declared (hero)', 'rms-declared', 'starpost at spawn, jump pressed #80', 81), ('starpost (half-pipe)', 'rms-starpost', 'starpost at spawn, jump pressed #150', 150),
             ('original, Continue', 'rms-continue', 'no sound effect on this screen', None), ('original, ending', 'rms-ending', 'no sound effect in these 7 s', None),
             ('GameplayCaptureTool', 'rms-tool', 'jump pressed #90 (Sonic 2)', 90)]
    arows, ajson = [], []
    for lab, pre, what, expect in hosts:
        s, m = audio(pre + '-sfx'), audio(pre + '-mus')
        ajson.append(dict(host=lab, sfx_only=s, music_control=m, event=what))
        verdict = 'SFX only' if s['silent_frames'] > 0 and m['silent_frames'] < m['frames'] * 0.2 and (s['mean_loud_db'] or -200) > -60 else \
                  'silent stem (music was the only sound)' if s['silent_frames'] == s['frames'] and m['mean_loud_db'] and m['mean_loud_db'] > -40 else 'CHECK'
        arows.append(f"<tr><td>{esc(lab)}</td><td class=r>{s['frames']}</td><td class=r>{s['silent_frames']}</td><td class=r>{s['mean_loud_db'] if s['mean_loud_db'] is not None else '-'}</td>"
                     f"<td class=r>{m['silent_frames']}</td><td class=r>{m['mean_loud_db']}</td><td>{esc(what)}</td><td>{verdict}</td></tr>")
    tp = audio('rms-toolpos-sfx')
    # re-stages
    rrows, rjson, png_cells = [], [], []
    for key, bars, title, status, probe, picks, (b0, anchors), what, script, limit in RESTAGE:
        src0, ev = place(b0, [(l, s, b, k) for l, s, b, k in anchors])
        n = bf(float(bars.split('-')[1])) - bf(b0)
        last = ev[-1]['src'] + 30 if key == 'R5' else src0 + n          # R5: she is under the card after the hit
        g, v, idle = speed(probe, src0, last, [e['src'] for e in ev])
        st = strip(probe, picks)
        evt = '; '.join(f"{e['event']} #{e['src']} on bar {e['bar']} beat {e['beat']}" + (f" ({e['dev']:+d} f)" if e['dev'] else '') for e in ev)
        rjson.append(dict(key=key, bars=bars, title=title, status=status, probe=probe, window=[src0, src0 + n], mean_gspeed=g, speed_px_f=v, idle_s=idle, events=ev, script=script))
        col = '#199e70' if status == 'confirmed' else '#c98500'
        rrows.append(f"<tr><td class=t rowspan=2><b>{key}</b><br>bars {bars}</td><td><b>{esc(title)}</b><br><span class=chip style='background:{col}'></span>{esc(status)}<br><br>{esc(what)}"
                     f"<div class=rs>{esc(limit)}</div></td><td><div class=dim>probe <code>{probe}</code>, window #{src0}-{src0 + n}<br>"
                     f"|gspeed| {g}, speed {v} px/f, slow and untouched {idle} s<br>{esc(evt)}<br>{esc(script)}</div></td></tr>"
                     f"<tr><td colspan=2><img src='{jpg(st)}' alt='{esc(title)}'></td></tr>")
        png_cells.append((key, bars, title, status, probe, picks, evt))
    # tunes
    tr, trows = tune_rows(), []
    for t in tr:
        fmt = lambda ev: '; '.join(f"{e['event']} bar {e['bar']} beat {e['beat']}" + (f" ({e['dev']:+d} f)" if e['dev'] else ' (0)') for e in ev)
        worst_b, worst_a = max(abs(e['dev']) for e in t['before']), max(abs(e['dev']) for e in t['after'])
        trows.append(f"<tr><td class=t>{t['bars']}</td><td><b>{esc(t['title'])}</b><br><span class=dim>{esc(t['note'])}</span></td><td>{esc(fmt(t['before']))}</td>"
                     f"<td>{esc(fmt(t['after']))}</td><td class=r>{worst_b} &rarr; {worst_a} f</td><td><code>{t['probe']}</code></td></tr>")
    # lockstep
    a, b = rows('w-ehz-pos-mod'), rows('w-ehz-pos-stock')
    cols = ['x', 'y', 'xvel', 'yvel', 'gspeed', 'air', 'rolling', 'cam_x', 'cam_y', 'sk_x', 'sk_y', 'rings']
    diff = sum(1 for i in range(min(len(a), len(b))) for c in cols if a[i][c] != b[i][c])
    json.dump(dict(build=dict(head=head, jar_sha256=jar), audio_check=ajson, tool_positioned_same_start=tp, restages=rjson, tunes=tr,
                   lockstep_positioned=dict(frames=len(a), columns=cols, differences=diff)), open(C / 'probes.json', 'w'), indent=1)

    doc = f'''<!doctype html><meta charset=utf-8><title>MICA &amp; TALON promo: stage B probes (checkpoint 5)</title>
<style>
body{{background:#0e1222;color:#e8ecf6;font:15px/1.5 system-ui,sans-serif;max-width:1500px;margin:0 auto;padding:28px}}
h1{{font-size:28px;margin:0 0 4px}}h2{{margin:40px 0 10px;font-size:22px;border-bottom:2px solid #2449db;padding-bottom:6px}}
table{{border-collapse:collapse;font-size:13.5px;width:100%}}td,th{{border:1px solid #2a3355;padding:6px 9px;vertical-align:top;text-align:left}}
th{{background:#18203d}}td.t{{white-space:nowrap}}td.r{{text-align:right;font-variant-numeric:tabular-nums}}
img{{display:block;border:1px solid #2a3355;max-width:100%;height:auto;image-rendering:pixelated;margin-bottom:6px}}
.box{{background:#151b33;border-left:4px solid #ffdc5a;padding:12px 16px;margin:12px 0}}.rs{{background:#2a1c14;border-left:3px solid #d95926;padding:5px 8px;margin-top:8px;font-size:12.5px}}
code{{background:#1b2342;padding:1px 4px;border-radius:3px;font-size:12px}}li{{margin:5px 0}}.dim{{color:#aab3cf;font-size:12.5px}}
.chip{{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:6px;vertical-align:-1px}}
</style>
<h1>MICA &amp; TALON promo: stage B probes</h1>
<p class=dim>Checkpoint 5. Probes only: no final captures. Every picture is a probe on the build below, which does not have the art branch yet,
so Hyper MICA's jade and TALON's flight frames are still the old art. All of these will be shot again as final takes.</p>

<div class=box><b>Summary</b><ul>
<li><b>Build:</b> <code>{esc(head)}</code> on local branch <code>feature/ai-mt-promo-redo</code> = integration <code>5af38c3ee5</code> + develop <code>4f885afbd6</code>
(one conflict, in <code>CHANGELOG.0.8.prerelease.md</code>; both entries kept). Not pushed. Example jar sha256 <code>{jar[:16]}</code>, unchanged from the delivered cut.</li>
<li><b>Capture hosts:</b> all five now record the SFX-only stem and all five pass the RMS check below, as does the stock tool.</li>
<li><b>Re-stages:</b> five confirmed (two with a noted limit or move), one confirmed in part (TALON's Sonic 2 shot has one Whisp kill, not two). None fell back.</li>
<li><b>Tunes:</b> Marble Garden, Sky Chase and the Hyper reveal now land within 1 frame of their beats. Casino Night's bumpers cannot be tuned; its worst offset is 4 frames.</li>
<li><b>Lockstep:</b> a positioned mid-act Emerald Hill pair (TIME 0:47, 28 rings) stays identical in {len(cols)} state columns over {len(a)} frames, so the split no longer needs an act start.</li>
</ul></div>

<h2>1. SFX-only audio check, every host</h2>
<p>Each host ran twice from the same inputs: once as it will capture (music volume 0) and once with the music left on. RMS is per video frame
(800 samples at 48 kHz); "silent" is digital silence. With the music on, almost no frame is silent; with it off, everything between the sound effects is.</p>
<table><tr><th>Host</th><th>Frames</th><th>Silent frames, SFX-only</th><th>RMS of the sounding frames (dBFS)</th><th>Silent frames, music on</th><th>RMS, music on</th><th>Sound effect in the take</th><th>Result</th></tr>
{''.join(arows)}</table>
<p>Audio length equals the frame count times 800 samples in every take. The positioned host and <code>GameplayCaptureTool --audio --no-music</code> from the same start put the first
sample of the jump sound at the same place (frame {tp['first_sound_frame']} for a press on #30), so the host is in step with the stock tool. The Continue screen and the ending have no sound
effects, so their stems are silent; the film will have only the music under those shots.</p>

<h2>2. The six re-stages</h2>
<table><tr><th>Shot</th><th>Result</th><th style="width:38%">Probe, measurements, script</th></tr>{''.join(rrows)}</table>

<h2>3. Beat offsets after the tunes</h2>
<p>Offsets are frames from the nearest tracked beat (+ is late; 1 frame is 17 ms).</p>
<table><tr><th>Bars</th><th>Take</th><th>Before</th><th>After</th><th>Worst offset</th><th>Probe</th></tr>{''.join(trows)}</table>

<h2>4. Changes to the approved plan</h2>
<ul>
<li><b>Pair location:</b> the lower bridge instead of the starpost deck, and the catch on beat 4 of bar 80 instead of bar 81.</li>
<li><b>TALON in Sonic 2:</b> one Whisp kill, on bar 35.</li>
<li><b>Launch Base duo:</b> top speed for the second bar only; the spring moves from beat 3 to beat 4 of bar 3 so the shot ends before the upper-deck machine appears.</li>
<li><b>Boss:</b> the ONE HIT. card edge moves about 8 px left. The boss now sits mid-frame, clear of the HUD.</li>
<li><b>No shot needed a third bar.</b> The longest re-stage is the Solar reveal at 2.5 bars, as planned. I will look again at both cuts once the final takes are in, the 9:16 especially.</li>
</ul>

<h2>5. Not done yet</h2>
<ul><li>No final capture. Waiting for the art branch SHA, as instructed.</li>
<li><code>edit/edit.py</code>, <code>out/</code> and the media archive are unchanged.</li>
<li>Stale skill line, not fixed: <code>promo-direction/SKILL.md:259</code> on develop still says there is no SFX-only stem.</li></ul>
'''
    (C / 'probes.html').write_text(doc)
    print(C / 'probes.html', f'{len(doc) / 1e6:.2f} MB')

    # ---- PNG version
    INK, DIM, BG = (240, 239, 236), (195, 194, 183), (14, 18, 34)
    for tw, colours in ((150, 96), (132, 72), (116, 48)):
        th = round(tw * 224 / 320)
        W = 1560
        H = 70 + len(png_cells) * (th + 64) + 40 + (len(tr) + 1) * 40 + 30
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.text((20, 14), 'MICA & TALON promo: stage B probes (checkpoint 5)', font=F22B, fill=INK)
        d.text((20, 44), 'Probes on integration + develop, old art. Five re-stages confirmed, one in part; five hosts and the tool pass the SFX-only RMS check.', font=F13, fill=DIM)
        y = 70
        for key, bars, title, status, probe, picks, evt in png_cells:
            d.text((20, y), f'{key}  bars {bars}  {title}', font=F13B, fill=INK)
            d.text((20, y + 16), status + '.  ' + evt, font=F13, fill=DIM)
            use = picks[:10]
            for k, i in enumerate(use):
                f_, real = frame(probe, i)
                im.paste(f_.resize((tw, th), Image.BOX), (20 + k * (tw + 3), y + 36))
            y += th + 64
        d.text((20, y), 'Beat offsets after the tunes (frames from the nearest beat)', font=F13B, fill=INK); y += 22
        for t in tr:
            fmt = lambda ev: ', '.join(f"{e['event']} {e['dev']:+d}" for e in ev)
            d.text((20, y), f"bars {t['bars']}  {t['title']}", font=F13B, fill=INK)
            d.text((330, y), f"before: {fmt(t['before'])}    after: {fmt(t['after'])}", font=F13, fill=DIM)
            d.text((330, y + 16), t['note'][:150], font=F13, fill=DIM); y += 40
        q = im.quantize(colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        buf = io.BytesIO(); q.save(buf, 'PNG', optimize=True)
        if buf.tell() < 512 * 1024:
            break
    (C / 'probes.png').write_bytes(buf.getvalue())
    print(C / 'probes.png', im.size, f'{buf.tell() / 1024:.0f} KB')
    for r in rjson:
        print(r['key'], r['bars'], r['status'], '| window', r['window'], 'g', r['mean_gspeed'], 'v', r['speed_px_f'], 'idle', r['idle_s'], '|', [(e['event'], e['bar'], e['beat'], e['dev']) for e in r['events']])
    for t in tr:
        print(t['bars'], t['title'], 'src0', t['src0'], [(e['event'], e['dev']) for e in t['before']], '->', [(e['event'], e['dev']) for e in t['after']])


if __name__ == '__main__':
    main()
