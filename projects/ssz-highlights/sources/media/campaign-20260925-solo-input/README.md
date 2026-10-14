# SSZ solo input exploration — 2026-09-25

Runtime33a5b0e21; no engine edits. Cold SSZ1 ordinary Sonic alone,320,donor off.
Reusing full team movie died13086; no solo completion inferred. GHZ controller
(target boss+16, normal jumps) after4400-input prefix produced sonic-ghz001,
5179 inputs, all8 hits and boss escape, ending511/2156 with0 rings.
Controller source target/SszSoloFightProbe.java (copy of existing SszFightProbe,
only class name and sidekick empty string changed). No gameplay writes.

middle001–003 mistakenly spliced at5400/5397 from an older first-replica capture.
The *current complete* canonical script's jump is5151–5180. These inputs never
jumped onto the first pad, eventually died; rejected. Always align CSV to the
exact source movie, not an earlier capture with similar name.

middle004 = ghz0015179 +100neutral +current team5151..8809,8938 total.
The first pad works, reaches first receiving platform. Subsequent team inputs
match near-exact positions until the jump atcurrent7205 (team7077): solo2px
behind misses the ledge around3370/1447 and falls onto lower route; dies7483.
sonic-mtz004.csv preserves the failed fresh attempt; do not certify it.
branch001 starts7205 and delays that jump1/2/4 inputs; all miss (lower apex).
branch002 starts7199 and tries jumps0/2/4inputs later; currently running.
Production GameplayInputBranchTool restores full registry/input history; these
branches are exploratory, successful route still needs fresh replay and tests.

Continuation: branch002 early jump is ignored while grabbing the swinging carrier;
player stays attached and makes a full loop. Branch003 frombranch002v0prefix7339
jumps on its upper/rightward swing; all3 variants reach3893/1388. Preferredv0.
Splice its7800prefix withcurrent team7327..8809 ->middle005/mtz005, but timing
differences miss upper platforms and settle5045/1196 (noMTZboss). Auto-hop probe
upper001 from7920also stalls there. Branch004 startsmtz005prefix7970 at4106/1196:
v2 (20R;30R+A;450R) lands on the next elevator at4416/1100 (25rings), alive.
Branch005 startsbranch004v2prefix8220 and jumps right off that bar; currentlyrunning.
No solo SSZ completion/rewind claim yet; only GHZdefeat plus physicalrouteprogress.

Further continuation (runtimeunchanged): branch005/006 jump fromrotating post
4416/1100 lacks horizontal speed to reach nextcloud; both falllower. Branch007
startedtooearly at8420 (4294/1164, not the end4513/1164), rejected. Branch008 uses
branch004v0 full8450prefix: variant1 waits8R then30R+A,500R and reaches5157/1004
at8626. Middle006 splices its8690prefix withteam7912..8809. MTZ006 controller
starts9588too late anddies9665. MTZ007 starts8900,boss+16 target,4hits thendeath9611.
MTZ008 targetbossX clearsbut0rings; MTZ009 targetbossX-16clearsall8andretains28rings.
MTZ00911200 inputs independently capturedwith20-fieldmatch,38.333s videoverified.
Canonicalreplicasresource andnew42-windowTestSszSoloColdRouteCapture uncommitted;
queuedMaven session59231 (logtarget/ssz-solo-replicas-test.log), behindbroad/Tails.

Upper002 =MTZ00911200 +team10000..14329,15530. FallsbeforeMecha at13774. Source
clouds shareS3kGradualSwing($8000,$100),period514frames; currentroutephaseoffset
1200, so342neutralatMTZpadmakes1542=3periods. Upper003 inserts342at11200; matching
cloudphase reachesoriginalupperwrap but4pxposition difference breaks laterjump.
Mecha002 thereforestalls4277/300; rejectedbeyondprefix13542. Left001 andbranches
009/010 earlierleft-hop alternatives failtocatchuppercloud; don'tuse them.

