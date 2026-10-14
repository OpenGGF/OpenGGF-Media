# Knuckles LRZ Act2 upper route, 2026-09-25

Source: feature/ai-sk-zone-completion after d85754836, test/input-only extension.
Cold Act1, ordinary solo Knuckles, donor off, native320. No position/ring/shield/
emerald setup. Canonical input lrz-knuckles-cold-act2-upper-320.bk2.

Run from /home/farrell/code/projects/OpenGGF/.worktrees/ai-sk-zone-completion:

```bash
DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main knuckles --sidekick none --input src/test/resources/routes/s3k/lrz-knuckles-cold-act2-upper-320.bk2 --frames 40046 --capture-from 33763 --stills 34339,37080,38916,40045 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-knuckles-act2-upper-320
```

All40046 fresh rows match branch122 variant1 on x/y, x/y velocity, ground speed,
air, rolling, hurt, dead, rings, camera x/y: zero differences/deaths/followers.
Final8501/236,0rings. Video6283frames60fps104.716667s, full ffmpeg decode passes.
Stills34339/38916/40045 inspected. New JUnit method passes53 full-registry immediate
restores and45-input replays,1test0fail/error/skip. Engine progress/rewind evidence,
not native pixel parity or Act2 completion. Main integration/push still pending.

Committed as dd3db3d61.
