#!/usr/bin/env python3
"""Generate the reviewable planning documents from the measured audio clock. No footage capture.
Origin: Emerald Remix promo design session, 2026-10-22. Inputs: audio/analysis.json.
"""
import csv,json,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1]
a=json.loads((root/'audio/analysis.json').read_text()); bpm=a['bpm']; first=a['first_beat_seconds']; period=a['period_seconds']
def frame(b):return round((first+b*period)*60)
def sec(b):return frame(b)/60
# First frame is deliberately moving footage, before the estimated first musical beat.
shots=[
 dict(id='S01',b0=0,b1=8,title='Know the way?',source='EHZ-A',action='Run into the borrowed Act 2 hills/dip; recognizable Emerald Hill art with an unfamiliar route.',copy='KNOW THE WAY?',anchor='Remixed x≈700–1792; the EHZ2 strip starts at x=896.',control='Cold EHZ1 route, hold right; tune a jump only if the route needs one. Start the excerpt with momentum, not an idle spawn.',accept='Sonic enters moving, terrain and route remain readable, no damage or stumble in the selected interval.'),
 dict(id='S02',b0=8,b1=16,title='The familiar turns fresh',source='EHZ-A',action='Continue into the waterfalls/early loops with a clean complete arc.',copy='EMERALD HILL. REMIXED.',anchor='Remixed x≈1792–4096, copied from EHZ1 columns 18–35.',control='Continue the same cold input log; select a later intact action with handles. If adjacent to S01 in source, preserve that continuity.',accept='The remix promise is readable by 6 seconds. Show the landing/exit before cutting.'),
 dict(id='S03',b0=16,b1=24,title='Identity on the phrase',source='EHZ-A',action='Moving scenery carries the title; keep the actual route visible around it.',copy='EMERALD REMIX',anchor='Choose a clean moving stretch before the triple corkscrew; exact source frames pending.',control='Use unused moving frames from EHZ-A. This is an editorial title, not a replacement for the stock game title.',accept='Title fills the upper third, clears Sonic, and leaves by the triple approach. No false custom title-screen claim.'),
 dict(id='S04',b0=24,b1=40,title='Triple corkscrew hero',source='EHZ-A',action='One continuous approach → double corkscrew → appended single → clean exit.',copy='THREE CORKSCREWS. ONE RUN.',anchor='Triple assembly x=4096–5247: EHZ1 columns 72–77 then 36–38. Take includes both approach and exit.',control='Build speed naturally from the cold route. Drive through the whole assembly. No position or velocity writes. Remove the overlay before the first full rotation.',accept='All three rotations and exit visibly occur in one uninterrupted take; CSV supports forward progress, no dead/hurt state. Extend by a bar if the complete action needs it.'),
 dict(id='S05',b0=40,b1=48,title='Keep the momentum',source='EHZ-A',action='An uninterrupted hill-and-valley run through the longer remixed middle, with room to read the route.',copy='',anchor='Remixed middle x=5248–9471, copied from EHZ1 columns 39–71.',control='Continue EHZ-A naturally after the triple. Choose a distinct continuous hill descent, not another angle of the same corkscrew.',accept='A fresh piece of motion, not another copy of S04. Skip this shot if it feels repetitive; give its bar to Clover Valley.'),
 dict(id='S06',b0=48,b1=61,title='Leave room for discovery',source='EHZ-A',action='The relocated single corkscrew and its run-out carry the bridge toward the new-zone reveal.',copy='AFTER EMERALD HILL ACT 2…',anchor='Repeated single at x=9472–9855, then run-out from x=9856 onward. Exact source timing pending; no held signpost padding.',control='Same cold run. Editorial jump forward is explicit in the next caption: Clover Valley follows Act 2, not Act 1.',accept='Caption reads before the reveal. Do not cut from an Act 1 results screen as though it directly loads Clover Valley.'),
 dict(id='S07',b0=61,b1=71,title='New ground',source='CV-A',action='Full-width first look at Clover Valley: pink flowers, layered mountains and rolling grass; Sonic runs through it.',copy='CLOVER VALLEY',anchor='Clover x≈96–960; authored start (96,544), first ledge x=960–1103.',control='Direct cold load of mod zone 11, act 1, hold right. No seeded rings, teleport, invulnerability or debug setup.',accept='New art shown full screen before any other layout. Horizon and supporting ground stay aligned through the hill.'),
 dict(id='S08',b0=71,b1=80,title='Find the upper line',source='CV-A',action='A purposeful jump past the monitor/step sequence into the approach to the spring.',copy='',anchor='Monitor x=1032; step/monitor section x≈1200–1500; spring approach near x=1760.',control='Author native jump holds and releases from observed next-session state. Do not reuse the test bot’s damage immunity.',accept='Show takeoff and landing. The shot sells a route choice; if the upper approach is not fun/readable, stay on the lower route.'),
 dict(id='S09',b0=80,b1=96,title='Clover Valley payoff',source='CV-A',action='Yellow spring → upper ring line → visible landing, with the parallax horizon moving behind the action.',copy='',anchor='Spring (1832,568), subtype 2: upright yellow. Upper ledge x=1792–2271 at y=400, rings y=384; hill/checkpoint around x=2408.',control='One natural continuous take; approach with native speed, allow spring impulse, adjust right/release timing to land. No artificial arc, ring count or camera keyframes.',accept='Spring actually fires, ring count increases if rings are visibly touched, landing has clear supporting ground. Treat this as the proposed hero until captured; substitute a clean hill descent if the trajectory cannot deliver it.'),
 dict(id='S10',b0=96,b1=109,title='One more run',source='CV-A',action='Late downhill/run-out into the signpost spin, letting the completion register.',copy='',anchor='Late slopes x≈3200–4000; signpost (5016,544), camera maxX=4800.',control='Continue CV-A through natural finish; pick the approach → contact → spin, with no debug completion. No requirement to fit the full tally inside this excerpt.',accept='Natural signpost trigger and visible response. If this needs more time, shorten S05, not the consequence.'),
 dict(id='S11',b0=109,b1=125,title='Take it for a spin',source='CV-END',action='A fresh moving Clover Valley tail under a softened/dimmed end card; final two-second fade.',copy='TAKE THE REMIX FOR A SPIN.',anchor='Unused 9 seconds of CV-A, or a second cold CV run. Never loop a short camera slice or freeze the last frame.',control='Reuse only unused valid moving frames; dim/blur is editorial. This is the only full information card.',accept='All identifying and practical copy readable for at least 6 seconds, with stable type. URL is a repository entry point, not an invented download page.')
]
for s in shots:
 s['f0']=0 if s['id']=='S01' else frame(s['b0']);s['f1']=frame(s['b1']);s['t0']=s['f0']/60;s['t1']=s['f1']/60
