# Emerald Remix promo — session status

Updated: 2026-10-22. **Planning session complete; awaiting the user’s review before footage capture.**

Owner/scope: design sub-agent in the assigned `promo-coach` checkout. Production files are under this directory only; `coaching/` was neither read nor modified. No gameplay footage, capture frames, simulation pass or live engine launch was produced. No repository source changes, commits, branch switches, fetch/pull, push or OpenGGF-Media writes were performed. Existing main/integration delivery rituals do not apply to this explicitly planning-only scope.

## Current source and production state

- Checkout: `/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach`.
- Branch: `feature/ai-promo-skill-coaching`.
- Source SHA: `8aa692b045c195ef8a42896b6bbc9549158470c0`; clean before and after planning, with generated build/dependency output under its ignored `target/`.
- Supplied ROM spelling preserved: `/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/s2.gen`. It is an existing link resolving to the main checkout’s `s2.gen`; no ROM link/file was created, copied or modified. Verified CRC32 `7B905383`, SHA-1 `8BCA5DCEF1AF3E00098666FD892DC1C2A76333F9` (S2 World REV01).
- Example built at `target/emerald-remix/emerald-remix.jar`; SHA-256: de1817fbf2950bf565b28c0f334f1de22b45cbd9e57a0cd8cba3cadf2e09e280.
- Disposable Python environment: checkout `target/promo-planning-venv`, NumPy and Pillow installed. No global Python installation changed.
- No task-owned jobs remain running at the end of this session. No agent/session workers were created. No exact aggregate execution or queue timing was measured; unrelated host test jobs were left alone.

## Done

- Read the checkout’s AGENTS.md and task-specific directing/capture/headless skills. Read recorded promo lessons before storyboarding.
- Studied actual mod layout, original-zone generator/map, palette, progression, parallax, spring subtype and route-test limits.
- Studied pinned Slay and Putt-Putt production source, with borrowing and limits in RESEARCH.md. Finished reference videos were not watched.
- Wrote BRIEF.md with promise, audience, choices and rejected alternatives; BEAT_SHEET.md, SHOT_LIST.csv and CAPTURE_PLAN.md with per-shot control strategy, source anchors and acceptance criteria.
- Rendered 76 s of actual S2 EHZ 2P SMPS music and a 70.367 s review bed, with reproducible scripts, hashes, beat grid, candidate sections, independent window/onset checks and processing notes under audio/.
- Verified the original Clover export and generated an authoring map reference, not a gameplay capture.
- Wrote design/review.html as a compact timeline/story board. HTML previews at desktop (728 px) and mobile (360 px) showed no console messages. Inspected the story cards and corrected mobile timeline label wrapping and tick alignment; final preview verified before inline display. It illustrates intended action rather than imitating captured footage.

## Checks and observed results

- `JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 examples/emerald-remix/build.py`: completed successfully; Java 25 source compiled and mod package validation reported **0 findings**. No engine tests ran; this is not a route/playability pass.
- `python3 examples/emerald-remix/tools/generate_clover_valley.py --check --preview <production>/design/clover-layout-reference.png`: **verified 12 files**; no committed assets rewritten.
- `<venv>/python tools/media/promo_kit.py fonts`: every role **ok**, including Fira Sans Compressed Heavy and Heavy Italic, condensed subtitle, Fira body and Hack mono. No font fallback. Fonts were inspected from the host; packaging font files/licenses for a future editor is still open.
- `scripts/render_music.py`: success; 3,648,000 sample frames at 48 kHz, stereo PCM16, 76.000 s. Loop reports `complete=false` as expected at the time cap. Removed its FM-only/register-log byproducts.
- `scripts/analyse_music.py`: success; 106.634169 BPM estimated, first beat 0.040711 s, raw first attack 0.034333 s after removing initial DC baseline; estimated phase within 6.38 ms of that attack. Independent windows estimate 106.602–106.650 BPM. Full method/limits in audio/MUSIC.md.
- `ffmpeg ... -af ebur128=peak=true -f null -`: raw −24.3 LUFS / −12.8 dBFS true peak; final high-passed review bed **−18.3 LUFS**, **1.5 LU LRA**, **−6.8 dBFS true peak**. No encoded AAC exists. Audio sample format and duration checked with ffprobe.
- Final audio decode, document/link/CSV consistency and Python syntax checks: passed: three production Python scripts compiled without writing bytecode; eleven output shots are contiguous through frame 4,222; end card is nine seconds; all source picks remain blank; 126 beat rows; both WAV hashes match analysis.json; local Markdown links resolve; HTML parses; both WAVs fully decode with `ffmpeg -v error -xerror -i <wav> -f null -`; ffprobe confirms PCM16 / 48 kHz / stereo and 76.000 s + 70.366667 s. Final git status is clean.
- No engine smoke/full suite was run: there are no engine changes and footage is explicitly out of scope. No final-film codec, motion or aesthetic pass is claimed.

