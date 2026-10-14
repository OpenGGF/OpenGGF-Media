# Knuckles cold Lava Reef route authoring

2026-09-25, begins on6e54f338a. The first native-controller slice uses full movie offset387121,3337inputs (trace lrz); native state is comparison/navigation only, never injected. Fresh cold Knuckles entry gives16/1965 matching the native start. First probe dies1330 after diverging at the early rock descent; input/phase differences need investigation before any defect claim. Existing Knuckles strict trace exclusions remain accepted. Goal is native320 solo cold Act1→Act2→directHPZ, without seeds.

native-first-3337.bk2 preserves only original Header and the input slice; no save state or other movie entries. GameplayInputBranchTool uses that slice from frame0 with ordinary cold boot.

Branch001 from native slice prefix500:300neutral then300R lets the crusher drop, but walking right misses the lower bridge and dies;600R alone remains high and stalls1653/2093. Correct branch005 starts001v0 prefix781 with50neutral, then30L+A;1L;100L+A;30neutral. It waits to LAND on bridge1358/2349 before jumping/gliding left, breaks the RING monitor972/2347, and ends991x963/y2326 gripping left wall,13rings,zero deaths. Branch003 jumped too early and gripped the upper wall;004 descending cannot pass the ledge. Branch002 turned left during the drop, missing the bridge. Branch006 walks in lava and dies. Branch007 leaves wall too low;008 climbs then holds first jump30frames, hits low ceiling/drops before glide and losesrings. Branch009 tries earlier glide after wall-jump (1RA1R110RA), from005v1prefix992 after60/90U. No engine defect established; no native state hydration. Latest verified canonical campaign remains Tails68977,6e54f338a.

Branch009v0 solves low ceiling: from005v1prefix992,60U;1RA;1R;110RA;25L;60neutral reaches1502/2348,13rings,zero deaths at1248. Immediate second jump/glide is essential;30-frame first jump hits the ceiling and falls too far before glide. Branch010v0 from009v0prefix1249 uses25RA;1R;100RA;20L;60neutral, safely lands2008/2344,17rings at1454. Longer010v1overshoots into lava. Branch011 repeats next rightward jump/glide from010v0prefix1455. No production changes; these are controller authoring results pending fresh replay/rewind certification. Task clean6e54f338a; no integration/push.

Branch011v0 lands2446/2327,17rings at1660. Walking under the timed crusher (012) gets crushed;013v0 uses1R5D2x(1DA3D)400R and clears it,ending2636/2353,17rings at2074. 014v0 jump/glide crosses the next enemies but loses some rings,ending3637/2480,5rings at2425. Immediatejump015 hits the swinging spike;016v0 waits90 then25RA1R100RA200R,passes unhurt to4033/2481 at2841. 017v0 uses25RA1R80RA200U200R, descends to4778/2864,8rings at3347. Plainwalk018stalls. 019v0 jump/glide reaches5493/2989,8rings at3823. 020v0 jump/glide grips the stair at5557/2925,8rings at4299;021 is trying Up/climb and further jumps. This is authoring only, not yet independent cold replay or rewind certification. Tails full chain remains committed6e54f338a.

021v1 climbs from020 grip with40U andjump/glide but drifts under next crusher anddies. Keepprefix4391 (5698/2831);022v0 20L30neutral1R5D2x(1DA3D)500R lands before it at5710/2865,8rings. 023v0 shortjump1RA30R then attemptedcharge while stillmoving; keepprefix5051 at5765/2861 stopped againstcrusher. 024v1 5D6x(1DA3D)40D500R catches opening, clears to6069/2864,8rings at5619. 025v0 jump/glide grips6133/2800;02640Ujump/glide180U400R climbs to6261/2668 at6841;027 climbs nextstep, useprefix7178 at6357/2572 rather than full stall tail. 02825RA1R100RA180U300R clears bigdoor/descent and ends7127/2800,11rings at7783. This is door13,button6984/2801: glide skipped it. 029jump fails atdoor. 030150L waits too long undernearbycrusher andfallsback; rejected. 031v1 65L500R pressesbutton and returns beforecrusher, opensdoor and ends7245/2801,14rings at8348. 032 continuesjump/glide/climb from031v1prefix8349. No runtime defects established. All authoring remains pending fresh/cold replay and rewind certification.

## Cloud escape and corrected continuation (2026-09-25, f3b0bb291)

Branches033–038 are diagnostics.033 full jump hits the low ceiling/spikes and dies9479;034 run-up alternatives unused.035v0 from032v0prefix9045 (`14A;1-;100RA;150U;300R`) early-glides over first spikes, ends9609 at8229/2845,1ring.036v0 from035v0prefix9610 (`repeat3{14A;1-;100RA;150R}`) advances then attaches Toxomister cloud; first grounded9937 at8516/2772.037 tries jumping off cloud, fails because cloud follows.038 waits before second spike jump; outcomes unused.

