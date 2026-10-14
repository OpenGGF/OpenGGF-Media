# Sonic3K Chaos Mode — rapid-fire reel revision

This is the separate revision2 of the2026-10-14 Chaos Mode promo. The first reel and its source archive remain unchanged. `out/sonic3k-chaos-mode-demo-v2.mp4` is the qualified81.067s export, with46 demonstrated effects across45shots; `out/edit-timeline.json` and `chapters.csv` identify every cut and its exact source frames. The new source ZIP preserves lossless masters, controller recipes, settings, per-presentation state, provenance, assets and reproducible edit tools. The user supplies the ROM; no ROM image is included.

The user requested more effects, worse Sonic crowds, physical rings left behind, full-screen angled rain, corrected bumper/ghost colours, a continuous soundtrack and occasional sliced screens. Claude Opus5.5 supplied the initial beat plan in `PLAN.md`/`edl.json`; root reviewed every selected interaction and adapted that plan. `SHOT_REVIEW.md` records visible actions and rejected claims. `source-selections.json` is the editorial approval lock. Different panels are independent actual captures, not claims that all shown effects ran in one world simultaneously. Every gameplay frame retains its recorded60Hz presentation speed; Fast Forward and Slow Motion use the game's own pacing effects.

The revised native footage records source543c076fd; the final allocator follow-up45fff2130 preserves ordinary palette allocation and does not change those small-roster scenes. Earlier unchanged scenes retain their actual source/package hashes, rather than being relabelled as new captures. The mod still has105 stable effect IDs. Too Many Sonics captures24 bright native poses; this does not imply24 distinct silhouettes are visible on every frame. Leaky Pockets uses a declared initial32-ring carried inventory, not rings earned in that shot. Its physical trail, loss and recollection are actual native interactions. Badnik size/rotation takes use a declared positioned setup. Defence demonstrates its moving board, inputs and score, without claiming travelling shots or a victory; Snake demonstrates moving segments without a food/win claim. The missed Vine grab and label-only Landmark are excluded.

One ROM-backed HCZ2 music render plays continuously through the main edit. All source gameplay PCM is muted because music and SFX were captured mixed. Explicit ROM stings are placed editorially; the ghost death cue follows the actual CSV death. Native PCM remains in the lossless source masters. The source ZIP's media checks prove recorded pixels/sample retention, not shipped-ROM parity or all-act/effect certification.

## Reproduce

Use Java25, Lua5.4, Maven and FFmpeg. Build the recorded source revision in an isolated OpenGGF checkout; set `OPENGGF_WORKTREE` to it, `OPENGGF_QUEUE_ROOT` to the shared up-to-date scheduler checkout, and `OPENGGF_S3K_ROM` to the existing absolute locked-on S3K ROM path. Its SHA1 is CFBF98C36C776677290A872547AC47C53D2761D6. Captures unset DISPLAY/WAYLAND_DISPLAY and use the production surfaceless-EGL path. They never send desktop keys.

```sh
export JAVA_HOME=/usr/lib/jvm/java-25-openjdk
export LUA_BIN=/usr/bin/lua5.4
export OPENGGF_WORKTREE=/path/to/recorded/checkout
export OPENGGF_QUEUE_ROOT=/path/to/shared/current/checkout
export OPENGGF_S3K_ROM=/path/to/your/locked-on-s3k.gen
python3 build_package.py
python3 capture.py rain leak bumper ghosts ghost-close
python3 assemble.py render --admission-worktree "$OPENGGF_WORKTREE"
python3 verify_v2.py --admission-worktree "$OPENGGF_WORKTREE"
python3 archive_sources.py --compact --admission-worktree "$OPENGGF_WORKTREE"
```

Capture helpers retain complete existing masters. To regenerate instead, set `CHAOS_MEDIA_ROOT` to a separate empty task directory; retain the recorded input/configuration and point the editorial source lock to those new masters. Archived exact source metadata remains authoritative for the published movie. New captures from newer engine code require a new review.

Every Java input author, capture, compiler, SDK packager, media decoder and encoder holds shared scheduler admission and propagates its lease descriptors to child processes. Capture provenance records exact Java PIDs/UTC intervals. The initial20-shot revision batch was launched before that coordination fix; its old provenance and the recorded exclusion/interruption remain honest. Immutable compiled classes alone do not provide measurement isolation. Existing queued requests were preserved; no foreign process or locks were stopped/deleted.

`verify_v2.py` checks export dimensions/cadence, decoded frames/PTS, chapters, fast-start, all cut/midpoint samples and actual loudness/peak. Its small frame strips support visual review. `archive_sources.py` compares every new decoded RGB frame and PCM sample with the raw captures before consuming only redundant owned PNG/WAV copies. Original first-reel files are read-only. Native code/runtime tests and their limits are recorded in the repository's dated Chaos intensity/reel plan.

Final media checks:1920×1080/60Hz,H264/AAC48kHz stereo,4864decoded frames,45chapters,fast-start,full decode and all cut/midpoint frames checked. Final soundtrack−14.28LUFS/−1.45dBTP. All36 new masters retain exactRGB/nativePCM; redundant rawPNG/WAV copies were consumed after equality checks. The original first reel and old masters were not changed. Audio measurement is not a listening review or nativeSFX-isolation claim.
