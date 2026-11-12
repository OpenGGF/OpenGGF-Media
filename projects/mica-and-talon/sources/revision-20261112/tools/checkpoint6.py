#!/usr/bin/env python3
"""Purpose: checkpoint 6, the character introduction cards, as ONE self-contained HTML file plus a PNG under 512 KB.
For each of MICA and TALON, in 16:9 and 9:16: a filmstrip of the card and a short render (the card's bar and the bar
after it, with the music for those bars), laid over stand-in play from takes on disk. Also the end card with the
duo drawing, and an optional title lock-up in the lettered names.
Edit layer only: no ROM time. The cards are edit/cards.py; the drawings are cut-outs in art/ (tools/sol_art.py).
Outputs: checkpoint6/cards.html, checkpoint6/cards.png. Origin: MICA & TALON promo redo, 2026-11-12."""
import base64, html, io, json, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

T = Path(__file__).resolve().parent.parent
C = T / 'checkpoint6'
C.mkdir(exist_ok=True)
sys.path.insert(0, str(T / 'edit'))
import cards  # noqa: E402

BT = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]
esc = html.escape
F13 = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Regular.ttf', 13)
F13B = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 13)
F22B = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 22)
BLUE2, RED2, YEL2 = (36, 73, 219), (255, 0, 0), (255, 255, 0)


def bf(n):
    k = int(n)
    return int(round((BT[k] + (BT[k + 1] - BT[k]) * (n - k)) * 60))


_FR = {}


def take(folder, name, i):
    key = (folder, name)
    if key not in _FR:
        fr = sorted((T / folder / name / 'frames').glob('*.png'))
        _FR[key] = (fr, [int(f.stem) for f in fr])
    fr, idx = _FR[key]
    j = min(range(len(idx)), key=lambda k: abs(idx[k] - max(0, i)))
    return Image.open(fr[j]).convert('RGB')


def play(folder, name, i, W, H, y0=22, x0=116):
    """Stand-in play the way the edit frames it: the 320x180 window at 6x, or the tall 126x224 window."""
    im = take(folder, name, i)
    im = im.crop((0, y0, 320, y0 + 180)) if W > H else im.crop((x0, 0, x0 + 126, 224))
    return np.asarray(im.resize((W, H), Image.NEAREST))


# who -> (bar the card lands on, take folder, take, take frame shown on the card's bar line, hero on the left?)
# MICA: Marble Garden chain, first kill (#65) on beat 2 of the next bar. TALON: Spring Yard, kills on beats 2 and 4.
WHO = {'mica': (14, 'captures', 'd-mgz2-chain', 44 - 84, True), 'talon': (28, 'captures', 'd-syz1-talon', 97 - 84, False)}
N = 168                                                     # the card's bar and the bar after it


def frame_of(who, W, H, k, intro):
    bar, folder, name, s0, _ = WHO[who]
    return intro.draw(play(folder, name, s0 + k, W, H), k, plate_until=N + 84)


def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def jpg(im, q=84):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return b64(buf.getvalue(), 'image/jpeg')


def strip(frames, tw, labels):
    th = round(tw * frames[0].shape[0] / frames[0].shape[1])
    s = Image.new('RGB', (len(frames) * (tw + 4) - 4, th + 17), (14, 18, 34))
    d = ImageDraw.Draw(s)
    for n, (f, lab) in enumerate(zip(frames, labels)):
        s.paste(Image.fromarray(f).resize((tw, th), Image.LANCZOS), (n * (tw + 4), 0))
        d.text((n * (tw + 4) + 3, th + 2), lab, font=F13, fill=(255, 220, 90))
    return s


def music(bar0, frames, out):
    """The owner's bed for these frames, AAC, for the preview only (scratch; never a repository)."""
    with wave.open(str(T / 'work/bed.wav')) as w:
        rate = w.getframerate()
    t0 = bf(bar0) / 60
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.4f}', '-t', f'{frames / 60:.4f}', '-i', str(T / 'work/bed.wav'), '-c:a', 'aac', '-b:a', '128k', str(out)], check=True)


def render(who, W, H, ow, oh, out):
    intro = cards.Intro(who, W, H, hero_left=WHO[who][4])
    aud = out.with_suffix('.m4a')
    music(WHO[who][0], N, aud)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '60', '-i', '-', '-i', str(aud),
                          '-vf', f'scale={ow}:{oh}:flags=lanczos', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'slow', '-crf', '27',
                          '-c:a', 'copy', '-shortest', '-movflags', '+faststart', str(out)], stdin=subprocess.PIPE)
    keep = {}
    for k in range(N):
        f = frame_of(who, W, H, k, intro)
        p.stdin.write(f.tobytes())
        if k in KS:
            keep[k] = f
    p.stdin.close(); p.wait()
    aud.unlink()
    return [keep[k] for k in KS]


