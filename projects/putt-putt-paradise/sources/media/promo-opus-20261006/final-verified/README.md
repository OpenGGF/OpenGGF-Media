# Putt Putt Paradise: public promo, final verified revision (r5, 2026-10-06)

`putt-putt-paradise-promo.mp4` is an 88.8-second promo for a general audience interested in the
OpenGGF engine. It is 1920x1080 at 60 fps, H.264 with 48 kHz AAC, and carries 12 chapters. All
gameplay is real engine footage at normal speed with its own recorded game audio, including the
whole-shot rewind heard in reverse.

It replaces the 87.0 s draft in `../final-polish/`, which is kept, unshipped. That draft's host and
practice audio had long DC-flat stretches with the zone music missing, and its rewinds played the
music forwards. Earlier revisions in `../intro-audio/` and `../paced/` are kept unchanged.

## The film
| Time (s) | Chapter | Footage |
|---|---|---|
| 0.0 | OpenGGF: the open-source engine for classic Sonic | OpenGGF 0.6 Sonic 2 promo shots, muted, under the ROM Title Screen theme |
| 5.4 | What if Sonic was the golf ball? | Sonic's power sweep, spin dash and launch, then "...or Tails?" |
| 10.8 | Putt Putt Paradise: Sonic 2 Mini Golf | The mod's menu with its ROM menu music. Then one take: Practice, START, the engine's fade, Sonic 2's own title card with the Emerald Hill music starting under it, the first tee |
| 17.6 | One button | One full shot; the panel follows the real shot stages: aim, hit point, power, spin dash, roll |
| 25.0 | Real Sonic 2 physics | Every loop, every spring, every sound |
| 36.0 | Rewind a whole shot | The VHS rewind, with the shot's own sound played backwards, and the stroke refunded |
| 41.1 | Two holes, two golfers, three ways to play | 1 button, 2 holes, 2 golfers, 3 ways to play |
| 43.4 | Local two-player | Turn handoff card, ready press, both golfers |
| 52.6 | Online play over direct IP | Host and guest side by side, two engine processes over TCP. Includes the guest's rewind, heard reversed on both peers |
| 63.7 | Make your own with the OpenGGF Mod API | The mod's actual `register` source and its size, beside the local match |
| 68.8 | The final putt: Hole Complete | Tails' last full-power putt, the signpost, Stage Clear and the scorecard tally |
| 79.8 | Learn more | Logo, modes, repository, disclaimers |

## Design
- **Captions and chapter cards** take Sonic 2's own title-card design: blue band, yellow strip,
  red serrated tab. The colours are sampled from the captured title card.
  - Chapter changes are a full mini title card (REWIND, AT A GLANCE, ONLINE, MAKE YOUR OWN).
  - In-chapter cuts use whip pans and a golf-cup iris.
- **Pixel art** is scaled nearest-neighbour by an integer factor, then area-filtered to 1080p.
- **Framing.**
  - Information chapters frame the game at 4x with a side panel.
  - Action uses a HUD-free 16:9 crop.
  - The title take expands from the framed menu to full height as START is pressed.
- **Pace.** No gameplay is sped up or slowed. Every gameplay frame is one captured 60 Hz row.

## Sound
- **Gameplay sound is the game's own.** Each output frame carries its captured row's 800-sample
  packet, from `Engine.presentOuterAudioFrame` through a live capture lease on the headless SMPS
  backend.
- **Rewinds.** The rewinds play the mod's `AudioReplay` reverse presentation as recorded.
  - Every voiced rewind packet in EHZ1 and in both online peers is a sample-exact reversal of a
    recorded forward packet (correlation 1.000), walking back one row per row.
  - See `capture/*/rewind-audio.json`; `verify_promo.py` re-checks this in the decoded film.
- **Cuts.**
  - Cuts crossfade the real audio with equal-power fades.
  - Where Emerald Hill music runs at normal tempo on both sides, the incoming clip shifts by under
    half a beat (at most 10 rows) to keep the pulse (`promo.edl.json`, `beat_alignment`).
  - Each clip is level-matched to the median clip within ±4 dB.
- **Editorial audio** is declared in `promo.audio.json`, the end card and the MP4 comment. It is all
  rendered from the same Sonic 2 ROM by OpenGGF's SMPS driver (`tools/`):
  - the Title Screen theme under the engine opener;
  - the Option Screen theme under the end card;
  - a quiet Spindash Release whoosh on the five chapter cards.
