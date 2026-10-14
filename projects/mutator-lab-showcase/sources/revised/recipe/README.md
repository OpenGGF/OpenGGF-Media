# Mutator Lab: revised pacing and native soundtrack

Root-owned revision after the user rejected cluttered audio and rapid cuts. Opus was stopped on request; its draft and per-take level estimates are preserved separately. The delivered film is `../out/mutator-lab-complete-showcase-revised.mp4`.

The edit is 116.5 seconds, 6,990 frames, 29 shots, 14 chapters; the preceding film was 90.883 seconds / 76 shots. Last 20-second cuts fall from 16 to 3. Each gameplay panel advances one existing captured frame per output frame. There is no new capture, interpolation, freeze or editorial speed change. The No Special Stages outcome deliberately compares different native post-transition times, labelled as loading cut. Bonus denial is S3K-only. Native source setup labels remain visible.

## Rebuild

Use a task-local Python3 environment with `requirements.txt` and FFmpeg 9. No engine/JVM, display or audio device is involved. From the `edit-r2` directory:

```sh
python3 recipe/build_film.py --plan
python3 recipe/build_film.py
python3 recipe/verify_film.py
```

Source archives are read in place:
- `/home/farrell/scratch/agent-tmp/claude/mutator-complete-showcase-20261010/captures`
- `/home/farrell/scratch/agent-tmp/codex/mutator-lab-gameplay-promo-e0603654-55a0-4717-897c-3d93d1137ff3/captures`

`reference_layout.py` preserves the earlier typography/nearest-neighbour panel layout; its original cut list is discarded by the new script. `build_film.py` supplies the new cut list, chapter map and audio envelopes. Native inputs, source PCM/PNGs/CSV and original films are unmodified. The existing source provenance, ROM identities and support limits remain in those archives. Clear regenerable `../work/` before rebuilding after any recipe change; cache reuse is only for unchanged shots. All FFmpeg invocations are bounded and reaped.

## Soundtrack

Follow the Sitar Hero reel's sustained phrases and equal-power handoffs, Multigame's selected audio ownership, and Hardened's intentional cues and quiet outro. One selected panel supplies native mixed music+SFX per continuous shot, with brief 200 ms equal-power joins. Source availability may shorten a join. Configuration windows are lowered 7 dB and low-passed at 1.6 kHz; no separated SFX stems or external score. Level trims are constant per take; final static gain leaves AAC reconstruction headroom rather than pumping or limiting. The 200% music-follow demonstration retains its native timing and waveform; its entire 144-frame passage is protected, with the handoff beginning afterward. The close fades to silence.

`../out/audio-manifest.json` specifies source/output sample intervals, constant trims/global gain, fades and configuration filter envelopes. This is editorial sound, not a raw capture soundtrack. Previous 76-segment PCM-exact measurements do not qualify this new mix. New full-decode/source-panel/cadence checks and AAC alignment are in `../out/verify.json`; selected frame inspection is under `../review/`. No physical-speaker or subjective listening claim is made.

The checkpoint review rejected source ranges containing settings despite `mode=LEVEL`; accepted ranges also require `paused=false`. The dead/run/loading footage is authentic; omitted settings/loading are declared. No repository code changed for this follow-up.
