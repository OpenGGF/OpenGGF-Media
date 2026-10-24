# b5-last-loop

Delivered: every-frame lossless 400×224 PNGs, state.csv, session.csv, authored input script/log. No audio or video editing.

Base: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current branch `feature/ai-sonic-echoes`, main checkout.
Entry: test-only capture room selection before ordinary stock boot; room `3-4`. No teleport flags or forced gameplay/drift.

Frame range: **0–1410**, 1411 PNGs and exactly matching state/session rows. **Room input starts at180**; 0–179 is necessary stock boot/READY pre-roll and is not suggested footage.

InputLogAuthorTool round-trip passed for final `inputs.script` → `inputs.txt`. All frame/player centre/camera columns compared exactly between state/session. No live deaths. No echo fractures.

Player mod actions are scheduled as `0:140:ECHO,1:170:ECHO,2:185:ECHO,3:249:ECHO` (zero-based loop / native loopFrame). These are exact authored reference route lengths, equivalent to E for Echo and R for Reset; wrapper calls the same `RoomSession.command` owner used by RoomActions. No physical keyboard input is sent. Each Echo command consumes one row followed by the full twelve rewind-hold rows (`13 -`).

## Key events

| Frame | Loop / loopFrame | Event | On screen / meaning |
|---:|---|---|---|
| 231 | 0 / 52 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 235 | 0 / 56 | `shard:5` | Chrono shard collected |
| 320 | 1 / 140 | `commit` | Recording committed; full native rewind flash follows |
| 320 | 1 / 140 | `rewind_start` | Rewind flash begins |
| 332 | 1 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 381 | 1 / 49 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 383 | 1 / 51 | `shard:5` | Chrono shard collected |
| 437 | 1 / 105 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 440 | 1 / 108 | `shard:6` | Chrono shard collected |
| 503 | 2 / 170 | `commit` | Recording committed; full native rewind flash follows |
| 503 | 2 / 170 | `rewind_start` | Rewind flash begins |
| 515 | 2 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 564 | 2 / 49 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 566 | 2 / 51 | `shard:5` | Chrono shard collected |
| 609 | 2 / 94 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 610 | 2 / 95 | `shard:6` | Chrono shard collected |
| 658 | 2 / 143 | `plate_on:gold` | Plate/channel/rift condition observed |
| 658 | 2 / 143 | `gate_open:cyan+magenta+gold` | Plate/channel/rift condition observed |
| 701 | 3 / 185 | `commit` | Recording committed; full native rewind flash follows |
| 701 | 3 / 185 | `rewind_start` | Rewind flash begins |
| 713 | 3 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 762 | 3 / 49 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 764 | 3 / 51 | `shard:5` | Chrono shard collected |
| 806 | 3 / 93 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 807 | 3 / 94 | `shard:6` | Chrono shard collected |
| 831 | 3 / 118 | `plate_on:gold` | Plate/channel/rift condition observed |
| 831 | 3 / 118 | `gate_open:cyan+magenta+gold` | Plate/channel/rift condition observed |
| 839 | 3 / 126 | `badnik_kill:live` | Native badnik destruction; nearest active participant corroborated visually |
| 856 | 3 / 143 | `plate_on:gold` | Plate/channel/rift condition observed |
| 856 | 3 / 143 | `gate_open:cyan+magenta+gold` | Plate/channel/rift condition observed |
| 963 | 4 / 249 | `commit` | Recording committed; full native rewind flash follows |
| 963 | 4 / 249 | `rewind_start` | Rewind flash begins |
| 975 | 4 / 0 | `restore` | World restored; native camera settles over the following ticks |
| 1024 | 4 / 49 | `plate_on:cyan` | Plate/channel/rift condition observed |
| 1026 | 4 / 51 | `shard:5` | Chrono shard collected |
| 1068 | 4 / 93 | `plate_on:magenta` | Plate/channel/rift condition observed |
| 1069 | 4 / 94 | `shard:6` | Chrono shard collected |
| 1093 | 4 / 118 | `plate_on:gold` | Plate/channel/rift condition observed |
| 1093 | 4 / 118 | `gate_open:cyan+magenta+gold` | Plate/channel/rift condition observed |
| 1101 | 4 / 126 | `badnik_kill:echo3` | Native badnik destruction; nearest active participant corroborated visually |
| 1118 | 4 / 143 | `plate_on:gold` | Plate/channel/rift condition observed |
| 1118 | 4 / 143 | `gate_open:cyan+magenta+gold` | Plate/channel/rift condition observed |
| 1193 | 4 / 218 | `clear` | ROOM CLEAR card |
| 1205 | 4 / 218 | `star:1` | Earned star pop (1 Clear, 2 Par) |
| 1223 | 4 / 218 | `star:2` | Earned star pop (1 Clear, 2 Par) |