039 from036v0prefix9938:
- v0 `5D;repeat2{1DA;3D};4R;14RA;1R;100RA;200U;300R`: true spindash9943–9950, but before fix anim34 remains forced and cloud kills10038.
- v1 `repeat8{1L;1R};14A;1-;100RA;200U;300R`: shakes free; survives10569inputs to8613/2749,1ring. Do not substitute this workaround for fixing spindash.

f3b0bb291 fixes one-shot glide landing animation ownership (native22/23); loc8FE50 unchanged. Production regression both landing paths/gravity directions and rewind;248+140 focused and33guard tests pass,zero skips. Fresh original039v0 cold playback now anim8 at9942,9 at9943, attached cloud removed9943;10560frames no deaths ends9847/2796,13rings. Full source log10570inputs. Capture ../campaign-20260925-knuckles-cloud-spindash-320 contains9900–10559,660frames60fps11s,verifieddecode/stills. No gameplay writes.

Post-fix authoring:
- 040v1 from039v0prefix10560: `25RA;1R;100RA;200U;350R` ends11235 at10357/2701,13rings;v0 adds200U first, same endpoint later.
- 041v1 from040v1prefix11236: `20L;25LA;1L;100LA;300U;350R` ends12031 at10429/2636,13rings. v0rightjump reaches same but loses allrings.
- 042v0 from041v1prefix12032: `25RA;1R;100RA;600U;350R` ends13107 at10429/2506,13rings,still gripping right wall below ceiling. v1U1000 same endpoint400frameslater.
- 043 launched from042v0prefix13108: left wall jump with immediate re-glide,100/180LA then700U100R; inspect outcomes next.

Knuckles cold Act1 completion is still open. All authoring is controller-only cold LRZ1,320,solo,donoroff. Canonical fixture and complete-route replay spots not yet committed. Shared movement change combined campaign broad/integration validation still owed; task branch local only.

Further climb authoring:
- 043v0 reaches9994/2541 by13208 and stalls duringUp; finalR walks back down. Keepprefix13220.
- 044v1 from043v0prefix13220: `25LA;1L;100LA;350U;150L` reaches9610/2477,13rings at13845. v0A14does not climb.
- 045v0 from044v1prefix13846: `25LA;1L;100LA;350U;150L` reaches9539/2314 gripping left wall below ceiling,13rings at14471. THIS IS THE GOOD CHAIN. v1A14losesrings, ends14460 at9538/2412,4rings.
- 046 mistakenly continues045v1; three repeated left hops/climbs die14701, unused.
- 047 fromGOOD045v0prefix14472, right wall jump with early/late glide and400U150R; inspect next.
- 047v0 ends15123 at10261/2319,13rings,0deaths;v1sameendpoint19frameslater. Useful new frontier, input15124.
- 048 from047v0prefix15124, `25RA;1R;100RA;400U;200R` /A14variant. Both remain near10200/2320; inspect CSV/stills before selecting. Do not assume repeated right-hop is correct: current grip/ceiling makes it jump left.

At checkpoint between goal turns: runtime fix committed f3b0bb291, taskworktree clean; no main integration/push. All jobs terminal. Continue Knuckles route from047v0prefix15124 or examine048frames. Full campaign remains active.

## Upper passage and miniboss approach (continuation after f3b0bb291)

- 049v0 from047v0prefix15124: wait45 then25RA1R100RA150U120R reachesrightwall10325/2254 beforefireballhits15230. Keep prefix15211. v1wait90fails;v2wait135dies.
- 050v0 from049v0prefix15211:50U1LA1L100LA150U200L reaches10058/2224,13rings at15712. Othersunused.
- 051v0 from050v0prefix15713:25LA1L100LA100U200L reaches9930/2160,1ring at16138. Otherwaitvariantsnotbetter.
- 052v0 from051v0prefix16139:25LA1L80LA100L300neutral reaches9819/2098,1ring at16644. Springimmediatelyleft.
- 053v1 from052v0prefix16645:12LA120neutral100R lands onredspring,thenupperledge9817/1648,1ring at16876. v0A20/v2A30overshoot spring.054 triesearlierR duringascent,fallsintoflyingbadnikanddies;055Aduringascentcannotenableglidefromspring andalsodies. Native lrz_2 rows2860–2990 show an enemy bounce during this arc; use onlygeometry, not as proofordinaryKnuxmustbounce (native powered roster differs).
- 056v0 from053v1prefix16877:25RA1R100RA150U300R usesjumpfromlowerledge, reaches10037/1580,1ring at17452. v1wait45dies.
- 057v0 from056v0prefix17453:25RA1R100RA150U300R reaches10371/1517,1ring at18028. v1A14cloudkills17904.
- 058v0 from057v0prefix18029:5D3x(1DA3D)500R clearsrock/lavafall to10641/1581,1ring at18545. v1jumplongersameendpoint.
- 059v0 from058v0prefix18546:25RA1R100RA150U400R gripsrightwall10813/1483,1ring at19221. v1shortjumpchargeslosesring/stalls.
- 060v1 from059v0prefix19222:100L5D3x(1DA3D)250L dropsleftunderlowpassage, ends10122/1817,4rings at19588. v0wait200Lsame100frameslater.
- 061 from060v1prefix19589 earlyjumps35R/25R producecloud/ringloss orwrongupperledge.062v2 fromsameprefix:65R5RA450R killsToxomisterandendsdoor11 at10613/1884,7rings at20108. v1R55also6rings;v0spindashfails.
- 063v0 from062v2prefix20109:55L30LA25R30RA350R pressesdoorbutton10491/1820 andentersboss. KEEP PREFIX20410 at11362/1969,10rings. RemainingR waitsatrightextremityandlosesrings. v1L45missesbutton.