KS = [0, 6, 14, 30, 46, 54, 62, 80, 90, 104, 150]
KLAB = ['0: the cut', '6', '14: both in', '30: line', '46: field parts', '54', '62: play shows', '80: linger', '90: they leave', '104', '150: plate']


def soft(folder, name, i, W, H):
    """The end card backdrop the edit uses: the pair take, columns right of the HUD, blurred and dimmed."""
    im = take(folder, name, i).crop((114, 4, 320, 120)) if W > H else take(folder, name, i).crop((116, 0, 242, 224))
    im = im.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(11))
    return (np.asarray(im).astype(np.float32) * 0.62).astype(np.uint8)


def lockup(W=1920, H=1080):
    """Option: the title drop's lock-up band in the lettered names (the film now sets it in Fira Sans italic)."""
    t = take('captures', 'title-s2', 860).crop((0, 26, 320, 206)).resize((W, H), Image.NEAREST).convert('RGBA')
    bh, y, strip_h = 150, 930, 16                           # where the delivered cut's band sits (rows 930-1079)
    band = Image.new('RGBA', (W, bh), BLUE2 + (255,))
    d = ImageDraw.Draw(band)
    d.rectangle((0, bh - strip_h, W, bh), fill=YEL2)
    for yy in range(0, bh - strip_h, 18):
        d.rectangle((0, yy, 44 + (9 if (yy // 18) % 2 else 0), yy + 18), fill=RED2)
    t.alpha_composite(band, (0, y))
    hname = 112
    m = cards.sticker('name-mica', height=hname, edge=False)
    tl = cards.sticker('name-talon', height=round(hname * 622 / 695), edge=False)
    amp = cards.label('&', 104, cards.YELLOW)
    x = (W - (m.width + amp.width + tl.width + 56)) // 2
    for im in (m, amp, tl):
        t.alpha_composite(im, (x, y + (bh - strip_h - im.height) // 2 + 1)); x += im.width + 28
    return np.asarray(t.convert('RGB'))


def main():
    vids, strips, pngrows = {}, {}, []
    for who in ('mica', 'talon'):
        for tag, (W, H, ow, oh, tw) in (('h', (1920, 1080, 960, 540, 250)), ('v', (1080, 1920, 432, 768, 126))):
            out = C / f'{who}-{tag}.mp4'
            frames = render(who, W, H, ow, oh, out)
            vids[who, tag] = out
            strips[who, tag] = strip(frames, tw, KLAB)
            if tag == 'h':
                pngrows.append((f'{who.upper()} introduction, 16:9', [frames[i] for i in (2, 3, 5, 6, 7, 9, 10)], 216))
            else:
                pngrows.append((f'{who.upper()} introduction, 9:16', [frames[i] for i in (2, 3, 5, 6, 7, 9, 10)], 96))
            print(out.name, out.stat().st_size // 1024, 'KB')
    ends = {}
    for tag, (W, H, tw) in (('h', (1920, 1080, 330)), ('v', (1080, 1920, 150))):
        ec = cards.EndCard(W, H)
        ts = [0, 8, 16, 30, 44, 70, 110]
        fr = [ec.draw(soft('probes-b', 'r6-final-look-b20k10', 404 + t, W, H), t) for t in ts]
        ends[tag] = strip(fr, tw, [f't = {t}' for t in ts])
        ends[tag + '1'] = Image.fromarray(fr[-1])
        pngrows.append((f'End card with the duo drawing, {"16:9" if tag == "h" else "9:16"}', [fr[i] for i in (1, 3, 6)], 330 if tag == 'h' else 120))
    alt = cards.EndCard(1920, 1080, duo='duo-sunrise-b')
    alt_f = alt.draw(soft('probes-b', 'r6-final-look-b20k10', 510, 1920, 1080), 110)
    lk = lockup()
    pngrows.append(('Option: title lock-up in the lettered names', [lk], 330))

    def vid(who, tag, w):
        return f'<video controls loop muted preload=metadata width={w} src="{b64(vids[who, tag].read_bytes(), "video/mp4")}"></video>'

    doc = f'''<!doctype html><meta charset=utf-8><title>MICA &amp; TALON promo: character introductions (checkpoint 6)</title>
<style>
body{{background:#0e1222;color:#e8ecf6;font:15px/1.5 system-ui,sans-serif;max-width:1500px;margin:0 auto;padding:28px}}
h1{{font-size:28px;margin:0 0 4px}}h2{{margin:40px 0 10px;font-size:22px;border-bottom:2px solid #2449db;padding-bottom:6px}}h3{{margin:22px 0 8px;font-size:17px}}
table{{border-collapse:collapse;font-size:13.5px}}td,th{{border:1px solid #2a3355;padding:6px 9px;vertical-align:top;text-align:left}}th{{background:#18203d}}
img,video{{display:block;border:1px solid #2a3355;max-width:100%;height:auto}}
.box{{background:#151b33;border-left:4px solid #ffdc5a;padding:12px 16px;margin:12px 0}}.warn{{border-left-color:#d95926}}
code{{background:#1b2342;padding:1px 4px;border-radius:3px;font-size:12px}}li{{margin:5px 0}}.dim{{color:#aab3cf;font-size:13px}}
.two{{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap}}
</style>
<h1>MICA &amp; TALON promo: character introductions</h1>
<p class=dim>Checkpoint 6. Edit-layer cards only; no ROM time and no final captures. The play under each card is a stand-in from takes on disk (old art, no
SFX stem yet), framed the way the edit frames it. The renders carry the music for their two bars; unmute to hear where the card sits on the beat.
The drawings are read from the release-promo project and cut out into this task's scratch <code>art/</code>; nothing went into the OpenGGF repo.</p>

<div class=box><b>Decisions to check</b><ul>
<li><b>Where they go:</b> MICA's card lands on bar 14 and TALON's on bar 28, the first bar of each character's own chapter, in place of the two banded
headers ("MICA / HOMING STRIKE", "TALON / FLIGHT CARRY DIVEBOMB"). I did not put them on the cold open's duo shot (bars 2-4): two cards there would cover
the whole run, which is the hook, so the small name tags stay on it.</li>
<li><b>One bar each, the owner's card grammar:</b> the field is on from the cut; the hero drawing, nearly the height of the frame, slides in from its side and the
lettered name from the other; on beat 3 the field parts along its slant and leaves first; drawing and name stay over the play to the bar line; then the drawing
leaves the way it came and the name shrinks into the corner, where it stays for the rest of that shot.</li>
<li><b>Sides:</b> MICA on the left, pointing at her name; TALON on the right, his wing behind his name. In 9:16 the name is across the top and the drawing fills
the lower two thirds: TALON's wings run off both sides, MICA keeps her pointing hand and gives up the tip of her tail.</li>
<li><b>Lines under the names</b> use the mod README's words: "JADE PANGOLIN. HOMING STRIKE." and "FALCON. FLIGHT. DIVEBOMB."</li>
<li><b>Time comes from trims, not the music</b> (table below): the 124 s length and the bar grid are unchanged.</li>
<li><b>End card:</b> the duo drawing on the left, the two lettered names stacked on the right in place of the Fira Sans lock-up, the same line, URL and disclaimer.</li>
</ul></div>
<div class="box warn"><b>Where a card costs something</b><ul>
<li><b>MICA's card covers her take's lead-in and her first jump.</b> The play shows from beat 3 of bar 14 and the drawing is over the left half until the bar line, so
her jump and first strike are behind it; the three kills land on beats 2, 3 and 4 of bar 15, just after the drawing has gone. I think that is a fair trade: nothing with
a hit is covered. It does mean the Marble Garden shot drops from 2 bars to 1.5.</li>
<li><b>TALON's card covers his take-off.</b> The play shows him already flying between the columns; both kills (beats 2 and 4 of bar 29) are clear of the card.</li>
<li><b>The corner name plate and the lives inset collide</b> in TALON's Spring Yard shot (both bottom right). I will end the plate when the inset arrives.</li>
<li><b>Two name treatments in one film:</b> the title drop (bars 12-14) still sets "MICA &amp; TALON" in white Fira Sans, two bars before the lettered MICA. Section 4 shows
that lock-up in the lettered names instead. I do not recommend it: jade and slate lettering reads poorly on the card blue at that size. I would keep the white lock-up as the
title's voice and use the lettered names on the two cards and the end card.</li>
<li><b>TALON has gloved hands in both duo drawings</b> (he has none in his hero drawing). I used <code>duo-sunrise</code>; the other is at the end of section 3.</li>
</ul></div>

<h2>1. MICA, bar 14</h2>
<div class=two>{vid('mica', 'h', 960)}{vid('mica', 'v', 300)}</div>
<h3>16:9</h3><img src="{jpg(strips['mica', 'h'])}" alt="MICA card 16:9">
<h3>9:16</h3><img src="{jpg(strips['mica', 'v'])}" alt="MICA card 9:16">

<h2>2. TALON, bar 28</h2>
<div class=two>{vid('talon', 'h', 960)}{vid('talon', 'v', 300)}</div>
<h3>16:9</h3><img src="{jpg(strips['talon', 'h'])}" alt="TALON card 16:9">
<h3>9:16</h3><img src="{jpg(strips['talon', 'v'])}" alt="TALON card 9:16">

<h2>3. End card with the duo drawing, bars 84-88</h2>
<p>The backdrop is still the pair take in soft focus; the duo rises in with the iris, MICA and TALON arrive a beat apart, then the line and the URL. The fade is unchanged.</p>
<img src="{jpg(ends['h'])}" alt="end card 16:9"><br>
<div class=two><img src="{jpg(ends['h1'].resize((960, 540), Image.LANCZOS))}" alt="end card 16:9, settled"><img src="{jpg(ends['v1'].resize((304, 540), Image.LANCZOS))}" alt="end card 9:16, settled"></div>
<img src="{jpg(ends['v'])}" alt="end card 9:16">
<p class=dim>The other duo drawing (<code>duo-sunrise-b</code>) in the same layout:</p>
<img src="{jpg(Image.fromarray(alt_f).resize((960, 540), Image.LANCZOS))}" alt="end card with duo-sunrise-b">

<h2>4. Option: the title lock-up in the lettered names</h2>
<img src="{jpg(Image.fromarray(lk).resize((960, 540), Image.LANCZOS))}" alt="lock-up option">

<h2>5. Where the two bars come from</h2>
<table><tr><th>Bars</th><th>Approved plan (checkpoint 4/5)</th><th>With the cards</th></tr>
<tr><td>14-16.5</td><td>14-16 Marble Garden chain, kills on bar 14 beat 4, bar 15 beats 1 and 2</td><td><b>14-15 MICA card</b> over the take's lead-in; 15-16.5 the chain, kills on bar 15 beats 2, 3, 4</td></tr>
<tr><td>16.5-18.5</td><td>16-18 strike triptych</td><td>16.5-18.5 strike triptych (unchanged length, half a bar later)</td></tr>
<tr><td>18.5-20</td><td>18-20 Hydrocity loop, 2 bars</td><td>18.5-20 Hydrocity loop, 1.5 bars, still out on the spring</td></tr>
<tr><td>20-28</td><td colspan=2>unchanged</td></tr>
<tr><td>28-30.5</td><td>28-30 Spring Yard, kills on bar 28 beat 4, bar 29 beat 2</td><td><b>28-29 TALON card</b> over his flight in; 29-30.5 Spring Yard, kills on bar 29 beats 2 and 4, then the run</td></tr>
<tr><td>30.5-32</td><td>30-32 Hill Top lake dive, 2 bars</td><td>30.5-32 lake dive, 1.5 bars, the dive starting one beat in</td></tr>
<tr><td>32-36</td><td colspan=2>unchanged</td></tr></table>
<p>Every phrase start that was on a cut still is (bars 20, 24, 28, 32, 36). The Marble Garden take needs no new probe: it is the tuned take with a different window.
Shots: 49 before, 51 with the two cards.</p>
'''
    (C / 'cards.html').write_text(doc)
    print(C / 'cards.html', f'{len(doc) / 1e6:.2f} MB')

    # PNG version
    BG, INK, DIM = (14, 18, 34), (240, 239, 236), (195, 194, 183)
    for scale, colours in ((1.0, 128), (0.88, 96), (0.76, 64)):
        W = 1560
        rows_h = [round(tw * scale * fr[0].shape[0] / fr[0].shape[1]) + 30 for _, fr, tw in pngrows]
        im = Image.new('RGB', (W, 70 + sum(rows_h) + 20), BG); d = ImageDraw.Draw(im)
        d.text((20, 14), 'MICA & TALON promo: character introductions (checkpoint 6)', font=F22B, fill=INK)
        d.text((20, 44), 'One bar each on bars 14 and 28; the field leaves first, drawing and name linger over the play; duo drawing on the end card. 124 s unchanged.', font=F13, fill=DIM)
        y = 70
        for (title, fr, tw), rh in zip(pngrows, rows_h):
            d.text((20, y), title, font=F13B, fill=INK)
            x = 20
            for f in fr:
                w = round(tw * scale); h = round(w * f.shape[0] / f.shape[1])
                im.paste(Image.fromarray(f).resize((w, h), Image.LANCZOS), (x, y + 18)); x += w + 4
            y += rh
        q = im.quantize(colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        buf = io.BytesIO(); q.save(buf, 'PNG', optimize=True)
        if buf.tell() < 512 * 1024:
            break
    (C / 'cards.png').write_bytes(buf.getvalue())
    print(C / 'cards.png', im.size, f'{buf.tell() / 1024:.0f} KB')


if __name__ == '__main__':
    main()
