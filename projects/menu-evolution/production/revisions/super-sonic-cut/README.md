# ROAD TO 9, Super Sonic cut (menu-evolution revision `super-sonic-cut`)

Recut 2026-10-29 by Claude Opus 5.5 (xhigh) after the user's review of the 87.333 s film:
"bit slow and repetitive. Do it against the S2 super sonic music, half the length". The earlier
steering "film it like a action movie montage, with various numbers slowly climbing" still applies.

**Deliverable:** `final/menu-evolution-super-sonic-cut.mp4` (1920x1080, 60 fps, H.264 + AAC stereo
48 kHz, 8 chapters) and the lossless master `final/menu-evolution-super-sonic-cut-master.mkv`
(FFV1 RGB + PCM, the same chapters). 43.200 s (2,592 frames), 49.5% of 87.333 s. Hashes are in
`provenance/deliverables.json`. The original film, master, edit and captures in the production root
(`../../`) are unchanged.

## What changed and why

The cause was structural, so the cut was rebuilt rather than sped up. The first film took 25 s to
reach its first comparison, then ran the same six-stop 3.5 -> 9 climb, chart and tally four times
over 10.5-14 s reps. This cut follows the Super Sonic track's own form: 146.48 BPM, a 12-bar loop
(2-bar rising intro, 4-bar melody A, 4-bar stabs B, 2-bar C-E-G cadence). It plays as one bed from
its first sample to the stab that resolves its third loop.

| Before (r3b, 87.3 s) | Super Sonic cut (43.2 s) |
|---|---|
| Metropolis bed, Got an Emerald jingle, title theme under the end card | Super Sonic only, start to stab; no switch of music |
| 7.4 s cold open, 3.5 s title, 7 s prologue, 7 s round-0 grid | 3.3 s cold open (sweep on the intro's rising riff), 3.3 s title on the melody's entrance, one-bar 0.5 glimpse + one-bar pre-redesign hub; round-0 grid cut |
| Four reps (Libraries, Settings, Pickers, Hub & dialogs), each the same climb | Three reps, 6.55 s each, with jump cuts on bar lines and three different moves: Libraries steps one stop a beat on the stabs; Pickers plays old and new **side by side at 3x** and the new score climbs silently on the riff; Settings sweeps once while the score spins two stops a beat. Hub & dialogs, the smallest visual change, is cut (its dialogs stay in the wall) |
| 9.9 s climax, payoff on a jingle, 7 s hero | 6.55 s climax on the B stabs; 27 / 27 slams on the cadence's downbeat; relight under the PSG runs; Giant Ring iris to the delivered hub on the high G; end card lines on the riff's half-bar steps; fade after the G-major stab |
| 117 placed sounds: blips on wall pops, Tally End after each tally leg, spindash charge | 74: one swish per chapter wipe, blips only on two climbs and the families tally, Tally End on each 9 (0.7) and on 27 (0.9), UI tones at 0.7 instead of 1.1 |

Other decisions: the editorial score footnote ("Judgments, not measurements") moved under the first
rep's pane, replacing the round-0 card; the 27 / 27 banner sits wholly in the top margin (the r3b
position crossed 6 rows into the pane); the two-up's new score is right-aligned so "/10" stays
on screen. Every number still stops only on a recorded value (`SCORES`, unchanged).

Rejected while cutting: doubling the playback speed (the user asked for less repetition, not faster
menus); a 1-bar rapid-fire run of four menus (too short to read the UI); splicing the bed to put the
payoff on a melody entrance (the uncut loop already gives a 1.5-beat rest before the cadence);
ending on the cadence at 39.3 s (it would leave the end card on silence).

## Sources and rebuild

```
sources/promo/edit.py        the edit: brief and beat sheet in its docstring, SRC intervals, cue mapping,
                             master/mp4/remix/loudness/lists commands
sources/promo/review.py      motion, strips, exact-pixel, loudness, stereo and stinger checks
sources/promo/changes.py     visible-change frames of a take (in-point picking)
sources/promo/pairgrid.py    old|new pair grid of a take (in-point picking)
sources/promo/{chapters.txt,edl.csv,cues.json}   chapter map, per-shot source intervals, UI cue placements
sources/audio/HeaderProbe.java                   identity probe for the music (header vs the disassembly)
audio/music/s2-music-93-paced.wav                the bed (ROM render, see below)
provenance/source-map.json   base commit, reused inputs with hashes, music identity and command, tools
provenance/deliverables.json film and master
review/                      pair grids of the takes, consecutive-frame strips, final contact sheet
```

1. Music: build `d823ce643` (build-only), then
   `FmSfxRenderTool --game s2 --rom <S2 REV01> --music 93 --rate 48000 --max-seconds 90 --paced`
   (full command in `provenance/source-map.json`).
2. Edit (Python with numpy 2.5.4 + Pillow 13.0.0; `OPENGGF_WORKTREE` = a tree with
   `tools/media/promo_kit.py` at `c7d66bbf9` or later unchanged): `edit.py check`, `edit.py master`,
   `edit.py mp4`. Clips, SFX and UI tones are read from the production root two levels up, in place.

