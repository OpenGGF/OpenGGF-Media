# b4-paradox

Delivered: every-frame lossless 400×224 PNGs, state.csv, session.csv, authored input script/log. No audio or video editing.

Base: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current branch `feature/ai-sonic-echoes`, main checkout.
Entry: test-only capture room selection before ordinary stock boot; room `3-1`. No teleport flags or forced gameplay/drift.

Frame range: **0–2001**, 2002 PNGs and exactly matching state/session rows. **Room input starts at180**; 0–179 is necessary stock boot/READY pre-roll and is not suggested footage.

InputLogAuthorTool round-trip passed for final `inputs.script` → `inputs.txt`. All frame/player centre/camera columns compared exactly between state/session. No live deaths. The intended naive take fractures echo0 once; the correct route has no fracture.

Player mod actions are scheduled as `0:240:ECHO,1:220:RESET,0:240:ECHO,1:401:ECHO` (zero-based loop / native loopFrame). These are exact authored reference route lengths, equivalent to E for Echo and R for Reset; wrapper calls the same `RoomSession.command` owner used by RoomActions. No physical keyboard input is sent. Each Echo command consumes one row followed by the full twelve rewind-hold rows (`13 -`).

## Key events

| Frame | Loop / loopFrame | Event | On screen / meaning |
|---:|---|---|---|
| 227 | 0 / 48 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 227 | 0 / 48 | `gate_open:cyan` | Plate/channel/rift condition observed |
| 230 | 0 / 51 | `shard:4` | Chrono shard collected |
| 286 | 0 / 107 | `shard:5` | Chrono shard collected |
| 288 | 0 / 109 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 420 | 1 / 240 | `commit` | Recording committed; full native rewind flash follows |
| 420 | 1 / 240 | `rewind_start` | Rewind flash begins |
| 432 | 1 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 480 | 1 / 48 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 480 | 1 / 48 | `gate_open:cyan` | Plate/channel/rift condition observed |
| 483 | 1 / 51 | `shard:4` | Chrono shard collected |
| 539 | 1 / 107 | `shard:5` | Chrono shard collected |
| 541 | 1 / 109 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 552 | 1 / 120 | `fracture:0` | Native PARADOX banner; recorded cyan runner organically diverged after early live plate contact |
| 701 | 0 / 48 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 701 | 0 / 48 | `gate_open:cyan` | Plate/channel/rift condition observed |
| 704 | 0 / 51 | `shard:4` | Chrono shard collected |
| 760 | 0 / 107 | `shard:5` | Chrono shard collected |
| 762 | 0 / 109 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 894 | 1 / 240 | `commit` | Recording committed; full native rewind flash follows |
| 894 | 1 / 240 | `rewind_start` | Rewind flash begins |
| 906 | 1 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 954 | 1 / 48 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 954 | 1 / 48 | `gate_open:cyan` | Plate/channel/rift condition observed |
| 957 | 1 / 51 | `shard:4` | Chrono shard collected |
| 1013 | 1 / 107 | `shard:5` | Chrono shard collected |
| 1015 | 1 / 109 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 1221 | 1 / 315 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1221 | 1 / 315 | `gate_open:cyan` | Plate/channel/rift condition observed |
| 1308 | 2 / 401 | `commit` | Recording committed; full native rewind flash follows |
| 1308 | 2 / 401 | `rewind_start` | Rewind flash begins |
| 1320 | 2 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 1368 | 2 / 48 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1368 | 2 / 48 | `gate_open:cyan` | Plate/channel/rift condition observed |
| 1371 | 2 / 51 | `shard:4` | Chrono shard collected |
| 1427 | 2 / 107 | `shard:5` | Chrono shard collected |
| 1429 | 2 / 109 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 1632 | 2 / 312 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1632 | 2 / 312 | `gate_open:cyan` | Plate/channel/rift condition observed |
| 1721 | 2 / 401 | `clear` | ROOM CLEAR card |
| 1733 | 2 / 401 | `star:1` | Earned star pop (1 Clear, 2 Par) |
| 1751 | 2 / 401 | `star:2` | Earned star pop (1 Clear, 2 Par) |
| 653 | 0 / 0 | scheduled RESET | Ordinary player Reset removes the naive recording and restarts; next authored input is654. Shared sidecar has no explicit reset/instant-restore event, but loopFrame, loop and echo state reset here. |

## Visual review and limitations

Opened representative final PNG frames: 551, 552, 555, 653, 654, 1769. Whole HUD, normal Sonic/echo sprites, required contacts, clear card and earned stars inspected. No debug overlays.

The ordinary room checkpoint restores camera to its authored initial clamp, then native camera following settles during the first several movement ticks. The restore frame can omit HUD/player; early native ticks can have Sonic below view. These raw transitions are retained honestly (including every12-frame rewind flash), with no camera overrides. Boot pre-roll also holds a static off-room view before room input180. This is a presentation limitation, not frozen gameplay or a missing route segment. Stationary recording padding and the clear-card tail are intentional.

## Reproduce

Exact argv, environment and capture jar SHA256: `command.json`. Java25 / supplied S2 REV01 SHA1 `8bca5dcef1af3e00098666fd892dc1c2a76333f9`.

```sh
export PATH="/usr/share/idea/plugins/maven-plugin/lib/maven3/bin:$PATH"
export JAVA_HOME=/home/james/.jdks/corretto-25.0.4.1
env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -q -Dmse=off -Dopenggf.headless.gl=surfaceless-egl -Dechoes.capture.room=3-1 -Dechoes.capture.session=/home/james/tmp/sonic-echoes-promo/captures/b4-paradox/session.csv -Dopenggf.saveRoot=/home/james/tmp/sonic-echoes-promo/captures/b4-paradox/save -Dechoes.capture.actions=0:240:ECHO,1:220:RESET,0:240:ECHO,1:401:ECHO exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool '-Dexec.args=--game s2 --rom '"'"'/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen'"'"' --mod /home/james/tmp/sonic-echoes-promo/captures/b5-last-loop/promo-action-capture.jar --zone cpz --act 1 --width 400 --every 1 --input /home/james/tmp/sonic-echoes-promo/captures/b4-paradox/inputs.txt --no-video --out-dir /home/james/tmp/sonic-echoes-promo/captures/b4-paradox'
```

Shared observer is Worker A’s unedited `PromoCaptureMod.java`. Additional test-only source: `examples/sonic-echoes/src/test/java/echoes/PromoActionCaptureMod.java`. Separate capture jar `../b5-last-loop/promo-action-capture.jar`; rebuild script there. Never packaged in distributed mod. No suites run, no commits/pushes/branch changes.

Final every-PNG scan: 2002 images at400×224; wrong sizes=0, black images=0. Longest byte-identical PLAYING streak=1 frames starting180.
