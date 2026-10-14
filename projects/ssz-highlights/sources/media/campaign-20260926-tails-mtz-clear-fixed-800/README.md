# SSZ solo Tails MTZ clear, 800px

Runtime source committed as75c9caf16 (feature/ai-sk-zone-resume based on
ed828779d), with the preliminary camera projection correction. Native S3K, solo Tails, donor off, cold start,
no position/ring/health/clock seed. Input: `src/test/resources/routes/s3k/ssz1-tails-solo-cold-replicas-800.bk2`.

GameplayCaptureTool: --game s3k --zone ssz --act 1 --width 800 --main tails
--donor off --rom /home/farrell/code/projects/OpenGGF/s3k.gen
--input src/test/resources/routes/s3k/ssz1-tails-solo-cold-replicas-800.bk2 --frames 9683 --capture-from 7688 --scale 2
--out-dir /home/farrell/Videos/OGGF/ssz-bring-up/campaign-20260926-tails-mtz-clear-fixed-800

All 9683 state.csv rows exactly match the independent delay8-800 probe;
zero deaths/followers. MP4 fully decoded by ffmpeg, 60fps/1600x448. Defeat and
released receiving-pad stills inspected. Complete wide Mecha route and native
emulator parity remain separate. Eight neutral frames at the stationary GHZ
approach account for the configured proportional deadzone's later lock.