(root/'BRIEF.md').write_text('''# Emerald Remix — “Know the way?”

Planning review • 22 October 2026 • design only • source `8aa692b045c195ef8a42896b6bbc9549158470c0`

Audience: Sonic fans who know Emerald Hill by feel and want a fresh reason to run it.

Form and evidence: a music-led gameplay trailer. All playable action comes from ordinary OpenGGF gameplay under controller inputs. The title and chapter treatments are editorial. No Stageplay, fake physics, editor tour or developer monologue is needed.

Promise: rediscover Emerald Hill Act 1, then explore the original Clover Valley zone.

The emotional route is recognition → surprise → discovery → “I want a turn.” Lead with familiar grass, loops and momentum. Let the new arrangement challenge the viewer’s memory. Show the triple corkscrew as a complete action. Open the picture into Clover Valley and let its new landscape carry the second half. Finish with the native signpost and a practical invitation.

Hero moments: Emerald Hill’s joined triple corkscrew is the memorable remix proof. Clover Valley’s proposed spring → ring line → landing is the new-zone payoff. Its trajectory remains an unverified capture target; do not advertise it as achieved. The fallback is a sustained hill descent with a clear landing and parallax.

Sound: one coherent Emerald Hill 2P bed (S2 `0x91`), already used by Clover Valley. It keeps the Sonic 2 identity while feeling like a side of Emerald Hill some fans hear less often. No mid-cut clip music. At most two quiet editorial ROM stingers: swish on title/reveal and ring on the invitation, separately rendered if useful after review. No voice-over. The planning bed has no SFX yet.

Delivery target: approximately 70.37 seconds, 1920×1080 at 60 fps, landscape. The edit has eleven proposed source blocks, including one moving end card. Most action takes last 4.5–9.5 seconds. More than 90% of the proposed timeline retains moving gameplay as its background; there are no menus. Reallocate bars if a complete action needs room. Never speed up gameplay to fit music.

## Why these choices

This mod changes two places rather than adding a large feature system. The best invitation is to show how those places feel to run. A tutorial or code panel would spend its strongest seconds addressing mod authors. A rapid feature montage would repeat the same few routes. The selected treatment gives fans time to recognize a piece, notice the surprise and follow the consequence.

The triple corkscrew is stronger evidence than “remixed” written over an ordinary hill. Clover Valley earns an uninterrupted full-width reveal; its original tiles, flowers and layered horizon deserve equal attention. The late spring/landing shot gives the original zone a climax of its own. Stock Act 2 stays outside the showcase, with a short explicit progression caption so the edit cannot imply that Clover directly follows Act 1.

A 45–50 second version was considered: it would compress two route identities, two hero actions and practical copy into short fragments. A 90-second developer tour would overstate the scale of this small example. The current 70-second proposal is a reviewable middle; S05 is the first cut if the pacing needs tightening, and the repeated single in S06 is expendable if it repeats the hero. The information-rich end card gets nine seconds so the invitation can actually be read.

## Visual direction

Use broad, stable gameplay views and crisp Sonic 2-inspired diagonal type. Travel and transitions run left → right. Only the title and Clover reveal get a short banded wipe; ordinary changes are clean musical cuts. One restrained dissolve leads into the end card. Avoid zoom punches during the corkscrew or spring arc: they could hide the action this film is selling.

Capture the hero passes at 400×224. Preserve the whole frame with a static 4× nearest-neighbour enlargement (1600×896), positioned at (160,92) on the 1080p canvas. Use an edge-to-edge moving extension of the same scenery, softened and dimmed, behind it; no solid letterbox field. Keep the foreground view large and visually unboxed. If that treatment feels inset at review, use a static aspect-preserving 1920×1075.2 fit with BOX filtering after integer upscale, and inspect motion for softness. Never stretch 400×224 directly into 16:9. Native 320×224 is a fallback if 400-wide behavior proves unstable; widen the background treatment rather than crop a landing.

Primary colors come from Clover Valley’s committed Genesis palette, decoded with the generator’s RGB conversion: grass `#6DDA6D` (line 2 index 10), sky `#6DB6FF` (shared sky), flower-center gold `#FFDA00` (line 2 index 14), and deep green `#004800` (line 2 index 7). White is a text neutral. These are original-zone colors, not invented samples from uncaptured gameplay. Recheck the rendered display profile next session.

Use installed Fira Sans Compressed Heavy / Heavy Italic for the editorial title: a deliberate heavy condensed fallback because Emerald Remix keeps Sonic 2’s stock title and ships no mod logo/font. Title 150–180 px at 1080p; chapter 100–130 px; promise 64–76 px; practical copy 30–40 px. White/gold fill, dark green 6–8 px outline and firm shadow. A short diagonal grass/sky band is original editorial decoration, not claimed to be ROM title-card art. Type enters in 12–16 frames, exits in 8; hold informational lines still. Leave Sonic’s path, jump apex, landing and HUD readable. Use no more than one sales idea at once and keep most of the new-zone action text-free.

## Copy and invitation

Opening: “KNOW THE WAY?” → “EMERALD HILL. REMIXED.” The promise must read by six seconds, even though the full identity arrives at the first strong section candidate around nine seconds.

Title: “EMERALD REMIX” / “A fresh run through Sonic 2.”

Remix hero: “THREE CORKSCREWS. ONE RUN.” Remove before the rotations.

Bridge: “AFTER EMERALD HILL ACT 2…” → “CLOVER VALLEY”. Avoid a false direct Act 1 → Clover handoff.

End card, stable for roughly 9 seconds:

- EMERALD REMIX
- Take the remix for a spin.
- `github.com/OpenGGF/OpenGGF` • `examples/emerald-remix`
- Development example • Mod API 0.7 candidate
- Java 25 + matching development JVM build
- Fan-made and free. Not affiliated with SEGA. Requires your own ROM.
- Sonic 2 World REV01

Use the repository URL plus visible folder path as the call to action; there is no verified standalone download page. Native game title, other zones and EHZ Act 2 remain stock. Do not imply a full new campaign, new bosses, stock-ROM compatibility or inclusion in the public 0.6 release. The example manifest’s `1.0.0` is its own package version, not engine-release status.

## Session boundary

This package is ready for a creative review. No gameplay or reference footage has been captured. The generated map is an authoring reference, not an engine screenshot. Capture begins only in a later session after the user reviews this plan. No repository edits, commits, pushes or OpenGGF-Media changes are authorized in this session. The skills’ eventual archive requirement is deferred by that explicit boundary.
''')
(root/'RESEARCH.md').write_text('''# Study notes and borrowing

All engine/mod observations below refer to checkout `8aa692b045c195ef8a42896b6bbc9549158470c0`, branch `feature/ai-promo-skill-coaching`. This was source study and a generated static-layout inspection, not a playthrough. No claim about the quality of unrecorded motion is implied.

## The actual example

Read `examples/emerald-remix/README.md`, `EmeraldRemixMod.java`, `RemixedLevel.java`/recipe interfaces as needed, the exact `ehz1.remix` strip recipe, Clover Valley’s `level.json`, terrain generator and parallax implementation. Read the package/progression and route-test portions of `TestEmeraldRemix`.

The borrowed EHZ2 passage occupies remixed map columns 7–13 (x=896–1791). EHZ1 columns 18–35 follow. The triple uses remixed columns 32–40 (x=4096–5247): the original double, then the original single. The single reappears at remixed columns 74–76 (x=9472–9855). Those are layout anchors, not invented captured frame numbers.

Clover is one original act, with gentle hills, step-ups, floating ledges, small flowers and clover decorations, a long ring line, monitors, a yellow upright spring, checkpoint and signpost. The generated static map in `design/clover-layout-reference.png` was made with `--check --preview`: it verified all twelve committed exports and wrote no source assets. It omits player/object gameplay and is not evidence that any planned jump succeeds. Its extended background tiling is a layout view, not a production camera preview.

Clover’s scroll owner uses 1/8 camera movement for sky/clouds, 1/4 for mountains/hills and 1/16 vertical rise. Borrow that sense of depth in a long travelling take, rather than covering the horizon with a caption.

Important capture finding: runtime registry appends Clover after Sonic 2’s eleven stock zone entries, so the sole-mod CLI zone is **11**, act **1**. JSON `zoneIndex:64` and `levelIndex:1024` are different internal identities. Confirm resolved identity at capture time; more enabled mods could change the index. The route test uses damage immunity every frame, so it proves a narrower terrain/progression claim and is not a capture recipe for a normal player run.

## Slay the Robotnik — musical organization

Read the complete `build()` edit, music mixer, `render_audio.py`, production README and chapter list at OpenGGF-Media commit `c2f0c0218a2fa97a204ed527a36810babadb4b41` (read-only HTTP; no media checkout touched).

- [Edit source](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/slay-the-robotnik/sources/promo/tools/promo.py)
- [Audio renderer](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/slay-the-robotnik/sources/promo/tools/render_audio.py)
- [Production notes](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/slay-the-robotnik/sources/promo/README.md)

Borrow the beat clock, chapters at musical changes, short title treatment over motion, one coherent bed and an uninterrupted action into its consequence. Its sixteen-beat title interval and longer journey/final-blow intervals demonstrate that a title or payoff need not be a rapid montage. Its debugging setup is explicitly documented; borrow that honesty, not the debug kills. Do not copy its three-game engine pitch, card statistics or crowded event grid: Emerald Remix has a simpler audience promise.

The old renderer depends on another worktree’s test helper and an S3K startup-scene mod. Adapted the *principle* to the current production `FmSfxRenderTool`, which renders S2 music directly through SMPS without graphics or a temporary mod.

## Putt-Putt Paradise — Sonic 2 editorial type

Read `card_caption()`, `chapter_card()`, transition code and relevant `build()` sections in [render_promo.py](https://github.com/OpenGGF/OpenGGF-Media/blob/c2f0c0218a2fa97a204ed527a36810babadb4b41/projects/putt-putt-paradise/sources/media/promo-opus-20261006/final-verified/render_promo.py).

Borrow its staggered heading arrival, strong italic letters, outline/shadow and a decisive departure. Its red serrated spine, blue band and yellow subtitle motivate a coherent Sonic 2 visual language. For this production, use a lighter original grass/sky/gold treatment so it supports the landscape instead of advertising mini golf. Do not copy the cup iris or tutorial panels.

## Local craft and workflow references

Read `.agents/skills/promo-direction/SKILL.md`, `references/lessons.md`, relevant `references/moves.md`, `gameplay-highlights`, `gameplay-capture`, `bk2-input-authoring` and `headless-rendering`.

The archived complaints “very rushed” and “cluttered audio and rapid cuts” are the reason for fewer complete actions and one soundtrack owner. The documented fractional-zoom and vertical-ground-alignment failures motivate stable source framing and a motion review of feet, terrain and jump landings. No screenshot or codec check will substitute for watching those sequences.

Limits: the referenced finished videos were not available in this checkout and were not watched. Reference claims here concern inspected source, chapter timing and recorded feedback, not motion or listening judgments. No footage or visual asset from those productions is reused. No external commercial soundtrack is introduced; the planning WAV is a local ROM-derived render, not represented as royalty-free or independently licensed music.
''')
# Separate long-form beat sheet and machine-readable shot plan.
lines=['# Beat sheet — planning version','',f'Clock: {bpm:.6f} BPM; first estimated beat {first:.6f} s; {period:.9f} s/beat. Beat labels are zero-based editorial counts, not confirmed score bar numbers. Frame rounding is nearest at 60 fps. Output starts at frame 0 with motion.', '', 'Chapter intent: recognition (0–9.05), identity (9.05–13.55), rearrangement (13.55–34.37), new ground (34.37–61.37), invitation (61.37–70.37). The 16 and 61 boundaries match strong detected spectral changes. Other changes are bar/phrase candidates; the music has not been physically auditioned. Preserve continuous actions across music changes.', '', '| Shot | Beats | Output seconds | Output frames, end exclusive | Picture / type / sound |', '|---|---:|---:|---:|---|']
for s in shots:
 cue='Bed continues; no captured BGM.'
 if s['id']=='S03':cue='Title band, 12–16 frame arrival; optional quiet editorial swish.'
 if s['id']=='S07':cue='Single chapter wipe; bed continues unchanged.'
 if s['id']=='S11':cue='Dissolve into moving tail; optional editorial ring; bed fades over final 2 s.'
 lines.append(f"| {s['id']} — {s['title']} | {s['b0']}–{s['b1']} | {s['t0']:.3f}–{s['t1']:.3f} | {s['f0']}–{s['f1']} | {s['action']} Copy: {s['copy'] or 'none'}. {cue} |")
