# Native-pair MHZ1 → MHZ2 → playable FBZ

Captured2026-09-27 from unchanged production83cf9a0a8. Native locked-on S3K,
Sonic + CPU Tails,320px, donor off, cold MHZ1 entry. No position, ring, health,
clock or debug seeds. Canonical input.script/input.bk2 contains40,630 frames;
Committed route/tests: b3428e8d7. Repository owner: src/test/resources/routes/s3k/mhz2-team-incoming-320.*.
ROM /home/farrell/code/projects/OpenGGF/s3k.gen.

GameplayCaptureTool arguments: --game s3k --zone mhz --act1 --main sonic
--sidekick tails --donor off --width320 --frames40630 --capture-from33500
--every1 --scale2, plus absolute --rom/--input/--out-dir paths.
state.csv contains the entire cold route: zero deaths, no missing registered
follower, all37,972 boss-author and40,270 exit-author rows match on all fields
except input-text representation. Final Sonic(201,1219) is playable FBZ1;
Tails is in the native CPU respawn sentinel in this final loop section, so the
registered-roster claim does not mean continuously on-screen Tails.

capture.mp4:7130 frames,60fps,640x448,118.833333s; full ffmpeg decode passed.
defeat-and-fbz-handoff.mp4:2710 frames starting at input37920,60fps,45.166667s;
trimmed by source-frame number4420 and fully decoded. Both represent engine
presentation, not aligned native emulator parity.

Key inputs:35000 shared-handle pulley climb;36600 final catapult;37971 final
boss hit (four rings);38795 capsule approach;39700 scripted wait;40000 overhead
ship;40269 actual FBZ load;40629 ordinary destination movement. These stills
were inspected with state.csv. Whole-registry route replay and production live
history isolation have separate committed tests; see the campaign audit.

The accepted route uses the upper swing-vine release, not the lower mushroom
pocket behind airborne-inaccessible standard breakable walls. Late shared-handle
pulls use8 Down/8 neutral so the CPU follower permits retraction. Turning right
while pressing the final capsule avoids walking into its still-solid body later.

Integrated verification: b3428e8d7,79 focused cases passed, zero failures/errors/
skips; recorded in0adeded4a and pushed to develop. Temporary worktree removed.

Reproduction notes for rejected authoring branches (counts are ordinary inputs):
- From the accepted pre-late-pull prefix34643, repeating16 D/16 neutral leaves
  the shared handle extended; the accepted script uses8 D/8 neutral instead.
- From accepted prefix38730,15 L;45 L+A;120 neutral then repeated30 R+A/30 R
  drifts left of the opened capsule and blocks the later forced walk. Accepted
 15 L;35 L+A then Right reverses earlier and reaches the actual FBZ load.
- The lower mushroom/wall pocket follows a five-input swing-vine release after
 33550; the accepted eight-input release reaches the upper route. Inspect the
 live object inventory: terrain-only views omit the three breakable-wall owners.
The discarded branch PNGs/CSVs and temporary Java adapters were not retained;
canonical inputs and the existing policy/branch tools reproduce the useful work.
