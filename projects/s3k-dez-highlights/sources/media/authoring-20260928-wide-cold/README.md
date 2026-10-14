# DEZ 800px cold route authoring checkpoint

Runtime f411b75db, integrated and pushed to develop; delivery record 8ec5aa0fa.
Sonic solo, DEZ Act 1 cold start, 800px, no donor, no teleport, no state seeds,
no settle. The retained script/BK2 contains 7,795 ordinary pad inputs.
Independent GameplayCaptureTool replay matches all 7,795 author rows on twelve
player fields, zero deaths. Final centre (9912,2100), eight rings, turbine room.

fresh-prefix/capture.mp4 covers inputs 6800..7794: 995 frames, 60fps,
1600x448, 16.583 seconds. Full decode passed; final turbine still inspected.
The capture is silent. This is an unfinished Act 1 input-authoring frontier,
not whole-act completion, rewind certification, or native-emulator parity.

Earlier braking, repeated ordinary jumps through the lower conveyor and a jump
across its following gap replaced the failed descent inputs. No DEZ runtime
code changed. Resume from turbine-7795.bk2.


## Turbine gate cleared

`turbine-clear-14450.script/.bk2` extends the cold prefix through all six panels
and the gate. Read-only diagnostic bits changed 0x39 -> 0x3b -> 0x3f: the missing
left middle/bottom contacts were reached by a timed downward approach.
Fresh production capture matches all14,450 author rows on twelve player fields,
zero deaths. `turbine-clear/capture.mp4`:1450 frames at60fps,1600x448,24.167s,
covering inputs13000..14449; complete decode passed. Runtime f411b75db.
The route remains unfinished; later native-input reuse returns to the moving
staircase and fails its upper transfer. No DEZ runtime changes.


## Act 1 boss arrival

`boss-arrival-17230.script/.bk2` reaches the real boss from cold DEZ1. The full
17,230-frame independent replay matches all twelve authored player fields,
zero deaths, ending at(14234,749),15 rings. The moving staircase needs a longer
run-up to clear the upper gap. `boss-arrival/capture.mp4` covers15140..17229:
2090 frames,60fps,1600x448,34.833s,complete decode passes. Runtime f411b75db.
Boss defeat and the continuing Act2 route remain unfinished; no new engine
behavior is claimed. This is the current independently verified frontier.
