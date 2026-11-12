#!/usr/bin/env python3
"""Purpose: the final vertical review as ONE self-contained HTML file: the 9:16 master at 540 px tall, CRF 30
(base64), a contact sheet of the encoded file, the framing of every shot, and stills at the framing cuts.
Inputs: out/master-9x16.mp4 (+ .loudness.json), out/master-16x9.loudness.json, out/contact-9x16-2s.jpg.
Output: final/vertical-review.html. Origin: MICA & TALON promo redo 2026-11-12."""
import base64, html, io, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

T = Path(__file__).resolve().parent.parent
OUT = T / 'final'
OUT.mkdir(exist_ok=True)
FILM = T / 'out/master-9x16.mp4'
esc = html.escape
F = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 15)


def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def jpg(im, q=86):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return b64(buf.getvalue(), 'image/jpeg')


def grab(t, h=640):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(FILM), '-frames:v', '1', '-vf',
                        f'scale=-2:{h}:flags=lanczos', '-f', 'image2pipe', '-c:v', 'png', '-'], capture_output=True, check=True)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB')


def strip(ts, h=640):
    ims = [grab(t, h) for t in ts]
    w = ims[0].width
    s = Image.new('RGB', (len(ims) * (w + 6) - 6, h + 22), (14, 18, 34))
    d = ImageDraw.Draw(s)
    for k, (t, im) in enumerate(zip(ts, ims)):
        s.paste(im, (k * (w + 6), 0))
        d.text((k * (w + 6) + 4, h + 2), f'{t:.2f} s', font=F, fill=(255, 220, 90))
    return jpg(s)


small = OUT / 'master-9x16-540.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(FILM), '-vf', 'scale=-2:540:flags=lanczos', '-c:v', 'libx264',
                '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-preset', 'slow', '-crf', '30', '-c:a', 'aac', '-b:a', '128k',
                '-movflags', '+faststart', str(small)], check=True)
probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,width,height:format=duration,size',
                                   '-of', 'json', str(small)], capture_output=True, text=True, check=True).stdout)
vs = next(s for s in probe['streams'] if s['codec_name'] == 'h264')
LV = json.load(open(T / 'out/master-9x16.loudness.json'))
LH = json.load(open(T / 'out/master-16x9.loudness.json'))

