# Second Strike — AIZ development excerpt

This **47-second / 2,820-frame** edit uses four long, ordered excerpts
from one native-entry Sonic solo development capture. There are three picture
cuts, with only one cut in the final twenty seconds. It is rendered, fully decoded and reviewed at the bounded scope below; source publication follows the normal Media delivery flow. Earlier production
sources and the 2026-10-14 film remain unchanged.

| Output | Source frames, end exclusive | Source seconds | Story |
| --- | --- | --- | --- |
| 0–10 s | 10000–10600 | 166.666667–176.666667 | Forest approach and native lookout passage |
| 10–20 s | 11750–12350 | 195.833333–205.833333 | Guarded fire continuation |
| 20–32 s | 13560–14280 | 226–238 | Warning, second wave and native fatal hit |
| 32–47 s | 15035–15935 | 250.583333–265.583333 | Playable Act 2 arrival and traversal |

All ranges use integer native frame boundaries. The selected rows are alive
`LEVEL` frames, not menu/results footage. The first shot carries one ring, the
second carries zero or one, and the final two carry zero. Those observations do
not establish a complete ring-placement inventory or promise every enemy change
is visible. In particular, do not claim a long Caterkiller from this edit without
new observed movie evidence.

The interval 10400–11400 was rejected as a whole: it includes a long stationary
native fire/reload presentation. The short lookup actor appears at 10483–10528.
The first-boss warning runs 13603–13618, the follow-up starts 13619, HP reaches zero
at 14217 and native defeat state follows 14230. Results run 14556–15033. Physical
act 1 from 11293 remains the apparent Act 1 fire continuation; actual Act 2 input
readiness begins 15035. The route dies later at 16089. This edit ends 15935.

## Source and qualifications

The source is `cold/sonic-solo-r7/cold-campaign.mkv`, 320×224 FFV1 at 60 fps with
synchronized stereo 48 kHz FLAC, 16,090 frames /268.166 s /1,550,352,897 bytes.
CSV frame 0 maps to movie frame 0; each video frame corresponds to 800 stereo audio
samples. Full identities, exact inspected milestones, provided engine HEAD,
staged source tree and the separately loaded creator-jar hash are in
[`provenance.json`](provenance.json). The source engine/driver development HEAD is
`22841e86ae4de2fd4206bef5cab0cad535127728`, with staged source tree
`6508a7a64826a0aba53a09d1aba2e0dfa79d503a`. This is not today's C3 candidate or a
claim of delivered-revision footage.

[`capture/`](capture/) preserves the exact admitted ordinary-input script,
graphics receipt and completion/mux summary. The original capture invocation is
not present in that summary; none is invented here. Rebuilding this *edit* uses
the existing external movie and small capture files, without launching Engine.
Recapture, if ever needed, requires the original driver and its actual source
state, rather than guessing from current main.

This is a development excerpt reaching playable Act 2, not a complete AIZ route,
HCZ handoff, whole campaign, native-parity claim or physical-speaker measurement.
The editorial omission of native waits/results is declared. The existing stills
support chosen scene/milestone identity, not moving or subjective audio approval.

## Picture and audio

Native gameplay advances one frame per output frame at 60 fps, without speed
changes or interpolation. Integer 3× nearest-neighbour scaling produces 960×672
gameplay centred on a 1600×900 canvas, with captions outside play. No ROM-derived
art is added to the surrounding canvas.

Each shot uses its own **synchronized original mixed music+SFX**, fixed −1.5 dB
gain, and 50 ms opening/closing fades. Fades do not overlap, so two source excerpts
never own the output audio simultaneously. There is no external score, music
loop, isolated/invented SFX, extra audio recording or dynamic loudness pumping.
The boss warning and follow-up lie well inside the third shot, beyond its fade.
This policy is different from the older reel's continuous music-only stem.

## Relocate and assemble

Supply Python3, Git (destination safety check), ffmpeg/ffprobe and DejaVu Sans with an explicit `--font` if the default path differs on your host. Put the
external `cold-campaign.mkv`, `state.csv`, `admitted.script` and `capture.txt` back
under one relocated `sonic-solo-r7` directory. The root catalog identifies their
original location; no movie, frame dump, audio recording, ROM, save or packaged
mod bytes are included in Git. Small archived capture sources can be copied to
that working directory if missing. Keep earlier captures and films untouched.

