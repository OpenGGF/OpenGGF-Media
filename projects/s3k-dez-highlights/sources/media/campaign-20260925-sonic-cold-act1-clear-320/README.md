# Sonic solo cold DEZ1 completion

Source engine dfe7baae1; current milestone adds inputs/tests only. Native320 Sonic, no sidekick, donoroff, cold DEZ1, no state seeds. Input route.script and route.bk2 preserve23533 inputs, including1200neutral after load. Search003 source22333 prefix independently matches x,y,xvel,yvel,gspeed,air,rolling,spindash,hurt,dead,rings,mapping_frame in every row. No deaths/followers in23533 rows.

Command (from task worktree with Java21 DISPLAY=:0, target/classes plus target/capture-classpath.txt):
GameplayCaptureTool --rom /home/farrell/code/projects/OpenGGF/s3k.gen --game s3k --zone dez --act 1 --main sonic --sidekick none --width 320 --input /home/farrell/Videos/OGGF/s3k-dez-bring-up/campaign-20260925-sonic-cold-act1-clear-320/route.bk2 --capture-from 20300 --stills 20600,21800,23532 --out-dir /home/farrell/Videos/OGGF/s3k-dez-bring-up/campaign-20260925-sonic-cold-act1-clear-320

Video3233frames60fps53.883333s, full ffmpeg decode passes, selectedstills inspected. Final320/940 freecontrol confirmed by TestDezSoloColdRouteCapture:1pass0fail0error0skip18.89s test40.572s Maven,61full-registry immediate restore/45-input replay windows. Engine evidence, not native parity. Campaign verification/integration remains open.