ROWS = [
    ('0.0-3.0', 'S3K roll-in, whole width', 'Black, then the smear frames in a full-height centre window; from the flash the whole title screen (columns 28-292, rows 0-188 at 4.09x) on its own sky, logo whole. No move.'),
    ('3.0-5.75', 'Launch Base, both heroes, full frame', 'Two bands, one hero each at the same size, tags above them. At 5.05 s (beat 3 of bar 3) TALON takes off and the picture cuts to the tall frame for his flight over MICA. <b>Changed since the last render</b>: before, he flew out of the top of his band and his tag hung over empty air.'),
    ('5.75-11.3', 'The carry, full frame', 'A closer two-shot until the catch (6.2 s), then the tall frame for the climb; the promise line on two lines.'),
    ('11.3-14.1', 'Hyper fragment', 'Tall frame following her, kept 22 px inside both edges.'),
    ('14.1-22.5', 'Sonic 2 title + lock-up band', 'The whole title on its own ground at the top; the card as a tall block from the "1 PLAYER" row down, lock-up stacked MICA / & TALON.'),
    ('22.5-25.25', 'Marble Garden chain', 'Tall frame; header as a vertical card.'),
    ('25.25-30.8', 'Strike triptych (slanted slices)', 'Three stacked bands, each never left of x 111 so the HUD is out whole.'),
    ('30.8-36.4', 'Sky Chase', 'Tall frame on MICA and the wing; CHAIN x2 at the top, pilot callout at the bottom.'),
    ('36.4-39.2', 'Casino Night pair', 'Tall frame.'),
    ('39.2-44.8', 'TALON in Spring Yard + lives inset', 'Tall frame; the lives display, which the tall frame drops, comes back whole as an inset.'),
    ('44.8-50.35', 'TALON verbs triptych', 'Three stacked bands.'),
    ('50.35-55.9', 'Lockstep split, left and right', 'Two stacked bands, stock above, MICA & TALON below, the same window in both (rows 52-224, never left of x 64).'),
    ('55.9-61.5', 'Titles triptych', 'Three whole title screens stacked; the S3K one timed so the stock fly-by is behind the emblem.'),
    ('61.5-67.1', 'Signposts, then the Sonic 2 tally', 'Two stacked panels; the tally whole on stripes.'),
    ('67.1-72.7', 'Special stages triptych', 'Three stacked bands; the Sonic 2 band zoomed 1.5x so its 256 px borders are out.'),
    ('72.7-76.9', '2x2 grid', 'Four wide strips.'),
    ('76.9-81.8', 'Sonic 2 ending: side view, then the pose', 'Whole windows on their own sky: side view (0,60)-(200,200), pose (60,12)-(280,196).'),
    ('81.8-89.6', 'Gilded run-in, Hydrocity', 'Tall frame; POWERED UP as a vertical card.'),
    ('89.6-94.5', 'Trails pair', 'Two stacked bands: jade above, gold below.'),
    ('94.5-100.8', 'Solar TALON, Carnival Night', 'Tall frame.'),
    ('100.8-105.7', 'Powered triptych', 'Three stacked bands.'),
    ('105.7-109.25', 'Hyper MICA, Death Egg', 'Tall frame.'),
    ('109.25-112.06', 'Launch Base boss + ONE HIT. card on the right', 'A fixed window at native x 140 so boss and MICA are both whole; from the hit an upright card slides in beside the boss with ONE / HIT. stacked.'),
    ('112.06-117.7', 'The pair, full frame', 'A closer two-shot for the twin transformation (native x 111-217, rows 0-188, the HUD out whole), then from the catch (113.4 s) the tall frame for the carry, tags above and below them. <b>Changed since the last render</b>: the close window took rows 58-224 and cut both heads while they were in the air.'),
    ('117.7-124.0', 'End card', 'Card block with the stacked lock-up, line and URL on two lines, disclaimer; the pair take behind it in soft focus.'),
]
rows = ''.join(f'<tr><td class=t>{t}</td><td>{esc(a)}</td><td>{b}</td></tr>' for t, a, b in ROWS)

