#!/usr/bin/env python3
"""Purpose: checkpoint 4, the pacing re-storyboard (stage A of the 2026-11-12 revision), as ONE self-contained HTML
file plus a PNG version under 512 KB. No new captures: every picture is from a take already on disk.
Contents: the measured table of the current 124 s cut (shot, time range, mean |gspeed|, interactions, verdict,
where it goes in the new plan), the new plan on the tracked bar grid with each shot's source window, its measured
speed and how far each hit lands from a beat, the re-stages that need a probe in stage B with their fallbacks,
and an old-versus-new cut timeline.
Inputs: checkpoint4/pacing-current.json (tools/pacing.py), work/beat-track.json, captures/*.
Outputs: checkpoint4/storyboard.html, checkpoint4/storyboard.png, checkpoint4/plan.json.
Origin: MICA & TALON promo redo, pacing revision 2026-11-12."""
import base64, html, io, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

T = Path(__file__).resolve().parent.parent
C = T / 'checkpoint4'
sys.path.insert(0, str(T / 'tools'))
import pacing  # noqa: E402

BT = [b['t'] for b in json.load(open(T / 'work/beat-track.json'))['bars']]
esc = html.escape


def bf(n, beat=1):
    """Output frame of bar n (may be fractional), beat 1-4."""
    n = n + (beat - 1) / 4
    k = int(n)
    return int(round((BT[k] + (BT[k + 1] - BT[k]) * (n - k)) * 60))


END = bf(88) + 36
BEATS = [bf(b, k) for b in range(0, 89) for k in (1, 2, 3, 4)]


def near_beat(f):
    j = min(range(len(BEATS)), key=lambda i: abs(BEATS[i] - f))
    return j // 4, j % 4 + 1, f - BEATS[j]


# verdict / treatment categories (validated dark categorical slots 1-4)
CAT = {'keep': '#3987e5', 'trim': '#199e70', 'replace': '#c98500', 're-stage': '#d95926'}
CATLAB = {'keep': 'keep', 'trim': 'trim (same take, shorter or re-timed)', 'replace': 'replace (window or take already on disk)',
          're-stage': 're-stage (new staging, probe in stage B)'}

