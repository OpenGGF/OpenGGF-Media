# b3-spring-relay

Delivered: every-frame lossless 400×224 PNGs, state.csv, session.csv, authored input script/log. No audio or video editing.

Base: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current branch `feature/ai-sonic-echoes`, main checkout.
Entry: test-only capture room selection before ordinary stock boot; room `3-2`. No teleport flags or forced gameplay/drift.

Frame range: **0–2088**, 2089 PNGs and exactly matching state/session rows. **Room input starts at180**; 0–179 is necessary stock boot/READY pre-roll and is not suggested footage.

InputLogAuthorTool round-trip passed for final `inputs.script` → `inputs.txt`. All frame/player centre/camera columns compared exactly between state/session. No live deaths. No echo fractures.

Nonfinal authored loops run to automatic timeout720, padded with neutral, followed by12 rewind rows. No scheduled mod actions.

## Key events

| Frame | Loop / loopFrame | Event | On screen / meaning |
|---:|---|---|---|
| 228 | 0 / 49 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 235 | 0 / 56 | `shard:4` | Chrono shard collected |
| 899 | 1 / 720 | `commit` | Recording committed; full native rewind flash follows |
| 899 | 1 / 720 | `timeout` | Room clock reached720 |
| 899 | 1 / 720 | `rewind_start` | Rewind flash begins |
| 911 | 1 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 959 | 1 / 48 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 962 | 1 / 51 | `shard:4` | Chrono shard collected |
| 1025 | 1 / 114 | `spring:live` | Native spring impulse; echo1 is the second echo |
| 1064 | 1 / 153 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 1064 | 1 / 153 | `gate_open:cyan+magenta` | Plate/channel/rift condition observed |
| 1631 | 2 / 720 | `commit` | Recording committed; full native rewind flash follows |
| 1631 | 2 / 720 | `timeout` | Room clock reached720 |
| 1631 | 2 / 720 | `rewind_start` | Rewind flash begins |
| 1643 | 2 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 1691 | 2 / 48 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1694 | 2 / 51 | `shard:4` | Chrono shard collected |
| 1757 | 2 / 114 | `spring:live` | Native spring impulse; echo1 is the second echo |
| 1757 | 2 / 114 | `spring:echo1` | Native spring impulse; echo1 is the second echo |
| 1794 | 2 / 151 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 1794 | 2 / 151 | `gate_open:cyan+magenta` | Plate/channel/rift condition observed |
| 1796 | 2 / 153 | `shard:5` | Chrono shard collected |
| 1836 | 2 / 193 | `clear` | ROOM CLEAR card |
| 1848 | 2 / 193 | `star:1` | Earned star pop (1 Clear, 2 Par) |
| 1866 | 2 / 193 | `star:2` | Earned star pop (1 Clear, 2 Par) |

## Visual review and limitations

Opened representative final PNG frames: 1760, 1800, 1884. Whole HUD, normal Sonic/echo sprites, required contacts, clear card and earned stars inspected. No debug overlays.

The ordinary room checkpoint restores camera to its authored initial clamp, then native camera following settles during the first several movement ticks. The restore frame can omit HUD/player; early native ticks can have Sonic below view. These raw transitions are retained honestly (including every12-frame rewind flash), with no camera overrides. Boot pre-roll also holds a static off-room view before room input180. This is a presentation limitation, not frozen gameplay or a missing route segment. Stationary recording padding and the clear-card tail are intentional.

## Reproduce

Exact argv, environment and capture jar SHA256: `command.json`. Java25 / supplied S2 REV01 SHA1 `8bca5dcef1af3e00098666fd892dc1c2a76333f9`.

```sh
export PATH="/usr/share/idea/plugins/maven-plugin/lib/maven3/bin:$PATH"
export JAVA_HOME=/home/james/.jdks/corretto-25.0.4.1
env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -q -Dmse=off -Dopenggf.headless.gl=surfaceless-egl -Dechoes.capture.room=3-2 -Dechoes.capture.session=/home/james/tmp/sonic-echoes-promo/captures/b3-spring-relay/session.csv -Dopenggf.saveRoot=/home/james/tmp/sonic-echoes-promo/captures/b3-spring-relay/save exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool '-Dexec.args=--game s2 --rom '"'"'/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen'"'"' --mod /home/james/tmp/sonic-echoes-promo/captures/a-helper-proof/promo-capture.jar --zone cpz --act 1 --width 400 --every 1 --input /home/james/tmp/sonic-echoes-promo/captures/b3-spring-relay/inputs.txt --no-video --out-dir /home/james/tmp/sonic-echoes-promo/captures/b3-spring-relay'
```

Shared observer is Worker A’s unedited `PromoCaptureMod.java`. No Worker B helper used in this take. No suites run, no commits/pushes/branch changes.

Final every-PNG scan: 2089 images at400×224; wrong sizes=0, black images=0. Longest byte-identical PLAYING streak=1 frames starting180.
