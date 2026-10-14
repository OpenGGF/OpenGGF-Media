# Starpost Valley trailer polish — 2026-10-10

Final picture: `starpost-valley-promo.mp4`, 106.416667 seconds, 1920×1080,
60 fps, H.264 and stereo 48 kHz AAC. `edit.json` is the exact frame edit list.
`edit.py` assembles the picture and audio; `soundtrack.wav` is the lossless mix.
The public playback copy is `../starpost-valley-promo.mp4`.

The trailer builds from fishing through farming and neighbours into seasons,
returning adventure and celebrations. Four upright vertical masks have angled
separators and show all four seasons together, changing farm → town → lake.
Gameplay uses the native captured 60 Hz frame clock. The music uses 65% of its
original tempo with pitch preserved, about 7.14% slower than the reviewed 70%
edit. ROM SFX accompany actions and selected cuts at their normal speed/pitch.
The opening card background uses a long continuous native take, with no short
loop or camera reset. Tails' corrected tail accessory is in `farmers-fixed`.

## Reproduce the edit

The existing Slay the Robotnik promo virtualenv supplies Pillow and NumPy;
ffmpeg must provide libx264 and the Rubber Band filter. Fonts are the installed
Fira Sans compressed/condensed family. From this directory:

```bash
ffmpeg -y -i azure-lake.wav -af rubberband=tempo=0.65:pitch=1 -ar 48000 -ac 2 azure-lake-65.wav
ffmpeg -y -i /home/farrell/Videos/OGGF/slay-the-robotnik-promo/audio/m-dataselect.wav -af rubberband=tempo=0.65:pitch=1 -ar 48000 -ac 2 data-select-65.wav
/home/farrell/Videos/OGGF/slay-the-robotnik-promo/.venv/bin/python edit.py render
/home/farrell/Videos/OGGF/slay-the-robotnik-promo/.venv/bin/python edit.py sheet
ffmpeg -v error -xerror -i starpost-valley-promo.mp4 -f null -
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of json starpost-valley-promo.mp4
```

`azure-lake.wav` was synthesized from the user's supplied locked-on S3K ROM
(song 0x20, 110 seconds) with the reference promo's `tools/render_audio.py`.
Data Select and the SFX bank are the existing ROM-rendered reference assets.
The bank stores 3-second slots in this ID order:
`33 AB B6 B3 AF B4 B8 63 6E 9F 3C 42 B1 6A AC 9C 62 4E`.
The lossless mix peak is −1.77 dBFS. The encoded export measures −16.7 LUFS integrated loudness and −1.8 dBFS true peak; it does not clip. Full MP4 decode succeeded.

## Capture provenance

Original picture sources remain at `/home/farrell/scratch/sv-promo/final`;
the renderer's `NEW` set selects takes in this directory. Each take includes
400×224 native framebuffer PNGs, per-frame state CSV and signed little-endian
16-bit stereo PCM at 48 kHz (800 stereo samples per video frame). They are real
`HeadlessGameBoot`/`GameLoop.step` captures, not hand-painted gameplay. The
retained `StarpostPromoCapture.java` and `.txt` inputs reproduce the setups.
`updated-mods/starpost-valley.jar` includes 65% in-mod pacing and the Tails fix;
`farmers-fixed` was captured with that jar and the updated feature engine.
A runtime witness with this packaged mod observes 65% at frame 10 in the mod scene and frames 160/300 in the native town act, with no creator faults. Its take is `tempo-witness/`. Season/location takes use the preceding presentation-compatible capture build.
They have music disabled, and only their picture is used in the final edit.

Compile the driver against the chosen engine's `target/classes`, test classes
and dependency classpath, then launch:

```bash
java -cp '<capture classes>:<worktree>/target/test-classes:<worktree>/target/classes:<dependencies>' \
 com.openggf.StarpostPromoCapture '<absolute S3K ROM>' '<absolute S1 ROM>' \
 '<absolute packaged-mod directory>' '<absolute take directory>' '<absolute input script>' 600
```

Use an isolated working directory so relative save paths cannot read/write a
player's existing save. Farmer select used the fresh `character-select-run/` cwd
and 720 frames. Seasonal scripts are under `slice-inputs/`, 600 frames each;
the source frame range starts at 240 after setup. Capture inputs use `place=`
for explicit native position setup, `state=` for retained season/weather/time,
and `jump=` for public debug scene transitions. The old `native=` lines in
some earlier scenic inputs are ignored by this driver; the observed continuous
camera/position comes from its CSV, not those lines.

The historical driver CSV heading has extra/misnamed columns. The actual eleven
row fields are: frame, mode, centre_x, centre_y, ground_speed, airborne, rings,
calendar_clock, camera_x, camera_y, input_mask. The editor reads by those actual
indices. State rows are editorial evidence and never drive engine gameplay.

These are seeded showcase takes, not certification of a full year played from
cold start or of arbitrary generated Ruins seeds, ROM parity, every viewport,
team or donor. Native gameplay speed is preserved; set-up gaps are cut out.

## Retained revisions and QA

`previous-edit.mp4` preserves the old 119.8-second chapter tour;
`feature-tour-85.mp4` and `edit-85.py` preserve the first quieter draft.
`review-sheet.jpg` and `review-*.png` inspect each chapter/cut and all three
season-gallery locations. `render-final.log` records final audio metrics and
render completion. Repo-side implementation and validation evidence lives in
`docs/architecture/designs/2026-10-09-starpost-valley.md` on PR #220.

## Watering-can refresh — 2026-10-11

The farming shots now use `grow-can-walk/`: a fresh production take with Sonic
walking between successful watering actions, holding the new original can. Its
picture and captured ROM SFX replace the preceding grow take. Harvest starts at
source frame 1730 instead of 890. The timeline, other chapters, 65% pitch-preserved
score, seasonal slices and transition cues are unchanged. `edit.json` is the
regenerated final edit list; all source ranges and raw PCM/frame counts pass.

The export has 6,385 frames (106.416667 seconds), 1920×1080/60 fps, stereo 48 kHz
AAC. Full error-fatal MP4 decode passes. EBU R128 measurement gives −16.7 LUFS
integrated, 3.7 LU range and −1.8 dBFS true peak. Both public playback copies and
this export have SHA-256
`911817a4a09fd3ba5363e116b56c24a2e82a2354f1f799b4714e1b242afebef2`.

`../watering-can/README.md` records the driver, input, hand-alignment and refusal
checks. Its `previous-trailer.mp4` and `edit-before-can.py` preserve the preceding
revision. `grow-can/` preserves the first can take, used to inspect all three
farmers. The trailer uses `grow-can-walk/` exclusively for the farming chapter.

## Facing-tile correction — 2026-10-11

The farming chapter now uses `grow-can-forward/`: the actual wet plot, can spray
and target marker agree on the adjacent tile in Sonic's facing direction.
Input-only serpentine walking waters nine planted plots once each. The retained
source, observer and isolated facing/refusal checks are recorded in
`../watering-can/front-tile/README.md`. Previous sources/edits remain retained.

The refreshed export keeps 6385 frames/106.416667 seconds, 1920×1080/60 fps and
stereo 48 kHz AAC. Full error-fatal decode and all source/PCM counts pass.
It measures −16.7 LUFS and −1.8 dBFS true peak. All three playback copies have
SHA-256 `4096f005542c6a7dbf17a7a6d41b359fb4c33b91474bfaaf7ab6618929f43df8`.
