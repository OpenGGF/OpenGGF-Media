#!/usr/bin/env python3
"""Purpose: build checkpoint 1 (storyboard) as ONE self-contained HTML file: music plan + figure, beat sheet (from
the edit's own NOTES), a contact sheet of the chosen native in-points, composed key frames and the composed edit
at one frame per second. All media is embedded as base64; nothing is linked.
Inputs: edit/edit.py, work/music-figure.png, work/build-h/frame-*.png and sheet-*.png (promo_kit frames/sheet).
Origin: MICA & TALON promo redo 2026-11-12."""
import base64, html, importlib.util, io, json, os, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
sys.path.insert(0, str(ROOT / 'tools/media'))
import promo_kit  # noqa: E402

spec = importlib.util.spec_from_file_location('mt_edit', T / 'edit/edit.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
e = promo_kit.Edit(**mod.EDIT)
mod.build(e)
NOTES = mod.NOTES
stats, warns = e.pacing()
warns = e.check()


def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def jpg(im, q=86):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return b64(buf.getvalue(), 'image/jpeg')


def png_file(p):
    return b64(Path(p).read_bytes(), 'image/png')


F = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 15)
FS = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Regular.ttf', 13)


def inpoints_sheet():
    tw, th, lab = 288, 202, 300
    cols = max(len(n['src']) for n in NOTES)
    S = Image.new('RGB', (lab + cols * (tw + 6), len(NOTES) * (th + 22)), (14, 18, 34))
    d = ImageDraw.Draw(S)
    for r, n in enumerate(NOTES):
        y = r * (th + 22)
        d.text((8, y + 6), f"{n['t0']:6.2f}-{n['t1']:6.2f} s", font=F, fill=(255, 220, 90))
        d.text((8, y + 26), f"bars {n['b0']:g}-{n['b1']:g}  {n['section']}", font=FS, fill=(200, 210, 230))
        words, linebuf, yy = n['shot'].split(), '', y + 48
        for w in words:
            if d.textlength(linebuf + ' ' + w, font=FS) > lab - 16:
                d.text((8, yy), linebuf, font=FS, fill=(255, 255, 255)); yy += 16; linebuf = w
            else:
                linebuf = (linebuf + ' ' + w).strip()
        d.text((8, yy), linebuf, font=FS, fill=(255, 255, 255))
        for k, (name, i) in enumerate(n['src']):
            fr = sorted((T / 'captures' / name / 'frames').glob('*.png'))
            im = Image.open(fr[min(i, len(fr) - 1)]).convert('RGB').resize((tw, th), Image.NEAREST)
            x = lab + k * (tw + 6)
            S.paste(im, (x, y))
            d.text((x + 2, y + th + 2), f'{name} #{i}', font=FS, fill=(170, 230, 200))
    return S