Controller-only temporary author target/KnucklesLrzFightAuthor.java adapted existingTailsauthor toKnuckles; compiledtarget/knux-author-classes tosharepackagewithprefixScript. Source-launch initiallyfailedIllegalAccessbeforeboot,noevidencefromthatfailedattempt. fight01 from063v0prefix20410,aim11420,handchasing; health6→5 at21356, then death22502with0rings. fight02 disableshandchasing,aimscentreexceptdrilldodges; outcome pending. No gameplaywrites ortracehydration.

Milestone9890bcd70: canonical cold miniboss arrival saved as lrz-knuckles-cold-miniboss-320.script/bk2,20410inputs,byte-identical controller rows to063v0prefix. TestLrzKnucklesColdRouteCapture passes70 immediate full-registry restore +45-input replay spots,1test0failure/error/skip,17.57stest39.085sMaven. Real cloudattachment9937 andspindashrelease9943 asserted. Independent fresh capture all20410rows matches12fields0differences/deaths; final11362/1969,10rings,highpriority,liveboss. Arrivalvideo821frames60fps13.683s19589–20409,fullffmpegdecode andstill20409inspected. Docs/matrix/backlogupdated. Selectionagainstf3b0bb2912918classesassetfallback; proportionate test/input-only focused fullnewroute verification, notfullsuite. Sourcef3b0bb291 sharedmovementfixstillrequirescombinedcampaignbroad/integrationverification. Worktreeclean9890bcd70,nomainmerge/push.

Fight outcomes (all controller-only, NO engine bug established):
- 01 handchasingfulljump22: health6→5 at21356,death22502.
- 02 centre11420fulljump22without handchase:death21638.
- 03 adds live lost-ring recovery to02: firsthurt20751,recoversring20835; hits5at21301,4at21348,loseslast ring21649; health3at22204;death22457. Best attempt. Fullinputs/state.csv in ../campaign-20260925-knuckles-fight03. Possible continuation prefix21400 preserves two hits andone ring.
- 04 projectile-proximity jumps insteadofcontinuous; nohits,death22117(dropdodge too slowfromground).
- 05 patrolleft/rightduringhandphase;death21547.
- 06 leftcornerwithoutjumpduringhandphase; handcollisionlosesrings,death20925.
- 07 jumpheld16 vs22isidenticaltrajectory (fulljumpcutoffalreadyearlier),same03death22457.
- 08 jumpheld5:death22464.
- 09 base03target11360:death20906.
- 10 base03target11490:death21655.

Temporary current source target/KnucklesLrzFightAuthor.java resetto03base, compiledtarget/knux-author-classes. Copies -fight03,-fight04,-fight05,-fight07 preserve diagnostics. Search/record inputs only; controller positions/timers are readlive; outputs always replayfromcoldboot. The author needs a better way to avoid handshot volleys, rather than more static offsets. A bounded future-input search using full-registry engine snapshots (like GameplayInputBranchTool) is a possible next step: predict several controller patterns90frames, restore, commit only first20inputs, penalizehurt/death andpreferbossdamage/ringretention. This is NOT implemented yet. No native state hydration or runtimebossedits justified. All tooljobs terminal at this checkpoint.

## Act1 completion milestone6bff013cc

Temporary target/KnucklesLrzFightSearch.java searches15 target/jump policies90frames withengine-owned snapshots, checks fullsnapshotimmediaterestore,commits20inputs. No gameplaywrites except restoringstatesactuallyreached fromcoldinput; no native rowsused. search01incomplete logicalJump maskstoppedanddiscarded. search02(correctmask) fromfight03prefix21400 avoidsvolley,retains1ringandhits3at22185,2at23052; thenmissesbecauselandingouteredge/jumpingbeforecentre. Fresh non-search replay to25000matchesHPs andring,confirmingmissesnotsearch-specific. Detailprobe24690–24860 showslivecollision6,invulnerabilityfalse,playerlandsoutsidehittablecentre. search03 fromsearch02prefix23100 waitsforcentrebutcannotwalkthroughdrill'ssolidside. search04 fromsearch03prefix23780 allowsjumpontopfromfloor,centreswhileonobjectbeforeattacking. Fifthhit23907,sixth24777,actualAct2load25112,script25113inputs. search02/03stoppedintentionallyforpolicychanges;allotherjobs terminal. Noenginefixforthisfight.

