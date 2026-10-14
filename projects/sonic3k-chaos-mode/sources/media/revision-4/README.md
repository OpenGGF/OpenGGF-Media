# Sonic3K Chaos Mode — focused gallery revision 4

Completed export: `out/sonic3k-chaos-mode-demo-v4.mp4`, 106 seconds, 6,360 frames, 96,779,395 bytes. SHA-256: `1775172882038bc1d50de22c8c66e054bc1ddb43679480997a0046661a978558`.

The edit selects 20 distinct effects across 12 zones in a stationary card gallery. One large native-cadence picture plays at a time; completed effects accumulate in the right wall. Gentle 18-frame dissolves retain the earlier ROM lettering and humour. The export is 106 seconds at 1920×1080 / 60 Hz, with 22 chapters. Secret minigames and related challenge/chat footage are omitted.

“Ring Repellent” uses the existing `ring-repulsion` / “Get Away, Rings!” effect instead of the attraction demonstration. The mod's 105-effect pool is unchanged. The packed JAR is byte-identical to revision 3 (`e5460b29643b176683ba0a62eaeeff413a24d717aed112c9e84294ae36be1d02`). No production engine changes were needed for this media revision.

## Borrowed production methods

The music and SFX capture borrow Slay the Robotnik and Flappy Tails' creator scene soundboard route: `ctx.audio()` → normal AudioManager / S3K profile / driver-session presentation producer. Earlier asset names alone were not accepted as DAC proof. Typing of the Hedgehog supplied the established ROM-lettering/plate style, and Mutator Lab's restrained revised mixing informed a single coherent bed.

The previous music exporter, `FmSfxRenderTool`, used a legacy physical policy and direct stream reads that bypassed S3K's queued native DAC enable service. Revision 3 also deliberately ducked HCZ and retained the ghost picture's entire DEZ mixed PCM. This revision replaces that media workflow; it does not claim to fix the general exporter.

## Source qualification

Nineteen picture intervals reuse earlier qualified lossless masters. Their positioned/checkpoint entry qualifications remain intact: this is a curated showcase, not a continuous route completion. `cards.json` is the authoritative selection; prior revisions and source intervals remain preserved.

The new ordinary AIZ1 take `repellent-early-brake-aiz1` uses scripted controller input only, without position/ring/world writes. Rings rise and flee while Sonic brakes, with the camera fixed through the clearest moment. All 1,200 frames retain ring inventory zero and no hurt/death. Its full 1,200-frame 400×224 RGB sequence and 960,000 stereo PCM frames match the original captures exactly; only those verified duplicate PNG/WAV files were compacted. The selected window is 770–992, thumbnail 805. Earlier jump-train and late-brake takes remain excluded because the displacement was hard to read. Two earlier source-review requests ended 130 before admission and proved nothing; the retained TTY retry completed successfully. The late-brake raw PNG/WAV are retained because its interrupted comparison never ran.

The 120-second HCZ2 native render observes 526 DAC-enable writes and 980,211 nonconstant DAC data writes. The DAC-only control has nonzero AC output; the all-muted control has zero AC variance. `assets/hcz2/render-provenance.json` records the actual chip/output checks. Neither an audio filename nor a nonzero full mix alone proves DAC percussion.

The fresh ghost replay matches all 1,200 state/input rows and all 342 selected RGB frames of the earlier picture. The music-free native soundboard reproduces all 61 ordered accepted SFX admissions, using captured raw requests so S3K ring stereo toggling is preserved. It supplies a full-source timeline at 800 stereo samples per presentation, origin zero, trimmed exactly at 552–894. The selected picture includes 20 admitted sounds, including the actual ghost apparition/fade cues. Frame 748's `0x35` is the actual profile-translated hurt request with `hurt=1/dead=0`, not an inserted player-death event. See `audio-source/README.md` for the rejected resolved-ID and wrong-sidekick attempts and their preservation limits.

The isolated audio is native ROM SFX rendered from observed accepted events. It is not a recovered stem from the old mixed PCM. No DEZ music, guessed ghost cue or external percussion is added.

## Mixing and reproduction

`audio.json` gives HCZ one fixed +10 dB gain through all effect cards, isolated ghost SFX +8 dB, and a bounded final limiter. Only the whole-film ending fades. Source bed measurement is −25.58 LUFS / −12.72 dBTP; the actual final AAC measures −15.48 LUFS / −2.28 dBTP.

Use an isolated OpenGGF worktree with matching compiled production/test capture helpers, the supplied native ROM, and the archived input/settings recipes. Every Java/compiler/FFmpeg child participates in the normal shared admission and inherits its lease. No ambient desktop is used. For example, from this production directory, with `CHAOS_WORKTREE` set to the owned engine checkout and `S3K_ROM` to the existing ROM:

```bash
python3 capture.py --admission-worktree "$CHAOS_WORKTREE" --rom "$S3K_ROM" --mod out/sonic3k-chaos-mode.jar repellent-early-brake-aiz1
python3 review_sources.py --admission-worktree "$CHAOS_WORKTREE" --effects ring-repulsion --compact
python3 render_audio.py --admission-worktree "$CHAOS_WORKTREE" --rom "$S3K_ROM" --mod out/sonic3k-chaos-mode.jar --mode all
python3 measure_audio.py --admission-worktree "$CHAOS_WORKTREE"
python3 assemble.py preview --admission-worktree "$CHAOS_WORKTREE"
python3 assemble.py render --admission-worktree "$CHAOS_WORKTREE"
python3 verify.py --admission-worktree "$CHAOS_WORKTREE"
```

Native ROM SHA-1: `CFBF98C36C776677290A872547AC47C53D2761D6`. New source engine commit: `88fc03dacd9835437070d40109d62b97a665f944`. The archived production tree contains plans, recipes, source helpers, observed-event metadata and final edit settings; bulk ROM/media/JAR/state remains in the external media catalogue, with earlier revisions untouched.

Final verification passed complete audio/video decoding, all 6,360 video PTS, source intervals/death/EOF, all 22 chapters, fast-start and loudness. Cue-free AAC waveform comparisons before, during and after the ghost card have zero-lag correlations 0.999920 / 0.999942 / 0.999824 and retain the configured gain. These are bounded encoded-output evidence, not whole-track bit parity or a listening review. Root inspected all 120 actual moving/cut samples plus five bookend samples across seven generated pages; independent visual review is recorded in SHOT_REVIEW.md. No engine full-suite or native ROM parity claim is made for a media-only edit.