## Open for the next session

1. User review of the central idea, proposed length, copy and EHZ 2P soundtrack. This is the agreed session boundary, not a new permission ceremony imposed by a skill.
2. Listen to the bed and confirm pulse/bar phase and formal section changes. Automated novelty markers are candidates, not musical truth. No physical listening was performed here.
3. Author and round-trip actual input logs; check the routes without invulnerability. Capture exact timings only then. The existing terrain bot grants damage immunity and cannot be presented as an ordinary player performance.
4. Exercise EGL and the production capture host with this mod and 400-wide framing. Verify actual Clover registry identity; source inspection says sole-mod zone 11, not asset index 64. No rendering prerequisite is certified merely by compilation.
5. Verify the proposed yellow-spring → ring-line → landing hero. If it fails or looks awkward, use the clean hill/descent fallback. All source in/out CSV cells intentionally remain empty.
6. Check the long S06 single/run-out interval can sustain moving footage. Shorten/reallocate a bar rather than pad a finished signpost. Protect complete triple and spring actions.
7. Prove the nine-second moving end-card tail exists, set final type sizes from the full composition, package any external fonts with their licenses, and check all practical text at 1×.
8. Final-film assembly, source provenance, chapters, complete moving review, decode and encoded audio measurements are later work. OpenGGF-Media preparation/publication remains deferred until the user permits that stage; nothing was archived or published.

## Tool and documentation problems encountered

- System Python lacked NumPy, so the first `promo_kit.py fonts` invocation failed with `ModuleNotFoundError`. Resolved with the disposable checkout-local venv. All subsequent kit commands use it.
- Web tool could not fetch the archive directory (`Failed to fetch restricted URL`). Read-only GitHub API/raw HTTP succeeded, so reference source was studied at a pinned commit without modifying OpenGGF-Media.
- Maven emitted `WARNING: java.io.tmpdir directory does not exist` at build startup, but compilation/packaging completed normally. No workaround outside the owned target tree was required; watch for a real temp-file failure in a later tool run.
- The archived Slay audio recipe assumes an older S3K helper/test classpath in another checkout. Used the current checkout’s production FM/music render tool instead; no stale helper was copied or patched.
- The capture skill describes `--audio`, but it is a full music+SFX export, not SFX-only. Plan uses silent gameplay plus the separately rendered bed; any later stingers are explicitly editorial. No invented `--sfx-only` flag or audio separation is promised.
- A first-nonzero PCM onset check is invalid here because the chip starts with a constant DC offset (~0.008789). Replaced it with attack detection relative to the initial baseline and a 20 Hz high-pass on the review bed. Raw render is preserved.
- Musical-section detection returns weak/zero candidates too. The draft uses selected strong cues; bar/downbeat listening review is still open. No confidence claim is inferred from the CLI’s success.

Next action: user reviews the plan and music; later session begins with listening and route/input reconnaissance, then capture. **Stop here before footage.**
