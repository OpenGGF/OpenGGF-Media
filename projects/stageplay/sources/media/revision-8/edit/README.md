# Revision eight edit — first-time directors

`build_edit.py` implements the approved story-first cut. It opens with the complete
short, introduces a clearly labelled six-second paused rehearsal, runs the native
scene exactly once without skipped action or retiming, shows one real A/B sequentially, and
ends over eight seconds of **new** moving-platform tail. For a 26-second story and
two five-second comparison windows the film is 76 seconds. `--pause-frames 0`
removes the deliberate instructional freeze if the source reading time permits.

The native 320×224 picture becomes 1280×896 through nearest-neighbour scaling;
no actors or scene edges are cropped. It occupies 55% of the 1920×1080 canvas.
The story uses a centered cinema-like margin and simple title, without lesson
notes. Instruction uses a 560-pixel side column: one large condensed heading,
one 42-pixel explanation and a restrained 34-pixel command cue. Editorial
annotations are labelled. Notes partition the **actual measured source timeline**,
so changing a note never restarts the action. There is no seven-slide feature list,
tiny fake timeline or repeated ending climax.

The navy/cream/gold Fira treatment follows the existing production and the
Slay the Robotnik code/live-view hierarchy, adapted to sustained dialogue.
All scene and dialogue panels remain untouched. `preview-provisional.png` is a
layout check against revision seven, **not revised performance evidence**.
The provisional manifest assumes tail/A-B timings only for layout checks; it
does not authorize rendering those old intervals as a film.
The black viewport in the standalone layout PNG is transparent, filled by footage.

## Build

Requires Python 3/Pillow, FFmpeg/FFprobe and the two external Fira files declared
at the top of the script (SIL OFL). Use `--font-dir /path/to/fonts` to relocate
both named files. Every text line checks its actual drawn bottom against the
canvas/column boundary; oversized notes or an endcard collision fail explicitly. All output must be a new take directory.
No engine, desktop or Maven invocation is part of this compositor.

```bash
python3 build_edit.py final-manifest.json \
  --music ../../revision-7/music-bed.mkv \
  --out candidate-01 --standalone
```

For preview-only validation use `--previews-only` and a different output directory.
The script refuses overwrite, validates source aspect/cadence and interval bounds,
and emits precise `chapters.json` and `plan.json`. Intermediate FFV1 normalized
segments use finite disk-backed temporary storage and four encoding threads.
They are deleted on exit. The MP4 receives one final H.264/AAC encode, chapters
and fast-start metadata. Source PNG/Matroska frame timestamps are explicitly
normalized to timebase 1/60 before framesync; this avoids a measured one-frame
loss at each segment's EOF. Output is CFR 60, with no unlabeled holds or speedups.

`--standalone` makes `finished-short.mp4` from the source story and its original
combined soundtrack. This separate copy does not layer another bed over it.
The main tutorial ignores every video source's audio. Only explicit `paths.sfx`
and `paths.comparisonSfx` enter the mix. Missing stems give silent effects,
never fallback combined music; resolve missing stems before approving delivery.
The existing 98-second revision-seven `music-bed.mkv` is the continuous native
DEZ2 ROM track ID 23, rendered through OpenGGF, with provenance in revision seven.
It is trimmed once from zero, never restarted/looped. Default music and SFX gains
are both 0 dB; both are configurable **globally**, not per chapter. A 0.85 linear
ceiling limiter provides mix headroom and a 1.5-second final fade ends the bed.
Meter the actual AAC before choosing final gains. No listening is claimed.

## Manifest contract

Paths are relative to the manifest directory. `fps` is 60. `storyFrames` excludes
the new tail; `totalFrames` includes it. Required paths are `story`, `clean`,
`comparison`; optional paths `sfx`, `comparisonSfx` must be genuinely SFX-only.
`story` includes dialogue; `clean` omits it but matches the native performance.
Source identities, measured markers and evidence can remain in additional fields.

```json
{
  "fps": 60,
  "storyFrames": 1560,
  "totalFrames": 2040,
  "paths": {
    "story": "story.mkv", "clean": "clean.mkv",
    "comparison": "variant.mkv", "sfx": "sfx.wav",
    "comparisonSfx": "variant-sfx.wav"
  },
  "tutorialNotes": [
    {"startFrame": 0, "endFrame": 1560,
     "title": "DIRECT A CHOICE", "body": "Replace this with measured event-linked notes.",
     "command": "Actual command and value from the screenplay"}
  ],
  "comparison": {
    "startFrame": 600, "endFrame": 900, "variantStartFrame": 600,
    "labelA": "A · ORIGINAL", "labelB": "B · ONE CHANGE",
    "change": "State the real single changed setting.",
    "outcome": "State the measured visible consequence.",
    "commandA": "original value", "commandB": "changed value"
  },
  "endcard": {
    "frames": 480,
    "samplePath": "examples/stageplay-demo/wait-for-me.stageplay",
    "url": "github.com/OpenGGF/OpenGGF", "status": "Development preview"
  }
}
```

Use several short notes with sensible reading time, jointly covering [0, storyFrames)
with no gaps/overlaps. Put upcoming choices slightly ahead of their measured event;
keep consequences visible. A/B windows must include the comparable outcome in both
sources. The compositor does not derive empirical claims or fabricate measurements.
Path wrapping inserts visual whitespace after slashes; EDL/manifest paths are exact.

## Focused verification and remaining work

Focused temporary codec tests used one second of revision-seven footage with
artificial intervals. The first test exposed EOF framesync loss (97/102 frames).
Normalizing both input timebases fixed it: 102/102 frames without a pause and
114/114 with the deliberate pause, 1920×1080 at 60/1 with H.264/AAC and exact
chapter boundaries. Both corrected files fully decoded; standalone encoding and
Python compilation passed. Regenerable codec artifacts were deleted after review.

The housekeeping check generated nine layouts from the existing provisional
manifest using explicit `--font-dir`, then removed its temporary directory.
An intentionally excessive note raised the expected bottom-bound error. A
representative provisional composition was inspected as an image; this does not
establish normal-speed motion or audio quality.

Before delivery parent must adapt/read the real scene manifest; check event-linked
note content, dialogue/panel motion and the comparison outcome; render the full
candidate; compare decoded frame count and chapter boundaries with the EDL; fully
decode using `ffmpeg -v error -xerror -i candidate-01/tutorial.mp4 -f null -`; meter
integrated/sectional loudness and true peak **after AAC encoding**; perform full 1×
playback; archive source code/manifest/provenance in OpenGGF-Media with external
media catalog entries. Final scene/candidate/archive are not yet certified here.

Final editorial correction: `final-manifest.json` derives from the immutable scene
manifest and chooses `source: story` for the count-in note only. The dialogue
becomes visible at the same source frames; every native actor/camera/world sample
remains continuous and equivalent. Candidate 01 hid the count while explaining
it; candidate 02 corrects that teaching gap. Earlier candidate retained as superseded.

In `final-manifest.json`, the compositor `paths` map is relocated relative to
`edit/`. Inherited scene asset/provenance paths still refer to the original
`scene/manifest.json` directory; use that immutable manifest to verify captures.
Final results are recorded in the parent production README and candidate-02 evidence.
