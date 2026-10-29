# ROAD TO 9: OpenGGF menu evolution promo

## Latest delivery: the Super Sonic cut (2026-10-29)

The half-length recut [`production/revisions/super-sonic-cut/`](production/revisions/super-sonic-cut/README.md)
answers the user's review of the first film, "bit slow and repetitive. Do it against the S2 super
sonic music, half the length". Its external film `revisions/super-sonic-cut/final/menu-evolution-super-sonic-cut.mp4`
is **43.200 seconds** (2,592 frames), 1920x1080 at 60 fps, H.264 with AAC stereo 48 kHz
(integrated -15.0 LUFS, true peak -1.6 dBTP) and 8 chapters, with a lossless FFV1 + PCM master.
Made by **Claude Opus 5.5 (xhigh)**; delivered for review, so the user's acceptance is not recorded here.

It is cut on Sonic 2's Super Sonic music (engine `0x93`, native `$96` MusID_SuperSonic, ROM
`$0FCBBC` of canonical S2 REV01, rendered with `FmSfxRenderTool --paced`), one bed from its first
sample to the G-major stab ending its third loop's intro. It reuses the first film's authentic
captures unchanged. The round-0 grid, the long prologue and the fourth rep are gone. Three matched
comparisons remain, and each climbs differently: stepwise on a divider, side by side at 3x, or
in one spinning sweep. Then come 27 / 27 on the track's cadence and a Giant Ring iris into the
delivered hub. Sound was checked by measurement only, and motion through consecutive-frame strips.

- [Revision README](production/revisions/super-sonic-cut/README.md): what changed and why, music identity,
  viewer pass, checks and limits.
- [Edit](production/revisions/super-sonic-cut/sources/promo/edit.py): brief and beat sheet in its docstring;
  chapters, per-shot source intervals and UI cues beside it.
- [External assets of the recut](external-assets.super-sonic-cut.json): film, master, the music render and
  review images, hashed and not uploaded.

## First delivery (87.333 s, retained)

The sections below describe the first film, which the user found "bit slow and repetitive". It
stays byte-identical with its edit, captures and records; the recut reads those captures in place.

Finished production, 2026-10-29. The external film `final/menu-evolution-promo.mp4` is **87.333 seconds**,
1920x1080 at 60 fps, H.264 with AAC stereo 48 kHz (integrated -14.2 LUFS, true peak -1.4 dBTP) and
10 chapters; a lossless FFV1 + PCM master sits beside it. Made by **Claude Opus 5.5 (xhigh)** for the
request "a promo video of the old menu vs the new one. Could even include the old 0.5 menu", steered
to "an action movie montage, with various numbers slowly climbing".

A training montage for the engine's menus: the OpenGGF 0.5 game select (`77c6364ce`), the 0.7 menus
before the redesign (`2f9ca84b1`) and the delivered menus (`d823ce643`), each recorded frame by frame
from its own production code with scripted keys. Old and new run the same task in sync while a
before/now divider sweeps across one pane and the design review's dated scores climb to 9; the
climax counts menu families at 9 (0 -> 13 -> 26 -> 27). The scores are the review's subjective
judgments (docs/architecture/audits/2026-10-27-menu-design-review.md), not usability measurements;
the end card says so. Sound was checked by measurement only; real-time viewing was replaced by
consecutive-frame strips and per-frame measurements.

## Sources

- [Production README](production/README.md): eras, rebuild steps, capture notes and limits, revisions
  and the viewer pass.
- [Edit](production/sources/promo/edit.py) (promo_kit compositor): brief and beat sheet in its docstring,
  every score with its round, date and audit section, audio prep and the master/MP4 commands.
  Superseded edit snapshots: `production/sources/promo/revisions/edit.r2.py`, `edit.r3.py`; `edit.r3b.py` = final.
- Chapters, edit list and UI cue map: `production/sources/promo/{chapters.txt,edl.csv,cues.json}`.
- Capture: `production/sources/capture/capture.py`, the recorders (`java/` for 2f9ca84b1 and d823ce643; `java05/`
  for 0.5 with its EGL compatibility shim) and the beat-grid take recipes `takes/*.take`.
- Capture records: `production/clips/<era>/<take>/{events.csv,provenance.json,take.txt,state.csv}`.
- Provenance: `production/provenance/source-map.json` (commits, build commands, ROM identities, fonts, tools),
  `production/provenance/deliverables.json` (film/master hashes).

## External, not uploaded

[external-assets.json](external-assets.json) hashes the film, master and superseded revisions, every
native frame sequence, the ROM-derived music/SFX renders, the synthesised UI tones, review images and
the Fira faces. ROMs, compiled trees, the Python environment and logs are excluded.
