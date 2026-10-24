# Sonic Echoes promo — capture brief and shot list

Lead/editor: Claude (assembles everything with `tools/media/promo_kit.py`).
Capture workers: write ONLY under `<task>/captures/<shot-id>/` where `<task>` = this directory
(`/home/james/tmp/sonic-echoes-promo`). Do not edit the edit file, music or sfx folders.

## The film (so you know what the footage must prove)

~90 s gameplay showcase on Chemical Plant's theme (139.44 BPM). Promise: *"Run it. Loop it. Team up
with yourself."* Arc: (1) the loop — your attempt comes back as an echo, the same buttons give the
same Sonic; (2) echoes are real — they hold plates, ride Hill Top seesaws, take springs, pop badniks;
(3) Paradox — same buttons in a changed world break the echo; (4) climax: The Last Loop, four
loops stacked then one final loop where all four echoes work at once; (5) progress: stars and the hub.
Hero moment: room 3-4's final loop.

## Capture rules (all shots)

- Build from the current branch `feature/ai-sonic-echoes` (HEAD `5fca08819f` or later) in the main
  checkout `/home/james/IdeaProjects/OpenGGF`. Do not commit, push, branch or change the mod's
  distributed behaviour. Test-only capture helpers under `examples/sonic-echoes/src/test/java/echoes/`
  are fine (list them in your report); never package them in the distributed jar.
- `GameplayCaptureTool` via `python3 tools/testing/maven_queue.py exec:java ...` (see the
  `gameplay-capture` skill). Linux display-free: `-Dopenggf.headless.gl=surfaceless-egl` in the
  JVM, `DISPLAY`/`WAYLAND_DISPLAY` unset. Never touch the user's desktop.
- `--width 400` (the mod's 16:9 profile), **every frame** (`--every 1`), lossless PNGs, **no audio**
  (the edit owns sound). A low-res MP4 preview is useful for your own review; PNGs are the deliverable.
- Isolated save roots per shot under `<task>/captures/<shot-id>/save` unless the shot says otherwise.
- Real entries only: from the title, or the mod's capture entrypoint selecting a room before stock
  boot (`RoomCaptureMod`, `-Dechoes.capture.room=<id>`), driven by the room's authored reference
  inputs. Record the exact entry method. No teleports, no forced positions, no forced drift.
- **Per-frame session sidecar (required)**, `<shot>/session.csv`, one row per captured frame, aligned
  to `state.csv`'s frame column: `frame, room, loop, loopFrame, phase` (READY / PLAYING /
  REWIND_HOLD / CLEAR / HUB / TITLE / OTHER), `liveX, liveY` (ROM centre coords), `camX, camY`,
  for each echo slot 0–4 `eNx, eNy, eNstate` (inactive / active / holding / fractured),
  `channels` (active channel names), `shards`, and an `events` column naming anything that happened
  that frame: `commit`, `timeout`, `rewind_start`, `restore`, `fracture:N`, `shard:N`, `plate_on:ch`,
  `gate_open:ch`, `spring:who`, `seesaw_launch:who`, `badnik_kill:who`, `clear`, `star:N`,
  `hub_move`, `hub_confirm`. Add it through a test-only observer (e.g. a capture wrapper mod around
  the ordinary mod) — never through the distributed jar. Also record each frame's live input mask.
- In `<shot>/NOTES.md`: command lines, input script(s), entry method, base commit, frame count,
  and a table of key event frames (from session.csv) with one line each on what is on screen.
- LOOK at frames before reporting: confirm the subject is on screen, the echoes read, HUD whole.

## Shots

### Worker A — Emerald Hill, title and hub

| ID | Content | Must show |
|---|---|---|
| `a1-chain` | ONE continuous take from cold boot: S2 title intro → ECHOES wordmark → Start → Echo Engine hub → select 1-1 → room 1-1 played with its **shard** reference route (scout loop + par route so all three stars are earned) → ROOM CLEAR card with all three stars popping → confirm → back to the hub showing 1-1's three stars and 1-2 unlocked. `--title-screen --interactive-pacing`. Trim waiting only by keeping inputs tight; let each loop's rewind flash play in full. | The relationship in one take: the attempt becomes the cyan echo. Report whether a native S2 title card appears on room entry. |
| `a2-two-hands` | Room 1-2 full session from room start, reference par route. | Two echoes holding two plates, gate opening, clear. |
| `a3-escort` | Room 1-4 full session, reference route. | The echo popping the native Buzzer in the final loop (frame), clear. |
| `a4-hub-tour` | Hub only, with a save that has **real earned progress**: earn it by replaying reference solutions (par + shard routes) for rooms 1-1…2-4 and 3-1…3-3 in the same save root (any honest headless means; label it), leaving 3-4 unlocked but unplayed. Then capture from the title: open the hub, move across all three world tabs slowly (about one move per 26 frames), land on 3-4 THE LAST LOOP, confirm, and keep capturing into the room's first 120 frames. | Stars filling, world tabs, locks gone, the finale card. |

### Worker B — Hill Top, Chemical Plant and the finale

| ID | Content | Must show |
|---|---|---|
| `b1-double-bounce` | Room 2-2 full session, reference route. | Both native seesaw launches (frames), live Sonic reaching the high ledge, clear. |
| `b2-counterweight` | Room 2-4 full session, reference route (3 echoes). | Plate under the seesaw end, the launch, clear. |
| `b3-spring-relay` | Room 3-2 full session, reference route. | Echo 2 taking the native spring onto the high plate (frame), clear. |
| `b4-paradox` | Room 3-1 in one session: the authored **naive** route first, so the live run disturbs echo 1 and it fractures organically (native PARADOX banner), then Reset/Undo as a player would and play the correct reference route to clear. If one session cannot express this honestly, capture `b4a-naive` and `b4b-solved` separately and say so. | A real fracture caused by the live run (frame + slot), then the fix. |
| `b5-last-loop` | Room 3-4 full session, reference par route, every loop (all four recording loops and the final loop), through the ROOM CLEAR card and its star pops. | Each loop's live run (for a 2×2 "four loops" grid), then the final loop with four echoes working at once, the fourth echo rolling the native Spiny (frame), sealed rift opening, clear. |
| `b6-clockwork` | Room 3-3 full session, reference route. | Three timed latches, sealed rift. |

## Report back (each worker)

Per shot: path, frame range, entry method, notable event frames, anything that did not work and why,
any test-only helper you added. Keep it concise; the NOTES.md files carry the detail.
