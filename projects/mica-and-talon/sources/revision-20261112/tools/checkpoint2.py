#!/usr/bin/env python3
"""Purpose: build checkpoint 2 (draft) as ONE self-contained HTML file: the draft video re-encoded to 640 px
CRF 30 and embedded as base64, the lead's five fixes with frames from the encoded draft, the viewer-pass table,
promo_kit.py check, loudness measured on the encoded AAC, the stinger table and the honesty notes.
Inputs: checkpoint2/draft-16x9.mp4 (+ .loudness.json, stingers.json, sectional-loudness.json, fade-tail.json,
promo_kit-check.txt, overrun.json), edit/edit.py. Origin: MICA & TALON promo redo 2026-11-12."""
import base64, html, io, json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

T = Path(__file__).resolve().parent.parent
C = T / 'checkpoint2'
DRAFT = C / 'draft-16x9.mp4'
BT = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]


def bt(n):
    k = int(n)
    return BT[k] + (BT[k + 1] - BT[k]) * (n - k)


def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def jpg(im, q=86):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return b64(buf.getvalue(), 'image/jpeg')


def grab(t, w=640):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(DRAFT), '-frames:v', '1', '-vf', f'scale={w}:-2:flags=lanczos',
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


small = C / 'draft-640.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(DRAFT), '-vf', 'scale=640:360:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow',
                '-crf', '30', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(small)], check=True)
loud = json.load(open(C / 'draft-16x9.loudness.json'))
sect = json.load(open(C / 'sectional-loudness.json'))
sting = json.load(open(C / 'stingers.json'))
tail = json.load(open(C / 'fade-tail.json'))
over = json.load(open(C / 'overrun.json'))
check = (C / 'promo_kit-check.txt').read_text().strip()
freeze = (C / 'freeze.txt').read_text().strip()
probe = loud['ffprobe']
v = next(s for s in probe['streams'] if s['codec_name'] == 'h264')
a = next(s for s in probe['streams'] if s['codec_name'] == 'aac')
esc = html.escape