Canonical lrz-knuckles-cold-act1-clear-320.script/bk2: prefix25113 +650Right,25763inputs. Coldnative320,soloKnuckles,donoroff,noposition/ring/shield/emeraldseed. 6hits21301,21348,22185,23052,23907,24777; no deaths;load25112x11560→296ring1;Act2titleresetsrings;final430/1969ring0controlsreleased.
NewTestLrzKnucklesColdRouteCapture.coldKnucklesClearsMinibossAndRestoresFightAndActTwoHandoff passes37full-registryimmediaterestore+45inputreplayspots,0fail/errors/skips,18.75stest40.084sMaven. Earlier70traversalspotsretainednotrerun. Freshcaptureall25113source rowsmatch12fields0diff/deaths;executed25763. Clip ../campaign-20260925-knuckles-act1-clear-320/capture.mp4 frames20410–25762,5353frames60fps89.216667s,decode/defeat24777andAct2end25762stillsverified. Test/input-onlyscope2918classassetfallbackplaninspected; focusedcompleteproductionreplay+freshcaptureproportionate. Sharedruntimef3b0bb291andcampaignintegrationbroadverificationstillowed.

Act2 continuation:
- 064v0 fromcanonical25763:400R ends26162 at2357/1980,0rings. v1jumpsequenceends1863/1980later.
- 065v1 from064v0prefix26163:25RA1R100RA150U200R reaches2741/1900,3rings at26638. v0plainRstalls2357.
- 066fromsameprefixU160500Rstalls;U80jumpvariantdies26250. Do not use; prior screenshot lookedlikegripbutUpalonecannotadvance.
- 067 fromGOOD065v1prefix26639 at2741/1900:500R or25RA1R100RA150U300R; outcomes pending. Inspectprefixobjectsforverticaldoor/possiblebutton.
Taskclean6bff013cc,nomainintegration/push. KnucklesAct2→directHPZ iscurrentmandatoryroute; ordinarybossactdoesnotapply. Fullgoalallsevenlevelsstillactive.

Act2 further:
- 067 bothcandidatesstallat2741/1900door1. Prefixobjects showhorizontalbutton2744/1838,door2768/1888. Jumpingdirectlyunderbuttoniswrong; mustbackupleftandapproachside.
- 068v0 from065v1prefix26639:35L35RA1R80RA300R opensdoor, butwalksintoorbitingspikesanddies27073. KEEP prefix26851 at2815/1900,3rings. v1L50missesbutton.
- 069v0 from068v0prefix26851:25RA1R100RA200R advancesacrossspikeballfloor,losesrings,ends27176at3253/1916,0rings,alive. v1A30/glide130sameendpointlater.
- 070v1 from069v0prefix27177:25RA1R100RA150U300R clearsledge,ends27752at3509/1836,alive. Prefixobjects aremovingplatforms andinvisibleblocks,notunimplementedbreakablewall. v0spindashalternativeunused. InspectCSVforrings andcontinuefromv1prefix27753.
Atendofgoalturn taskclean6bff013cc;alljobs terminal;alllevelgoalremainsactive. No main merge/push.

## Act 2 tube section, continued 2026-09-25

- 071v1 from 070v1 prefix 27753: `25 R+A;400 R` reaches 4245/1868 at 28177.
- 072v1 from 071v1 prefix 28178: jump/glide sequence reaches the next step, 4277/1836 at 28753.
- 073v0 from 072v1 prefix 28754 enters the upper tube and exits at 4472/2284; continuing Right returns through the same tube. Its held glide input loses exit momentum.
- 074/075: walking left or jumping left from that stopped exit lacks the speed to traverse the curved wall. 076 spindash attempt launched right and returned to the upper route; 077/078 did not advance the frontier. These are rejected input attempts, not engine fixes.
- 079v1 from 072v1 prefix 28754: `25 R+A;80 R;500 -`. Releasing directional input before the tube exit preserves enough momentum to traverse the lower curve; at 28964 Knuckles is 3925/2158, matching the native route geometry. Keep prefix 28965. Right held through the exit (079v0) brakes the leftward launch and loops back.
- 080 from 079v1 prefix 28965 tries 120 or 160 Left, then 600 Right. Outcomes pending.

The map4000/map4000b captures are explicitly positioned geometry inspection, not cold-route evidence. No engine changes or new completion claims in this slice.