```sh
python3 assemble.py --capture-root /your/capture/sonic-solo-r7
# After the host grants normal admission and the intended-tree lease:
python3 assemble.py --capture-root /your/capture/sonic-solo-r7 \
  --output-root /your/new/external/reel-directory --font /your/DejaVuSans.ttf --render
```

The default prints a plan after checking source size, small-file SHA-256 values,
the CSV-selected frames and the ffprobe header; it does not encode or create an
output directory. `--verify-movie-sha256` additionally hashes the 1.55 GB input and
must be used only when that I/O is appropriate/admitted. The recorded movie hash was independently recomputed inside the first admitted root attempt and matches the capture owner. A render refuses a nonempty output directory and any output inside
this source archive.

The lead owns scheduling. On an OpenGGF development host it can run the render
inside the existing normal `maven_slot`/`handle_termination` owner from the
intended engine worktree's current `tools/testing/maven_queue.py`; these pure
media sources do not bypass that admission or automatically launch another job.
There is no Java, engine, display or audio-device dependency in this assembly.

The first admitted root attempt (7099) verified the movie SHA-256 but stopped
before FFmpeg: the original fixed ancestor-offset guard treated a relocated
standalone source copy's host directory as the archive. No film was created.
The corrected guard detects actual Git working trees and protects the source
directory itself. A real inside-Git destination is rejected before encoding;
the second attempt (65175,645seconds admission wait) also stopped before FFmpeg: empty host `.git` directories were mistaken for repositories. The final guard validates actual Git working-tree identity and has been checked against both the external scratch location and real Media/engine worktrees. The relocated `source-r3` attempt uses a fresh external `render-r3` directory.
Attempt38036 then passed the corrected destination guard but stopped before encoding because the Debian-style default font path was absent here. The installed `/usr/share/fonts/TTF/DejaVuSans.ttf` is now passed explicitly and identified in provenance; Git, encoder/filter availability, font readability and destination checks were verified before submitting `source-r4`/`render-r4`. Earlier source copies remain external as historical material. These corrections do not change the four source intervals, native cadence, picture or audio. FFmpeg on this host also rejected the removed `-filter_complex_script` option in39327 before any movie was encoded; source-r5 supplies the exact same preserved graph through supported `-filter_complex` argv instead. Its option availability is checked against the installed FFmpeg help before admission.

The script creates a single final H.264/AAC encode with chapters and fast-start
metadata. It preserves its exact argv/filter graph, copies the EDL/provenance and
records a header probe alongside the unreviewed output. It deliberately creates
no pass/approval receipt. Source videos are read in place, not copied into Git.

## Observed output and review

The external finished movie is `render-r5/second-strike-aiz-development.mp4` under
`second-strike/aiz-campaign-production`: **106,628,242 bytes**, SHA-256
`df7529b0fb89add3fce4c1f54238160155661da9a0ee65155799b20ee99e4bf6`.
The actual H.264/AAC file is47seconds,2820frames,1600×900 at60fps, with stereo48kHz
audio and chapters0–10/10–20/20–32/32–47seconds. Full decode exits0 and produces
exactly2,256,000 stereo frames. Decoded audio peaks at−9.656315dBFS with zero
NaN/infinite samples; fixed gain and nonoverlapping fades do not layer sources.

One uninterrupted1× T3 browser playback reaches the end without mid-playback
stall or corruption (2820frames reported,1dropped by that preview). Selected moving
chapter, caption, interaction/consequence and all three cut boundaries were
inspected; four sampled motion-hash sets contain48/48/57/72 distinct frames.
The235 browser audio-analyser samples are nonzero. Playback uses zero output gain:
this is decoded-stream analysis, **not subjective listening, physical speaker
latency or native pixel/audio parity certification**. The initial simple local
HTTP server lacks byte-range seeking; subsequent paused cut checks use a fully
loaded immutable movie Blob. No movie bytes changed during review.

[Provenance](provenance.json) preserves actual identities, bounded review and
failed pre-encode host setup history. [Recorded argv](recorded-command.json) and
[filter graph](recorded-filters.txt) preserve the exact successful assembly;
relocate paths or use `assemble.py` to regenerate them. No new capture or Engine
run was used for this edit. Native source footage/inputs and earlier films remain
untouched. The external asset catalog inventories locations, not downloads.
