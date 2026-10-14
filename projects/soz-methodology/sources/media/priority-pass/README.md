# SOZ sprite priority pass — 2026-09-16

All captures use the production GameLoop after a positioned setup. They are
visual inspection evidence, not native-emulator pixel parity or full cold routes.
PNG stride is four gameplay frames; encoded movies are 15 fps at real-time speed.

- `act1-victory-wide800`: intermediate mask/dust correction, before shared order correction (PNGs/CSV).
- `act1-victory-wide800-final`: corrected shared ordering, Sonic + Tails, native movement, 800px; arena entry, golem defeat and playable Act2. All 5,325 gameplay-state rows match `../acceptance-followup/act1-victory-wide800/state.csv` exactly.
- `act2-mechanisms-final/{upper,lower,rock,switch}`: native movement at 400px. Upper/rock/switch use Sonic + Tails; lower is solo. Respectively 680, 3,065, 240 and 180 state rows.
- `act2-boss-final`: Sonic solo at 320px; eight hits, capsule/results and playable Lava Reef. All 3,050 state rows match `../completion-endboss-victory/native-320/state.csv` exactly. Includes executed input log.

Each final directory contains lossless PNG frames, `state.csv`, and `capture.mp4`.
Movies passed full FFmpeg decode checks. The chronological highlights use the
corrected Act1 arena/defeat/handoff and Act2 boss/rescue/handoff footage. All earlier
captures and the original archival compilation remain intact.

## Complete correction

`complete/` supersedes the earlier `*-final` directories, which are retained as
intermediate evidence before the pillar art-word and BG-high mask fixes. It holds
`act1-victory-wide800`, `act2-boss`, and `act2-mechanisms/{upper,lower,rock,switch}`.
All six state CSVs are identical to their intermediate counterparts; all six
movies pass full decode checks. The highlights use these final boss/transition
clips and the lower-room rising-sand interval at 16–28 seconds.

`native-sand-priority-1` is a positioned native controller observation that dies
before the desired comparison height. `native-sand-priority-held-1` is explicitly
an isolated presentation probe: P1 is repeatedly held at 22A0/0340 from frame500,
while native sand/pillar routines advance. Both have 1,600 sequential observation
rows, completion markers and successful host results. Only the held probe has no
level-frame-counter reset. Its 960/1200/1440 screenshots corroborate burial of
the pillar/spikes; they do not establish ordinary route completion or trajectory
parity. Native frames are kept in the archive, not added as stills to the reel.

Latest Act 1 source: `complete-debris/act1-victory-wide800/`, with native detached-part and hit-reaction priority rules. All 5325 state rows match the preceding capture; full movie decode passed. Earlier captures remain intact.