VIEW = [
    ('0-4', 'Black for 0.55 s, then MICA\'s smear frames and the game\'s white flash (1.0 s); the Sonic 3 logo drops with MICA wagging a finger, wink at 2.8 s. Cut at 3.0 s: Launch Base, MICA and TALON running side by side; name tags pop a beat apart.',
     'A familiar intro with an unfamiliar hero, then both heroes named in play inside four seconds.', ''),
    ('4-8', 'The tags ride with them to 5.75 s. Angel Island: TALON drops to MICA, ROM grab sound on the catch (6.2 s), they lift off; the promise line rises at 7.1 s.',
     'Second hero, first ability; the promise is said once.', ''),
    ('8-12', 'The carry climbs out of the canopy to open sky and sea. 11.3 s: Death Egg, Hyper MICA in the air with banded after-images.',
     'A height reveal, then a flash of the climax on the riser.', ''),
    ('12-16', 'Hyper strike and explosion on bar 9 (12.7 s). 14.1 s: the Sonic 2 emblem on black; MICA rises, then TALON. The emblem is still from 15.9 s.',
     'The fragment pays off with a kill; a second game appears; one second of stillness before the drop.', 'weak'),
    ('16-20', 'The title\'s own white flash ON the drop (16.9 s) with Big Ring; sky and island appear; the card band slides in; MICA, &, TALON pop a beat apart; a gold glint sweeps the names on bar 14 (19.7 s).',
     'The title lands on the track\'s first big downbeat.', ''),
    ('20-24', 'The title holds under the lock-up to 22.5 s; banded wipe; header MICA / HOMING STRIKE; Marble Garden: reticle locks, strikes one and two (23.6, 23.8 s) with the counter.',
     'Reading time for the name, then her signature move.', 'weak'),
    ('24-28', 'Third strike, "3 CHAIN" (24.2 s). 25.3 s: triptych. Sonic 1 slice drops and chains two Buzz Bombers; Sonic 2 slice (26.0), Whisp strike; Sonic 3 & K slice (26.7), Rhinobot strike.',
     'Three hits counted, then the same move in three games on one screen.', ''),
    ('28-32', 'The three slices play on (Sonic 1 chains a second pair). 30.8 s: Sky Chase. MICA leaps from the Tornado\'s wing and strikes a Balkiry (31.1 s).',
     'A new place: open sky, a biplane, and a pilot who is not Tails.', ''),
    ('32-36', 'Strike two ON bar 23 (32.2 s), the chained 200 at 32.8 s with CHAIN x2; she lands back on the wing; callout TALON FLIES THE TORNADO (34.3 s).',
     'A real Sonic 2 chain, and the partner shown at the stick.', ''),
    ('36-40', '36.4 s: Casino Night. Neon skyline, both heroes run and leap off the ledge, TALON following her down. 39.2 s: banded wipe to Spring Yard, header TALON.',
     'Third palette in ten seconds; the pair together in Sonic 2; chapter turn on the break.', ''),
    ('40-44', 'TALON flies between the columns; reticle; two divebomb kills on the beat (40.9, 41.6 s; native 100 then 200); 42.0 s IN SONIC 1, TOO and the lives inset reading TALON; he lands and runs the ramp.',
     'A flyer in a game that never had one, with terrain around him and his name on the HUD.', ''),
    ('44-48', '44.8 s: triptych FLIGHT / CARRY / DIVEBOMB, a slice every two beats; divebomb kill at 46.8 s.',
     'His three verbs side by side: one consistent character.', ''),
    ('48-52', 'The slices play on (the carry climbs; he flies back over the clearing). 50.35 s: banded wipe ON the B drop to the lockstep split, header EVERY SCREEN / REDRAWN; Sonic & Tails and MICA & TALON jump as one.',
     'The biggest claim arrives on the drop: the same game, with different heroes.', ''),
    ('52-56', 'Roll, skid, look up, duck, spindash, both halves in step; the line SAME INPUTS. SAME PHYSICS. EVERY FRAME. lands at 53.1 s. 55.9 s: push to the titles.',
     'The eye checks left against right: every pose is redrawn and nothing drifts.', ''),
    ('56-60', 'Three title screens drop two beats apart: Sonic 1 (MICA pops up and wags), Sonic 2 (both heroes), Sonic 3 & K (the wink).',
     'Three art styles, one cast.', ''),
    ('60-64', 'Titles hold to 61.5 s. Signposts: Sonic 1 pops in, Sonic 2 a beat later; both spin to MICA; Sonic 1 signpost sound as she passes it.',
     'Same moment, two games.', ''),
    ('64-68', '64.3 s: Sonic 2 full screen. MICA GOT THROUGH ACT 1 flies in, bonuses, tally. 67.1 s: push to the special stages.',
     'The game\'s own lettering says her name.', ''),
    ('68-72', 'Three special stages, a slice every two beats: the Sonic 1 maze turning, the Sonic 2 half-pipe with TALON behind her, Sonic 3 & K Blue Sphere with jumps.',
     'Three very different stages, each posed in its own style.', ''),
    ('72-76', '72.7 s: 2x2 grid, a cell a beat: Continue countdown, Data Select portraits, special-stage HUD names, lives TALON x 3.',
     'Breadth at a glance, every cell moving.', ''),
    ('76-80', 'The grid runs to 78.3 s (countdown ticking). Sonic 2 ending: MICA flies beside the Tornado with TALON piloting.',
     'A new kind of screen: the ending.', 'weak'),
    ('80-84', '80.4 s: the front-view pose; MICA lands on the wing; ENDINGS, TOO. 83.25 s: Hydrocity. MICA jumps and winds up, white silhouette, ROM transform sound; she snaps open gold ON bar 60 (83.94 s).',
     'The ending\'s big drawing, then the turn into the climax exactly on the chorus.', ''),
    ('84-88', 'Ring of glints; header POWERED UP / 50 RINGS MID-ACT; Gilded MICA runs and rolls the Hydrocity curve shedding glints; GILDED MICA pill at 86.8 s.',
     'The first powered form, full screen, bright gold.', ''),
    ('88-92', 'Gilded run to 89.6 s. Stacked pair on the same Rhinobot: normal strike with its jade trail (90.2 s), Gilded strike with its gold trail a bar later (91.6 s).',
     'A comparison the viewer can read in one look: jade above, gold below.', ''),
    ('92-96', 'The pair plays on to 94.5 s. Carnival Night: TALON winds up (transform sound); the flame-lit reveal ON bar 68 (95.16 s) with a flare ring.',
     'The partner gets his own transformation, on its own downbeat.', ''),
    ('96-100', 'Solar TALON lifts off and crosses the carnival night, embers streaming from each flap; SOLAR TALON pill.',
     'Flight with a trail of fire over a dark sky.', ''),
    ('100-104', '100.8 s: triptych, a slice every two beats: Gilded MICA transforms in Sonic 1, Solar TALON transforms in Sonic 2, Solar TALON divebombs a Rhinobot in Sonic 3 & K (102.9 s).',
     'Powered forms in all three games, a Super form in Sonic 1 included.', ''),
    ('104-108', 'Triptych to 105.7 s. Death Egg: Hyper wind-up; the reveal ON bar 76 (106.42 s) with flash; Prism Gilt colours cycling; HYPER MICA pill; an Instagib kill at 107.9 s.',
     'The third tier lands on the lift; the after-images are new on screen.', ''),
    ('108-112', 'After-image dash to 109.2 s. Launch Base arena: the mini-boss swings in overhead; she hops; THE hit ON bar 79 (110.65 s): flash, boss-hit and explosion sounds; ONE HIT. slams; the machine flies apart; she lands.',
     'The hero moment.', ''),
    ('112-116', 'Cut ON bar 80 (112.06 s): the signpost drops in (112.4 s), lands and spins to MICA (113.7 s); MICA GOT THROUGH ACT 1 is complete ON bar 82 (114.89 s); bonuses follow.',
     'The consequence: the act is won, in the game\'s own words.', ''),
    ('116-120', 'Bonus tally under the track\'s loudest bars. 117.7 s: gold iris and Big Ring into the end card: fire ground, band, MICA & TALON, line, URL.',
     'Resolution, then where to get it.', ''),
    ('120-124', 'Disclaimer; the music is at -6 dB by 121.3 s; the picture fades to black across bar 87; black from 123.3 s.',
     'A clean end with the fade.', ''),
]
view_rows = ''.join(f"<tr class='{c}'><td class=t>{esc(t)}</td><td>{esc(n)}</td><td>{esc(w)}</td></tr>" for t, n, w, c in VIEW)

