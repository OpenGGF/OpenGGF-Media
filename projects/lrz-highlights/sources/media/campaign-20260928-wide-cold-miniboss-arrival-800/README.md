# LRZ widescreen cold miniboss arrival — 2026-09-28

Runtime: develop f46863ed002e359137cbe268bea819d204de9dc7. No runtime or source edits in this extension.
Native Sonic + Tails, donor off, width 800, cold LRZ Act 1 start, no position/ring/shield seeds.

`capture-input.script` and round-tripped `capture-input.bk2` contain 18,547 ordinary controller inputs. Independent GameplayCaptureTool replay completes all inputs with zero deaths, ending at (11439,1958), 9 rings, high priority enabled, camera (11024,1808), inside the miniboss arena. Every CSV field across all 18,547 rows matches the authoring probe. This is forward engine evidence, not native parity or new rewind certification.

Video: capture.mp4, inputs 14129–18546 inclusive, 4,418 frames at 60 fps, 1600×448, 73.633333 seconds. Full ffmpeg decode passes. Stills 15023, 16100 and 18546 inspected. Covers the high launch, late cloud, westbound crushing-platform passage, descending platforms, east spring and miniboss arrival.

The prior independently verified prefix ended at 13,225 inputs. Corrections use ordinary controller actions: face right before high-launch spindash; spindash out of Toxomister cloud; jump west from the lava edge; wait 120 charged frames for the west crushing platform; jump over the east spring. No physics or terrain tuning.

Authoring lineage (all under main target/, date suffix -20260928):
- lrz-wide-high-launch-facing/variant-0 through 14770
- lrz-wide-late-cloud/variant-0 through 15023
- lrz-wide-west-lower/variant-1 through 15233
- lrz-wide-west-step2/variant-1 through 15446
- lrz-wide-west-crusher-wait/variant-0 through 15850
- lrz-wide-late-elevator/variant-0 through 16901
- lrz-wide-east-spring-exit/variant-1 through 17006
- lrz-wide-east-spring-jump/variant-1 through 17196
- lrz-wide-east-final-descent/variant-0 through 18547, frozen here.

Rejected continuations: copied native fight inputs die at 19830; a 180-frame crusher wait dies while the 120-frame wait clears it. Full failed suffixes are exploratory only. Resume the fight from the durable input here, or an earlier prefix if phase alignment requires it. Next: author a surviving miniboss clear, then add full-registry rewind coverage and integrate the frozen route under repository policy. No whole-act completion claim.