# ---- the new plan. pane = (take, src0 | ('anchor', event_src, bar, beat), key, label); m = measure override (a, b)
A = 'anchor'
PLAN = [
    (0, 2, 'COLD OPEN', 'S3K title roll-in, whole width, no move', 'keep', [('title-s3k', 234, '', '', 1.57)],
     'Unchanged: black for 0.55 s (the SEGA logo is never shown), then the smear frames, native flash, logo drop, wink.', None),
    (2, 4, 'COLD OPEN', 'Launch Base 1: MICA and TALON cross the bridge at full speed, spring launch', 're-stage',
     [('q-walk-14500', (A, 200, 3, 4), '', 'stand-in')],
     'Was a run from a standstill (mean |gspeed| 863). Same act, started further back so both are at top speed (1536) on the first frame; name tags a beat apart; the spring fires on beat 4 of bar 3 and the cut follows the launch.',
     dict(target='both at |gspeed| 1536 for the whole shot; spring on bar 3 beat 4', probe='start x about 13500-14000 on the same floor, R held on both pads',
          fallback='q-walk-14500 #112-222 as a 1.3-bar shot behind a longer roll-in hold', m=(112, 222))),
    (4, 6, 'COLD OPEN', 'Angel Island 1: carry swoop. MICA jumps from a run, TALON catches her in the air and carries her on', 're-stage',
     [('d-carry-fly', (A, 58, 4, 2), '', 'stand-in')],
     'Was 4 bars with TALON walking up to a standing MICA, then a slow vertical climb (mean speed 2.5 px/f, no interaction after the catch). Now 2 bars: both moving when he catches her, the catch on a beat, then travel across the canopy. Promise line on bar 5.',
     dict(target='catch on bar 4 beat 3 with MICA airborne from a run; camera travelling at 3 px/f or more after it', probe='pad 2 jumps and flaps toward her while pad 1 runs and jumps (the pair take already steers a carry with L/R)',
          fallback='the current take from #37 (catch on beat 2), cut at 2 bars')),
    (6, 7, 'COLD OPEN', 'Angel Island 1: TALON divebombs a Rhinobot', 'replace', [('d-aiz-talon-dive', (A, 120, 6, 3), '', '')],
     'One bar. Was a pane of the verbs triptych; here it is his first hit, full frame, on the beat.', None),
    (7, 8, 'COLD OPEN', 'Angel Island 1: MICA strikes the second Rhinobot, jade trail', 'replace', [('d-aiz-normal', (A, 163, 7, 3), '', '')],
     'One bar. Her first hit, a beat pattern with the shot before: his hit on beat 3 of bar 6, hers on beat 3 of bar 7.', None),
    (8, 10, 'COLD OPEN (riser)', 'Mushroom Hill 1: Hyper MICA through two loops with banded after-images', 'replace', [('p-mhz1-hyper', 262, '', '')],
     'Replaces the Death Egg Hyper fragment, which showed the same kill twice in the film (here and at bar 77). The loops are the fastest picture on disk: 10.5 px/f, camera 700 px/s.', None),
    (10, 12, 'TITLE', 'Sonic 2 title: MICA then TALON rise over the emblem', 'keep', [('title-s2', 589, '', '')],
     'Unchanged; the native flash still lands on the drop (bar 12).', None),
    (12, 14, 'TITLE', 'Title flash on the drop, lock-up band, names pop a beat apart', 'trim', [('title-s2', 757, '', '')],
     'Hold cut from 4 bars to 2: glint on bar 13, out on bar 14.', None),
    (14, 16, 'MICA', 'Marble Garden 2: lock-on, three Mantises in one flight (100, 200, 500)', 'keep', [('d-mgz2-chain', (A, 65, 14, 4), '', '')],
     'Same take, two bars earlier. First kill on beat 4 of bar 14; the next two are 4 and 3 frames early of the following beats, to be tuned to 21-frame gaps in stage B. Ends before she is hurt (#183).',
     dict(target='kills on bar 14 beat 4, bar 15 beats 1 and 2', probe='delay the second and third strike presses by 4 and 1 frames', fallback='the take as it is (4 and 3 frames early)', tune=True)),
    (16, 18, 'MICA', 'Slanted triptych: the strike in Sonic 1, Sonic 2, Sonic 3 & K', 'trim',
     [('d-ghz2-buzz', (A, 60, 16, 3), '', 'S1'), ('d-arz1-whisp', (A, 138, 16, 4), '', 'S2', 1), ('aiz-hero', (A, 70, 17, 1), '', 'S3K', 2)],
     'Cut from 4 bars to 2. Slices drop on beats 1, 2, 3; the three strikes land on beats 3, 4 and the next downbeat, a 1-2-3.', None),
    (18, 20, 'MICA', 'Hydrocity 1: rolling through the curved channel at speed, out on the spring', 'replace', [('h-hcz1', 228, '', '')],
     'New. A loop at speed; the cut out is the spring launch.', None),
    (20, 21, 'MICA', 'Chemical Plant 1: spindash rev, release off the ledge', 'replace', [('d-cpz1-run', (A, 45, 20, 2), '', '')],
     'New, one bar. The release fires on beat 2 and she drops through the plant at 11 px/f. (After #137 this take slows to a walk, so it stops at one bar.)', None),
    (21, 22, 'MICA', 'Green Hill 1 (Sonic 1): downhill at top speed', 'replace', [('p-ghz-ss-a', 73, '', '')],
     'New, one bar: Sonic 1 in the speed run, so the block is not all Sonic 2.', None),
    (22, 24, 'MICA', 'Emerald Hill 2: corkscrew, then the side spring', 'replace', [('ehz2-chain-b', (A, 133, 23, 3), '', '')],
     'New. Spring on beat 3 of bar 23.', None),
    (24, 26, 'MICA', 'Mushroom Hill 1: mushroom spring into the canopy, ring arc', 'replace', [('f-mhz1-team', (A, 108, 24, 3), '', '')],
     'New. Spring on beat 3; seven rings in half a second.', None),
    (26, 28, 'MICA', 'Casino Night 1: MICA and TALON bounce through the bumpers', 'replace', [('d-cnz2-team', 171, '', '')],
     'Same take as now, moved 131 frames later: the current window ends as the bumpers start. Four bumper hits within 6 frames of beats.',
     dict(target='bumper hits on beats', probe='shift the leap by a few frames', fallback='the window as measured', tune=True)),
    (28, 30, 'TALON', 'Spring Yard 1: flight, lock-on, two Crabmeats (100, 200); lives read TALON', 'trim', [('d-syz1-talon', (A, 118, 28, 4), '', '')],
     'Cut from 4 bars to 2. The kills are 42 frames apart, exactly two beats: beat 4 of bar 28 and beat 2 of bar 29. Lives inset on beat 3. He lands and runs at top speed to the cut.', None),
    (30, 32, 'TALON', 'Hill Top 1: divebomb streak across the lake', 'replace', [('f-htz1-talon', (A, 114, 30, 2), '', '')],
     'Replaces the slow flight pane (mean speed 3.2 px/f, nothing touched). The dive starts on beat 2 and reaches 24 px/f; camera 625 px/s.', None),
    (32, 34, 'TALON', 'Death Egg 1: dive, land, run into the booster', 'replace', [('g-dez1-talon-a', (A, 239, 33, 3), '', '')],
     'Replaces the carry pane, which repeated the cold open. Booster on beat 3 of bar 33.', None),
    (34, 36, 'TALON', 'Aquatic Ruin 1: TALON divebombs two Whisps in a row', 're-stage', [('f-lbz1-talon', 109, '', 'stand-in (fallback)')],
     'New. His Sonic 2 hits, on the two bars before the drop. He has kills in Sonic 1 and Sonic 3 & K on disk but none in Sonic 2.',
     dict(target='kills on bar 34 beat 3 and bar 35 beat 1', probe='TALON solo at the position of MICA\'s Whisp take (8300, 860)',
          fallback='Launch Base 1 flight over the dome (f-lbz1-talon #109-277), no kill')),
    (36, 37, 'EVERY SCREEN', 'Lockstep split, Chemical Plant 1: run, jump, roll', 'trim',
     [('f-stock-cpz-medley', 80, '', 'stock'), ('f-cpz-medley', 80, '', 'mod')],
     'The 1.5 s of look-up and duck (speed 0) is cut out: the split now plays two moving bars with a cut on bar 37.', None),
    (37, 38, 'EVERY SCREEN', 'Lockstep split: spindash release into the spring', 'trim',
     [('f-stock-cpz-medley', (A, 289, 37, 2), '', 'stock'), ('f-cpz-medley', (A, 289, 37, 2), '', 'mod')],
     'Release on beat 2 in both halves. The line lands here.', None),
    (38, 40, 'EVERY SCREEN', 'Lockstep split, Emerald Hill 1 at top speed', 'replace',
     [('f-stock-ehz1-run', 709, '', 'stock'), ('f-ehz1-run', 709, '', 'mod')],
     'New window from takes on disk: the same inputs at 7.4 px/f. From the act start (TIME 0:11), as the Chemical Plant split is; a positioned mid-act pair will be tried in stage B.', None),
    (40, 42, 'EVERY SCREEN', 'Slanted triptych: the three title screens', 'trim',
     [('title-s1', 408, '', 'S1'), ('title-s2', 841, '', 'S2', 1), ('title-s3k', 321, '', 'S3K', 2)],
     'Cut from 4 bars to 2; slices on beats 1, 2, 3.', None),
    (42, 43, 'EVERY SCREEN', 'Signposts spin and land on MICA: Sonic 1 and Sonic 2', 'trim',
     [('d-ghz-clear', 227, '', 'S1', 0, 'act clear, no control'), ('d-ehz-clear', 377, '', 'S2', 0, 'act clear, no control')],
     'Was 2 bars of running in and standing (idle 2.0 s and 1.4 s). Now one bar that starts mid-spin; both signs land on her face on beat 4.', None),
    (43, 44, 'EVERY SCREEN', 'Sonic 2 tally: MICA GOT THROUGH flies in', 'trim', [('d-ehz-clear', 471, '', '', 0, 'results tally')],
     'Was 2 bars, static after the fly-in. Now the fly-in only.', None),
    (44, 46, 'EVERY SCREEN', 'Slanted triptych: the three special stages', 'trim',
     [('f-ghz-ss', 916, '', 'S1'), ('halfpipe-run', 741, '', 'S2', 1), ('q-blue-c', 431, '', 'S3K', 2)],
     'Cut from 4 bars to 2; slices on beats 1, 2, 3.', None),
    (46, 48, 'EVERY SCREEN', '2x2: Continue, Data Select, special-stage HUD names, lives TALON', 'trim',
     [('continue', 77, '', ''), ('data-select', 405, '', '')],
     'Cut from 3 bars to 2; cells pop on beats 1 to 4 of bar 46.', None),
    (48, 50, 'EVERY SCREEN', 'Sky Chase: MICA strikes three badniks from the wing; TALON pilots', 'trim', [('h-scz-b', (A, 259, 48, 2), '', '')],
     'Cut from 4 bars to 2 and moved next to the ending, so the Tornado plays as one beat. First kill on beat 2; the other two are 3 and 6 frames early of their beats, to be tuned in stage B. Callout on beat 3 of bar 49.',
     dict(target='kills on bar 48 beat 2, bar 49 beats 1 and 3', probe='stretch the two gaps from 60 and 39 frames to 63 and 42', fallback='the take as it is', tune=True)),
    (50, 51, 'EVERY SCREEN', 'Sonic 2 ending: MICA flies beside the Tornado', 'trim', [('ending', 2676, '', '', 0, 'ending cutscene')],
     'Was 1.5 bars; one bar.', None),
    (51, 52, 'EVERY SCREEN', 'Ending pose: MICA lands on the wing, TALON at the stick', 'trim', [('ending', (A, 4098, 51, 2), '', '', 0, 'ending cutscene')],
     'Was 2 bars; one bar, the landing on beat 2.', None),
    (52, 54, 'BUILD', 'Metropolis 1: the fastest normal-form run, 11 px/f', 'replace', [('h-mtz1-asteron', 271, '', '')],
     'New. Opens the build into the chorus.', None),
    (54, 56, 'BUILD', 'Launch Base 1: down the slope, spring, ring line', 'replace', [('h-lbz1', (A, 143, 54, 3), '', '')],
     'New. Spring on beat 3.', None),
    (56, 57, 'BUILD', 'Green Hill 2 (Sonic 1): monitor pop on the low road', 'replace', [('d-ghz2-buzz', (A, 264, 56, 2), '', '')],
     'New window of a take already in the film. One bar.', None),
    (57, 58.5, 'BUILD', 'Emerald Hill 2: run-up and a Buzzer struck on the bar', 'replace', [('ehz2-chain-b', (A, 281, 58, 1), '', '')],
     'New. The kill lands on bar 58; the Gilded run-in starts two beats later.', None),
    (58.5, 62, 'POWERED UP', 'Hydrocity 1: normal MICA jumps, winds up, snaps open gold; Gilded run, spring', 'trim',
     [('d-hcz1-gilded-runin', (A, 160, 60, 1), '', '')],
     'Cut from 5.5 bars to 3.5. Reveal on the chorus (bar 60) as now; the spring lands on beat 3 of bar 61 and the shot ends on bar 62.', None),
    (62, 64, 'POWERED UP', 'Same Rhinobot twice: jade trail above, gold trail below', 'trim',
     [('d-aiz-normal', (A, 55, 62, 3), '', 'normal'), ('gilded-aiz', (A, 93, 63, 1), '', 'Gilded')],
     'Cut from 3.5 bars to 2; the two strikes land two beats apart.', None),
    (64, 65, 'POWERED UP', 'Gilded MICA in Sonic 1: Star Light at speed', 'replace', [('f-slz1-gilded', 112, '', '')],
     'Was a triptych pane. One bar, full frame.', None),
    (65, 66, 'POWERED UP', 'Gilded MICA in Sonic 2: Aquatic Ruin treetops, spring', 'replace', [('s2-gilded-arz', (A, 251, 65, 2), '', '')],
     'New. 10 px/f; spring on beat 2.', None),
    (66, 67.5, 'POWERED UP', 'Gilded MICA in Sonic 2: gold streak through the Chemical Plant tubes', 'replace', [('f-cpz1-gilded', (A, 238, 66, 2), '', '')],
     'New. Spring on beat 2.', None),
    (67.5, 70, 'POWERED UP', 'Solar TALON: wind-up, flame reveal on bar 68, straight into a divebomb kill on bar 69', 're-stage',
     [('d-cnz1-solar', (A, 76, 68, 1), '', 'stand-in')],
     'Was 4.5 bars with 3.5 s of slow hovering after the reveal (mean speed 2.4 px/f, nothing touched). Now 2.5 bars: reveal, then he dives at once and the kill lands a bar later, embers trailing.',
     dict(target='reveal on bar 68; kill on bar 69', probe='Solar TALON at the Angel Island Rhinobot position (his solar kill take is there): transform within reach, dive on the next bar',
          fallback='the Carnival Night take to bar 69, then its own fast flight (#190-274) for bar 69-70, a time cut inside the take, disclosed')),
    (70, 72, 'POWERED UP', 'Solar TALON in Death Egg 1: ember flight into the booster', 'replace', [('g-dez1-solar', (A, 331, 71, 2), '', '')],
     'New. Booster on beat 2 of bar 71.', None),
    (72, 73, 'POWERED UP', 'Solar TALON in Sonic 1: Spring Yard', 'replace', [('g-syz1-solar', 405, '', '')],
     'One bar at 7.8 px/f; with the next shot it replaces the slow Mystic Cave pane as the proof in the other two games.', None),
    (73, 74, 'POWERED UP', 'Solar TALON in Sonic 2: Hill Top', 'replace', [('f-htz1-solar', 165, '', '')],
     'One bar: the dive across the lake, with embers.', None),
    (74, 75.5, 'POWERED UP', 'Solar TALON divebombs a Rhinobot in Angel Island', 'trim', [('d-aiz-solar-dive', (A, 186, 74, 3), '', '')],
     'Was a triptych pane with 1.6 s of approach. Full frame, the kill on beat 3 of bar 74.', None),
    (75.5, 78, 'HERO', 'Death Egg 1: Hyper MICA reveal on the lift, one strike, after-image dash', 'keep', [('d-dez1-hyper', (A, 185, 77, 1), '', '')],
     'Same take and length. The kill now sits exactly on bar 77; the reveal is then 4 frames early of bar 76. In stage B the strike press moves 4 frames earlier so both land.',
     dict(target='reveal on bar 76 and kill on bar 77', probe='strike press 4 frames earlier', fallback='kill on the bar, reveal 4 frames early', tune=True)),
    (78, 80, 'HERO', 'Launch Base 1 mini-boss: Hyper MICA runs in and strikes once; ONE HIT.', 're-stage', [('d-lbz-boss', (A, 648, 79, 1), '', 'stand-in')],
     'She stands and waits 1.4 s for the boss in the current take. Re-staged so she is moving until the hop: back off inside the locked arena, run in as it swings down, strike on bar 79. The card and the revert it covers are unchanged.',
     dict(target='no standing; hit on bar 79', probe='after the camera locks: L for about 30 frames, R, jump', fallback='the current take cut in half a bar later (the Death Egg shot runs to 78.5)')),
    (80, 84, 'HERO: THE PAIR', 'Launch Base 1: twin transformation, then TALON catches Hyper MICA and flies her across the skyline', 're-stage',
     [('d-lbz-pair-312', 49, '', 'stand-in')],
     'The twin reveal on beat 2 stays. Two things change: nobody stands (TALON lifts off on the reveal instead of walking over for 0.8 s), and the carry travels across the towers instead of rising in place (now 1 px/f, camera 66 px/s).',
     dict(target='reveal on bar 80 beat 2, catch on bar 81, then 3 px/f of travel to the end card', probe='start about 650 px left of the starpost on the open bridge so the carry can fly right for 3 bars; hold R with the flaps',
          fallback='the current take')),
    (84, 88, 'END CARD', 'Lock-up, line, URL, disclaimer over the pair take; music fades bars 85-88', 'keep', [('d-lbz-pair-312', 415, '', '', 0, 'end card backdrop')],
     'Unchanged.', None),
]