- 080v1 from 079v1 prefix 28965: 160 Left reaches the drop at 3755/2294 (29115); turning right too soon lands on the 3760/2438 spring and returns upward. These are springs, not damage launches (ring count stays 18).
- 081 variants returned upward or stopped at 4053/2284; not retained.
- 082v1 from 080v1 prefix 29116: `40 L;500 R` drops beside the spring, stopping against its side at 3733/2412, input 29655.
- 083v1 from 082v1 prefix 29656: `25 R+A;600 R` jumps over the spring and reaches the lower passage, 4158/2668 at 30280, 3 rings, alive. The passage has a moving solid platform ahead.
- 084 from 083v1 prefix 30281 tries jump/glide or ordinary jump over that platform. Outcomes pending.

- 084v0 reaches the climb grip at 4277/2607 (30836). 085v1 jumps off and proceeds beneath the moving platform. Keep prefix 31048 at 4690/2684, before the spike-chain collision at 31054. Later death in the discarded tail is not retained.
- 086v1 from 085v1 prefix 31048: `25 R+A;650 R` clears the chain, ends 4821/2604 at 31722 with 3 rings and no deaths, just before a static spike shelf.
- 087 from 086v1 prefix 31723 tries ordinary jump vs jump/glide/climb past the shelf. Outcomes pending.

- 087v1 clears the spike shelf, ending 5173/2668 at 32498, 3 rings. Door2 is controlled by the horizontal button at 5176/2606.
- 088 jumps from directly underneath do not open it. 089v0 from prefix32499 (`35 L;35 R+A;1 R;80 R+A;600 R`) opens it. Keep prefix32661 at5235/2668 with5rings, before the Toxomister contact costs them.
- 090 tries jumping after that contact, but an attached Toxomister cloud prevents ordinary jumping; both discarded tails die. 091 uses normal spindash inputs from32661 to release/avoid the cloud and cross the badniks. Outcomes pending.

## Act2 middle milestone d85754836

- 091v1 from089v0 prefix32661 uses a normal spindash, then jump/glide, reaches5717/2956 at33310 without a death. Rings fall to0 later in the lower chamber.
- 092v1 from091v1 prefix33311 jumps onto the next step. Keep prefix33372 (5805/2924), before the moving solid pushes Knuckles back.
- 093v1 from092v1 prefix33372: `25 R+A;650 R` passes the moving block and enters the long tube at6072/2928. Keep prefix33763,6678/1132,0rings,0deaths, released control. Continuing Right loops back into the same tube.
- Canonical lrz-knuckles-cold-act2-middle-320.script/bk2 is exactly093v1 prefix33763. Test coldKnucklesRestoresActTwoTraversalToTheMiddleCorridor passes48 full-registry immediate restore+45input replay spots;1test0fail/error/skip,22.61s test42.807s Maven. Freshcaptureall33763rowsmatch12fields0differences/deaths/followers. Video3482frames60fps58.033333s covers30281–33762, full decode and32695/33762stills checked. Commitd85754836; taskclean, no main integration/push.
- 094 fromcanonical33763 triesRight jump/glide and loops back through the tube. Rejected.
- 095 fromcanonical33763: leftjump/glide/U variant dies33801 against flame at6650/1085. Ordinary25Left+A300Left ends6666/1132 at34087, alive, but no forward progress. Next: author the upper climb carefully around flame timing; native path navigational reference reaches6965/640 then6734/139, but powered-native damage/speed cannot be assumed for ordinary Knuckles. Start from canonical33763, not discarded095tail.
All tool and Maven jobs terminal at this checkpoint. Goal remains all seven levels; current mandatory KnucklesAct2→directHPZ completion still open.

Upper climb continuation after d85754836:
- 096 from canonical33763 tries100/180/260 neutral before left jump/glide. v2 (260 neutral) safely reaches6602/1068 at34093. Keep prefix34094; its longer idle tail dies34137 to the timed flame. v0/v1 discarded.
- 097v0 from096v2 prefix34094:1R25RA1R60RA200U reaches right wall grip6709/1003 at34154. Keep prefix34155; waiting to start Up until34181 dies34186. Variant1 held jump from previous input without release and is invalid as a jump attempt.
- 098 from097v0 prefix34155 starts Up immediately, trying95 or45frames before left jump/glide and further climb. Outcomes pending. No production changes.

- 098 immediate climb dies34174 to the upper flame; 099/101 vary initial wait but full-height second jump still enters the upper jet. 100 immediate wall-jump left also crosses that jet. These discarded attempts do not indicate an engine defect.
- 102v2 from096v2 prefix34094: `20 R;5 R+A;100 R` makes a shorter jump and lands safely on the lower emitter at6709/1036, input34218. Keep prefix34219. This is a safe waiting point below the upper jet. v1/v3 also survive; v0 with no run-up dies before reaching the emitter.
- 103 from102v2 prefix34219 varies wait0/40/80 before jumping into right-wall climb and then left. Outcomes pending.

