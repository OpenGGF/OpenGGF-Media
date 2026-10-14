# Sitar Hero promo (edit-v2, final)

`sitar-hero-promo.mp4` is a 71.2-second promo for the Sitar Hero example mod. All 12
chapters are real engine footage at normal speed, each with its own recorded ROM audio.

## Format

| Property | Value |
|---|---|
| Video | 1920x1080 H.264 High, yuv420p, 60 fps, 4,268 frames |
| Audio | AAC LC, 48 kHz stereo |
| Chapters | 12 |
| Size | 19.6 MB |
| SHA-256 | `54903ea2ac7d360e24c903b5f21d8dea8eb4cbfabcf4a2d2789f4d98603f875a` |

## Verification

- `ffmpeg -v error -xerror -i sitar-hero-promo.mp4 -f null -` exited 0.
- EBU R128 loudness: -16.0 LUFS integrated, LRA 4.7 LU, true peak -1.5 dBFS, no
  clipped samples.
- Every cut and every segment was inspected as frames. Audio was checked in 0.5-second
  windows: no dropouts beyond the game's own silent count-in, which lasts about
  0.75 seconds after the menu theme fades.

## Chapter map

Output times are seconds in the promo. Source times are seconds in the raw capture
(tick ÷ 60), relative to this folder.

| Output | Chapter | Source | Source interval |
|---|---|---|---|
| 0.000–5.983 | Sitar Hero: title tableau, wordmark drop, band rehearsing on Angel Island, Data Select theme, cursor clicks | `../raw-v2/career/career.mp4` | 0.0–6.0 |
| 5.983–11.583 | Tour every world: performer, instrument, level, S3K tour, world board | career | 5.98–11.6 |
| 11.583–19.267 | A satirical career: Angel Island intermission, three lines | career | 11.58–19.67 |
| 19.267–21.367 | Full songs: big-ring cue, ROM title card slides in | career | 21.6–24.0 |
| 21.367–27.967 | Count-in and Sonic on sitar (Angel Island 1, DEMO) | career | 194.0–201.0 |
| 27.967–32.567 | Knuckles on bongos, Sonic 1 Green Hill | `../raw-v2/gh-bongos/gh-bongos.mp4` | 138.33–143.33 |
| 32.567–37.167 | Tails on synth, Sonic 2 Chemical Plant | `../raw-v2/cpz-synth/cpz-synth.mp4` | 158.33–163.33 |
| 37.167–41.767 | Robotnik on harp, S3K Launch Base 1 | `../raw-v2/lbz-harp/lbz-harp.mp4` | 169.17–174.17 |
| 41.767–48.867 | Local score duel: Mecha Sonic vs Robotnik, Sky Sanctuary | `../raw-v2/duel/duel.mp4` | 132.5–140.0 |
| 48.867–57.633 | Streaks and Star Power: 50-note banner, READY, activation at ×8 | `../raw-v2/finale/finale.mp4` | 152.5–161.67 |
| 57.633–63.633 | Results: song end, act-clear jingle, tally, stars | finale | 251.83–258.33 |
| 63.633–71.133 | Play it: title after two returns (Chemical Plant venue), launch caption | `../raw-v2/outro/outro.mp4` | 2.0–9.5 |

## Edit

- **Files.** `edit-list.json` is the edit list. `render_promo.py` and `pixelfont.py` are
  the exact assembly scripts. `sitar-hero-promo.edl.json` holds the resolved intervals
  and the first loudness pass.
- **Command.** `python3 render_promo.py edit-list.json --sitar-ui <worktree>/examples/sitar-hero/src/main/java/sitarhero/ui/SitarUi.java --out sitar-hero-promo.mp4 --work <tmp>`.
- **Framing.**
  - Each 800x448 capture (400x224 at 2x) is scaled nearest-neighbour to 1600x896 (4x)
    and framed on a 1920x1080 stage.
  - Captions use the mod's own 5x7 font, parsed from `SitarUi.java`.
- **Joins.**
  - Contiguous moments of the career take are joined with a one-frame dissolve.
  - Other cuts use 0.3–0.5-second dissolves with equal-power audio crossfades.
  - There is a two-pass loudnorm to -16 LUFS.
- **Speed.** No footage is sped up or slowed: one captured tick is one output frame.

## Honesty notes

- **Autoplay.** Every performance is the scene's tool-only autoplay. The game shows
  **DEMO** and saves no record, which the results footer states.
- **Loading.** Loading spans are cut. The capture loop is not paced to the wall clock,
  so its loading lengths are not real time.
- **Multiplayer.** Two-player footage is local only; no direct-connect session was
  captured, so none is shown.
- **Timing.** Offline audio shows content and cue timing. It does not show speaker
  latency, controller timing or NAT behaviour.
- **Stages.** Emerald Hill is staged on Chemical Plant because the ROM pictures no
  Emerald Hill act. The game names the song; the chapter map lists the venue.

## Provenance

The raw captures are in `../raw-v2` (see its `README.md`, `provenance.txt` and
`commands.txt`). They were recorded from `feature/ai-sitar-hero-polish` at
`676a433c49f3fc001f25e3df90daa275480f4e7f`, which is the polish commit `fd39e29bc` merged
with develop `33d3976c5`.

All 40 mod source/resource files hashed at capture time match that commit. The only
uncommitted paths at capture were three documentation files.

ROM SHA-1 values:

| ROM | SHA-1 |
|---|---|
| S1 | `69E102855D4389C3FD1A8F3DC7D193F8EEE5FE5B` |
| S2 | `8BCA5DCEF1AF3E00098666FD892DC1C2A76333F9` |
| S3K | `CFBF98C36C776677290A872547AC47C53D2761D6` |

The running game was S3K, which supplies the menu audio. After final verification,
the earlier draft captures/edit, one-off preview helpers, consumed render logs and
compiled build copies were removed. The final raw-v2 captures and audio, scripts,
source hashes, edit list and chapter map are preserved. The repository's dated
presentation-polish design records the rejected approaches and audio investigation.