SHOTS = {x['id']: x for f in sorted((T / 'shots').glob('batch*.json')) for x in json.load(open(f))}
SCORES = [('Launch Base 1 (cold open)', 'd-lbz1-team'), ('Angel Island 1, the carry', 'd-carry-fly'), ('Death Egg 1, Hyper', 'd-dez1-hyper'),
          ('Marble Garden 2 chain', 'd-mgz2-chain'), ('Casino Night 1 (Sonic 2)', 'd-cnz2-team'), ('Spring Yard 1 (Sonic 1), TALON', 'd-syz1-talon'),
          ('Green Hill 1 signpost', 'd-ghz-clear'), ('Emerald Hill 1 signpost and results', 'd-ehz-clear'), ('Hydrocity 1, Gilded', 'd-hcz1-gilded'),
          ('Carnival Night 1, Solar', 'd-cnz1-solar'), ('Launch Base 1 mini-boss, Hyper', 'd-lbz-boss')]


def srow(label, cid):
    pr = SHOTS[cid]['props']
    tf = int(pr['promo.timer'])
    return (f"<tr><td>{esc(label)}</td><td>{tf // 3600}:{tf // 60 % 60:02d}</td><td>{pr['promo.rings']}</td>"
            f"<td>{int(pr['promo.score']):,}</td><td><code>{cid}</code></td></tr>")


score_rows = ''.join(srow(l, c) for l, c in SCORES)
sect_rows = ''.join(f"<tr><td>{esc(s['section'])}</td><td>{s['t0']:.2f}&ndash;{s['t1']:.2f}</td><td>{s['lufs']:.1f}</td><td>{s['true_peak']:.1f}</td></tr>" for s in sect)
NAMES = {'s3k-sfx-4a': 'S3K Grab', 's3k-sfx-b4': 'S3K Explode', 's3k-sfx-b3': 'S3K Big Ring', 's3k-sfx-9f': 'S3K Super Transform', 's3k-sfx-6e': 'S3K Boss Hit',
         's1-sfx-c1': 'S1 badnik pop', 's2-sfx-c1': 'S2 Explosion', 's1-sfx-cf': 'S1 Signpost'}