# ---- verdicts for the current cut: shot index -> (verdict, where it goes)
VERDICT = {
    0: ('keep', 'bars 0-2, unchanged'),
    1: ('re-stage', 'bars 2-4: same act from a run-up, top speed, spring on a beat'),
    2: ('re-stage', 'bars 4-6: 4 bars to 2, a catch in motion and travel after it'),
    3: ('replace', 'bars 8-10: Hyper loops in Mushroom Hill (this kill is shown again at bar 77)'),
    4: ('trim', 'bars 10-14: lock-up hold 4 bars to 2'),
    5: ('keep', 'bars 14-16: kills re-timed to beats'),
    6: ('trim', 'bars 16-18: 4 bars to 2, strikes on consecutive beats'),
    7: ('trim', 'bars 48-50: 4 bars to 2, beside the ending'),
    8: ('replace', 'bars 26-28: same take, the bumper window'),
    9: ('trim', 'bars 28-30: 4 bars to 2, both kills on beats'),
    10: ('replace', 'bars 30-36: three full-frame shots (lake streak, booster run, Sonic 2 kills); the dive kill moves to bar 6'),
    11: ('trim', 'bars 36-38: look-up and duck cut out; plus a top-speed split at 38-40'),
    12: ('trim', 'bars 40-42: 4 bars to 2'),
    13: ('trim', 'bar 42: 2 bars to 1, from mid-spin'),
    14: ('trim', 'bar 43: 2 bars to 1, the fly-in only'),
    15: ('trim', 'bars 44-46: 4 bars to 2'),
    16: ('trim', 'bars 46-48: 3 bars to 2'),
    17: ('trim', 'bar 50: 1.5 bars to 1'),
    18: ('trim', 'bar 51: 2 bars to 1, landing on a beat'),
    19: ('trim', 'bars 58.5-62: 5.5 bars to 3.5'),
    20: ('trim', 'bars 62-64: 3.5 bars to 2'),
    21: ('re-stage', 'bars 67.5-70: reveal straight into a divebomb kill'),
    22: ('replace', 'bars 64-67.5 and 72-75.5: one-bar full-frame shots at speed; the dive kill tightened'),
    23: ('keep', 'bars 75.5-78: kill moved onto bar 77'),
    24: ('re-stage', 'bars 78-80: she runs in instead of waiting'),
    25: ('re-stage', 'bars 80-84: no standing, and the carry travels'),
    26: ('keep', 'bars 84-88, unchanged'),
}
NAMES = ['S3K title roll-in', 'Launch Base duo', 'The carry', 'Hyper fragment (Death Egg)', 'Sonic 2 title + lock-up', 'Marble Garden chain',
         'Strike triptych', 'Sky Chase', 'Casino Night duo', 'TALON, Spring Yard', 'TALON verbs triptych', 'Lockstep split',
         'Titles triptych', 'Signposts', 'Sonic 2 tally', 'Special stages', 'UI grid', 'Ending, side view', 'Ending, pose',
         'Gilded run-in', 'Jade and gold trails', 'Solar TALON, Carnival Night', 'Powered triptych', 'Hyper MICA, Death Egg',
         'Launch Base mini-boss', 'The pair', 'End card']