## Visual review and limitations

Opened representative final PNG frames: 250, 450, 660, 840, 1099, 1101, 1104, 1180, 1241. Whole HUD, normal Sonic/echo sprites, required contacts, clear card and earned stars inspected. No debug overlays.

The ordinary room checkpoint restores camera to its authored initial clamp, then native camera following settles during the first several movement ticks. The restore frame can omit HUD/player; early native ticks can have Sonic below view. These raw transitions are retained honestly (including every12-frame rewind flash), with no camera overrides. Boot pre-roll also holds a static off-room view before room input180. This is a presentation limitation, not frozen gameplay or a missing route segment. Stationary recording padding and the clear-card tail are intentional.

Hero loops: native-input ranges180–319,333–502,516–700,714–962,976–1193 (clear at1193). Command rows320/503/701/963; restore rows332/515/713/975. Final echo3 (fourth echo, lime) rolls the Spiny at1101; reviewed before/after frames1099/1101/1104. Other echoes hold cyan/magenta/gold while live Sonic approaches the rift. Camera cannot show every widely separated echo at once. Clear+Par earned; Shards is intentionally unearned by par route.

Rejected timeout hero: third recording died at native loopFrame195 because the live Sonic remained beside the moving Spiny after its authored185-frame route. Replaced with authored scheduled ECHO presses; rejected PNGs were deleted. Removing the stock-entry prefix also truncates input during entry presentation, so the final take retains that pre-roll.

## Reproduce

Exact argv, environment and capture jar SHA256: `command.json`. Java25 / supplied S2 REV01 SHA1 `8bca5dcef1af3e00098666fd892dc1c2a76333f9`.

```sh
export PATH="/usr/share/idea/plugins/maven-plugin/lib/maven3/bin:$PATH"
export JAVA_HOME=/home/james/.jdks/corretto-25.0.4.1
env -u DISPLAY -u WAYLAND_DISPLAY python3 tools/testing/maven_queue.py -q -Dmse=off -Dopenggf.headless.gl=surfaceless-egl -Dechoes.capture.room=3-4 -Dechoes.capture.session=/home/james/tmp/sonic-echoes-promo/captures/b5-last-loop/session.csv -Dopenggf.saveRoot=/home/james/tmp/sonic-echoes-promo/captures/b5-last-loop/save -Dechoes.capture.actions=0:140:ECHO,1:170:ECHO,2:185:ECHO,3:249:ECHO exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool '-Dexec.args=--game s2 --rom '"'"'/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen'"'"' --mod /home/james/tmp/sonic-echoes-promo/captures/b5-last-loop/promo-action-capture.jar --zone cpz --act 1 --width 400 --every 1 --input /home/james/tmp/sonic-echoes-promo/captures/b5-last-loop/inputs.txt --no-video --out-dir /home/james/tmp/sonic-echoes-promo/captures/b5-last-loop'
```

Shared observer is Worker A’s unedited `PromoCaptureMod.java`. Additional test-only source: `examples/sonic-echoes/src/test/java/echoes/PromoActionCaptureMod.java`. Separate capture jar `../b5-last-loop/promo-action-capture.jar`; rebuild script there. Never packaged in distributed mod. No suites run, no commits/pushes/branch changes.

Final every-PNG scan: 1411 images at400×224; wrong sizes=0, black images=0. Longest byte-identical PLAYING streak=1 frames starting180.
