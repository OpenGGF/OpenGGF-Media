# a1-chain

Base commit: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current main checkout, `feature/ai-sonic-echoes`. No commits/push/branch changes.

Entry: Cold title boot (`--title-screen --interactive-pacing`), real Genesis Start/hub navigation/confirmation. No teleport, seeded recordings, forced drift or gameplay mutation. **No native S2 room title card appears in this capture** (capture tool default; mod room entry finishes initial presentation).

3130 PNGs, **frames 0–3129**, 400×224, 60 Hz, every frame, lossless, silent, surfaceless EGL with DISPLAY/WAYLAND_DISPLAY unset. No audio enabled. `preview.mp4` is a silent uncut convenience encode.

`state.csv` / `session.csv`: equal row counts and frame numbers; live centre/camera coordinates match on every row. Logical held input, face actions and Start are recorded. Echo slots are zero-based. Shard events use room placement indices. `star:1/2/3` means Clear/Par/Shards. `hubSelected` records selected card where available.

Test-only helpers: shared `PromoCaptureMod.java` plus Worker B’s `PromoActionCaptureMod.java`. See `../HELPER.md` and `../HELPER_BUILD.py --actions`. ECHO commands are scheduled at authored loop/frame boundaries through the ordinary mod command path. Genesis input is compiled and round-trip-validated with InputLogAuthorTool. Each nonfinal authored loop is followed by 13 neutral rows (command plus 12-frame rewind hold). Distributed sources/jar are untouched.

Exact capture command (JAVA_HOME and Maven PATH as assigned in task):

```sh
python3 tools/testing/maven_queue.py -q -Dmse=off -Dopenggf.headless.gl=surfaceless-egl -Dechoes.capture.session=/home/james/tmp/sonic-echoes-promo/captures/a1-chain/session.csv -Dopenggf.saveRoot=/home/james/tmp/sonic-echoes-promo/captures/a1-chain/save -Dechoes.capture.actions=0:100:ECHO,0:100:ECHO,1:300:ECHO exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool '-Dexec.args=--game s2 --rom '"'"'/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen'"'"' --mod /home/james/tmp/sonic-echoes-promo/captures/a-helper-proof/promo-actions.jar --zone 0 --act 1 --width 400 --every 1 --input /home/james/tmp/sonic-echoes-promo/captures/a1-chain/inputs.txt --no-video --stop-on-death false --out-dir /home/james/tmp/sonic-echoes-promo/captures/a1-chain --title-screen --interactive-pacing'
```

Exact authored Genesis input:

```text
900 -
1 S
60 -
1 S
200 -
40 R
60 -
13 -
240 R
120 -
1 A
240 -
1 L
25 -
1 A
200 -
40 R
60 -
13 -
100 L
200 -
13 -
240 R
120 -
1 A
240 -
```

| Frame | Event | On-screen evidence |
| --- | --- | --- |
| 961 | hub_confirm | Real controller confirm launches selected room. |
| 1198 | plate_on:cyan;gate_open:cyan | Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen. |
| 1204 | shard:3 | Live/echo collects room shard(s), indicated by placement index. |
| 1262 | commit;rewind_start | Authored attempt commits; mod’s twelve-frame rewind flash starts. |
| 1274 | restore | World returns to room spawn; recorded echo joins next loop. |
| 1311 | plate_on:cyan;gate_open:cyan | Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen. |
| 1317 | shard:3 | Live/echo collects room shard(s), indicated by placement index. |
| 1433 | shard:5 | Live/echo collects room shard(s), indicated by placement index. |
| 1437 | clear | ROOM CLEAR overlay begins at the rift. |
| 1449 | star:1 | Result star pop; Clear=1, Par=2, Shards=3. |
| 1467 | star:2 | Result star pop; Clear=1, Par=2, Shards=3. |
| 1876 | hub_move | Real controller navigation moves selected hub card to 1-1. |
| 1902 | hub_confirm | Real controller confirm launches selected room. |
| 2139 | plate_on:cyan;gate_open:cyan | Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen. |
| 2145 | shard:3 | Live/echo collects room shard(s), indicated by placement index. |
| 2203 | commit;rewind_start | Authored attempt commits; mod’s twelve-frame rewind flash starts. |
| 2215 | restore | World returns to room spawn; recorded echo joins next loop. |
| 2251 | shard:4 | Live/echo collects room shard(s), indicated by placement index. |
| 2252 | plate_on:cyan;gate_open:cyan | Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen. |
| 2258 | shard:3 | Live/echo collects room shard(s), indicated by placement index. |
| 2516 | commit;rewind_start | Authored attempt commits; mod’s twelve-frame rewind flash starts. |
| 2528 | restore | World returns to room spawn; recorded echo joins next loop. |
| 2564 | shard:4 | Live/echo collects room shard(s), indicated by placement index. |
| 2565 | plate_on:cyan;gate_open:cyan | Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen. |
| 2571 | shard:3 | Live/echo collects room shard(s), indicated by placement index. |
| 2687 | shard:5 | Live/echo collects room shard(s), indicated by placement index. |
| 2691 | clear | ROOM CLEAR overlay begins at the rift. |
| 2703 | star:1 | Result star pop; Clear=1, Par=2, Shards=3. |
| 2739 | star:3 | Result star pop; Clear=1, Par=2, Shards=3. |

Representative frames personally opened:

- `00899.png`: Native Sonic 2 emblem and ECHOES wordmark, reviewed.
- `00930.png`: Fresh Echo Engine hub, 0/36, room 1-1 selected; reviewed.
- `03090.png`: Returned hub: 1-1 has three lifetime stars, 1-2 unlocked; reviewed.

Quality: Sonic, readable echoes and whole mod HUD inspected; native terrain moves correctly. Expected READY, rewind and results holds are intentional. No debug overlays. Black transition ranges: 327–328, 468–468, 480–485, 497–504, 516–523, 982–983, 1923–1924. These are short stock title/launch fades; the longest is eight rows. No sustained black gameplay.

Shot-list limitation: the authored shard route uses two echoes while par is one. This continuous take first earns Clear+Par, returns to the hub, reselects 1-1 with real input, then earns Shards. The final hub honestly shows all three lifetime stars and 1-2 unlocked. The shard-run results pop Clear and Shards, with Par hollow; three simultaneous result-star pops cannot be achieved with these authored routes. No behavior change was made.

Sidecar phase normalization: 154 READY rows in native non-LEVEL entry modes relabeled OTHER from aligned state.csv; all recorded values/events unchanged. Latest helper identifies uninitialized entry directly.

Hub return phase boundaries: see session.csv; phase transitions supply return evidence (hub_move/hub_confirm are input events, not synthetic return labels). Final controller-selected next card is 1-2 with three filled 1-1 stars.
