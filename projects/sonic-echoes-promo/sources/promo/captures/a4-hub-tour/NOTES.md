# a4-hub-tour

Base commit: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current main checkout, `feature/ai-sonic-echoes`. No commits/push/branch changes.

Entry: Cold title boot (`--title-screen --interactive-pacing`), real Genesis Start/hub navigation/confirmation. No teleport, seeded recordings, forced drift or gameplay mutation. **No native S2 room title card appears in this capture** (capture tool default; mod room entry finishes initial presentation).

1453 PNGs, **frames 0–1452**, 400×224, 60 Hz, every frame, lossless, silent, surfaceless EGL with DISPLAY/WAYLAND_DISPLAY unset. No audio enabled. `preview.mp4` is a silent uncut convenience encode.

`state.csv` / `session.csv`: equal row counts and frame numbers; live centre/camera coordinates match on every row. Logical held input, face actions and Start are recorded. Echo slots are zero-based. Shard events use room placement indices. `star:1/2/3` means Clear/Par/Shards. `hubSelected` records selected card where available.

Test-only helpers: shared `PromoCaptureMod.java` plus Worker B’s `PromoActionCaptureMod.java`. See `../HELPER.md` and `../HELPER_BUILD.py --actions`. ECHO commands are scheduled at authored loop/frame boundaries through the ordinary mod command path. Genesis input is compiled and round-trip-validated with InputLogAuthorTool. Each nonfinal authored loop is followed by 13 neutral rows (command plus 12-frame rewind hold). Distributed sources/jar are untouched.

Exact capture command (JAVA_HOME and Maven PATH as assigned in task):

```sh
python3 tools/testing/maven_queue.py -q -Dmse=off -Dopenggf.headless.gl=surfaceless-egl -Dechoes.capture.session=/home/james/tmp/sonic-echoes-promo/captures/a4-hub-tour/session.csv -Dopenggf.saveRoot=/home/james/tmp/sonic-echoes-promo/captures/a4-hub-tour/save exec:java -Dexec.mainClass=com.openggf.tools.GameplayCaptureTool '-Dexec.args=--game s2 --rom '"'"'/home/james/IdeaProjects/OpenGGF/Sonic The Hedgehog 2 (W) (REV01) [!].gen'"'"' --mod /home/james/tmp/sonic-echoes-promo/captures/a-helper-proof/promo-capture.jar --zone 0 --act 1 --width 400 --every 1 --input /home/james/tmp/sonic-echoes-promo/captures/a4-hub-tour/inputs.txt --no-video --stop-on-death false --out-dir /home/james/tmp/sonic-echoes-promo/captures/a4-hub-tour --title-screen --interactive-pacing'
```

Exact authored Genesis input:

```text
900 -
1 S
60 -
1 R
25 -
1 R
25 -
1 R
25 -
1 R
25 -
1 D
25 -
1 R
60 -
1 A
180 -
1 U
119 -
```

| Frame | Event | On-screen evidence |
| --- | --- | --- |
| 961 | hub_move | Real controller navigation moves selected hub card to 1-2. |
| 987 | hub_move | Real controller navigation moves selected hub card to 2-1. |
| 1013 | hub_move | Real controller navigation moves selected hub card to 2-2. |
| 1039 | hub_move | Real controller navigation moves selected hub card to 3-1. |
| 1065 | hub_move | Real controller navigation moves selected hub card to 3-3. |
| 1091 | hub_move | Real controller navigation moves selected hub card to 3-4. |
| 1152 | hub_confirm | Real controller confirm launches selected room. |

Representative frames personally opened:

- `00930.png`: Emerald Hill tab, all four cards cleared, 33/36; reviewed.
- `00987.png`: Hill Top tab, all four cards cleared, 33/36; reviewed.
- `01039.png`: Chemical Plant tab, 3-1…3-3 cleared and 3-4 unlocked; reviewed.
- `01120.png`: 3-4 THE LAST LOOP selected, ready and unplayed; reviewed.
- `01333.png`: First ordinary native tick after real Up input; mod HUD appears while entry camera settles; reviewed.
- `01370.png`: Live Sonic and whole mod HUD visible after camera settles; reviewed.
- `01452.png`: Finale room after 120 ordinary gameplay ticks, live Sonic and whole mod HUD visible; reviewed.

Quality: Sonic, readable echoes and whole mod HUD inspected; native terrain moves correctly. Expected READY, rewind and results holds are intentional. No debug overlays. Black transition ranges: 327–328, 468–468, 480–485, 497–504, 516–523, 1173–1174. These are short stock title/launch fades; the longest is eight rows. No sustained black gameplay.

Earned save: `save/mods/sonic-echoes/progress.txt` contains 33 stars from real reference-route replays of 1-1…2-4 and 3-1…3-3. Room 3-4 is absent (unplayed). Each par and shard solution was driven by InputLogAuthorTool logs in `earned/`, with a complete `state.csv`. Earnings runs use one initial PNG (`every=999999`) because they are progress replays rather than film takes. World 1 and most world 2 runs use timeout commits; the 2-4 shard retry and world 3 use tight ECHO commands. The earlier timeout 2-4 shard attempt reached an existing provider identity limit at frame 3401; progress was already earned by the successful par route and the compact shard retry completed. No save file was fabricated or edited.

Entry review and limit: native TITLE_CARD/initial setup is retained continuously and its artwork is omitted by the capture default. READY holds the initial room camera with Sonic below the viewport; an actual one-frame Up at 1333 starts normal camera/clock service. By frame 1370 Sonic and the full HUD are visible; frame 1452 is loopFrame120. Use the hub and frames 1370–1452 for the finished shot; early entry frames are documented setup, not clean gameplay footage. Two earlier short endings were rejected during image review and replaced. The save remains 33/36 and 3-4 unplayed/unrecorded.
