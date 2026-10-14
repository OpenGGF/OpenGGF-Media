# SOZ native cold-start handoff

Candidate bugfix/ai-seamless-presentation, base6088735c8. Native Sonic solo,320px, unchanged soz1-cold-sonic.bk2, no position/health/ring/clock seeds. GameplayCaptureSession with S3K_SKIP_INTROS=false; one neutral ordinary GameLoop step executes the initial Process_Sprites setup, then input frame0 begins. This matches the route test, which executes the same setup token before its input loop. The stock GameplayCaptureTool forces skip-intros=true, so its default startup is incompatible with this native-intro recording.

31,492 cold frames; actual Act2 at31392. All31,492 candidate state rows equal the matched base, zero deaths.160 frames at60fps, nearest-neighbour2x, silent. Engine visual evidence, not native pixel parity. Production changes and delivery pending broad verification.