sting_rows = ''.join(f"<tr><td>{s['frame']}</td><td>{s['t']:.2f}</td><td>{NAMES.get(s['sfx'], s['sfx'])} (<code>{s['sfx']}</code>)</td><td>{s['gain']}</td>"
                     f"<td>{s['under_bed_db']:+.1f}</td><td>{s['l_minus_r_db']:+.1f}</td></tr>" for s in sting)
fix1 = strip([(0.30, '0.30 s: black while the logo would be on screen'), (0.57, '0.57 s: first roll-in frame (source frame 267)'), (2.80, '2.80 s: the wink')])
fix2 = strip([(4.2, 'Launch Base 1 (declared 268,400)'), (86.0, 'Hydrocity 1 (declared 41,900)'), (97.5, 'Carnival Night 1 (declared 124,500)'),
              (107.2, 'Death Egg 1 (declared 512,600)'), (40.3, 'Spring Yard 1 (declared 58,200)'), (37.0, 'Casino Night 1 (declared 31,700)')])
fix3 = strip([(40.3, 'take-off between the columns'), (bt(29) + 0.40, 'first divebomb kill, on beat 2 of bar 29'), (42.6, 'IN SONIC 1, TOO + lives inset')])
fix4 = strip([(bt(79) - 0.20, 'mid-hop, 0.20 s before the hit'), (bt(79) - 0.05, '0.05 s before: the strike, jade with banded after-images'), (bt(79) + 0.45, 'ONE HIT.; the machine in pieces'),
              (bt(81) + 0.35, 'signpost spinning to MICA'), (bt(82) + 0.1, 'MICA GOT THROUGH ACT 1, complete on bar 82'), (bt(83) + 0.7, 'bonuses under the peak bars')])
fix5 = strip([(118.6, 'end card arriving'), (120.5, 'settled'), (122.6, 'fading with the music')])
import numpy as np  # noqa: E402


def contrast():
    a_ = np.asarray(grab(120.5, 1920)).astype(float) / 255
    c_ = np.where(a_ <= 0.03928, a_ / 12.92, ((a_ + 0.055) / 1.055) ** 2.4)
    L = 0.2126 * c_[..., 0] + 0.7152 * c_[..., 1] + 0.0722 * c_[..., 2]
    out = []
    for (y0, y1, x0, x1), fill in (((608, 676, 560, 1360), 1.0), ((700, 772, 640, 1280), 0.9278), ((962, 1004, 420, 1500), 1.0)):
        g = float(np.median(np.r_[L[y0 - 14:y0 - 4, x0:x1].ravel(), L[y1 + 4:y1 + 14, x0:x1].ravel()]))
        out.append((max(g, fill) + 0.05) / (min(g, fill) + 0.05))
    return out


CON = contrast()
STEP = max(abs(sect[i + 1]['lufs'] - sect[i]['lufs']) for i in range(len(sect) - 1))
UB = (min(x['under_bed_db'] for x in sting), max(x['under_bed_db'] for x in sting), max(abs(x['l_minus_r_db']) for x in sting))
NCH = int(subprocess.run(['ffprobe', '-v', 'error', '-show_chapters', '-of', 'json', str(DRAFT)], capture_output=True, text=True).stdout.count('"start_time"'))

