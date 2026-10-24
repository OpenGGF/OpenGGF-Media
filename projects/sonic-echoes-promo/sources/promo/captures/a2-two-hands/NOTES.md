# a2-two-hands

Base commit: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current main checkout, `feature/ai-sonic-echoes`. No commits/push/branch changes.

Entry: Pre-boot room selection through `echoes.capture.room=1-2`, then ordinary stock boot. 180 neutral entry rows. No teleport, seeded recordings, forced drift or gameplay mutation. **No native S2 room title card appears in this capture** (capture tool default; mod room entry finishes initial presentation).

831 PNGs, **frames 0–830**, 400×224, 60 Hz, every frame, lossless, silent, surfaceless EGL with DISPLAY/WAYLAND_DISPLAY unset. No audio enabled. `preview.mp4` is a silent uncut convenience encode.

`state.csv` / `session.csv`: equal row counts and frame numbers; live centre/camera coordinates match on every row. Logical held input, face actions and Start are recorded. Echo slots are zero-based. Shard events use room placement indices. `star:1/2/3` means Clear/Par/Shards. `hubSelected` records selected card where available.

Test-only helpers: shared `PromoCaptureMod.java` plus Worker B’s `PromoActionCaptureMod.java`. See `../HELPER.md` and `../HELPER_BUILD.py --actions`. ECHO commands are scheduled at authored loop/frame boundaries through the ordinary mod command path. Genesis input is compiled and round-trip-validated with InputLogAuthorTool. Each nonfinal authored loop is followed by 13 neutral rows (command plus 12-frame rewind hold). Distributed sources/jar are untouched.

Exact capture command (JAVA_HOME and Maven PATH as assigned in task):

```sh
python3 tools/testing/maven_queue.py -q -Dmse=off -Dopenggf.headless.gl=surfaceless-egl -Dechoes.capture.session=/home/james/tmp/sonic-echoes-promo/captures/a2-two-hands/session.csv -Dopenggf.saveRoot=/home/james/tmp/sonic-echoes-promo/captures/a2-two-hands/save -Dechoes.capture.room=1-2 -Dechoes.capture.actions=0:100:ECHO,1:165:ECHO exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool '-Dexec.args=--game s2 --rom '"'"'/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen'"'"' --mod /home/james/tmp/sonic-echoes-promo/captures/a-helper-proof/promo-actions.jar --zone 0 --act 1 --width 400 --every 1 --input /home/james/tmp/sonic-echoes-promo/captures/a2-two-hands/inputs.txt --no-video --stop-on-death false --out-dir /home/james/tmp/sonic-echoes-promo/captures/a2-two-hands'
```

Exact authored Genesis input:

```text
180 -
40 R
60 -
13 -
65 R
100 -
13 -
240 R
120 -
```

| Frame | Event | On-screen evidence |
| --- | --- | --- |
| 216 | plate_on:cyan | Room/HUD state changes; matching frame PNG available. |
| 222 | shard:4 | Live/echo collects room shard(s), indicated by placement index. |
| 280 | commit;rewind_start | Authored attempt commits; mod’s twelve-frame rewind flash starts. |
| 292 | restore | World returns to room spawn; recorded echo joins next loop. |
| 329 | plate_on:cyan | Room/HUD state changes; matching frame PNG available. |
| 335 | shard:4 | Live/echo collects room shard(s), indicated by placement index. |
| 378 | plate_on:magenta;gate_open:cyan+magenta | Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen. |
| 458 | commit;rewind_start | Authored attempt commits; mod’s twelve-frame rewind flash starts. |
| 470 | restore | World returns to room spawn; recorded echo joins next loop. |
| 507 | plate_on:cyan | Room/HUD state changes; matching frame PNG available. |
| 513 | shard:4 | Live/echo collects room shard(s), indicated by placement index. |
| 551 | plate_on:magenta;gate_open:cyan+magenta | Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen. |
| 629 | shard:6 | Live/echo collects room shard(s), indicated by placement index. |
| 633 | clear | ROOM CLEAR overlay begins at the rift. |
| 645 | star:1 | Result star pop; Clear=1, Par=2, Shards=3. |
| 663 | star:2 | Result star pop; Clear=1, Par=2, Shards=3. |

Representative frames personally opened:

- `00551.png`: Cyan and magenta echoes visible on their plates; live Sonic crossing magenta plate; gate condition opens. Reviewed.
- `00663.png`: ROOM CLEAR with Clear and Par stars; reviewed.

Quality: Sonic, readable echoes and whole mod HUD inspected; native terrain moves correctly. Expected READY, rewind and results holds are intentional. No debug overlays. No fully black frames.
