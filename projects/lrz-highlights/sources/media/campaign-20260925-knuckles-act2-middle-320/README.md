# Knuckles LRZ Act2 progress, 2026-09-25

Source: feature/ai-sk-zone-completion after6bff013cc, test/input-only extension.
Cold Act1, ordinary solo Knuckles, donor off, native320. No position/ring/shield/
emerald setup. Canonical input src/test/resources/routes/s3k/lrz-knuckles-cold-act2-middle-320.bk2.

Run from /home/farrell/code/projects/OpenGGF/.worktrees/ai-sk-zone-completion:

```bash
DISPLAY=:0 /usr/lib/jvm/java-21-openjdk/bin/java -Xmx768m -cp "target/classes:$(cat target/capture-classpath.txt)" com.openggf.tools.GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone lrz --act 1 --width 320 --main knuckles --sidekick none --input src/test/resources/routes/s3k/lrz-knuckles-cold-act2-middle-320.bk2 --frames 33763 --capture-from 30281 --stills 31722,32695,33762 --out-dir /home/farrell/Videos/OGGF/lrz-bring-up/campaign-20260925-knuckles-act2-middle-320
```

33763 fresh rows match branch093 variant1 prefix33763 on x/y, x/y velocity,
ground speed, air, rolling, hurt, dead, rings, camera x/y: zero differences,
deaths or followers. Final6678/1132,0rings. Video3482frames,60fps,58.033333s,
full ffmpeg decode passes. Stills32695/33762 inspected. Focused JUnit test
passes48 full-registry restore+45-input replay spots,1test0fail/error/skip.
This is engine progress and rewind evidence, not native pixel parity or Act2 completion.

Committed as d85754836. Main integration and push remain pending.