def edit_sheet():
    parts = [Image.open(p) for p in sorted((T / 'work/build-h').glob('sheet-*.png'), key=lambda p: int(p.stem.split('-')[1]))]
    S = Image.new('RGB', (parts[0].width, sum(p.height for p in parts)))
    y = 0
    for p in parts:
        S.paste(p, (0, y)); y += p.height
    return S.resize((1600, S.height * 1600 // S.width), Image.LANCZOS)


def frame(n):
    return Image.open(T / f'work/build-h/frame-{n:05d}.png')


bt = json.load(open(T / 'work/beat-track.json'))['bars']
tb = lambda b: bt[b]['t']
esc = html.escape
rows = ''.join(
    f"<tr><td class=t>{n['t0']:.2f}&ndash;{n['t1']:.2f}</td><td>{n['b0']:g}&ndash;{n['b1']:g}</td><td class=s>{esc(n['section'])}</td>"
    f"<td>{esc(n['shot'])}</td><td>{esc(n['proves'])}</td><td>{esc(n['accompaniment'])}</td></tr>" for n in NOTES)
tempo_rows = ''.join(f"<tr><td>{a}&ndash;{b}</td><td>{tb(a):.2f}&ndash;{tb(b):.2f}</td><td>{x}</td><td>{y}</td><td>{z}</td><td>{note}</td></tr>" for a, b, x, y, z, note in [
    (0, 43, '172.3&ndash;171.9', '1.5&ndash;4.4', '0&ndash;8 (17 once)', 'steady'),
    (44, 83, '171.9&ndash;170.0', '2.1&ndash;5.0', '0&ndash;3 (15 once)', 'slow drift, &minus;0.05 BPM a bar; pulse locked'),
    (84, 88, '169.8&ndash;168.7', '2.2&ndash;3.2', '1&ndash;4', 'drift quickens to &minus;0.3 BPM a bar; still locked. The fade lives here'),
    (89, 93, '168.3&ndash;164.4', '1.6&ndash;2.4', '2&ndash;8', 'ritardando of &minus;1 BPM a bar; lock slipping'),
    (94, 104, '163.7&ndash;156', '0.7&ndash;2.0', '3&ndash;13', 'three-bar dropout, then a reprise neither tracker can hold'),
])
KF = [(1181, 'Title drop', 'bar 14: the Sonic 2 title as it ships, after its own flash on bar 12; the lock-up band covers the native menu rows whole.'),
      (3218, 'A comparison', 'bars 36&ndash;40: stock Sonic &amp; Tails | MICA &amp; TALON on the same input script. HUD rows are out of both halves whole.'),
      (7233, 'End card', 'bars 84&ndash;88: lock-up, line, URL, disclaimer over the blurred, darkened fire of the last shot (HUD cropped out).')]
KF2 = [(3480, 'Titles triptych (bars 40&ndash;44)'), (5722, 'Solar TALON, the flame-lit reveal on bar 68'), (6679, 'ONE HIT. (bar 79)')]
kf_html = ''.join(f"<figure><img src='{jpg(frame(n), 90)}'><figcaption><b>{t}.</b> {c}</figcaption></figure>" for n, t, c in KF)
kf2_html = ''.join(f"<figure class=half><img src='{jpg(frame(n).resize((1280, 720), Image.LANCZOS), 88)}'><figcaption>{c}</figcaption></figure>" for n, c in KF2)

doc = f"""<!doctype html><html lang=en><meta charset=utf-8><title>MICA &amp; TALON promo redo: storyboard checkpoint</title>
<style>
body{{background:#0e1222;color:#e8ecf6;font:16px/1.5 system-ui,sans-serif;max-width:1500px;margin:0 auto;padding:28px}}
h1{{font-size:30px;margin:0 0 4px}}h2{{margin:44px 0 10px;font-size:23px;border-bottom:2px solid #2449db;padding-bottom:6px}}
h3{{margin:22px 0 6px;font-size:18px;color:#ffdc5a}}
table{{border-collapse:collapse;width:100%;font-size:14px}}td,th{{border:1px solid #2a3355;padding:6px 8px;vertical-align:top;text-align:left}}
th{{background:#18203d}}td.t{{white-space:nowrap;color:#ffdc5a;font-variant-numeric:tabular-nums}}td.s{{white-space:nowrap;color:#7fe0b8}}
img{{max-width:100%;display:block;border:1px solid #2a3355}}figure{{margin:14px 0}}figure.half{{display:inline-block;width:32.6%;vertical-align:top;margin:6px 0}}
figcaption{{font-size:14px;color:#c4cbe0;margin-top:5px}}.box{{background:#151b33;border-left:4px solid #ffdc5a;padding:12px 16px;margin:12px 0}}
code{{background:#1b2342;padding:1px 5px;border-radius:3px;font-size:13px}}li{{margin:5px 0}}.dim{{color:#aab3cf}}
</style>
<h1>MICA &amp; TALON promo redo: storyboard (checkpoint 1)</h1>
<p class=dim>Branch <code>feature/ai-mt-promo-redo</code> at <code>1e0faac123</code>, no repository changes. Example jar sha256 <code>449ada47&hellip;1abfce</code>.
Everything below was captured fresh from that build. No final render exists yet. Task folder: <code>~/scratch/agent-tmp/mt-promo-redo-20261111/</code>.</p>

<div class=box><b>Decisions I want checked</b>
<ol>
<li><b>Length: 2:04.</b> The track plays uncut from its first sample to 123.41 s. That is what "no splices, fade before it goes off the rails" gives. If that is too long for a share-able trailer, the clean earlier outs are bar 60 (83.9 s, before the chorus) and bar 76 (106.4 s); both lose the lift the hero moment sits on, so I recommend the full length.</li>
<li><b>The fade:</b> raised cosine from bar 85 (119.14 s) to bar 88 (123.41 s), three bars, silent before the pulse breaks at bar 89. Evidence in section 1.</li>
<li><b>The beat grid is tracked, not fixed.</b> The track slows from 172.2 to 170.2 BPM by bar 80. A fixed 172.218 grid would be a third of a bar late there. Every cut below is on a tracked bar line.</li>
<li><b>No camera moves at all.</b> Every full-screen shot is a fixed 320&times;180 window of the native frame at exactly 6&times;. The S3K roll-in is rows 8&ndash;188 (the "&amp; KNUCKLES" banner whole, menu rows out), from the black frame to the wink, ending on source frame 411; the title's stock Tornado fly-by puts its first pixel on screen at frame 412. The SEGA logo is in frame for the first 0.5 s, as the game ships it. Say if you want that avoided.</li>
<li><b>The proof of "not a palette swap"</b> is a lockstep split (bars 36&ndash;40): stock Sonic &amp; Tails beside MICA &amp; TALON on one input script in Chemical Plant. Measured: all 461 frames match in position, velocity, camera, sidekick position and roll/air/spindash state.</li>
<li><b>Powered chapter = the whole chorus and lift (bars 60&ndash;84):</b> Gilded reveal on bar 60, jade-versus-gold trails, Solar reveal on bar 68, powered forms in all three games, Hyper reveal on bar 76 (the lift), one Instagib hit on the Angel Island mini-boss on bar 79, the jungle ablaze by bar 83, end card on 84.</li>
<li><b>New finds:</b> a Sonic 2 homing chain exists in Sky Chase (native 100 then 200), with TALON flying the Tornado in play; the Sonic 1 special stage is filmed through the real giant ring; TALON's first full shot is in Sonic 1.</li>
<li><b>Not filmed:</b> Competition (same exception as last time), slot reels (not attempted). Details in section 5.</li>
</ol></div>

<h2>1. Music plan: where it fades and why</h2>
<p>"RUN INTO THE SUNSHINE (Chiptune Remix)", owner-supplied, 162.8 s, sha256 <code>569a921b&hellip;8481ff</code>. It stays outside every repository. Bed = source samples 0 to 123.407 s, unspliced, multiplied only by the fade (<code>tools/build_bed.py</code>).</p>
<img src="{png_file(T / 'work/music-figure.png')}">
<p><b>How I decided.</b> I tracked the pulse bar by bar (<code>tools/beat_track.py</code>: a comb tracker on a 2.5 ms spectral-flux envelope, searching local period and phase) and cross-checked tempo by autocorrelation per region (<code>tools/music_analysis.py</code>, <code>tools/music_sections.py</code>).</p>
<table><tr><th>Bars</th><th>Seconds</th><th>Local BPM</th><th>Pulse lock (on-beat onset / mean)</th><th>Beat jitter, ms</th><th>Reading</th></tr>{tempo_rows}</table>
<ul>
<li><b>Where it goes off the rails: bar 89 (124.84 s).</b> Bar-lag autocorrelation holds at 0.39&ndash;0.60 up to 123.4 s and collapses to 0.11 for 123.4&ndash;129 s. The tracker's lock falls from about 3 to under 2 at bar 90 and under 1 by bar 96. Beat jitter goes from 1&ndash;2 ms to 5&ndash;13 ms. Bars 94&ndash;96 drop out (to about &minus;21 dB), and the reprise comes back at a tempo two methods disagree on (156&ndash;161 or 176&ndash;178 BPM).</li>
<li><b>The phrase boundary: bar 88 (123.41 s).</b> Phrases run in eights from bar 12 (12, 20 &hellip; 76, 84). Bars 83&ndash;85 are the loudest of the clean part (&minus;16.1 dB RMS against about &minus;17.2 around them). Bar 88 is a break bar: after its downbeat the low band falls by up to 27 dB over the next three beats. The fade reaches silence exactly there.</li>
<li><b>The fade:</b> starts on bar 85, after the two loudest bars have played at full level under the end card's arrival; &minus;6 dB at 121.27 s; silent at 123.41 s. Two short stutter-stops inside the fade (bar 85 beat 4, bar 86 beat 3) are in the track itself.</li>
<li><b>Sections used for the edit</b> (tracked bar starts): intro 0 (0.18 s), riser 8 (11.32), A 12 (16.89), break 28 (39.20), build 32, B 36 (50.35), stabs 44 (61.51), pre-chorus 52 (72.72), chorus 60 (83.94), lift 76 (106.42), peak 83&ndash;85.</li>
<li>Master plan: bed at 0.75, ROM stingers near game level, then two-pass loudnorm to &minus;14 LUFS with true peak &le; &minus;1.0 dBTP, re-measured on the encoded AAC with <code>ebur128=peak=true</code>. <b>I cannot hear the film; sound is checked by measurement only.</b></li>
</ul>

<h2>2. Beat sheet</h2>
<p class=dim>Times are output seconds; bars are tracked bar lines of the uncut track. {stats['shots']} shots, mean {stats['mean_shot_s']} s, busiest 20 s has {stats['busiest_window_cuts']} cuts, {stats['cuts_in_last_window']} cuts in the last 20 s. <code>promo_kit.py check</code>: {('no warnings' if not warns else esc('; '.join(warns)))} (its bare-stretch test only sees <code>Game</code> shots, so the accompaniment column is the real check).</p>
<table><tr><th>Time (s)</th><th>Bars</th><th>Section</th><th>Shot</th><th>What it proves</th><th>Accompaniment</th></tr>{rows}</table>
<p class=dim>Chapter changes sit on section changes: title drop on the A drop (bar 12), TALON on the break (28), "Every screen" on the B drop (36), "Powered up" on the chorus (60), Hyper on the lift (76). The three transformation shots start half a bar early so the wind-up plays and the reveal itself lands on the downbeat.</p>

<h2>3. Three composed key frames</h2>
{kf_html}
<h3>Three more, for the comparisons and the hero</h3>
{kf2_html}

<h2>4. Contact sheet of chosen in-points</h2>
<p class=dim>Native capture frames (320&times;224, untouched) at the in-point or event of each shot, labelled with capture id and frame number. Recipes are in <code>shots/batch*.json</code>; each capture has <code>provenance.json</code> and <code>state.csv</code>.</p>
<img src="{jpg(inpoints_sheet(), 84)}">

<h2>5. Honesty: positioned starts, omissions, things not filmed as they ship</h2>
<ul>
<li><b>Positioned starts with declared rings and timer</b> throughout, never continuous cold routes. Powered shots are all mid-act: Hydrocity 1 at 1:40 with 66 rings, Carnival Night 1 at 1:35 with 68, Death Egg 1 at 1:40 with 75 and Super Emeralds, Angel Island 1 mini-boss at 2:07 with 64, Star Light and Mystic Cave at 1:10&ndash;1:20 with 70. Sky Chase and the Chemical Plant lockstep start at the act's own start position, and the title screens are cold title-first boots (normal forms only).</li>
<li><b>Competition: not filmed.</b> The capture reaches the Competition menu, then <code>GameplayCaptureTool</code> throws <code>IllegalStateException: Native arena has no published VInt registers</code>, as last time. <b>Slot reels: not attempted.</b></li>
<li><b>Sonic 1 results card</b> still draws its act oval over "HAS PASSED" (engine, stock Sonic too). Sonic 1 is shown to the signpost; results are shown in Sonic 2.</li>
<li><b>Stock art avoided by timing or crop:</b> the S3K title's small Tornado fly-by (the roll-in ends before it; the triptych slice never reaches it) and the Data Select "No Save" tile (outside its grid cell).</li>
<li><b>Debug component entries</b>, as before: the Sonic 2 half-pipe (ROM starpost entry), Continue and the Sonic 2 ending. The Sonic 1 special stage is entered the real way, by jumping into the giant ring with 55 rings.</li>
<li><b>Widescreen rejected.</b> The engine's 400-px width fills 16:9 without a crop, but camera-locked arenas leave an unrendered band on the right (the boss shot) and sprites are 17 % smaller. Everything is native 320 wide.</li>
<li><b>Sonic 2 chain:</b> probes in Metropolis (five Asterons), Aquatic Ruin (three Whisps) and Oil Ocean found none; Sky Chase gives 100 then 200 on frames 324 and 360 of <code>h-scz-a</code>.</li>
</ul>

<h2>6. The composed edit, one frame per second</h2>
<p class=dim>Rendered from <code>edit/edit.py</code> as it stands (16:9 only; the vertical cut is designed after the draft is approved). Yellow numbers are output frame and time.</p>
<img src="{jpg(edit_sheet(), 80)}">
<p class=dim>Next after your reply: fixes, the full 16:9 draft render, viewer pass, <code>promo_kit.py check</code> and loudness numbers.</p>
</html>"""
out = T / 'checkpoint1/storyboard.html'
out.write_text(doc)
print(out, f'{out.stat().st_size / 1e6:.1f} MB', 'notes', len(NOTES), 'warnings', warns)
