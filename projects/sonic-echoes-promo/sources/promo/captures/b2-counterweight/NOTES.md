# b2-counterweight

Delivered: every-frame lossless 400×224 PNGs, state.csv, session.csv, authored input script/log. No audio or video editing.

Base: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current branch `feature/ai-sonic-echoes`, main checkout.
Entry: test-only capture room selection before ordinary stock boot; room `2-4`. No teleport flags or forced gameplay/drift.

Frame range: **0–2814**, 2815 PNGs and exactly matching state/session rows. **Room input starts at180**; 0–179 is necessary stock boot/READY pre-roll and is not suggested footage.

InputLogAuthorTool round-trip passed for final `inputs.script` → `inputs.txt`. All frame/player centre/camera columns compared exactly between state/session. No live deaths. No echo fractures.

Nonfinal authored loops run to automatic timeout720, padded with neutral, followed by12 rewind rows. No scheduled mod actions.

## Key events

| Frame | Loop / loopFrame | Event | On screen / meaning |
|---:|---|---|---|
| 199 | 0 / 20 | `shard:4` | Chrono shard collected |
| 308 | 0 / 129 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 315 | 0 / 136 | `shard:5` | Chrono shard collected |
| 899 | 1 / 720 | `commit` | Recording committed; full native rewind flash follows |
| 899 | 1 / 720 | `timeout` | Room clock reached720 |
| 899 | 1 / 720 | `rewind_start` | Rewind flash begins |
| 911 | 1 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 931 | 1 / 20 | `shard:4` | Chrono shard collected |
| 1040 | 1 / 129 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1046 | 1 / 135 | `seesaw_launch:live` | Native seesaw upward impulse |
| 1047 | 1 / 136 | `shard:5` | Chrono shard collected |
| 1133 | 1 / 222 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 1631 | 2 / 720 | `commit` | Recording committed; full native rewind flash follows |
| 1631 | 2 / 720 | `timeout` | Room clock reached720 |
| 1631 | 2 / 720 | `rewind_start` | Rewind flash begins |
| 1643 | 2 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 1663 | 2 / 20 | `shard:4` | Chrono shard collected |
| 1704 | 2 / 61 | `shard:5` | Chrono shard collected |
| 1704 | 2 / 61 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1765 | 2 / 122 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1778 | 2 / 135 | `seesaw_launch:echo1` | Native seesaw upward impulse |
| 1814 | 2 / 171 | `plate_on:gold` | Plate/channel/rift condition observed |
| 1838 | 2 / 195 | `plate_on:gold` | Plate/channel/rift condition observed |
| 1865 | 2 / 222 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 2363 | 3 / 720 | `commit` | Recording committed; full native rewind flash follows |
| 2363 | 3 / 720 | `timeout` | Room clock reached720 |
| 2363 | 3 / 720 | `rewind_start` | Rewind flash begins |
| 2375 | 3 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 2395 | 3 / 20 | `shard:4` | Chrono shard collected |
| 2436 | 3 / 61 | `shard:5` | Chrono shard collected |
| 2436 | 3 / 61 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 2497 | 3 / 122 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 2510 | 3 / 135 | `seesaw_launch:echo1` | Native seesaw upward impulse |
| 2510 | 3 / 135 | `seesaw_launch:live` | Native seesaw upward impulse |
| 2546 | 3 / 171 | `plate_on:gold` | Plate/channel/rift condition observed |
| 2570 | 3 / 195 | `plate_on:gold` | Plate/channel/rift condition observed |
| 2597 | 3 / 222 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 2616 | 3 / 241 | `clear` | ROOM CLEAR card |
| 2628 | 3 / 241 | `star:1` | Earned star pop (1 Clear, 2 Par) |
| 2646 | 3 / 241 | `star:2` | Earned star pop (1 Clear, 2 Par) |

## Visual review and limitations

Opened representative final PNG frames: 1814, 1860, 2510, 2600, 2664. Whole HUD, normal Sonic/echo sprites, required contacts, clear card and earned stars inspected. No debug overlays.

The ordinary room checkpoint restores camera to its authored initial clamp, then native camera following settles during the first several movement ticks. The restore frame can omit HUD/player; early native ticks can have Sonic below view. These raw transitions are retained honestly (including every12-frame rewind flash), with no camera overrides. Boot pre-roll also holds a static off-room view before room input180. This is a presentation limitation, not frozen gameplay or a missing route segment. Stationary recording padding and the clear-card tail are intentional.

## Reproduce

Exact argv, environment and capture jar SHA256: `command.json`. Java25 / supplied S2 REV01 SHA1 `8bca5dcef1af3e00098666fd892dc1c2a76333f9`.

```sh
export PATH="/usr/share/idea/plugins/maven-plugin/lib/maven3/bin:$PATH"
export JAVA_HOME=/home/james/.jdks/corretto-25.0.4.1
env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -q -Dmse=off -Dopenggf.headless.gl=surfaceless-egl -Dechoes.capture.room=2-4 -Dechoes.capture.session=/home/james/tmp/sonic-echoes-promo/captures/b2-counterweight/session.csv -Dopenggf.saveRoot=/home/james/tmp/sonic-echoes-promo/captures/b2-counterweight/save exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool '-Dexec.args=--game s2 --rom '"'"'/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen'"'"' --mod /home/james/tmp/sonic-echoes-promo/captures/a-helper-proof/promo-capture.jar --zone htz --act 1 --width 400 --every 1 --input /home/james/tmp/sonic-echoes-promo/captures/b2-counterweight/inputs.txt --no-video --out-dir /home/james/tmp/sonic-echoes-promo/captures/b2-counterweight'
```

Shared observer is Worker A’s unedited `PromoCaptureMod.java`. No Worker B helper used in this take. No suites run, no commits/pushes/branch changes.

Final every-PNG scan: 2815 images at400×224; wrong sizes=0, black images=0. Longest byte-identical PLAYING streak=1 frames starting180.