- 103v0 (no extra wait) succeeds up the right wall to6709/880, jumps left and lands6602/924, then its next held-A instruction jumps again. Keep prefix34460 at6602/847, while airborne alongside the left wall. Long discarded tail dies34749 after walking into the flame again. v1/v2 timing alternatives fail earlier.
- 104 from103v0 prefix34460 releases/represses jump to grip the left wall, then climbs and tries the upper corridor. Outcomes pending.

- 104 grips6603/855 at34462, but waiting40frames before Up is fatal. 105 startingUpimmediately also dies at34484/833 to the next jet.
- Safe ledge below this climb is103v0 prefix34426,6602/924,grounded, jump released. 106 tries30/60/90/120/150neutral there, then25LA1L2LA100U25RA1R100RA100U300R. Outcomes pending.

- 106v4 (150 neutral) completes the flame climb and lands in the upper corridor. End35229:6837/812,1earnedring,alive. Shorter waits die during the left-wall jump/climb; no runtime fix indicated. Keep prefix35230.
- 107 tries jump/glide/climb vs ordinary jump from that step. Outcomes pending.

- 107v1 ordinary jump reaches6901/748 at35754. Keep prefix35755.
- 108v0 jump/glide reaches6965/680, then the flame costs the earned ring during the climb. It lands alive at6965/684 by35930. Keep prefix35931; idle tail dies36042.
- 109 from108v0 prefix35931 immediately jumps/grips/climbs, then tries left wall-jump at two heights. Outcomes pending.

- 109v1 (130Up) reaches right-wall top6965/522, jumps left and grips the ledge at6858/522 at36141, collecting3rings. Keep prefix36142. v0 shorterUp falls back down, and v1 longtail eventuallyfalls/dies; neither tail is retained.
- 110 from109v1 prefix36142 climbs onto that ledge and travels left toward the next shaft. Outcomes pending.

- 110v0 climbs onto6846/492 and walks left to6794/492 at36352. Keep prefix36353. Later Right falls back down.
- 111v1 (`25 L+A;500 L`) reaches6730/428 at36877,3rings,alive. Keep prefix36878.
- 112 from111v1 prefix36878 jumps/grips the left wall and climbs toward the top door corridor. Outcomes pending.

- 112's climb is interrupted by the moving solid near6755/344: X changes6731→6728, then the native stored-X wall-grip check releases Knuckles. No runtime fix indicated.
- 113 waits before the climb; v0–v4 all clear it. Chosen v1 (80neutral) climbs to the upper corridor, ending6538/236 at37546 with2rings. Keep prefix37547. v5(240neutral) misses the opening.
- 114 tries left jump/glide/climb then Right, or rightward jump/glide, from that upper checkpoint ledge. Outcomes pending.

- 114v0 climbs left to grip6475/138 at38402. Keep prefix38403.
- 115v0 jumps right across the checkpoint; a jet costs rings and knocks Knuckles back, but he survives on the lower top ledge. Keep prefix38584 at6731/236 (before walking off the moving-platform gap). Upperdoor4 at6896/160 is controlled by horizontalbutton6840/244 below the main passage. Long tails fall back down.
- 116 from115v0 prefix38584 tries two brake/drop timings toward the moving platform below the button, plus directjump/glide. Outcomes pending.

- 116v0 actually lands safely on the moving platform at6804/292 (38614),4rings. Its later full jump rises into the upper flame and knocks Knuckles back; use prefix38615. v1 misses that platform and falls to492; 117's right-wall climb from there is killed by the hurt-block/moving-solid section and is discarded.
- 118 from116v0 prefix38615 tries5R5RA160R,15R5RA160R,5R10RA160R to pressbutton4 with a short hop under the jet. Outcomes pending.

- 118v1 from116v0 prefix38615 (`15 R;5 R+A;160 R`) pressesbutton4. Keep prefix38646 at6824/243,4rings. The following119 prefix-object inventory confirms door4 has begun moving:6896/156 instead of160.
- 119v0 from118v1 prefix38646 (`1 L;40 L+A;150 U;25 R+A;1 R;120 R+A;500 R`) retreats to the left ledge, jumps across the opened door and reaches the east side. Keep prefix39037 at7114/172,0rings; the discarded tail is slowed by cloud and dies39187.
- 120 from119v0 prefix39037 tries spindash or jump/glide across that cloud corridor. Outcomes pending.

- 120 down while still moving rolls instead of charging; discarded. 121v0 brakes6Left,1Right,20Down then charges3taps and releasesRight. This clears the cloud corridor and collects3rings, but the long tail rebounds near7580 and returns into clouds. Keep prefix39121 at7482/241,rolling at~2600ground speed. v1/v2 over-brake, face left and launch backwards.
- 122 from121v0 prefix39121 jumps over the rebound/step, with and without subsequentglide. Outcomes pending.