No engine code changed and no menu was recaptured: every UI frame is a frame of the original takes.

## Music identity

Engine music `0x93` is `Sonic2Music.SUPER_SONIC`, native `$96` `MusID_SuperSonic`
(s2.constants.asm:854), the song the game starts with `SndID_SuperTransform` when Sonic turns Super
(s2.asm:37488-37491). The loader reads it from ROM `$0FCBBC`, between Mus_2PResult and Mus_HTZ as in
the disassembly's includes (s2.asm:91771-91773). Its decompressed header (`F6 15 06 03 01 FA`) matches
`Supersonic_Header`: 6 FM and 3 PSG channels, tempo divider 1, tempo `$FA`. ROM: canonical S2 REV01,
SHA-1 8BCA5DCEF1AF3E00098666FD892DC1C2A76333F9, read in place. The render is sample-identical to
the first 90 s of the original production's unused candidate `audio/candidates/s2-music-93-paced.wav`.

## Viewer pass (every ~4 s: what is new on screen)

| s | On screen |
|---|---|
| 0-3.3 | Emerald Hill run; the old picker pops over the HUD on beat 1; the gold divider sweeps to the framed panel; "SAME GAME. NEW MENUS." |
| 3.3-6.6 | flash; ROAD / TO / 9 pop a beat apart (spindash release, ka-ching); the line |
| 6.6-9.8 | 0.5 game select one bar, pill 0.5; push to the 0.7 hub, pill rolls 0.5 -> 0.7, carousel moves |
| 9.8-13.1 | the old Mod manager opens; cursor; trust page; 3.5 -> 6.5 -> 7.5 -> 8 -> 8.5 a beat apart, divider stepping |
| 13.1-16.4 | 9 and a jump cut: Eggman's Sky's switch turns on, Details opens |
| 16.4-19.7 | old and new side by side at 3x: both cursors march down (ROM? rows vs icons and a scroll bar) |
| 19.7-22.9 | jump cut to the wrong file: error text vs error card; the new score climbs 4 -> 9 |
| 22.9-26.2 | Settings old (truncated labels), one sweep while the score spins to 9; a switch toggles |
| 26.2-29.5 | a value changes; jump cut to the save prompt listing old -> new |
| 29.5-32.8 | six new menus drop in, one a beat |
| 32.8-36.0 | wall dims; families at 9 tally 0 -> 13 -> 26 with pass tags |
| 36.0-39.3 | 27 / 27 slam and flash; banner; menus relight one by one; Giant Ring iris into the delivered hub, carousel moves |
| 39.3-43.2 | end card lines on the riff's steps; the stab; fade to black |

## Checks (measured on the final files)

- ffprobe: both 1920x1080, 60/1, 2,592 frames, 43.200 s; MP4 H.264 High L5.0 yuv420p BT.709 TV
  range + AAC LC 48 kHz stereo; master FFV1 bgr0 + PCM s16le; 8 chapters in the same order and
  times in both (0, 3.283, 6.550, 9.833, 16.383, 22.933, 29.483, 37.267 -> 43.200 s).
- Full decodes `ffmpeg -v error -xerror` of MP4 and master: exit 0, 2,592 frames each.
- Source intervals (`edl.csv`): 22 era/take intervals, none past its take's last frame.
- Pixels: 20/20 sampled panes exact integer nearest-neighbour copies of their source frames in the
  master (4x panes, 3x side-by-side panes except the one native column under the 6 px centre rule,
  2x wall cells, the 0.5 and hero shots).
- Motion: no frozen runs (>= 20 identical frames). Consecutive-frame strips at every transition,
  tick, jump cut, the slam, the iris and the fade (`review/strips-*.png`).
- Sound (AAC, ebur128): integrated -15.0 LUFS, true peak -1.6 dBTP; chapters -16.7 (cold open,
  the intro bed) to -14.1 LUFS (Pickers), all <= -1.6 dBTP. L/R within 0.3 dB in every chapter;
  digital silence after the bed cut (frame 2567 on).
- Stingers against the bed under them (loudest 100 ms): swish -9 to -7 dB, blips -8 to +14 dB,
  Tally End +3 to +11 dB, spindash +4 dB, Giant Ring +4 dB, UI tones +4 to +12 dB; all centred;
  no `promo_kit` balance warnings.
- `edit.py check`: no warnings; 13 shots, mean 3.3 s, busiest 20 s window 8 cuts.

Limits: sound was checked by measurement only; nobody listened to the mix. Motion was reviewed
through consecutive-frame strips, contact sheets and per-frame measurements, not by real-time
viewing. The UI cue tones' alignment to the bed's beats drifts by up to a few frames because the
takes were recorded on the old bed's 26.25-frame beat grid; they stay on their picture frames.

## Archive payload

`archive-payload/` (built by `sources/archive/make_revision_payload.py`) holds the additive
OpenGGF-Media payload for project `menu-evolution`: this revision's text sources under
`projects/menu-evolution/super-sonic-cut/`, the updated project index, and catalog fragments.
Film, master, the music render and review images stay external and are hashed.
