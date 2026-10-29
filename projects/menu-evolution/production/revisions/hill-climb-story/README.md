# ROAD TO 9, hill-climb story cut (menu-evolution revision `hill-climb-story`)

Rebuilt 2026-10-29 by Claude Opus 5.5 (xhigh, fast mode off) after the user's review of the 43.2 s
Super Sonic cut: "not bad but the direction sucks. It's difficult to see what the video is getting
at. We need to establish the context (do you have it? We asked Opus originally to classify the menus
based on categories, then asked it to raise that classification in a hill climb until 8 overall (and
then raised it to 9)". Kept from earlier steering: Sonic 2 Super Sonic music throughout, about 43-44 s,
action-montage energy with climbing numbers, readable real moving UI.

**Deliverable:** `final/menu-evolution-hill-climb-story.mp4` (1920x1080, 60 fps, H.264 + AAC stereo
48 kHz, 13 chapters) and the lossless master `final/menu-evolution-hill-climb-story-master.mkv` (FFV1 RGB
+ PCM, the same chapters). 43.200 s (2,592 frames). Hashes: `provenance/deliverables.json`. The first film
(`../../final/`) and the Super Sonic cut (`../super-sonic-cut/`) are unchanged (hashes re-verified).

## The rejection, recorded

| Film | What the user said | Cause |
|---|---|---|
| r3b, 87.333 s | "bit slow and repetitive" | 25 s before the first comparison; the same six-stop climb four times |
| super-sonic-cut, 43.2 s | "the direction sucks. It's difficult to see what the video is getting at" | numbers rose with no assignment behind them: nobody on screen said who scored, on what scale, against which target, or why a number moved; the only context was a footnote and the end card |

The fix is structural, not a caption: the film is now the account of the experiment, told by one
evolving score board, with the real menus and the review's own pictures as proof.

## The story and what each chapter answers

| Chapter (s) | Viewer question | On screen |
|---|---|---|
| The ask (0-3.3) | what was asked? | six round-0 menus drop into a wall; "WE GAVE AN AI EVERY OPENGGF MENU." (Claude Opus, 27 Oct); "STEP 1: SORT THEM INTO GROUPS" and the six group labels land on their menus |
| The rubric (3.3-6.6) | how was it judged? | the labels fly into the rows of the round-0 matrix: seven criteria columns, 1-10, "judged from screenshots", an OVERALL column ("one judgment, not an average"), the scale 5 visibly amateur / 7 good indie / 9 production polish; overlays "not yet pictured in round 0" |
| The goal (6.6-9.8) | what was the target, how does a round work? | "STEP 3: EVERY GROUP TO 8 OR BETTER", a TARGET 8+ column, then the loop CHANGE -> RECAPTURE -> RESCORE -> KEEP OR REVERT |
| Rounds 1-4 (9.8-13.1) | what changed? | the Mod manager and the legal notice, round 0 -> the 8 build, moving; ROUND 0..4 laps with the loop steps lit; the six overall scores climb; "CLOSE. NOT 8 YET." |
| Every family (13.1-16.4) | how far did it reach? | the six groups become 27 menu families (plus the bundled Time Attack mod) as tiles; all but three light at 8; Time Attack 5.5 -> 8, old and new by divider |
| All at 8 (16.4-19.7) | the turning point | "ALL 27 AT 8" slam; "THEN WE RAISED THE BAR." |
| Road to 9 (19.7-22.9) | why did the target rise, what does it mean? | TARGET 8 rolls to 9, every tile falls below it; ROAD / TO / 9; "9 MEANS PRODUCTION POLISH. NONE ARE THERE." |
| Pass 1 (22.9-26.2) | did it just work? | a crowded hub capture at 8, then its pass-1 picture; hub 8 -> 8.5, five 8.5s, families at 9: 0; the audit's "No family reached 9 overall in this pass." |
| Fresh review (26.2-29.5) | is the AI marking its own homework? | the independent review's red mark-up draws onto that capture; hub, help, editor HUD and Stageplay fall 8.5 -> 8, notices rise to 8.5, the trace plates show "?" (their pictures were invalid); "SCORES WENT DOWN, NOT UP." |
| Structure (29.5-32.8) | what fixed it? | the audit's "The remaining blockers are structural rather than polish."; marked-up hub -> rebuilt hub by divider; hub 9; 13 of 27 |
| Finish (32.8-36.0) | was that the end? | another review sends one 9 back (13 -> 12, Editor projects); Settings, structural capture -> delivered moving with its new captions; 26 of 27; the last gap, Time Attack's TAB: DETAILS key hint |
| 27 / 27 (36.0-38.9) | what is the result? | 27 / 27 AT 9; the hub's final criteria row, two of them still 8.5 under an overall 9: "EVERY FAMILY 9 OVERALL. SOME CRITERIA STILL 8.5."; Giant Ring iris into the same six groups, delivered and moving |
| End card (38.9-43.2) | who, where | badge, title, one line, URL, status, the AI agents who did the work, the fan-made disclaimer |

Decisions, one line each:
- ROAD TO 9 is no longer an opening title: it lands at 19.7 s as the turning point, when the target rises.
- The opening 10 s state the assignment as three steps (sort, score, reach 8) and the loop that moves the
  numbers; the matrix columns are the seven criteria, the rows and later the tiles are menu groups and
  families, so the two never share an axis.
- Numbers only change on a recorded pass and every change is tied to a picture of the change or to a
  stated pass; scores fall where the review lowered them.
- Moving UI where moving footage is true: the round-0 menus, the 8-build Mod manager and legal notice
  (pixel-identical to the audit's captures, `sources/promo/identity.py`), delivered Settings and the
  delivered six groups. The review's own still captures appear as labelled evidence, including the
  reviewer's annotated picture at 1:1.
- Quotation marks surround only two verbatim sentences of the design review document; there is no chat
  transcript and no paraphrase in quotes. Other lines are the film's own narration.
- Who did what: Claude Opus is named at the start (it classified and scored); the "fresh review" is named
  as a new Claude Opus session; the end card names Claude Opus 5.5 with OpenAI Codex GPT-6.1 on later
  passes (commit trailers), so the film does not credit one model with every implementation or acceptance.
- Honest limits on screen, not in a footnote: "judged from screenshots", "one judgment, not an average",
  "not yet pictured in round 0", invalid evidence shown as "?", a rejected 9, and criteria still at 8.5.

Rejected while building:
- Re-captioning the Super Sonic cut with an explanatory card: the user asked for structure, not a disclaimer.
- Keeping the 0.5 glimpse: it is not part of the hill climb.
- One divider position per round: no moving captures of intermediate rounds exist, so panes are labelled
  ROUND 0 and AT 8 and the board carries the rounds.
- The open-project editor picture for the send-back beat: a fourth layout inside 3.3 s; the red tile and
  its label carry it.
- Ducking the bed under the two cadence sections: their +3 to +4 LU are mostly the music's own TURN
  section (+2.7 LU in the bed alone); kept, with both Tally Ends and the Giant Ring lowered instead.

## Numbers and their sources

Every score is a recorded value of `docs/architecture/audits/2026-10-27-menu-design-review.md` at
`d823ce643` (`ROUND0`, `ROUNDS`, `PASSES`, `HUB_FINAL` in `sources/promo/edit.py`, each with its section).
They are subjective design judgments from captures, not usability or performance measurements. The
"12" after the second independent review is derived (13 claimed minus the rejected Editor projects 9);
the audit records that rejection and its repair, not a revised number, so the tile keeps a red 9.
Families: the 27 of the toward-9 matrices, grouped into the six original groups (Stageplay chrome with
the overlays and editors, as class F listed them) plus the bundled Time Attack mod, which began as a
report-only class H and was included in the 8 pass.

## Sources and rebuild

```
sources/promo/edit.py        the edit: brief and beat sheet in its docstring, the record (scores), evidence
                             stills, source intervals, cue mapping, master/mp4/remix/loudness/keys commands
sources/promo/review.py      motion, strips, exact pixels, loudness, stereo, stingers, edit-list intervals
sources/promo/identity.py    pixel identity of the takes against the audit's captures per head
sources/promo/{chapters.txt,edl.csv,cues.json}   chapter map, per-shot source intervals, UI cue placements
sources/archive/make_revision_payload.py         the OpenGGF-Media payload builder for this revision
provenance/source-map.json   base, request, score source, reused inputs and evidence stills with hashes
provenance/deliverables.json film and master
review/                      consecutive-frame strips at every transition, final contact sheet
```

Path overrides: `OPENGGF_WORKTREE` (a tree with `tools/media/promo_kit.py`, `c7d66bbf9` or later unchanged),
`MENU_EVIDENCE` (the directory holding `menu-target9-20261028/` and `all-menus-final-families-20261028/`,
default the production root's parent), and the production root, which the edit finds two levels above
this revision (clips, SFX, UI tones, and the Super Sonic cut's music bed, hash-checked by `master`).
Python with numpy 2.5.4 + Pillow 13.0.0: `edit.py check`, `edit.py master`, `edit.py mp4`. No engine code
changed, no menu was recaptured and the music was not re-rendered.

## Viewer pass (every ~4 s: what is new, and why a viewer keeps watching)

| s | New on screen | Why keep watching |
|---|---|---|
| 0-4 | six old menus land; the premise; groups labelled | an AI was given these: what will it do? |
| 4-8 | the matrix fills with low scores, 3.5 to 6.5; the scale | the scores are bad, and now we know on what scale |
| 8-12 | the target 8+; the loop; the Mod manager's old bracket rows sweep to switches | a concrete change and the first climb |
| 12-16 | legal notice transforms; ROUND 4, "NOT 8 YET"; 27 tiles light | the job is bigger than six screens |
| 16-20 | Time Attack 5.5 -> 8; ALL 27 AT 8; "THEN WE RAISED THE BAR" | the goal is met and immediately moved |
| 20-24 | target 9, every tile falls; ROAD TO 9; pass 1 starts on one hub picture | the stakes reset |
| 24-28 | pass 1 stalls at 0; a fresh review marks up the same picture | the plateau and a critic |
| 28-32 | scores fall; then the rebuilt hub; the count climbs to 13 | the climb has to be earned |
| 32-36 | a 9 sent back; Settings changes live; 26; the last key hint | one more check, one last gap |
| 36-40 | 27 / 27; the honest criteria row; the six groups, delivered | the result, with its limits |
| 40-43 | end card, stab, fade | where to find it |

## Checks (measured on the final files)

- ffprobe: both 1920x1080, 60/1, 2,592 frames counted, 43.200 s; MP4 H.264 High yuv420p BT.709 TV range +
  AAC LC 48 kHz stereo; master FFV1 bgr0 + PCM s16le; 13 chapters in the same order and times in both
  (0, 3.283, 6.550, 9.833, 13.100, 16.383, 19.667, 22.933, 26.217, 29.483, 32.767, 36.050, 38.917 -> 43.200 s).
- Full decodes `ffmpeg -v error -xerror` of MP4 and master: exit 0.
- Source intervals (`review.py edl`): 27/27 take intervals inside their takes and evidence stills present;
  the round-0 wall fades out by b16, before its shortest take (legal, 420 frames) ends, so no source
  frame is held.
- Pixels (`review.py pixels` on the master): 21/21 sampled panes exact integer nearest-neighbour copies of
  their sources (2x wall cells of both eras, 4x Mod manager, legal notice and Time Attack panes, 3x
  evidence panes and the delivered Settings frame, the annotated review picture 1:1).
- Pixel identity of labels (`identity.py`): see `provenance/source-map.json` `pixel_identity`.
- Motion (`review.py motion` on the MP4): no frozen runs (>= 20 identical frames); consecutive-frame strips
  at all 18 transitions and score events in `review/strips-{a,b,c}.png`.
- Sound (AAC, ebur128): integrated -14.6 LUFS, true peak -1.5 dBTP (AAC gain -0.7 dB). Chapters -16.0 to
  -14.8 LUFS except the two milestones on the music's TURN sections: All 27 at 8 -12.6, 27 / 27 -11.5 LUFS
  (the bed alone is +2.7 LU there). L/R within 0.38 dB in every chapter; digital silence after the bed cut.
- Stingers against the bed (loudest 100 ms): Blip -7.7 to +11.3 dB, Swish -6.8 to -6.1, Beep -5.6 to +4.8,
  Tally End +1.5 to +3.3, Spindash +3.3, Giant Ring +3.0, UI tones +7.0 to +10.5 dB; all centred;
  `edit.py check` has no warnings (6 shots, mean 7.2 s; the board changes every bar inside them).

Limits: sound was checked by measurement only; nobody listened to the mix. Motion was reviewed through
consecutive-frame strips, contact sheets and per-frame measurements, not by real-time viewing. Several
proof beats are the review's still captures rather than moving footage, because no moving captures of
those intermediate passes exist; they are labelled as captures. Time Attack's earlier key hint (A: OPEN)
was never pictured, so only the fixed TAB: DETAILS cap is shown. The user's acceptance is not recorded here.

## Archive payload

`archive-payload/` (built by `sources/archive/make_revision_payload.py`) holds the additive
OpenGGF-Media payload for project `menu-evolution`: this revision's text sources under
`projects/menu-evolution/production/revisions/hill-climb-story/`, the updated project index, its external
asset index and catalog fragments (sources, assets, one new external root for the evidence stills, the
project row and the README table row). Film, master, evidence stills and review images stay external and
are hashed; the music bed is the Super Sonic cut's, already catalogued.