## Upper-route milestone dd3db3d61

- 122v1 from121v0 prefix39121 (`25 R+A;900 R`) clears the rebound and reaches8501/236 at40045,0rings,0deaths. Canonical lrz-knuckles-cold-act2-upper-320.script/bk2 is this complete40046-input route.
- Test coldKnucklesRestoresActTwoUpperClimbsAndDoorRelease passes53 full-registry immediate restore+45input replay spots,1test0fail/error/skip,41.64s test1:07 Maven. Existing107 Act1+48 Act2 spots retained,208total. Freshcaptureall40046rowsmatch12fields0differences/deaths/followers. Video6283frames60fps104.716667s covers33763–40045; full decode and34339/38916/40045stills checked. Source script was regenerated through the input author/loader round trip.
- Commit dd3db3d61, taskclean, no main integration or push. Test/input-only selection2918classes inspected; proportionate focused validation; combinedcampaignbroadverification stillowed.
- 123 directjump variants cannot pressbutton9 from underneath.
- 124v0 fromcanonical40046: `35 L;35 R+A;1 R;80 R+A;900 R` opensdoor9 and reaches8693/236 at41096,alive. KEEP prefix41097 from branch124/variant-0.bk2 for continuation. v1(30Left) drops to8565/492; discard. This extension is authoring evidence only, not yet independently captured or rewind-certified.
Next: jump/climb the step at8693 and continue east to Knuckles' directHPZ exit atx16352. Fullall-levelgoalremainsactive. No tool/Maven job remains active at this checkpoint.

Eastern continuation after dd3db3d61:
- 125 immediatejumpfrom124v0 prefix41097 dies41105 in the flame at8648/175.
- 126v0 waits40neutral then jumps/glides onto right-wall grip8757/170. Keep prefix41176; the unnecessarily long held-glide tail waits there until the flame kills at41237. Other initialwaits do not improve this.
- 127 from126v0 prefix41176 startsUpimmediately, then tries normalRight orjump/glideeast. Outcomes pending.

- 127v1 starts60Up then25RA1R100RA800R; it climbs onto8768/140, jumps east and enters the next tube, reaching the lower passage. Keep prefix41366 at9747/556,0rings,grounded after glide landing. Idle/run tail dies41402 under the downward flame jet. v0 waits too long on8768/140 and dies41244.
- 128 from127v1 prefix41366 tries short or longer spindash charge, plusjump/glide, to leave the landing safely. Outcomes pending.

- 128v1 (`1 D;1 D+A;700 R`) escapes the jet, collects8rings and reaches the paired curved-tube floor at10171/544 at42067,alive. Keep prefix42068. Longer charge dies before release; jump enters the jet.
- 129 from128v1 prefix42068 tries chargedspindash through the curve or jump/glide/climb. Outcomes pending.

- 129v0 charges through the paired curves and reaches10581/492 at42906,alive. Keep prefix42907. v1 jump/glide loses curve momentum.
- 130 tries jump/glide or ordinary jump past the next upward flame nozzle. Outcomes pending.

- 130 immediate jumps hit the active upward nozzle and return to10581/492 (survive with1ring). Reject tails. 131 varies40/80/120/160neutral before25RA700R from129v0 prefix42907. Outcomes pending.

- 131v1 (80neutral) crosses the upward jet and collects rings, ends10685/492 at43711 with11rings,alive. Keep prefix43712. Next obstacle is the moving solid block, not another nozzle.
- 132 from131v1 prefix43712 tries jump/glide/climb or ordinaryjump over it. Outcomes pending.

- 132v1 ordinaryjump passes the movingblock, but continuedRight cycles through an end-of-platform launch back to10964/492. Keep prefix43885 at11071/492,11rings,grounded, before the drop/launch trigger. Its longer tail collects21rings but does not advance. v0 dies in the movingblock/jet area.
- 133 from132v1 prefix43885 jumps across the drop, trying sustainedglide orordinaryjump. Outcomes pending.

- 133v0 reaches right-wall grip11189/416; 134 confirms the wall is capped near394 and cannot be climbed into an eastward exit. Discard both longtails. The placed return launcher is spring11184/574.
- 135 returns to132v1 prefix43885 (11071/492,11rings), brakesLeft to drop short of that spring and attempts the lower westward passage seen in native navigation. Outcomes pending.

- 135v0 (`250 L;800 R`) successfully brakes before the spring, follows the lower curve west to10442/791, then heads east beneath the upperfloor to11045/940 at44934,15rings,alive. Keep prefix44935.
- 136 tries ordinaryjump vs jump/glide over the lower upward flame nozzles. Outcomes pending.

