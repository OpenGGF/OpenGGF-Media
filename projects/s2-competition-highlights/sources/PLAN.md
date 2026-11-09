# S2 Competition highlights for James (2026-11-09)
Brief: personal share. Vibe: "Look, I recreated your competition work that I accidentally deleted the branch for a few months ago."
Sources: DebugSonic2CompetitionRouteVideo -Ds2video.audio=true on PR #273 head (source-commit.txt); native BizHawk frames ~/Videos/OGGF/s2-competition/native-full (comparison only, labelled).
Note: frozen routes run one player at a time (P1 then P2 in act 1; P2 then P1 in act 2) - the other half idles. Frame the active half; do not call it a simultaneous race.

Tie route milestones (row = engine route row, 60 fps):
- title 0-972 (2P VS selected late), menu 972-1172, EHZ1 card 1172-1260
- act1 P1 runs 1315 -> finish 3749 (loop ~2640-2940); P2 runs 3775 -> finish 6307 (loop ~5040-5280)
- act1 results 6489 (1P WINS), EHZ2 card 10141-10229
- act2 P2 runs 10256 -> 12323; P1 runs 12385 -> 14499; results 14681 (2P WINS)
- tie -> special stage 18365: fade-to-white 23, white hold 104, startup, fade-from-white, START, run to 18966
Zone-results route: zone results phase 3 at 18493-18614.
Native frame for act-1 engine row r = r + 69 (engine row 1260 and native frame 1329 both have Level_frame_counter 0).
Captures: cap/ at a41d0c714 (PR #273 head after the special-stage pacing, tie re-stamp and S2 music request-byte fix). src/ is a superseded first capture at 9b2be2ab6 (CNZ failed there on the music crash).
