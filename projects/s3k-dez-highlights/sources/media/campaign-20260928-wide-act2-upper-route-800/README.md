# DEZ Act 2 widescreen upper-route progress — 2026-09-28

Runtime ee8e470e4; main checkout 8540cdab0 (documentation-only successor). No runtime changes for this input-authoring milestone.

Cold DEZ1 Sonic solo, 800px, donor off, no position/ring/clock seeds or settling. The 40,351-input movie includes both Act1 boss phases, seamless Act2 load, lower energy bridges, gravity switch, ceiling-spring bypass, vertical launch, upper return route and gravity shafts to the tilting bridge at centre (8885,2472), two rings.

Fresh GameplayCaptureTool replay matches all 40,351 author rows on every exported CSV field, zero death rows. Video: inputs34700–40350, 5651 frames,60fps,1600x448,94.183333seconds. Full ffmpeg decode passed; fresh frames35000 and39000 inspected. Complete route inputs preserved alongside state.csv.

This is partial engine route evidence, not a completed Act2 run, new rewind verification or matched emulator parity. A continuation copied too-late native-width inputs and fell into the pit after arriving low at the tilting bridge. This is not evidence for changing collision logic. Current next authoring probe: target/dez800-act2-tilting-jumps-20260928. Earlier failed continuation: target/dez800-act2-late-middle-20260928 (death40704).

Follow-up probes completed: tilting-jumps variants all fell; tilt-resync variants all died (variant0 reaches x8885/y2310 but later is hit); tilt-brake 8/10/12 Left also all fell. Inspecting CSV shows 8/10 Left settles at x8633/y2476, short of the native successful pause at x8653 (native inputs37550–37700). Zero braking settles at8725 and tilts the wrong portion. Next safe authoring step: move from the x8633 checkpoint (tilt-brake variant0 input40200) about20px right, stop and observe the bridge tilt before jumping, or try less initial braking. No source-level defect established. All probe JVMs terminal; no live session needs resuming.