F13 = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Regular.ttf', 13)
F13B = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 13)
F16B = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 16)
F24B = ImageFont.truetype('/usr/share/fonts/TTF/FiraSans-Bold.ttf', 24)
_FR = {}


# title stills are cropped to the rows the film shows (the SEGA plate and copyright rows are outside its windows)
CROP = {'title-s1': (0, 0, 320, 147), 'title-s2': (0, 26, 320, 206), 'title-s3k': (0, 8, 320, 188)}


def frame(take, i):
    if take not in _FR:
        _FR[take] = sorted((T / 'captures' / take / 'frames').glob('*.png'))
    fr = _FR[take]
    im = Image.open(fr[max(0, min(len(fr) - 1, int(i)))]).convert('RGB')
    if take in CROP:
        c = im.crop(CROP[take])
        im = Image.new('RGB', (320, 224), (0, 0, 0))
        im.paste(c, (0, (224 - c.height) // 2))
    return im


def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def jpg(im, q=80):
    buf = io.BytesIO()
    im.convert('RGB').save(buf, 'JPEG', quality=q, optimize=True)
    return b64(buf.getvalue(), 'image/jpeg')


def hard(e):
    return e['kind'] in ('kill', 'boss hit', 'spring', 'spindash')


def evtext(evs, limit=7):
    out, rings = [], 0
    for e in evs:
        if e['kind'] == 'rings':
            rings += int(e['detail'])
        elif e['kind'] == 'ring loss' and e['detail'] in ('-2',):
            continue                      # Super/Hyper ring drain, not a hit
        elif e['kind'] == 'kill' and e['detail'] == '+10':
            out.append('bumper')
        elif e['kind'] == 'air burst':
            out.append('strike or dive')
        else:
            out.append((e['kind'] + ' ' + e['detail']).strip())
    seen = []
    for o in out:
        if seen and seen[-1][0] == o:
            seen[-1][1] += 1
        else:
            seen.append([o, 1])
    s = [f'{n}x {o}' if n > 1 else o for o, n in seen][:limit]
    if rings:
        s.append(f'{rings} rings')
    return ', '.join(s) if s else 'none'


def build_plan():
    rows = []
    for b0, b1, chap, name, status, panes, why, rs in PLAN:
        f0, f1 = bf(b0), (END if b1 == 88 else bf(b1))
        n = f1 - f0
        pp = []
        for pane in panes:
            take, src, key, lab = pane[:4]
            enter = round(pane[4] * (bf(b0, 2) - f0)) if len(pane) > 4 else 0
            screen = len(pane) > 5 and pane[5]
            if isinstance(src, tuple):
                _, ev, ab, abeat = src
                src0 = ev - (bf(ab, abeat) - f0)
            else:
                src0 = src
            a, b = src0 + enter, src0 + n
            ma, mb = (rs or {}).get('m', (a, b))
            m = pacing.measure(take, list(range(ma, mb, 2)), key)
            if screen and m['kind'] == 'level':
                m = dict(m, kind=screen)
            hits = []
            if m['kind'] == 'level':
                for e in m['events']:
                    if hard(e) and a <= e['src'] < b:
                        bar, beat, dev = near_beat(f0 + e['src'] - src0)
                        hits.append(dict(kind=(e['kind'] + ' ' + e['detail']).strip(), src=e['src'], bar=bar, beat=beat, dev=dev))
            pp.append(dict(take=take, src0=a, src1=b, label=lab, m=m, hits=hits))
        rows.append(dict(b0=b0, b1=b1, f0=f0, f1=f1, t0=f0 / 60, t1=f1 / 60, chapter=chap, name=name, status=status, panes=pp, why=why, restage=rs))
    return rows


def thumbs(row, w=150, n=3):
    cells = []
    for p in row['panes'][:3]:
        k = n if len(row['panes']) == 1 else (2 if len(row['panes']) == 2 else 1)
        hits = [h['src'] for h in p['hits']]
        if k == 1:
            pick = [hits[0] + 3 if hits else (p['src0'] + p['src1']) // 2]
        else:
            pick = [p['src0'] + round((p['src1'] - p['src0']) * q) for q in ((0.12, 0.5, 0.88) if k == 3 else (0.3, 0.75))]
            if hits:
                j = min(range(k), key=lambda i: abs(pick[i] - hits[0]))
                pick[j] = hits[0] + 3
        if row['restage'] and 'm' in row['restage']:
            a, b = row['restage']['m']
            pick = [a + round((b - a) * q) for q in (0.1, 0.5, 0.95)][:k]
        for i in pick:
            cells.append((p['take'], i))
    h = round(w * 224 / 320)
    s = Image.new('RGB', (len(cells) * (w + 3) - 3, h), (26, 26, 25))
    for k, (take, i) in enumerate(cells):
        s.paste(frame(take, i).resize((w, h), Image.BOX), (k * (w + 3), 0))
    return s, cells


def timeline_svg(cur, plan, W=1340):
    """Two rows of shots on the tracked bar grid, coloured by verdict; hover gives the shot."""
    X0, X1 = 96, W - 16
    sx = lambda t: X0 + (X1 - X0) * t / (END / 60)
    o = [f'<svg viewBox="0 0 {W} 214" width="100%" role="img" aria-label="Old and new cut timelines" style="background:#1a1a19;border-radius:6px">']
    secs = [(0, 'intro'), (12, 'A (drop)'), (28, 'break'), (36, 'B (drop)'), (52, 'build'), (60, 'chorus'), (76, 'lift'), (84, 'fade')]
    for b in range(0, 89, 4):
        x = sx(BT[b])
        o.append(f'<line x1="{x:.1f}" y1="34" x2="{x:.1f}" y2="170" stroke="#383835" stroke-width="1"/>')
        o.append(f'<text x="{x:.1f}" y="186" fill="#c3c2b7" font-size="11" text-anchor="middle">{b}</text>')
    for b, lab in secs:
        o.append(f'<text x="{sx(BT[b]) + 3:.1f}" y="26" fill="#c3c2b7" font-size="12">{lab}</text>')
    o.append(f'<text x="{X0 - 8}" y="186" fill="#c3c2b7" font-size="11" text-anchor="end">bar</text>')
    for y, lab, rows in ((44, 'current cut', cur), (112, 'new plan', plan)):
        o.append(f'<text x="{X0 - 8}" y="{y + 30}" fill="#f0efec" font-size="13" text-anchor="end">{lab}</text>')
        o.append(f'<text x="{X0 - 8}" y="{y + 46}" fill="#c3c2b7" font-size="11" text-anchor="end">{len(rows)} shots</text>')
        for r in rows:
            xa, xb = sx(r['t0']) + 1, sx(r['t1']) - 1
            o.append(f'<rect x="{xa:.1f}" y="{y}" width="{max(1.5, xb - xa):.1f}" height="50" rx="2" fill="{CAT[r["status"]]}">'
                     f'<title>{esc(r["name"])}\n{r["t0"]:.2f}-{r["t1"]:.2f} s ({r["t1"] - r["t0"]:.1f} s)\n{r["status"]}</title></rect>')
    x = X0
    for k, lab in CATLAB.items():
        o.append(f'<rect x="{x}" y="196" width="12" height="12" rx="2" fill="{CAT[k]}"/><text x="{x + 18}" y="206" fill="#f0efec" font-size="12">{lab}</text>')
        x += 40 + 7 * len(lab)
    o.append('</svg>')
    return ''.join(o)


def main():
    cur_raw = json.load(open(C / 'pacing-current.json'))
    for r in cur_raw:                     # re-measure from the recorded source ranges (same frames, current detector)
        for p in r['panes']:
            if p['kind'] == 'level':
                p.update(pacing.measure(p['capture'], list(range(p['src'][0], p['src'][1] + 1, 2))))
    json.dump(cur_raw, open(C / 'pacing-current.json', 'w'), indent=1)
    plan = build_plan()
    cur = [dict(name=NAMES[r['shot']], t0=r['t0'], t1=r['t1'], status=VERDICT[r['shot']][0]) for r in cur_raw]

    # ---- table 1: the current cut
    t1 = []
    for r in cur_raw:
        v, goes = VERDICT[r['shot']]
        panes = r['panes'] or [dict(kind='card', capture='')]
        for k, p in enumerate(panes):
            lev = p['kind'] == 'level'
            g = f"{p['mean_gspeed']}" if lev else '-'
            sp = f"{p['mean_speed'] / 256:.1f}" if lev else '-'
            idle = f"{p['idle_s']:.1f}" if lev else '-'
            inter = evtext(p['events']) if lev else p['kind'].replace('_', ' ')
            first = (f"<td rowspan={len(panes)} class=n>{r['shot'] + 1}</td><td rowspan={len(panes)}><b>{esc(NAMES[r['shot']])}</b></td>"
                     f"<td rowspan={len(panes)} class=t>{r['t0']:.2f}-{r['t1']:.2f}</td>") if k == 0 else ''
            last = (f"<td rowspan={len(panes)} class=v><span class=chip style='background:{CAT[v]}'></span>{v}</td><td rowspan={len(panes)}>{esc(goes)}</td>") if k == 0 else ''
            slow = ' class=slow' if lev and (p['mean_speed'] < 768 or p['idle_s'] >= 0.7) else ''
            t1.append(f"<tr>{first}<td class=c>{esc(p.get('capture', ''))}</td><td class=r{' slow' if slow else ''}>{g}</td><td class=r>{sp}</td><td class=r{' slow' if lev and p['idle_s'] >= 0.7 else ''}>{idle}</td><td>{esc(inter)}</td>{last}</tr>")

    # ---- table 2: the new plan
    t2, chap = [], None
    for k, r in enumerate(plan):
        if r['chapter'] != chap:
            chap = r['chapter']
            t2.append(f"<tr class=chap><td colspan=6>{esc(chap)}</td></tr>")
        strip, _ = thumbs(r)
        stats = []
        for p in r['panes']:
            m = p['m']
            lab = f"<span class=dim>{esc(p['label'])}: </span>" if p['label'] else ''
            src = f"<code>{p['take']}</code> #{p['src0']}-{p['src1']}"
            if m['kind'] == 'level':
                hits = '; '.join(f"{h['kind']} on bar {h['bar']} beat {h['beat']}" + (f" ({h['dev']:+d} f)" if h['dev'] else '') for h in p['hits'][:6])
                stats.append(f"{lab}{src}<br>|gspeed| {m['mean_gspeed']}, speed {m['mean_speed'] / 256:.1f} px/f, camera {m['cam_px_per_s']} px/s, idle {m['idle_s']:.1f} s"
                             + (f"<br>{esc(hits)}" if hits else ''))
            else:
                stats.append(f"{lab}{src}<br><span class=dim>{m['kind'].replace('_', ' ')}</span>")
        rs = r['restage']
        extra = ''
        if rs:
            kind = 'Tune in stage B' if rs.get('tune') else 'Re-stage in stage B'
            extra = (f"<div class=rs><b>{kind}.</b> Target: {esc(rs['target'])}. Probe: {esc(rs['probe'])}. Fallback: {esc(rs['fallback'])}.</div>")
        bars = f"{r['b0']:g}-{r['b1']:g}"
        t2.append(f"<tr><td class=n>{k + 1}</td><td class=t>{bars}<br><span class=dim>{r['t0']:.2f}-{r['t1']:.2f}<br>{r['t1'] - r['t0']:.1f} s</span></td>"
                  f"<td class=i><img src='{jpg(strip)}' alt='stills for shot {k + 1}'></td>"
                  f"<td class=w><b>{esc(r['name'])}</b><br>{esc(r['why'])}{extra}</td><td class=s>{'<hr>'.join(stats)}</td>"
                  f"<td class=v><span class=chip style='background:{CAT[r['status']]}'></span>{r['status']}</td></tr>")

    # ---- numbers for the summary. Idle is counted once per shot (its slowest pane), gameplay shots only;
    # act-clear, tally and ending screens are counted by their length instead.
    SCREENS_CUR = {13, 14, 17, 18}
    cur_durs = [r['t1'] - r['t0'] for r in cur]
    new_durs = [r['t1'] - r['t0'] for r in plan]
    pidle = lambda ps: max([p['idle_s'] for p in ps if p['kind'] == 'level'] or [0])
    cur_idle = sum(pidle(r['panes']) for r in cur_raw if r['shot'] not in SCREENS_CUR and r['shot'] != 26)
    cur_screens = sum(r['t1'] - r['t0'] for r in cur_raw if r['shot'] in SCREENS_CUR)
    midle = lambda r: max([p['m']['idle_s'] for p in r['panes'] if p['m']['kind'] == 'level'] or [0])
    new_idle = sum(midle(r) for r in plan if r['status'] != 're-stage')
    stand_idle = sum(midle(r) for r in plan if r['status'] == 're-stage')
    new_screens = sum(r['t1'] - r['t0'] for r in plan if any(p['m']['kind'] in ('act clear, no control', 'results tally', 'ending cutscene') for p in r['panes']))
    noscore = set()
    for r in plan:
        for p in r['panes']:
            if p['m']['kind'] == 'level' and r['status'] != 're-stage':
                row = pacing.rows(p['take'])[max(1, p['src0'])]
                if pacing.num(row, 'score', 0) == 0:
                    noscore.add(p['take'])
    hits = [h for r in plan if r['status'] != 're-stage' for p in r['panes'] for h in p['hits'] if h['kind'].startswith(('kill', 'boss'))]
    onbeat = sum(1 for h in hits if abs(h['dev']) <= 2)
    counts = {k: sum(1 for r in plan if r['status'] == k) for k in CAT}
    ccounts = {k: sum(1 for r in cur if r['status'] == k) for k in CAT}
    summary = dict(current=dict(shots=len(cur), mean_s=round(sum(cur_durs) / len(cur_durs), 2), longest_s=round(max(cur_durs), 2), idle_s=round(cur_idle, 1),
                                act_clear_and_cutscene_s=round(cur_screens, 1), verdicts=ccounts),
                   plan=dict(shots=len(plan), mean_s=round(sum(new_durs) / len(new_durs), 2), longest_s=round(max(new_durs), 2),
                             idle_s_takes_on_disk=round(new_idle, 1), idle_s_restage_standins=round(stand_idle, 1),
                             act_clear_and_cutscene_s=round(new_screens, 1), takes_without_declared_score=sorted(noscore), statuses=counts,
                             kills_measured=len(hits), kills_within_2_frames_of_a_beat=onbeat))
    json.dump(dict(summary=summary, plan=[{k: v for k, v in r.items()} for r in plan]), open(C / 'plan.json', 'w'), indent=1, default=str)
    restages = [r for r in plan if r['restage'] and not r['restage'].get('tune')]
    tunes = [r for r in plan if r['restage'] and r['restage'].get('tune')]

    doc = f'''<!doctype html><meta charset=utf-8><title>MICA &amp; TALON promo: pacing re-storyboard (checkpoint 4)</title>
<style>
body{{background:#0e1222;color:#e8ecf6;font:15px/1.5 system-ui,sans-serif;max-width:1500px;margin:0 auto;padding:28px}}
h1{{font-size:28px;margin:0 0 4px}}h2{{margin:40px 0 10px;font-size:22px;border-bottom:2px solid #2449db;padding-bottom:6px}}
table{{border-collapse:collapse;font-size:13.5px;width:100%}}td,th{{border:1px solid #2a3355;padding:5px 8px;vertical-align:top;text-align:left}}
th{{background:#18203d;position:sticky;top:0}}td.n{{text-align:right;color:#aab3cf}}td.t{{white-space:nowrap;font-variant-numeric:tabular-nums}}
td.r{{text-align:right;font-variant-numeric:tabular-nums}}td.c{{font-family:ui-monospace,monospace;font-size:12px;color:#c9d1ea}}td.s{{font-size:12.5px;min-width:300px}}
td.slow{{background:#3a2412;font-weight:600}}td.v{{white-space:nowrap}}table.plan{{table-layout:fixed}}table.plan td.s{{min-width:0}}table.plan img{{max-width:100%;height:auto}}tr.chap td{{background:#18203d;font-weight:700;letter-spacing:.04em}}
img{{display:block;border:1px solid #2a3355;image-rendering:pixelated}}hr{{border:0;border-top:1px solid #2a3355;margin:5px 0}}
.box{{background:#151b33;border-left:4px solid #ffdc5a;padding:12px 16px;margin:12px 0}}.rs{{background:#2a1c14;border-left:3px solid #d95926;padding:5px 8px;margin-top:6px;font-size:12.5px}}
code{{background:#1b2342;padding:1px 4px;border-radius:3px;font-size:12px}}li{{margin:5px 0}}.dim{{color:#aab3cf}}
.chip{{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:6px;vertical-align:-1px}}
.kpi{{display:flex;gap:14px;flex-wrap:wrap}}.kpi div{{background:#151b33;padding:10px 16px;border-radius:6px;min-width:150px}}.kpi b{{display:block;font-size:24px}}
</style>
<h1>MICA &amp; TALON promo: pacing re-storyboard</h1>
<p class=dim>Checkpoint 4, stage A of the 2026-11-12 revision. No new captures: every picture and number is from takes already on disk
(<code>~/scratch/agent-tmp/mt-promo-redo-20261111/captures</code>). Nothing here is rendered; this is the plan to approve before stage B.</p>

<div class=kpi>
<div><span class=dim>Shots</span><b>{len(cur)} &rarr; {len(plan)}</b></div>
<div><span class=dim>Mean shot</span><b>{summary['current']['mean_s']:.1f} s &rarr; {summary['plan']['mean_s']:.1f} s</b></div>
<div><span class=dim>Longest shot</span><b>{summary['current']['longest_s']:.1f} s &rarr; {summary['plan']['longest_s']:.1f} s</b></div>
<div><span class=dim>Slow, untouched gameplay</span><b>{cur_idle:.1f} s &rarr; {new_idle:.1f} s</b><span class=dim>plus {stand_idle:.1f} s in the re-stage stand-ins, which stage B removes</span></div>
<div><span class=dim>Signposts, tally, ending</span><b>{cur_screens:.1f} s &rarr; {new_screens:.1f} s</b></div>
<div><span class=dim>Length</span><b>124.0 s</b><span class=dim>unchanged: bars 0-88, fade 85-88</span></div>
</div>

<div class=box><b>Decisions to check</b><ul>
<li><b>Length stays 124 s.</b> The music is not cut, so the film ends where the fade ends; ending earlier would lose the lift (bars 76-84) under the hero moment. The time freed by trimming goes to faster footage, not to a shorter film.</li>
<li><b>Two-bar cuts as the base, one-bar cuts in the builds.</b> Five shots run longer than two bars: the Gilded run-in (3.5), the Solar and Hyper reveals (2.5 each), the pair (4) and the end card. Every 4-bar phrase starts on a cut.</li>
<li><b>"Every screen" shrinks from 22 bars to 16</b> and its idle parts go: the look-up and duck in the lockstep split, the standing after the signposts, the static tally. A second, top-speed lockstep window is added.</li>
<li><b>{counts['replace']} shots use a faster window or a take already on disk</b> (loops, tube, corkscrew, springs, boosters, the lake dive). {counts['trim']} are the current shots made shorter, {counts['keep']} are kept.</li>
<li><b>{counts['re-stage']} re-stages need a probe in stage B</b>, each with a fallback that exists today: the Launch Base duo, the carry swoop, TALON's Sonic 2 kills, the Solar reveal-into-kill, the boss run-in and the pair.</li>
<li><b>The Hyper fragment in the cold open changes</b> from the Death Egg kill to the Mushroom Hill loops, so that kill is no longer shown twice.</li>
<li><b>Sky Chase moves</b> from bar 22 to bar 48, next to the ending, so TALON's Tornado is one beat. The Tornado's stock "SONIC" decal is still on screen in both; you have not ruled on it yet.</li>
</ul></div>

<h2>1. Cut timeline</h2>
{timeline_svg(cur, plan)}
<p class=dim>Hover a block for the shot. Grid lines are the tracked 4-bar phrases.</p>

<h2>2. The current cut, measured</h2>
<p>From <code>tools/pacing.py</code>: the exact source frames each shot shows, read against the take's per-frame state CSV.
<b>Mean |gspeed|</b> is in the CSV's units (256 = 1 px/frame). It reads 0 or stale in the air, so flight and jumps also get <b>speed</b>
(px/frame: the larger of the velocity and the real frame-to-frame movement). <b>Idle</b> is time below 1.5 px/frame with no interaction within half a second.
"Strike or dive" is a one-frame airborne velocity step: a homing strike or a divebomb starting. Shaded cells are the slow ones:
speed under 3 px/frame, or 0.7 s or more idle. Screens that are not gameplay have no speed.</p>
<table><tr><th>#</th><th>Shot</th><th>Time (s)</th><th>Take</th><th>Mean |gspeed|</th><th>Speed px/f</th><th>Idle s</th><th>Interactions</th><th>Verdict</th><th>In the new plan</th></tr>
{''.join(t1)}</table>

<h2>3. The new plan</h2>
<p>Bars are the tracked bars of the owner's track. Each source window is placed so its hit lands on a beat; the offset from that beat is in frames
("+3 f" is 50 ms late). Stage B captures sound with the picture, so these offsets are what will be heard. Stills are from the takes on disk;
for a re-stage they are a stand-in from the nearest existing take. Title stills are cropped to the rows the film shows.</p>
<table class=plan><colgroup><col style="width:36px"><col style="width:96px"><col style="width:476px"><col><col style="width:330px"><col style="width:104px"></colgroup>
<tr><th>#</th><th>Bars<br><span class=dim>time</span></th><th>Stills</th><th>Shot and why</th><th>Source window, measured</th><th>Status</th></tr>
{''.join(t2)}</table>

<h2>4. Stage B probes</h2>
<p>Re-stages ({len(restages)}):</p><ul>
{''.join(f"<li><b>Bars {r['b0']:g}-{r['b1']:g}, {esc(r['name'])}.</b> Target: {esc(r['restage']['target'])}. Probe: {esc(r['restage']['probe'])}. Fallback: {esc(r['restage']['fallback'])}.</li>" for r in restages)}
</ul><p>Timing tunes on takes that already work ({len(tunes)}):</p><ul>
{''.join(f"<li><b>Bars {r['b0']:g}-{r['b1']:g}, {esc(r['name'])}.</b> {esc(r['restage']['target'])}; {esc(r['restage']['probe'])}. Fallback: {esc(r['restage']['fallback'])}.</li>" for r in tunes)}
</ul>
<p>Of the {len(hits)} kills, bumper hits and boss hits measured in takes on disk, {onbeat} land within 2 frames of a beat with these windows; the rest are second hits of a chain or the tunes above.
{len(noscore)} of the takes picked here were shot without a declared score (their HUD reads SCORE 0): {', '.join(f'<code>{t}</code>' for t in sorted(noscore))}. Stage B re-captures them through the positioned host with a plausible score, as before. The exceptions are the takes that start an act (Sky Chase and the two lockstep pairs), where a low score is the true one.</p>

<h2>5. What stage A did not do</h2>
<ul><li>No ROM time was used: no probes, no captures. The re-stages are plans, not footage.</li>
<li>Nothing was rendered or mastered; <code>edit/edit.py</code> is unchanged.</li>
<li>Sound is not part of this page. Stage B drops the placed stingers and uses each take's own SFX-only audio (<code>--audio --no-music</code>).</li></ul>
'''
    (C / 'storyboard.html').write_text(doc)
    print(C / 'storyboard.html', f'{len(doc) / 1e6:.2f} MB')
    print(json.dumps(summary))
    return plan, cur, cur_raw, summary


def png(plan, cur, cur_raw, summary):
    """The same storyboard as one PNG under 512 KB: numbers, timeline, one still per new shot, the verdict table."""
    INK, DIM, BG, SURF = (240, 239, 236), (195, 194, 183), (14, 18, 34), (26, 26, 25)
    hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    for tw, colours in ((150, 96), (136, 72), (120, 56), (104, 40)):
        W, cols = 1560, 9
        th = round(tw * 224 / 320)
        cw = (W - 40) // cols
        rows_n = (len(plan) + cols - 1) // cols
        H = 250 + rows_n * (th + 62) + 40 + (len(cur_raw) + 1) * 19 + 30
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.text((20, 14), 'MICA & TALON promo: pacing re-storyboard (checkpoint 4)', font=F24B, fill=INK)
        s = summary
        d.text((20, 48), f"Shots {s['current']['shots']} to {s['plan']['shots']}   mean shot {s['current']['mean_s']:.1f} s to {s['plan']['mean_s']:.1f} s   "
               f"longest {s['current']['longest_s']:.1f} s to {s['plan']['longest_s']:.1f} s   slow, untouched gameplay {s['current']['idle_s']:.1f} s to "
               f"{s['plan']['idle_s_takes_on_disk']:.1f} s (+{s['plan']['idle_s_restage_standins']:.1f} s in re-stage stand-ins)   signposts, tally, ending "
               f"{s['current']['act_clear_and_cutscene_s']:.1f} s to {s['plan']['act_clear_and_cutscene_s']:.1f} s   length 124.0 s, unchanged", font=F13, fill=DIM)
        # timeline
        X0, X1 = 110, W - 20
        sx = lambda t: X0 + (X1 - X0) * t / (END / 60)
        d.rounded_rectangle((14, 72, W - 14, 236), 6, fill=SURF)
        for b in range(0, 89, 4):
            x = sx(BT[b]); d.line((x, 82, x, 200), fill=(56, 56, 53)); d.text((x, 203), str(b), font=F13, fill=DIM, anchor='ma')
        for y, lab, rr in ((88, 'current cut', cur), (146, 'new plan', plan)):
            d.text((X0 - 8, y + 16), lab, font=F13B, fill=INK, anchor='ra')
            for r in rr:
                xa, xb = sx(r['t0']) + 1, sx(r['t1']) - 1
                d.rounded_rectangle((xa, y, max(xa + 1.5, xb), y + 46), 2, fill=hexrgb(CAT[r['status']]))
        x = X0
        for k, lab in CATLAB.items():
            d.rounded_rectangle((x, 220, x + 11, 231), 2, fill=hexrgb(CAT[k])); d.text((x + 17, 218), lab, font=F13, fill=INK)
            x += 34 + d.textlength(lab, font=F13)
        d.text((20, 218), 'bar', font=F13, fill=DIM)
        # one still per new shot
        y0 = 250
        for k, r in enumerate(plan):
            x, y = 20 + (k % cols) * cw, y0 + (k // cols) * (th + 62)
            p = r['panes'][-1] if r['name'].startswith('Lockstep') else r['panes'][0]
            i = (p['hits'][0]['src'] + 3) if p['hits'] else (p['src0'] + p['src1']) // 2
            if r['restage'] and 'm' in r['restage']:
                i = sum(r['restage']['m']) // 2
            im.paste(frame(p['take'], i).resize((tw, th), Image.BOX), (x, y))
            d.rectangle((x, y + th, x + tw - 1, y + th + 3), fill=hexrgb(CAT[r['status']]))
            d.text((x, y + th + 6), f"{k + 1}  bars {r['b0']:g}-{r['b1']:g}  {r['status']}", font=F13B, fill=INK)
            words, line, lines = r['name'].split(), '', []
            for w_ in words:
                if d.textlength(line + ' ' + w_, font=F13) > cw - 12:
                    lines.append(line); line = w_
                else:
                    line = (line + ' ' + w_).strip()
            lines.append(line)
            for j, ln in enumerate(lines[:2]):
                d.text((x, y + th + 22 + j * 15), ln + ('...' if j == 1 and len(lines) > 2 else ''), font=F13, fill=DIM)
        # verdict table
        y = y0 + rows_n * (th + 62) + 14
        colx = (20, 60, 300, 420, 540, 630, 1010, 1110)
        for cx, h in zip(colx, ('#', 'Current shot', 'Time (s)', 'Mean |gspeed|', 'Idle s', 'Interactions', 'Verdict', 'In the new plan')):
            d.text((cx, y), h, font=F13B, fill=INK)
        d.line((20, y + 17, W - 20, y + 17), fill=(42, 51, 85))
        for r in cur_raw:
            y += 19
            v, goes = VERDICT[r['shot']]
            lev = [p for p in r['panes'] if p['kind'] == 'level']
            g = ' / '.join(str(p['mean_gspeed']) for p in lev) if lev else '-'
            idle = ' / '.join(f"{p['idle_s']:.1f}" for p in lev) if lev else '-'
            inter = '; '.join(evtext(p['events'], 3) for p in lev) if lev else (r['panes'][0]['kind'].replace('_', ' ') if r['panes'] else 'card')
            cut = lambda t, n: t if len(t) <= n else t[:n - 1].rstrip() + '...'
            for cx, txt in zip(colx, (str(r['shot'] + 1), NAMES[r['shot']], f"{r['t0']:.2f}-{r['t1']:.2f}", g, idle, cut(inter, 58), v, cut(goes, 64))):
                if cx == colx[6]:
                    d.rounded_rectangle((cx, y + 3, cx + 10, y + 13), 2, fill=hexrgb(CAT[v])); cx += 16
                d.text((cx, y), txt, font=F13, fill=INK if cx < 300 else DIM)
        q = im.quantize(colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        buf = io.BytesIO(); q.save(buf, 'PNG', optimize=True)
        if buf.tell() < 512 * 1024:
            break
    (C / 'storyboard.png').write_bytes(buf.getvalue())
    print(C / 'storyboard.png', im.size, f'{buf.tell() / 1024:.0f} KB', f'{colours} colours, thumbs {tw} px')


if __name__ == '__main__':
    png(*main())