doc = f"""<!doctype html><html lang=en><meta charset=utf-8><title>MICA &amp; TALON promo redo: draft checkpoint</title>
<style>
body{{background:#0e1222;color:#e8ecf6;font:16px/1.5 system-ui,sans-serif;max-width:1500px;margin:0 auto;padding:28px}}
h1{{font-size:30px;margin:0 0 4px}}h2{{margin:44px 0 10px;font-size:23px;border-bottom:2px solid #2449db;padding-bottom:6px}}
h3{{margin:22px 0 6px;font-size:18px;color:#ffdc5a}}
table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{border:1px solid #2a3355;padding:6px 8px;vertical-align:top;text-align:left}}
th{{background:#18203d}}td.t{{white-space:nowrap;color:#ffdc5a;font-variant-numeric:tabular-nums}}tr.weak td{{background:#2a1d1d}}
img,video{{max-width:100%;display:block;border:1px solid #2a3355}}figure{{margin:14px 0}}
.box{{background:#151b33;border-left:4px solid #ffdc5a;padding:12px 16px;margin:12px 0}}.warn{{border-left-color:#ff7a7a}}
code{{background:#1b2342;padding:1px 5px;border-radius:3px;font-size:13px}}li{{margin:5px 0}}.dim{{color:#aab3cf}}pre{{background:#151b33;padding:12px;overflow:auto;font-size:13px}}
</style>
<h1>MICA &amp; TALON promo redo: draft (checkpoint 2)</h1>
<p class=dim>Branch <code>feature/ai-mt-promo-redo</code> at <code>1e0faac123</code>, no repository changes. Full-size draft:
<code>~/scratch/agent-tmp/mt-promo-redo-20261111/checkpoint2/draft-16x9.mp4</code> ({float(probe['format']['duration']):.2f} s, {v['width']}&times;{v['height']}, {v['avg_frame_rate']} fps, H.264 {v['profile']}, {v['pix_fmt']}, AAC {int(a['bit_rate']) // 1000}k, {NCH} chapters, full decode exit {loud['full_decode_exit']}).
Edit: <code>edit/edit.py</code>. The vertical cut, archive and README come after this review.</p>

<h2>1. The draft</h2>
<video controls preload=metadata src="{b64(small.read_bytes(), 'video/mp4')}"></video>
<p class=dim>640&times;360, CRF 30, AAC 128k copy of the draft for review. Judge sharpness and loudness on the full-size file.</p>

<div class="box warn"><b>Three things changed that you did not ask for. Please check them.</b>
<ol>
<li><b>The boss is now Launch Base 1's mini-boss, not the Angel Island machine.</b> While fixing "ONE HIT" I ran the same inputs with Gilded MICA as a control. The Angel Island machine fire-bombs the jungle whether or not it is struck, and it never blows apart: struck by Hyper it only turns white and scores 1,000. My storyboard line "it blows apart and the jungle catches fire" credited the fire to her hit. That was wrong. The Launch Base mini-boss is a real fight: one Instagib strike breaks it apart (score 283,900 to 284,900), then the signpost drops, spins to MICA and the game writes "MICA GOT THROUGH ACT 1". That results card now sits on the track's loudest bars. Hit still on bar 79, end card still on bar 84. The earlier cut is kept as <code>edit/edit-aiz-boss-version.py</code>.</li>
<li><b>The end card's fire is now only a backdrop.</b> It is the Angel Island fire in soft focus, lifted as you asked, but it no longer follows from the last shot. If you would rather it grow out of the Launch Base results (purple wall, yellow floor), say so.</li>
<li><b>I applied "no SEGA mark" to the whole film, not only the opening.</b> The Sonic 2 title is framed on rows 26&ndash;206, which drops its "&copy; 1992 SEGA" row whole; the Sonic 1 title slice is framed on rows 0&ndash;147, which drops the emblem's SEGA plate; the labels of that triptych moved to the top. Say if that over-reads your note.</li>
</ol></div>

<h2>2. Your five fixes</h2>
<h3>Fix 1. No SEGA logo</h3>
<p>The film opens on black for 0.55 s (33 frames), the time the logo is on screen, then the roll-in plays as it ships from its first frame without the logo. The in-point did not move, so nothing inside the roll-in is cut and the flash (1.03 s) and wink (2.8 s) are where they were.</p>
<img src="{jpg(fix1)}">
<h3>Fix 2. SCORE 0 on mid-act starts</h3>
<p><code>GameplayCaptureTool</code> has flags for rings, timer and emeralds but none for score. I wrote a small capture host (<code>hosts/positioned/PromoCapture.java</code>, outside the repository) that mirrors the tool's loop and declares the score after boot through <code>GameStateManager.addScore</code>, the public call gameplay itself uses. The HUD draws it natively; nothing is painted. Each value is in the capture's <code>provenance.json</code> (<code>promo.score</code>) and the score column of its <code>state.csv</code>. Each take re-shot only to add a score was compared with its earlier capture on every frame: positions identical.</p>
<table><tr><th>Shot</th><th>Declared time</th><th>Declared rings</th><th>Declared score</th><th>Capture</th></tr>{score_rows}</table>
<p class=dim>Every shot that shows a HUD now carries a declared score, with one exception that is real: Sky Chase starts at the act's own start, so its score honestly runs 0, 100, 200, 400. Split panes and strips crop the HUD out whole.</p>
<img src="{jpg(fix2)}">
<h3>Fix 3. TALON's first full shot</h3>
<p>Moved from Star Light to Spring Yard 1 (still Sonic 1, lives reading TALON). He takes off between the columns, locks on and divebombs two Crabmeats on beats 2 and 4 of bar 29 (native 100 then 200), lands and runs the quarter pipe. Terrain is in frame throughout.</p>
<img src="{jpg(fix3)}">
<h3>Fix 4. ONE HIT</h3>
<p>See the note above on the change of boss. She stands right of centre; the machine swings in from the left overhead; she hops and starts her strike about 45 px to its right, so the whole strike is drawn on open wall, in her jade strike colours with the banded after-images. "ONE HIT." sits on native rows 68&ndash;100, columns 16&ndash;119: under the HUD, left of the machine and of her. One cut inside the take, on bar 80, skips 2.3 s of her standing after the kill.</p>
<img src="{jpg(fix4)}">
<h3>Fix 5. End card background</h3>
<p>Fire in soft focus at 86 % brightness with a vignette that only darkens toward the corners and the small type. Text gets a navy outline and hard shadow. Measured on the encoded draft at 120.5 s, text fill against the ground just above and below it: line {CON[0]:.1f}:1, URL {CON[1]:.1f}:1, disclaimer {CON[2]:.1f}:1.</p>
<img src="{jpg(fix5)}">

<h2>3. Viewer pass, one row per 4 s</h2>
<p class=dim>Written from the encoded draft: frames every 2 s, plus single frames at each event. Not a listening pass. Rows I rate weakest are tinted.</p>
<table><tr><th>Time (s)</th><th>New on screen</th><th>Why a viewer keeps watching</th></tr>{view_rows}</table>
<ul>
<li><b>12&ndash;16:</b> the Sonic 2 emblem is completely still from 15.88 to 16.90 s. That is the title as it ships (both heroes risen, waiting for its flash). Moving the in-point would cut into a rise.</li>
<li><b>20&ndash;24:</b> the lock-up holds 4.5 s over a nearly static title. I added a gold glint across the names on bar 14. Shortening it would pull the MICA chapter off bar 16.</li>
<li><b>76&ndash;80:</b> the grid's second half and a plain blue ending sky. The pose and "ENDINGS, TOO" arrive at 80.4 s.</li>
</ul>

<h2>4. <code>promo_kit.py check</code></h2>
<pre>{esc(check)}</pre>
<p>No warnings (stinger balance, one-sided stingers, cut density, captions). The kit's bare-stretch and overrun tests only see <code>Game</code> shots and this edit is built from <code>Custom</code> shots, so I checked those two separately:</p>
<ul>
<li><b>Sources outlived:</b> <code>tools/overrun_audit.py</code> rendered {over['sampled_frames']} frames (every {over['step']}nd) with the frame loader instrumented. Requests past the end of a capture: <b>{len(over['overruns'])}</b>{'' if not over['overruns'] else ' ' + esc(json.dumps(over['overruns']))}. An earlier draft froze three split panes for a second this way; those captures were re-shot longer.</li>
<li><b>Frozen or black picture</b> (<code>freezedetect</code> at &minus;60 dB for 0.5 s, <code>blackdetect</code>) on the encoded draft:<pre>{esc(freeze)}</pre>That is the opening black (fix 1), the native Sonic 2 title hold before its flash, and the closing fade.</li>
</ul>

<h2>5. Loudness, measured on the encoded AAC</h2>
<p><b>Whole film: {loud['integrated_lufs']:.1f} LUFS integrated, true peak {loud['true_peak_dbtp']:.1f} dBTP, loudness range {loud['lra_lu']:.1f} LU</b> (<code>ffmpeg ebur128=peak=true</code> on <code>draft-16x9.mp4</code>; two-pass linear loudnorm, no limiter and no extra gain needed).</p>
<table><tr><th>Section</th><th>Seconds</th><th>LUFS</th><th>True peak, dBTP</th></tr>{sect_rows}</table>
<p class=dim>Largest step between neighbouring sections: {STEP:.1f} LU. Sections are measured on seeked segments, so a section's peak can read 0.1 dB off the whole-file figure.</p>
<p><b>The fade</b>, RMS of the encoded file per half second from {tail['start']} s: {', '.join(f'{x:.1f}' for x in tail['rms_dbfs'])} dBFS. Full level to 119.1 s, &minus;6 dB at 121.3 s, silent by 123.5 s.</p>
<h3>Stingers</h3>
<p class=dim>Loudest 100 ms of each ROM sound (rendered <code>--paced</code>) against the music under it. Positive = under the music. Range {UB[0]:+.1f} to {UB[1]:+.1f} dB; largest left/right difference {UB[2]:.1f} dB. Each sits on the frame of its event in the capture's <code>state.csv</code> (score change, catch frame, transformation press, signpost pass); the two Big Rings punctuate graphics.</p>
<table><tr><th>Output frame</th><th>Time (s)</th><th>Sound</th><th>Gain</th><th>dB under the bed</th><th>L&minus;R dB</th></tr>{sting_rows}</table>
<p><b>Sound was checked by measurement only. I cannot hear the film.</b></p>

<h2>6. Other changes since the storyboard</h2>
<ul>
<li><b>MICA's chapter.</b> In the Marble Garden take she is hit and loses her rings one second after the third strike. The storyboard had that on screen. The take now ends before it (two bars), and the freed two bars are a new partners shot in Sonic 2's Casino Night.</li>
<li><b>Solar pane in the powered triptych.</b> The storyboard called it a "divebomb kill"; the event in that clip was a landing. It is re-shot as a real one (dive pressed frame 176, Rhinobot struck frame 186, score +100).</li>
<li><b>Sky Chase stingers</b> moved to the score-change frames (255, 324, 358); two were 2&ndash;3 frames late.</li>
<li><b>Blue Sphere pane.</b> The old take showed its "GET BLUE SPHERES" banner cropped, then whited out mid-pane when the stage ended. New take: jumps, no banner, stage still running.</li>
<li><b>Split panes and the HUD.</b> With five- and six-digit scores the HUD's digits reached into some slices. Panes now ease sideways while HUD rows are in view, so the HUD is out of every slice whole and a rising subject is not cut by the top edge.</li>
<li><b>Triptychs</b> drop a slice every two beats instead of every bar, so less time shows empty stripes.</li>
<li><b>Lock-up on the title</b> is part of the title shot, so the chapter wipe carries it away and the native menu row under it is never uncovered.</li>
<li><b>Name tags</b> in the cold open never sit on the HUD or on each other.</li>
</ul>

<h2>7. Not filmed, and not as it ships</h2>
<ul>
<li><b>Positioned starts with declared score, rings and timer</b> throughout; never continuous cold routes. Sky Chase and the Chemical Plant lockstep start at the act's own start; the titles are cold title-first boots.</li>
<li><b>One cut inside a take:</b> the Launch Base boss shot skips source frames 733&ndash;871 (2.3 s of MICA standing).</li>
<li><b>Hyper MICA at the boss transforms off camera</b> (frames 51&ndash;96 of that capture); her transformation is shown in Death Egg.</li>
<li><b>Competition: not filmed</b> (<code>Native arena has no published VInt registers</code> again). <b>Slot reels: not attempted.</b></li>
<li><b>Sonic 1 results card</b> still draws its act oval over the text for stock Sonic too; Sonic 1 is shown to the signpost.</li>
<li><b>Stock art avoided by timing or crop:</b> the S3K title's small Tornado fly-by, the Data Select "No Save" tile.</li>
<li><b>Debug component entries</b>, as before: the Sonic 2 half-pipe, Continue and the Sonic 2 ending. The Sonic 1 special stage is entered through the real giant ring.</li>
<li><b>Mushroom Hill's mini-boss</b> also dies to one strike, but that act draws a white rectangle on screen in this build (engine art gap, not the mod), so I did not use it.</li>
</ul>
<p class=dim>After your reply: fixes, final 16:9 render, the designed 9:16 cut, chapters, README, contact sheets and the local OpenGGF-Media archive.</p>
</html>"""
out = C / 'draft-review.html'
out.write_text(doc)
print(out, f'{out.stat().st_size / 1e6:.1f} MB', 'video', f'{small.stat().st_size / 1e6:.1f} MB')