lines+=['','The 9.0-second triple pass and 9.0-second spring pass are protected. If either cannot fit its approach and consequence, move a neighboring cut by four beats and shorten a less distinctive shot. No holds, looping short background slices, slow motion or accelerated gameplay as timing repairs. S10 may move from beat 96 to detected novelty beat 95 only after listening and action review. S11 begins at beat 109 for a nine-second reading interval. It is an editorial invitation point, not a claimed new musical section; listen before locking its exact entrance.','', 'There is no finished EDL yet. Source in/out frames stay unassigned until actual CSV and moving captures are inspected. This file assigns output timing only.']
(root/'BEAT_SHEET.md').write_text('\n'.join(lines)+'\n')
with (root/'SHOT_LIST.csv').open('w',newline='') as f:
 fields=['id','title','source','b0','b1','t0','t1','f0','f1','action','copy','anchor','control','accept','source_in_frame','source_out_frame','capture_status']
 w=csv.DictWriter(f,fields);w.writeheader()
 for s in shots:w.writerow(dict(s,source_in_frame='',source_out_frame='',capture_status='PLANNED — NOT CAPTURED'))
(root/'CAPTURE_PLAN.md').write_text('''# Capture plan — commands for the next session only

No command in this document was used to capture footage during planning. Start after creative review. Work only from `/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach`; its `target/` is the build location. Production root is `/home/farrell/Videos/OGGF/emerald-remix-promo`. Leave `coaching/` untouched.

## Sources and control

**EHZ-A**: a cold direct load of remixed Emerald Hill Act 1 with only Emerald Remix loaded, Sonic solo, no donor, width 400. Use a deterministic BK2/Input Log from act start through the triple and downstream single to natural completion. Start excerpts after acceleration, but retain the complete source prefix and state CSV. The shot list names layout anchors; actual input timing is deliberately not invented before running the level.

**CV-A**: a cold direct load of the original Clover Valley act with the same configuration. Author right movement, native jumps for the two step-ups and a spring approach. Keep the whole run through native signpost/results. S07–S10 can be excerpts from this one source; that does not imply an uninterrupted trailer or progression through Act 2. **CV-END** is an unused moving tail from CV-A, or a second cold pass when needed, never a looped still.

Default source kind is normal gameplay with scripted controller input, not a trace, Stageplay or parity reference. No invulnerability from `TestEmeraldRemix`, debug completion, ring seeds, position/velocity writes or altered level assets. If later exploration needs a positioned diagnostic, segregate and label it and recapture the final action from the cold route. Do not quietly promote a diagnostic to final evidence.

## Build and environment

Already completed successfully in this checkout:

```bash
JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 examples/emerald-remix/build.py
```

This compiled engine/tool classes, generated `target/examples-classpath.txt` and validated/packaged `target/emerald-remix/emerald-remix.jar` with zero validator findings. It did not launch the game or run route tests. Rebuild only for new source changes. Pin the exact future source SHA and mod JAR hash in each capture’s notes. Current SHA is in STATUS.md.

The input tool does not need graphics. Author each reviewed input script under the production root, compile it through `InputLogAuthorTool` and retain its production-loader round-trip result. Use absolute paths. For a future `inputs/ehz-route.script`:

```bash
JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 tools/testing/maven_queue.py -Dmse=off exec:java \
  -Dexec.mainClass=com.openggf.tools.InputLogAuthorTool \
  '-Dexec.args=--script /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/ehz-route.script --out /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/ehz-route.bk2 --game s2'
```

Scripts do not exist yet. A jump is a held-button state with explicit release; holding Jump for a duration produces one jump, not repeated taps. Tune action from observed state next session, not the test bot’s unconditional invulnerability. Record selected log hashes and any route revisions. Use distinct take directories to preserve rejected and superseded attempts.

## Planned capture commands

These templates intentionally depend on input logs to be authored after review. `--frames` is a safety budget, not a predicted route time; once the input length/finish time is known, replace it with the actual required budget and retain handles. Omit `--audio`: the current CLI’s audio export contains full music and effects, not an isolated SFX stem. This film uses a separate editorial bed; silent source captures avoid layered BGM. Optional stingers can be rendered separately with the already verified audio tool and identified as editorial accents.

```bash
# EHZ-A — next session, after input authoring.
env -u DISPLAY -u WAYLAND_DISPLAY JAVA_HOME=/usr/lib/jvm/java-25-openjdk \
  python3 tools/testing/maven_queue.py -Dmse=off -Dopenggf.headless.gl=surfaceless-egl \
  exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool \
  '-Dexec.args=--game s2 --rom /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/s2.gen --mod /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/target/emerald-remix/emerald-remix.jar --zone ehz --act 1 --width 400 --main sonic --sidekick none --input /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/ehz-route.bk2 --frames 12000 --every 1 --fps 60 --no-video --out-dir /home/farrell/Videos/OGGF/emerald-remix-promo/captures/ehz-a-take01'

# CV-A — next session. Numeric zone 11 is the sole-mod registry index, NOT JSON 64.
env -u DISPLAY -u WAYLAND_DISPLAY JAVA_HOME=/usr/lib/jvm/java-25-openjdk \
  python3 tools/testing/maven_queue.py -Dmse=off -Dopenggf.headless.gl=surfaceless-egl \
  exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool \
  '-Dexec.args=--game s2 --rom /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/s2.gen --mod /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/target/emerald-remix/emerald-remix.jar --zone 11 --act 1 --width 400 --main sonic --sidekick none --input /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/cv-route.bk2 --frames 6000 --every 1 --fps 60 --no-video --out-dir /home/farrell/Videos/OGGF/emerald-remix-promo/captures/cv-a-take01'
```

Both use one PNG per executed frame plus measured `state.csv`, preserving native speed. Frame budgets may generate large PNG sets; plan disk capacity before the first run and choose the required route duration from the input log. A lean/logic route reconnaissance could precede every-frame recording next session, but is not a substitute for the actual render. Surfaceless EGL, graphics/sprite correctness, 400-wide behavior and the CLI’s actual resolved Clover identity have not been exercised in this planning session. Fail closed if isolation cannot initialize; never fall back to the shared desktop.

If the public capture host cannot resolve the mod zone, first inspect its existing mod registry/load owner. Use a small production-folder helper calling `GameplayCaptureSession` and `ZoneKey.Mod("emerald-remix","clover-valley")` resolution if necessary; do not invent a stock zone alias or modify the game to disguise identity. This is a contingency, not an implemented or tested helper.

## Per-take verification and selection

1. Confirm actual zone/act/team, level name and runtime registry identity from boot/level metadata. Existing direct-capture CSV has motion fields but no zone identity column; retain boot metadata alongside it rather than treating numeric config alone as proof.
2. Read CSV before selecting frames: motion, camera, ring count, ground/air state, rolling, hurt/dead flags. Check all corkscrew motion and spring/landing progression against the picture. If a native event needs additional telemetry, use an owned diagnostic rather than inferring it solely from an authored command.
3. Make contact sheets after valid captures and assign exact source in/out frames, including 1–2 second handles. Keep native speed and actual PNG cadence; do not encode sparse sampling at 60 fps.
4. Watch complete takes and transitions at 1×. Check foreground alignment through vertical movement, feet at landing, player priority through corkscrews, full hero exits, horizon motion and absence of idle padding. Stills and state alone do not certify attractive footage.
5. Compare claims to observed action. If rings are visible but not collected, do not add pickup sounds or imply collection. Mark failed hero attempts and use the stated fallback rather than fake success.
6. When editing later, inspect source intervals for EOF holds, duplicate excerpts and unintended retiming. Final review will include chapter reconciliation, full decode, dimensions/cadence, encoded AAC loudness/true peak and a complete moving playback. Those final checks are not yet performed.

No engine suite is needed for this planning-only deliverable. A future capture-host failure or an engine modification needs proportionate focused checks under the repo’s queue policy. No public-release full suite is warranted here. OpenGGF-Media publication remains deferred by the user; do not describe a local plan as an archived or shipped promo.
''')
(root/'audio/MUSIC.md').write_text(f'''# Music choice and measured clock

Chosen bed: Sonic 2 **Emerald Hill Zone (2P)**, stock music ID `0x91` / decimal 145. Clover Valley’s `level.json` already selects it, so it ties the trailer’s familiar and original halves together. Keep one uninterrupted bed, not a switch between embedded clip music. This is a local ROM-derived planning soundtrack; no external license or clearance is claimed.

Listen for review: [emerald-remix-review-bed.wav](emerald-remix-review-bed.wav), **{a['review_duration_seconds']:.3f} s**, 48 kHz, stereo, PCM16. Source: [raw/s2-music-91-mix.wav](raw/s2-music-91-mix.wav), 76 s. No SFX, jingle or voice is mixed into either file. No physical listening review was performed by the agent.

## Rendering and reproduction

Built the example/tools in the assigned checkout with Java 25; used `com.openggf.tools.audio.FmSfxRenderTool --game s2 --music 91 --rate 48000 --max-seconds 76`. This reads the supplied S2 REV01 ROM and uses OpenGGF’s real SMPS driver, NTSC region and accurate FM core with full FM/DAC/PSG mix, without gameplay, graphics or desktop audio playback. The renderer reports `complete=false` because the music loops; it successfully reached the requested 3,648,000 stereo sample frames. This is not a failed render.

`../scripts/render_music.py` is the exact reproducible invocation. The tool also makes FM-only and YM register diagnostics; the script deletes those task-owned byproducts, preserving the full mix. Raw music remains local and is not included in any repository.

For analysis, created disposable `target/promo-planning-venv` in this checkout and installed NumPy/Pillow there. Use:

```bash
target/promo-planning-venv/bin/python tools/media/promo_kit.py beats /home/farrell/Videos/OGGF/emerald-remix-promo/audio/raw/s2-music-91-mix.wav
target/promo-planning-venv/bin/python /home/farrell/Videos/OGGF/emerald-remix-promo/scripts/analyse_music.py
```

The analysis script uses the checkout’s actual `promo_kit.py`, exports the JSON/CSV grid and makes the review bed with FFmpeg: 20 Hz high-pass to remove initial chip/DC offset, +6 dB gain, no tempo change, final two-second fade. It ends at frame 4,222 (60 fps), nearest the detected late change at editorial beat 125. Raw sound starts immediately with a chip baseline and a meaningful attack near 34 ms; there is no inserted count-in.

## Measurements and limitations

- Whole opening estimator: **{bpm:.6f} BPM**, period **{period:.9f} s**; first estimated beat **{first:.6f} s**.
- Independent 24-second analysis windows beginning at 0, 18 and 36 s estimate 106.634, 106.602 and 106.650 BPM. Their phases agree with the global clock to about 6 ms. No major tempo change detected within this bounded check.
- Independent first-attack threshold after initial-baseline removal: **{a['first_attack_over_initial_baseline_seconds']:.6f} s**, about **{a['phase_distance_from_first_material_ms']:.2f} ms** before the estimated first beat (less than one video frame). A naive first-nonzero test falsely reports t=0 due to DC; that approach was rejected.
- Raw file measured by FFmpeg `ebur128=peak=true`: integrated **−24.3 LUFS**, LRA **1.5 LU**, true peak **−12.8 dBFS**. Review-bed measurements are recorded in STATUS.md after its final high-pass render. These are PCM measurements, not encoded AAC certification or an RMS-to-LUFS substitution.
- The estimator returns pulse phase, not which pulse is a musical bar downbeat. Spectral novelty locates timbral changes, not certified formal sections. The tiny/zero early and weak late candidates are not reliable chapter cues. Listening/downbeat review remains open before capture/edit lock.

`beats.csv` contains beats 0–125 with exact seconds and 60-fps rounded frames. The bar column groups every four beats for editorial convenience only. `section-candidates.csv` retains the actual novelty scores; `analysis.json` includes source identity, method, onset check, independent windows, bed processing and SHA-256 hashes.

Strong candidates used for the draft: beat 16 ≈9.04 s (identity), beat 61 ≈34.36 s (Clover reveal); beat 32 ≈18.05 s occurs during the triple and deliberately does not force a cut. Beat 95 ≈53.49 s is a possible late action accent; the sheet currently keeps the intact spring pass to bar beat 96. Novelty beat 125 ≈70.37 s provides the proposed fade endpoint. The review bed fades rather than pretending a loop boundary is a composed ending.

Normal EHZ (`0x81`) was considered but not rendered: it would emphasize familiarity while giving Clover less distinction. Hydrocity 2 from the reference promo was rejected as a different game’s identity. An original commissioned score would add work before the route’s appeal is established. Keep the 2P choice provisional for the user’s listening review.
''')
# Compact visual plan, never a fake gameplay screenshot.
phase=[('Recognition',0,sec(16),'#6db6ff'),('Remix',sec(16),sec(61),'#6dda6d'),('Clover Valley',sec(61),sec(109),'#ffda00'),('Invitation',sec(109),sec(125),'#ff91da')]
segments=''.join(f'<div style="flex:{e-s};background:{c};color:#10251d" title="{s:.2f}–{e:.2f} seconds">{name}</div>' for name,s,e,c in phase)
cards=''.join(f'<article><small>{s["id"]} · {s["t0"]:.1f}–{s["t1"]:.1f}s</small><strong>{s["title"]}</strong><p>{s["action"]}</p></article>' for s in shots if s['id'] in ['S01','S04','S07','S09','S10','S11'])
html=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Emerald Remix direction review</title><style>
*{{box-sizing:border-box}}body{{margin:0;color:var(--foreground,#ecf5ef);font:15px/1.5 var(--font-sans,system-ui)}}.kicker{{font-size:11px;letter-spacing:.18em;color:var(--muted-foreground,#9bb4a7);margin:0 0 8px}}h1{{font-size:clamp(30px,7vw,49px);line-height:1.05;letter-spacing:-.045em;margin:0 0 14px;font-weight:950}}.promise{{max-width:65ch;margin:0 0 18px}}.timeline{{display:flex;gap:3px;height:60px;border-radius:8px;overflow:hidden;margin:16px 0 5px}}.timeline div{{display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;padding:7px;min-width:0;text-align:center}}.ticks{{position:relative;height:18px;font-size:11px;color:var(--muted-foreground,#9bb4a7)}}.ticks span{{position:absolute;top:0;transform:translateX(-50%)}}.ticks span:first-child{{transform:none}}.ticks span:last-child{{transform:translateX(-100%)}}.cards{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:20px}}article{{background:var(--card,#18291f);border:1px solid var(--border,#34513d);padding:16px;border-radius:var(--radius,10px)}}small{{color:var(--muted-foreground,#9bb4a7);font-size:11px}}strong{{display:block;font-size:17px;margin-top:5px}}article p{{font-size:13px;margin:7px 0 0}}.note{{font-size:12px;color:var(--muted-foreground,#9bb4a7);margin-top:16px}}.chips{{display:flex;gap:8px;flex-wrap:wrap}}.chips span{{border:1px solid var(--border,#34513d);border-radius:40px;padding:5px 10px;font-size:12px}}@media(max-width:450px){{.cards{{grid-template-columns:1fr}}.timeline{{height:76px}}.timeline div{{font-size:9px;padding:4px;overflow-wrap:anywhere}}}}
</style></head><body><p class="kicker">DIRECTION REVIEW · PLANNING ONLY</p><h1>Know the way?</h1><p class="promise">Familiar Emerald Hill, an unfamiliar route. Then a new valley to explore. Let complete runs, three corkscrews and a spring-to-landing payoff make the invitation.</p><div class="chips"><span>70.37 seconds proposed</span><span>One Sonic 2 music bed</span><span>106.634 BPM estimated</span><span>No footage captured</span></div><div class="timeline">{segments}</div><div class="ticks"><span style="left:0">0:00</span><span style="left:12.86%">0:09</span><span style="left:48.84%">0:34</span><span style="left:87.21%">1:01</span><span style="left:100%">1:10</span></div><div class="cards">{cards}</div><p class="note">This board describes intended action, not captured results. Spring trajectory, route timing, musical downbeats and moving-picture framing remain for the next session. Color swatches come from Clover Valley’s authored palette. Full beat and capture details are in the production files.</p></body></html>'''
(root/'design/review.html').write_text(html)
print('Wrote BRIEF.md, RESEARCH.md, BEAT_SHEET.md, SHOT_LIST.csv, CAPTURE_PLAN.md, audio/MUSIC.md and design/review.html')
