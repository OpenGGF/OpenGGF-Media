# Your first scene — revision eight

Audience: first-time Stageplay creators. This revision implements the approved
Opus 5.5 aesthetic direction with Sol scene and edit work: play the complete
26-second *Wait for me* short, explain it in one continuous annotated pass, change
one real jump setting, then invite the viewer to open the sample. The new ending
uses another eight seconds of native platform travel. It does not replay the
climax. Navy, cream and gold Fira typography accompanies a 4× native game view on
a 1920×1080 canvas. The count-in lesson retains its matching native dialogue to show reveal timing.
Editorial notes are explicitly labelled; they are not editor UI.

The preceding 124-second tutorial repeated scene fragments across seven lessons
and used small static notes. The review also found a roughly 7–8 LU increase at
the story boundary. Its evidence was source inspection, sampled images and audio
measurements, not full-motion viewing or physical listening. Earlier revisions
remain immutable and are not retroactively approved by this replacement.

The story acknowledges Tails can fly; crossing together is now an explicit choice.
Sonic crouches in response, returns, and finishes the count immediately before
native takeoff. Panels clear the platforms and jump arcs. The comparison changes
only Sonic's first jump hold from 20 to 8 frames. Both attempts land on the same
platform; native measurements show a 20.34375-pixel lower apex and landing eight
frames sooner. Initial positions are authored. This is a bounded LIVE performance,
not automatic pathfinding, cold level completion or ROM-parity evidence.

## Rebuild

Supply the ROM identified in `scene/manifest.json`, Java 25, Lua 5.4, FFmpeg and
Python/Pillow. Follow `scene/README.md` for the exact engine package, scene generator,
compile/simulate/capture commands and retained takes. The bundled engine example
is `examples/stageplay-demo/src/main/resources/scenes/wait-for-me.stageplay`.
All motion uses production Puppet inputs and native placed-object contacts.

`edit/README.md` documents the manifest-driven compositor and font relocation.
Its explicit rehearsal pause is labelled; every moving source interval runs at
native 60 Hz. `edit/candidate-02/chapters.json` records exact source/output frames.
One continuous ROM music stream and genuine native SFX stems have separate owners;
combined scene sound is not layered over a second music bed.

```bash
python3 edit/build_edit.py edit/final-manifest.json \
  --music scene/continuous-music.wav --out edit/candidate-02 \
  --music-gain-db 9 --sfx-gain-db 3
python3 verify_edit.py edit/candidate-02
```

Output directories are exclusive-create. Choose a new take when rebuilding.
Fira Sans Compressed Heavy Italic and Fira Sans Medium are external SIL OFL fonts;
use `--font-dir` to relocate them. ROMs, videos, audio, screenshots, packaged engine
and bulk native state remain external. Public production sources and their catalog
belong to `OpenGGF/OpenGGF-Media/projects/stageplay/sources/media/revision-8/`.
The catalog is not a video download service.

## Verification status

The final tutorial has 4,500 decoded frames at 1920×1080 / 60 Hz, eleven exact
chapters and stereo 48 kHz AAC. `verify_edit.py edit/candidate-02` passed a full
FFmpeg `-xerror` decode and frame/interval/chapter checks. Encoded audio measures
−17.3 LUFS integrated and −4.6 dBTP. Story and moving lesson sections measure
−16.5 to −18.0 LUFS; the explicitly paused rehearsal is quieter at −20.3 LUFS,
with only the continuous music, and the fading ending measures −18.4 LUFS.
There is no source-music restart or per-chapter gain switch.

Selected full-size frames, all cut boundaries and native contact/apex sheets
were inspected. Candidate 01 decoded and played correctly but hid the count
while explaining it; candidate 02 uses matching dialogue frames for that note,
without changing the world/action interval. The 26-second standalone completed
1× browser playback with 1,560 frames and zero reported drops. Final tutorial
browser playback also completed at 1× with all 4,500 frames and zero reported
drops; the record is retained in `production-provenance.json`.

The source package built once with `package -DskipTests`; all six native sources
compiled, simulated, rendered and fully decoded. The integrated bundled scene
matches those validated source bytes. Policy checks, Python/JSON syntax and
mirrored skill checks passed. No engine smoke/full-suite or ROM-parity pass is
claimed for this content-only change.
Physical listening and user creative acceptance are not claimed.