Climb001 replaysupper003prefix13542 (3088/4076), then existingwaypointcontroller
withTailsremoved, reaches3808/3840at13911,13912inputs. Right001 autoRhop from13912
reaches5284/3695at14483,14484inputs. Pad001 target5376reachesupperreceivingfloor
throughactualteleport,14885inputs. Upper004 =pad001 +team13580..14569,15875.
Final-pad001 target6720from15875crossesactualfinalteleport,16276inputs. Mecha003
nowrunning from16276usingSszSoloMechaFightProbe; readlog/outputbeforeclaiming.

Campaign broadsession94461stilllive; Tails84-windowtestsession60263queued; newSSZ
42-windowtestsession59231queued. No engine changes fromthese routeauthors.


Continuation through the final arena (2026-09-25):
- Climb001 cleared all five waypoints and ended at3808/3840,13912 inputs.
- Right001 continued with ordinary right/jump inputs to5284/3695,14484 inputs.
- Pad001 centred on5376 and completed that transporter,14885 inputs.
- Upper004 appends the current team movie's13580..14569 input span to Pad001,
  producing15875 inputs. Final-pad001 then approaches6720 and jumps onto the
  final transporter;16276 inputs,3 rings, alive in the actual Mecha arena.
- Mecha003 uses the previous team controller without a follower: dies16891,
  boss5HP. Offsets -32/+32 (004/005) also fail. Safe retreat006 dies17284 at5HP.
  Ring recovery007 and inward-side008 reach5HP but die during attack forms.
- Native source confirmed: loc_7C9C8 refreshes the separate collision child,
  checks ONLY parent status bit7 (defeat), then registers collision. Hit-flash
  bit6 does not suppress that hurt box. sub_7D260 reads byte_7D280 indexed by
  mapping frame. Runtime already matches this; no change is justified.
- Face009/close-face010 try the side opposite the secondary hurt box and only
  ground-level attacks, but still fail. Centre011 avoids chasing airborne
  attacks; no damage before failure. Anticipate012 additionally jumps during
  routine14's ground-dash wind-up; currently running, session90964. Its source
  is target/SszSoloMechaAnticipateProbe.java; read outputs before using it.
All these are controller-only attempts, not parity evidence or runtime fixes.

The replica capture is independently verified:11200 rows match20 state fields,
2300 video frames at60fps, full decode passed, no deaths. It is preserved as
src/test/resources/routes/s3k/ssz1-sonic-solo-cold-replicas-320.* plus the new
42-window TestSszSoloColdRouteCapture (uncommitted, focused test queued59231).
Tails ending84-window test remains queued60263. Broad session94461 is still
running from33a5b0e21; diagnostics target/category-tests/20260925T134954Z-1ed239af.
Do not restart the live run or count the later new tests as part of its compiled
selection. No integration or push has occurred.

## Authoritative continuation, 2026-09-25 15:52

All sessions described as running/queued above are now terminal. Anticipate012
and ground-avoid013 failed. Mecha014 used temporary
`target/SszSoloMechaLookaheadProbe.java` (package com.openggf.tools): twelve
180-input snapshot-forked policies, commit 30 inputs at a time. It defeated Mecha
without death; intentionally stopped at 18,286 before load-boundary trials.
The initial serializer omitted inherited B/C buttons, so complete001 failed
before the first boss; complete002 restores the exact original prefix buttons
and appends 3,000 neutral inputs. No runtime changes.
Fresh capture `campaign-20260925-sonic-solo-clear-320-v2` matches all 18,286
author rows on 20 state fields, no deaths, actual DEZ load at 19,844.
Canonical full route stops at that load (19,845 inputs). Both solo tests pass:
42 replica replay windows plus 41 additional upper/final windows and actual
history isolation, 2 tests, 0 failures/errors/skips, 42.345s Maven.
Committed locally as 17c191094. Previous Tails ending and SSZ replica tests
committed as 15d712413. Campaign ordinary lane passed 23,846 tests with 29 skips;
separate guards passed 672 with no skips. Integration/push remain open.
The useful lookahead author is still temporary; promotion must preserve all
buttons and stop trials before any level replacement. Do not re-run old probes
or treat these controller choices as native parity evidence.