- **Master.** Two-pass EBU R128: −15.0 LUFS integrated, −2.1 dBTP true peak, LRA 5.3 LU, no
  clipped samples.

## Provenance
- **Source.** The captures are `../../showcase-20261006-opus-final/`; see its README.
  - Recorded from `feature/ai-putt-putt-paradise` at `09d5ed2a22db4b759cfd955233ab35df2837b147`:
    82a reverse-audio fixes plus develop `f4b40f5026988c5152eb2ae1fadaaf7c648f5618` (Slay the
    Robotnik PR 211) merged.
  - Engine Java SHA-256 `e54abff60866814fd2f92db14df859ce38e5e1373d0ac8dc1d87f1351c3367a7`.
  - Golf main Java SHA-256 `73d3ddc77f914eadcd6a80fd04be809381b98c12c4efb1fc79140fed5d228407`.
  - Online wire protocol schema 6.
  - Mod jar `55c6e3fc6f04ed58f53cb7abd6113c502b6d874a44fce6b44f8b90391607296a`: `ggfmod validate`
    exits 0, and the jar is byte-identical to a fresh `javac` of these golf sources against the
    built classes (123/123).
- **Reproducibility.** The merged-source captures are byte-identical to the 82a captures in every
  PNG row and WAV. Rendering them again produced this exact MP4: SHA-256 `5bb6b99d…`, with
  identical decoded video and audio MD5s.
- **Route.** Every scenario starts from the production title screen: the menu, then START, the
  engine's fade, the Sonic 2 title card and a fresh course load.
- **Rewinds.**
  - EHZ1: Sonic rewinds his first shot from the Start menu.
  - Online: the guest rewinds its second chip, and the host restores both peers.
- **Engine opener.** OpenGGF 0.6 Sonic 2 promo master (`~/Videos/OGGF/S2-0.6/s2-0.6-V2.mov`),
  centre-cropped to 16:9.

## Checks (`putt-putt-paradise-promo.verify.json`)
- **Browser.** Played at 1x in T3's preview browser from a loopback HTTP server. See
  `browser-qa.json`.
- **Stream.** h264 1920x1080, exactly 60/1 fps, 5328 frames, 88.800 s, AAC 48 kHz stereo; chapter
  titles and order match `promo.chapters.csv`.
- **Full decode.** 5328 frames, no errors.
- **Picture.** 80 samples, 5 inside every gameplay segment away from transitions.
  - In each, the decoded frame is closest to the renderer's composite of its claimed row, not of
    the row before or after.
  - Rows where the game itself is still are marked non-discriminating.
- **Motion.** In every gameplay segment, no output frame holds still while its source row visibly
  moves.
- **A/V sync.** All 16 gameplay segments are cross-correlated against their own captured audio:
  lag 0 samples, correlation 0.94 to 0.999.
- **Reverse audio in the film.** Each rewind row is compared in the decoded film:
  - film packet against the source packet: medians 0.9986 (EHZ1) and 0.9997 (online);
  - film packet played backwards against the forward packet it reverses: the same values.
- **Soundtrack.**
  - The only silent run of 8 frames or more is the 18-row native silence under the Sonic 2 title
    card, and the source is silent there too.
  - `promo.waveform.png` plots the per-frame level, with editorial pieces shaded.

## Rebuild
1. Make a venv: `python3 -m venv .venv && .venv/bin/pip install numpy==2.5.3 pillow==12.3.0`.
2. Render the editorial stems: `tools/render_stems.sh`. This needs an OpenGGF build and your ROM.
3. Capture: in `../../showcase-20261006-opus-final`, follow its README.
4. Render: `.venv/bin/python render_promo.py render`.
5. Verify: `.venv/bin/python verify_promo.py putt-putt-paradise-promo.mp4`, then
   `waveform.py putt-putt-paradise-promo.mp4`.
6. Package: `.venv/bin/python package.py` writes `putt-putt-paradise-promo-kit.zip` and `SHA256SUMS`.

Other `render_promo.py` subcommands are `edl`, `frames N...`, `sheet [step]` (`promo.cuts.png`)
and `clip A B`.

The kit carries the scripts, inputs, per-row state, events and audio-request CSVs, the EDL, the
mod jar and the QA. It has no ROM, no ROM-rendered stems, no PNG rows or WAVs, and no engine build.
The native footage stays in the capture directory, hashed in `native-manifest.json`.