- 136v0 jump/glide crosses the lower nozzles, reaches11325/926 at46160 with18rings,alive. Keep prefix46161. Slowmovement here is the next curved tube slope, not a cloud.
- 137 charges spindash through that curve or tries jump/glide/climb. Outcomes pending.

- 137v0 spindash clears the lower curve and climbs to11477/780 at47099,18rings,alive. Keep prefix47100. v1 jump/glide cannot clear the curve.
- 138 attempts the first step in the eastern flame ascent. Outcomes pending.

- 138v1 gets the first step at11509/748 by47160. Use prefix47161 rather than retaining its long idle tail.
- 139 fromthatprefix makes the next jump, with optionalglide/climb. Outcomes pending.

- 139 immediatejump is knocked back to11509/748 by the active jet. 140 varies40/80/120/160neutral before jumping from138v1 prefix47161. Outcomes pending.

- 140v0 (40neutral) passes the stepped jets and proceeds east to12149/620 at47761,0rings,alive. Keep prefix47762. Other waits stop earlier.
- 141 attempts the next steps/climb from12149/620. Outcomes pending.

- 141v0 jumps/glides and climbs to the rightwall's cap at12213/401, input48637,alive. Keep prefix48638. The wall above is spiked; the next route transfer is left across the moving platform. v1 stops on the lowerstep.
- 142 tries leftwall-jump with/without glide toward that platform and leftledge. Outcomes pending.

- 142v0 leftwall-jump/glide reaches11914/492 at49283,alive. Keep prefix49284. v1 ordinaryjump falls back to the lower route and dies in flames.
- 143 attempts the leftsteppedclimb toward11850 and the top corridor. Outcomes pending.

- 143v0 jump/glide/climb clears the leftshaft and reaches12245/204 at50124 with8rings,alive. Keep prefix50125. v1 only reaches11883/460.
- 144 attempts the final upperstep and eastward run. Act2 timer is approaching7minutes; trim successful candidates before long idle tails where feasible to avoid an authored timeout. Outcomes pending.

- 144 immediatejump is knocked off the upperstep into the lower route; discard tails. 145 varies40/80/120/160neutral before the jump from143v0 prefix50125. Outcomes pending.

- 145v1 (80 neutral) clears the upper step and reaches13109/236 at50562,1ring,alive. Keep prefix50563 rather than idle tail. v3 also reaches it later; v0 falls back and v2 stops12581.
- 146 from145v1 prefix50563 tries jump/glide/climb vs ordinaryjump across the next corridor obstacle. Outcomes pending.

- 146 jumps directly below horizontal button10 at13112/174: head stops at208 and cannot reach the button side. Both tails remain13109/236. No runtime change.
- 147 backs away35/25frames then jumps right to contact the button side, as earlier horizontal switches required. Outcomes pending.

- 147v0 opens button10/door and reaches13493/236 at50847,2rings,alive. Keep prefix50848.
- 148v0 crosses the pipes and drops to14517/556 by51462,alive,0rings. Keep prefix51463. v1 also arrives; v2 dies.
- 149 tries jump/glide/climb or repeated ordinary jumps up the eastern stairs. Outcomes pending.

- 149v1 repeated ordinary jumps clear the eastern stairs and reach15285/236 at51813,0rings,alive. Keep prefix51814. Glide/climb stops lower on staircase.
- 150 tries jump/glide or repeated jumps across the final pipe rise toward the directHPZ exit. Outcomes pending.

- 150v1 repeated jumps reaches15797/140 at51961,alive,0rings; keep prefix51962. v0 dies at15609/172. The higher landing is beside a pipe/nozzle; native navigation passes below at y236.
- 151 tests climbing vs backing left and dropping to the lower passage. Outcomes pending.

- 151/152 cannot safely drop backward from nozzle top: immediate/80/120/160-frame waits all die in the leftward flame when dropping. Reject tails.
- 153 instead returns to150v1 prefix51924, before the third repeated jump that caused the high nozzle landing. Try simply running off the preceding ledge, or brief braking then run/spindash. Outcomes pending.

- 153 running off earlier ledge still enters active flame; both die.
- 154v0 (20neutral then30Left/50neutral/Right) drops beneath nozzle in its idle interval, breaks both placed rocks by ordinary Knuckles contact and crosses collapsing bridges. Reaches16085/268 at52180,alive,0rings; keep prefix52181. v7 (220neutral) also succeeds later; others die in flames.
- 155 jumps the final step then runs toward directHPZ. Outcomes pending.

- 155v0 reaches the real directHPZ load at52418 (zone22act1,16/748),0deaths. Canonical cold-hpz route preserves52419 inputs and appends240Right. Fresh full52659 playback matches every source row on12fields,0deaths/followers, ends1075/748,0rings. See ../campaign-20260925-knuckles-cold-hpz-320/README.md.
