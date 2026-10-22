# Music choice and measured clock

Chosen bed: Sonic 2 **Emerald Hill Zone (2P)**, stock music ID `0x91` / decimal 145. Clover Valley’s `level.json` already selects it, so it ties the trailer’s familiar and original halves together. Keep one uninterrupted bed, not a switch between embedded clip music. This is a local ROM-derived planning soundtrack; no external license or clearance is claimed.

Listen for review: [emerald-remix-review-bed.wav](emerald-remix-review-bed.wav), **70.367 s**, 48 kHz, stereo, PCM16. Source: [raw/s2-music-91-mix.wav](raw/s2-music-91-mix.wav), 76 s. No SFX, jingle or voice is mixed into either file. No physical listening review was performed by the agent.

## Rendering and reproduction

Built the example/tools in the assigned checkout with Java 25; used `com.openggf.tools.audio.FmSfxRenderTool --game s2 --music 91 --rate 48000 --max-seconds 76`. This reads the supplied S2 REV01 ROM and uses OpenGGF’s real SMPS driver, NTSC region and accurate FM core with full FM/DAC/PSG mix, without gameplay, graphics or desktop audio playback. The renderer reports `complete=false` because the music loops; it successfully reached the requested 3,648,000 stereo sample frames. This is not a failed render.

`../scripts/render_music.py` is the exact reproducible invocation. The tool also makes FM-only and YM register diagnostics; the script deletes those task-owned byproducts, preserving the full mix. Raw music remains local and is not included in any repository.

For analysis, created disposable `target/promo-planning-venv` in this checkout and installed NumPy/Pillow there. Use:

```bash
target/promo-planning-venv/bin/python tools/media/promo_kit.py beats /home/farrell/Videos/OGGF/emerald-remix-promo/audio/raw/s2-music-91-mix.wav
target/promo-planning-venv/bin/python /home/farrell/Videos/OGGF/emerald-remix-promo/scripts/analyse_music.py
```

The analysis script uses the checkout’s actual `promo_kit.py`, exports the JSON/CSV grid and makes the review bed with FFmpeg: 20 Hz high-pass to remove initial chip/DC offset, +6 dB gain, no tempo change, final two-second fade. It ends at frame 4,222 (60 fps), nearest the detected late change at editorial beat 125. Raw sound starts immediately with a chip baseline and a meaningful attack near 34 ms; there is no inserted count-in.

## Measurements and limitations

- Whole opening estimator: **106.634169 BPM**, period **0.562671429 s**; first estimated beat **0.040711 s**.
- Independent 24-second analysis windows beginning at 0, 18 and 36 s estimate 106.634, 106.602 and 106.650 BPM. Their phases agree with the global clock to about 6 ms. No major tempo change detected within this bounded check.
- Independent first-attack threshold after initial-baseline removal: **0.034333 s**, about **6.38 ms** before the estimated first beat (less than one video frame). A naive first-nonzero test falsely reports t=0 due to DC; that approach was rejected.
- Raw file measured by FFmpeg `ebur128=peak=true`: integrated **−24.3 LUFS**, LRA **1.5 LU**, true peak **−12.8 dBFS**. Review-bed measurements are recorded in STATUS.md after its final high-pass render. These are PCM measurements, not encoded AAC certification or an RMS-to-LUFS substitution.
- The estimator returns pulse phase, not which pulse is a musical bar downbeat. Spectral novelty locates timbral changes, not certified formal sections. The tiny/zero early and weak late candidates are not reliable chapter cues. Listening/downbeat review remains open before capture/edit lock.

`beats.csv` contains beats 0–125 with exact seconds and 60-fps rounded frames. The bar column groups every four beats for editorial convenience only. `section-candidates.csv` retains the actual novelty scores; `analysis.json` includes source identity, method, onset check, independent windows, bed processing and SHA-256 hashes.

Strong candidates used for the draft: beat 16 ≈9.04 s (identity), beat 61 ≈34.36 s (Clover reveal); beat 32 ≈18.05 s occurs during the triple and deliberately does not force a cut. Beat 95 ≈53.49 s is a possible late action accent; the sheet currently keeps the intact spring pass to bar beat 96. Novelty beat 125 ≈70.37 s provides the proposed fade endpoint. The review bed fades rather than pretending a loop boundary is a composed ending.

Normal EHZ (`0x81`) was considered but not rendered: it would emphasize familiarity while giving Clover less distinction. Hydrocity 2 from the reference promo was rejected as a different game’s identity. An original commissioned score would add work before the route’s appeal is established. Keep the 2P choice provisional for the user’s listening review.
