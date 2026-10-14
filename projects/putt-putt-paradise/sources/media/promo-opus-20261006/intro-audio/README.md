# Putt Putt Paradise promo: cold open and soundtrack (2026-10-06)

This revision answers "consider an intro to the promo. Fade in? audio?". It is the 88.47 s paced
cut (`../paced/promo-opus-paced.mp4`) with two additions: a 7.7 s cold open and a soundtrack
rendered from the Sonic 2 ROM. The paced edit after the intro is unchanged. All 14 segments keep
their ranges, lengths, captions and transitions, and each starts exactly 230 frames (7.667 s) later.
No gameplay was shortened. Total length is 96.13 s.

## The cold open
- **0.0–1.0 s.** Fade from black, with no frame or chrome. Real EHZ1 footage plays at normal speed with 4× pixel scaling, in the
  same window position as the rest of the film. Sonic finishes the previous roll and the power
  meter starts.
- **0.9 s.** The Sonic 2 Title Screen music fades up from its quiet opening ticks.
- **1.9 s.** On a fanfare beat, the line "**Sonic 2.**" appears. Sonic is launched at 2.05 s.
- **3.4 s.** On the next phrase, "A whole new way to play." completes the line. A small dim line
  reads "Recorded in the OpenGGF engine · music from the Sonic 2 ROM, added in editing".
- **7.67 s.** Where the fanfare's closing hit would land, the Emerald Hill Zone downbeat starts
  instead. The navy frame, top bar and rails dissolve in around the picture over 12 frames, and
  the paced hook "What if Sonic was the golf ball?" begins.
- **One take.** The intro is the same take that leads straight into the hook shot. The intro
  footage runs from native 1200 to 1684, and the hook starts at native 1660. The dissolve
  therefore shows identical source frames on both sides, so the take never cuts.

The Slay the Robotnik reel was the reference for:
- a cold open before the title;
- one main music bed with chapter changes inside it;
- a jingle on the climax, then a calmer track under the end cards;
- a few ROM sound cues on transitions only.

No Slay assets, S3K audio or scene code were used.

## Soundtrack (editorial)
The footage was recorded silent. The soundtrack was added in editing, and is credited as such on
the end card, in the cold-open kicker and in the MP4 comment. It is not synchronised gameplay
audio.

`tools/S2PromoAudioRender.java` renders each stem from the user's Sonic 2 REV01 ROM through
OpenGGF's own SMPS driver:
- loader and sequencer configuration: `Sonic2SmpsLoader` and `Sonic2SmpsSequencerConfig`;
- NTSC timing, the accurate FM core and 48 kHz output;
- one isolated driver session per stem.

| Out (s) | Stem | Use |
|---|---|---|
| 0.92–7.67 | music 0x96 Title Screen (stem 0–6.75 s) | Cold-open fanfare, 1 s fade-in; its closing hit is cut |
| 7.67–75.90 | music 0x81 Emerald Hill Zone | Main bed, from the hook to hole-complete; 0.4 s fade |
| 75.90–82.18 | music 0x97 Stage Clear | On hole-complete (state.csv native 4444) |
| 82.07–95.83 | music 0x89 Option Screen | Under the engine and end cards; 1.5 s in, 4 s out |
| 16.20 | SFX 0xBC Spindash Release | Title-drop stripe wipe |
| 91.37 | SFX 0xB5 Ring | End-card ball drops into the cup |

The mix is made with ffmpeg and two-pass EBU R128 linear normalisation:
- integrated loudness is −15.9 LUFS, true peak −1.8 dBTP and LRA 2.4 LU;
- no clipping;
- the first and last 0.2 s are digital silence.

The Slay reel measures −13.5 LUFS. This cut was kept slightly gentler.

## Checks
- `promo-opus-intro-audio.verify.json`:
  - 1920×1080, 30 fps, 2884/2884 frames decoded;
  - every PTS delta is 1/30 s;
  - full `ffmpeg -xerror` decode is clean;
  - 15 chapters;
  - audio and video both end at 96.133 s.
- `promo-opus-intro-audio.audio.json`: placements, stem hashes, loudness passes and audio checks.
- `promo-opus-intro-audio.fidelity.json` / `fidelity-intro.log`: 45/45 sampled frames match their
  source frame with normal-speed adjacency. That is the paced cut's 42 plus 3 in the intro.
- `source-lock-intro.json`: the 12 paced range hashes are byte-identical to
  `../paced/source-lock-paced.json`, plus `intro/main`.
- `tools/render_stems.sh` re-rendered all six stems byte-identically.
- `analysis/soundtrack-waveform.png`: overview of the final mix.

## Files
| File | What |
|---|---|
| `promo-opus-intro-audio.mp4` | The video: 96.13 s, H.264 crf16 with AAC 256 kb/s 48 kHz stereo, 15 chapters |
| `promo-manifest-intro.json` | Paced EDL plus the `intro` segment, the `build` transition, the end-card audio credit and the `audio` cue sheet (anchors are segment ids plus local frames) |
| `render_promo_intro.py` | Copy of `../paced/render_promo_paced.py` with an intro painter, a build dissolve, mixing, loudness, muxing and audio checks. The paced script is unchanged |
| `verify_fidelity.py` | Paced checker that also checks the intro |
| `tools/S2PromoAudioRender.java`, `tools/render_stems.sh` | Standalone stem renderer, compiled outside the repo against `target/classes` |
| `audio/` | The six rendered stems. They are ROM-derived, so they are not in the kit |
| `promo-opus-intro-audio.soundtrack.wav` | Final normalised mix (PCM). Not in the kit |
| `promo-opus-intro-audio.{edl.json,chapters.csv,cuts.png}` | Resolved timeline and contact sheet |
| `provenance.json`, `render-intro.log`, `fidelity-intro.log` | Provenance and run logs |
| `putt-putt-paradise-promo-kit-intro-audio.zip`, `SHA256SUMS` | Shareable kit |

## Reproduce
```sh
cd /home/farrell/scratch/gameplay-captures/putt-putt-paradise-20261005/promo-opus-20261006/intro-audio
sh tools/render_stems.sh        # OPENGGF=<worktree with target/classes> S2ROM=<Sonic 2 REV01 ROM>
python3 render_promo_intro.py --source-root ../../showcase-20261006-tails --tag v5 --final --out promo-opus-intro-audio.mp4
python3 verify_fidelity.py promo-opus-intro-audio.mp4 promo-opus-intro-audio.edl.json
```
`--no-audio` renders the same edit silent.

## Limitations
- **Mixing.** Stems are rendered in separate driver sessions and mixed linearly. In the game, SFX
  take over music channels; here they overlay the music instead.
- **No listening pass.** No one has listened to the result. The checks are numeric: levels,
  spectrogram and waveform shapes, and the timing of the jingle and the cut. Music rendered by
  the engine inherits any remaining SMPS or FM inaccuracies in OpenGGF.
- **Act Clear level.** Stage Clear plays about 3 dB above the EHZ bed. That is the ROM's own
  relative level, and it was left as is.
- **Beat alignment.** Cuts were not re-timed to the music, because the paced timing was
  preserved. Only the cold open, the music start and the cues were placed on beats or events.
- **Online play.** Online play is still shown only by the title-menu card and the HOST/JOIN
  graphic. There is no online footage.

Parent QA played the whole timeline at 1× in resumable browser chunks, inspected chapter snapshots and rechecked the opening. `browser-qa.json` records 309 distinct frame samples, EOF, audio decoding and the cumulative browser counters; encoded cadence is verified separately.
