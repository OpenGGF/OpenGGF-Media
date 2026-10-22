# Capture plan — commands for the next session only

No command in this document was used to capture footage during planning. Start after creative review. Work only from `/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach`; its `target/` is the build location. Production root is `/home/farrell/Videos/OGGF/emerald-remix-promo`. Leave `coaching/` untouched.

## Sources and control

**EHZ-A**: a cold direct load of remixed Emerald Hill Act 1 with only Emerald Remix loaded, Sonic solo, no donor, width 400. Use a deterministic BK2/Input Log from act start through the triple and downstream single to natural completion. Start excerpts after acceleration, but retain the complete source prefix and state CSV. The shot list names layout anchors; actual input timing is deliberately not invented before running the level.

**CV-A**: a cold direct load of the original Clover Valley act with the same configuration. Author right movement, native jumps for the two step-ups and a spring approach. Keep the whole run through native signpost/results. S07–S10 can be excerpts from this one source; that does not imply an uninterrupted trailer or progression through Act 2. **CV-END** is an unused moving tail from CV-A, or a second cold pass when needed, never a looped still.

Default source kind is normal gameplay with scripted controller input, not a trace, Stageplay or parity reference. No invulnerability from `TestEmeraldRemix`, debug completion, ring seeds, position/velocity writes or altered level assets. If later exploration needs a positioned diagnostic, segregate and label it and recapture the final action from the cold route. Do not quietly promote a diagnostic to final evidence.

## Build and environment

Already completed successfully in this checkout:

```bash
JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 examples/emerald-remix/build.py
```

This compiled engine/tool classes, generated `target/examples-classpath.txt` and validated/packaged `target/emerald-remix/emerald-remix.jar` with zero validator findings. It did not launch the game or run route tests. Rebuild only for new source changes. Pin the exact future source SHA and mod JAR hash in each capture’s notes. Current SHA is in STATUS.md.

The input tool does not need graphics. Author each reviewed input script under the production root, compile it through `InputLogAuthorTool` and retain its production-loader round-trip result. Use absolute paths. For a future `inputs/ehz-route.script`:

```bash
JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 tools/testing/maven_queue.py -Dmse=off exec:java   -Dexec.mainClass=com.openggf.tools.InputLogAuthorTool   '-Dexec.args=--script /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/ehz-route.script --out /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/ehz-route.bk2 --game s2'
```

Scripts do not exist yet. A jump is a held-button state with explicit release; holding Jump for a duration produces one jump, not repeated taps. Tune action from observed state next session, not the test bot’s unconditional invulnerability. Record selected log hashes and any route revisions. Use distinct take directories to preserve rejected and superseded attempts.

## Planned capture commands

These templates intentionally depend on input logs to be authored after review. `--frames` is a safety budget, not a predicted route time; once the input length/finish time is known, replace it with the actual required budget and retain handles. Omit `--audio`: the current CLI’s audio export contains full music and effects, not an isolated SFX stem. This film uses a separate editorial bed; silent source captures avoid layered BGM. Optional stingers can be rendered separately with the already verified audio tool and identified as editorial accents.

```bash
# EHZ-A — next session, after input authoring.
env -u DISPLAY -u WAYLAND_DISPLAY JAVA_HOME=/usr/lib/jvm/java-25-openjdk   python3 tools/testing/maven_queue.py -Dmse=off -Dopenggf.headless.gl=surfaceless-egl   exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool   '-Dexec.args=--game s2 --rom /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/s2.gen --mod /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/target/emerald-remix/emerald-remix.jar --zone ehz --act 1 --width 400 --main sonic --sidekick none --input /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/ehz-route.bk2 --frames 12000 --every 1 --fps 60 --no-video --out-dir /home/farrell/Videos/OGGF/emerald-remix-promo/captures/ehz-a-take01'

# CV-A — next session. Numeric zone 11 is the sole-mod registry index, NOT JSON 64.
env -u DISPLAY -u WAYLAND_DISPLAY JAVA_HOME=/usr/lib/jvm/java-25-openjdk   python3 tools/testing/maven_queue.py -Dmse=off -Dopenggf.headless.gl=surfaceless-egl   exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool   '-Dexec.args=--game s2 --rom /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/s2.gen --mod /home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/target/emerald-remix/emerald-remix.jar --zone 11 --act 1 --width 400 --main sonic --sidekick none --input /home/farrell/Videos/OGGF/emerald-remix-promo/inputs/cv-route.bk2 --frames 6000 --every 1 --fps 60 --no-video --out-dir /home/farrell/Videos/OGGF/emerald-remix-promo/captures/cv-a-take01'
```

Both use one PNG per executed frame plus measured `state.csv`, preserving native speed. Frame budgets may generate large PNG sets; plan disk capacity before the first run and choose the required route duration from the input log. A lean/logic route reconnaissance could precede every-frame recording next session, but is not a substitute for the actual render. Surfaceless EGL, graphics/sprite correctness, 400-wide behavior and the CLI’s actual resolved Clover identity have not been exercised in this planning session. Fail closed if isolation cannot initialize; never fall back to the shared desktop.

If the public capture host cannot resolve the mod zone, first inspect its existing mod registry/load owner. Use a small production-folder helper calling `GameplayCaptureSession` and `ZoneKey.Mod("emerald-remix","clover-valley")` resolution if necessary; do not invent a stock zone alias or modify the game to disguise identity. This is a contingency, not an implemented or tested helper.

## Per-take verification and selection

1. Confirm actual zone/act/team, level name and runtime registry identity from boot/level metadata. Existing direct-capture CSV has motion fields but no zone identity column; retain boot metadata alongside it rather than treating numeric config alone as proof.
2. Read CSV before selecting frames: motion, camera, ring count, ground/air state, rolling, hurt/dead flags. Check all corkscrew motion and spring/landing progression against the picture. If a native event needs additional telemetry, use an owned diagnostic rather than inferring it solely from an authored command.
3. Make contact sheets after valid captures and assign exact source in/out frames, including 1–2 second handles. Keep native speed and actual PNG cadence; do not encode sparse sampling at 60 fps.
4. Watch complete takes and transitions at 1×. Check foreground alignment through vertical movement, feet at landing, player priority through corkscrews, full hero exits, horizon motion and absence of idle padding. Stills and state alone do not certify attractive footage.
5. Compare claims to observed action. If rings are visible but not collected, do not add pickup sounds or imply collection. Mark failed hero attempts and use the stated fallback rather than fake success.
6. When editing later, inspect source intervals for EOF holds, duplicate excerpts and unintended retiming. Final review will include chapter reconciliation, full decode, dimensions/cadence, encoded AAC loudness/true peak and a complete moving playback. Those final checks are not yet performed.

No engine suite is needed for this planning-only deliverable. A future capture-host failure or an engine modification needs proportionate focused checks under the repo’s queue policy. No public-release full suite is warranted here. OpenGGF-Media publication remains deferred by the user; do not describe a local plan as an archived or shipped promo.