doc = f'''<!doctype html><meta charset=utf-8><title>MICA &amp; TALON promo redo: 9:16 review</title>
<style>
body{{background:#0e1222;color:#e8ecf6;font:16px/1.5 system-ui,sans-serif;max-width:1400px;margin:0 auto;padding:28px}}
h1{{font-size:28px;margin:0 0 4px}}h2{{margin:40px 0 10px;font-size:22px;border-bottom:2px solid #2449db;padding-bottom:6px}}
table{{border-collapse:collapse;font-size:14px}}td,th{{border:1px solid #2a3355;padding:5px 9px;vertical-align:top;text-align:left}}
th{{background:#18203d}}td.t{{white-space:nowrap}}
img,video{{max-width:100%;display:block;border:1px solid #2a3355}}
.box{{background:#151b33;border-left:4px solid #ffdc5a;padding:12px 16px;margin:12px 0}}.warn{{border-left-color:#ff7a7a}}
code{{background:#1b2342;padding:1px 5px;border-radius:3px;font-size:13px}}li{{margin:5px 0}}.dim{{color:#aab3cf}}
.two{{display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap}}
</style>
<h1>MICA &amp; TALON promo redo: 9:16 review</h1>
<p class=dim>Full-size file: <code>~/scratch/agent-tmp/mt-promo-redo-20261111/out/master-9x16.mp4</code> (1080&times;1920, {float(LV['ffprobe']['format']['duration']):.2f} s).
The copy below is {vs['width']}&times;{vs['height']}, CRF 30, {int(probe['format']['size']) / 1e6:.1f} MB. It has the same sound and the same cut times as the 16:9 master.</p>

<div class=two>
<video controls preload=metadata width={vs['width']} height={vs['height']} src="{b64(small.read_bytes(), 'video/mp4')}"></video>
<div style="flex:1;min-width:420px">
<h2 style="margin-top:0">Measured on the encoded masters</h2>
<table><tr><th></th><th>16:9</th><th>9:16</th></tr>
<tr><td>Duration</td><td>{float(LH['ffprobe']['format']['duration']):.2f} s</td><td>{float(LV['ffprobe']['format']['duration']):.2f} s</td></tr>
<tr><td>Integrated loudness</td><td>{LH['integrated_lufs']:.1f} LUFS</td><td>{LV['integrated_lufs']:.1f} LUFS</td></tr>
<tr><td>True peak</td><td>{LH['true_peak_dbtp']:.1f} dBTP</td><td>{LV['true_peak_dbtp']:.1f} dBTP</td></tr>
<tr><td>Loudness range</td><td>{LH['lra_lu']:.1f} LU</td><td>{LV['lra_lu']:.1f} LU</td></tr>
<tr><td>Full decode</td><td>exit {LH['full_decode_exit']}</td><td>exit {LV['full_decode_exit']}</td></tr></table>
<p>Sound was checked by measurement only. Nobody listened to these files.</p>
<div class=box><b>Please check</b><ul>
<li>The three framing cuts inside takes: 5.05 s (TALON takes off), 6.2 s (the carry catch), 113.4 s (the pair catch). Each goes from a closer framing to the tall frame on the event.</li>
<li>ONE HIT. as an upright card beside the boss (110.65 s on).</li>
<li>The pair's close two-shot: both whole, a third of the way down, sky above them.</li>
<li>The stacked lock-up (MICA / &amp; TALON) on the title drop and the end card.</li>
</ul></div>
<div class="box warn"><b>One thing in both cuts that you have not ruled on.</b> The Tornado keeps its stock livery, with the word
"SONIC" on its side. It is readable in Sky Chase (30.8&ndash;36.4 s) and the ending's side view (76.9&ndash;79.0 s). The 2026-11-11 cut
cropped it out at the lead's request then. I left the plane whole because TALON piloting it is on the list of features to show.
Say if you want it cropped or the shots re-timed.</div>
</div></div>

<h2>Contact sheet, one frame every 2 s of the encoded 9:16 master</h2>
<img src="{b64((T / 'out/contact-9x16-2s.jpg').read_bytes(), 'image/jpeg')}">

<h2>Framing cuts inside takes</h2>
<p>Launch Base duo: bands until he takes off, then the tall frame.</p>
<img src="{strip([3.3, 4.2, 4.9, 5.02, 5.08, 5.3, 5.6])}">
<p>The carry: closer two-shot, then the tall frame from the catch.</p>
<img src="{strip([5.9, 6.1, 6.2, 6.3, 7.5, 9.5, 11.0])}">
<p>ONE HIT.</p>
<img src="{strip([109.6, 110.4, 110.66, 110.75, 110.9, 111.3, 111.9])}">
<p>The pair: white, silhouettes, both revealed, the catch, the tall frame, then the end card.</p>
<img src="{strip([112.2, 112.36, 112.5, 113.0, 113.3, 113.45, 115.0, 117.0, 119.5])}">

<h2>Every shot: 16:9 picture and its 9:16 framing</h2>
<table><tr><th>Time (s)</th><th>16:9</th><th>9:16</th></tr>{rows}</table>
'''
(OUT / 'vertical-review.html').write_text(doc)
print(OUT / 'vertical-review.html', f'{len(doc) / 1e6:.1f} MB', vs['width'], vs['height'])
