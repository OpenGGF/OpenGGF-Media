# DEZ ordinary solo cold authoring, 2026-09-25

Base dfe7baae1, task worktree .worktrees/ai-sk-zone-completion. All probes cold DEZ1, native320, donoroff, main sonic or tails, no sidekick or state seeds. Java21 DISPLAY=:0, GameplayInputBranchTool with /home/farrell/code/projects/OpenGGF/s3k.gen. Prefix/candidates are complete controller inputs and engine-owned restore only; accepted milestones still require independent capture and full-registry tests.

Initial team-input replay: soloSonic dies7666; first position difference from prior team capture7129 on conveyor (ring collection differs earlier). Tails falls into lower start area then timesout36000, no route completion.

Sonic:
-001 source teamending prefix7560, delay8/10/12/16Right then original7560..8999. All cross missedgap. v3 reaches10183/2131 at9015,16rings,alive; keep9016.
-002 v3prefix9016 +original9000..14999 remains turbine room (six-panel timing differs); rejecttail.
-003 v3prefix9016:20cycles30/60/90Up+Down,900Right. v1(60) exitsroom,25rings,ends11125/2124. Keep11641 at upper launcher phase11127/1968. v0staysroom;v2escapesupperleft instead.
-004 from003v1prefix11641 jumpRight orLeft; both reach11445/1708 with33rings. Keepv0prefix11989,first step arrival after launch/return curve.
-005 from004v0prefix11989 ordinaryjump+Right vs repeatedjumps, pending.

Tails:
-001 source teamending prefix480,flightRight with12/20-frame flaps,500Right. v1gets real hangcarrier endpoint1753/1916,12rings;keep1157.
-002/003 attempting flightLeft fromhangcarrier hits ceiling, falls into lowerroute; discardtails. Increasing flapfrequency does not change ceiling obstruction.
-004 from001v1prefix1157:1Left+A,600Left, follows native lower return passage to1593/1968,12rings at1757. Initial invocation used incorrect ROM path and failed before boot; corrected authoritative invocation uses projectroot s3k.gen.
-005 from004v0prefix1758 continueLeft orjumpLeft, pending.

- Sonic005 jumps the step but stops at eastern bumper11797/1708. Wrong direction for progression: native navigation and live placement show launcher11264/1712 sends the player back up-left. Discard005tails;006 returns to004v0prefix11989 and heads250Left then600Right.
- Tails005 continues slowly left against conveyor,2357 at1467/1968 with12rings (v0). 006 tries charged spindash to clear the opposing belt, fromprefix2358.

- Sonic006 enters launcher11264/1712 but Right during flight alters the upper transfer and returns to launcher. Keepprefix12101 at captured launcher, then007 tries500neutral through the scripted launch.
- Tails006 chargedspindash clears opposingbelt to1001/1904,15rings. Keepv0prefix2509. 007 jumpLeft thenRight tries the upperledge; its first malformed argument invocation failed beforeboot and was corrected.

- Sonic007 neutral flight reaches rising platform10442/1260 at12471, then eventual badnik hit12595 if left idle. Keep12541 (10442/1207,36rings) for008 jumpRight or40wait+jumpRight.
- Tails007 jumpLeft strikes monitor underside and returns down the slope. Rejecttail. 008 returns006v0prefix2509 and jumps/fl iesRight toward the upper route. First malformed invocation failed before boot; rerun with a temporary argument-safe wrapper (target/dez_branch.py) to prevent copied ROM/input-order errors.

- Sonic008 immediate jump hits badnik;40wait avoids it but jumps too low to clear upperledge and falls back. Rejecttails.009 tries50/54/60 waits at007v0prefix12541.
- Tails008 rightjump/flight clears upperpassage to2705/1584,0rings at3040. Keepprefix3041.009 jumps the spike edge with/without flight.

- Sonic009 identifies the incoming hazard as the actual torpedo from launcher10552/1137, not a badnik (corrects earlier shorthand). v2lands back on raised stair at12620,10442/1132,alive,0rings. ContinuedRight walks off its edge;010 releasesJump then makes a fresh jump from that raised position.
- Tails009v0 flight clears spikeedge and reaches4021/1584,4rings at3455. Keep3456.010 tries leftward stair climb or direct flight up rightwall.

- Sonic010 jumps from fullyraised stair but from standstill too far left to reach the next platform.011 adds20/30Right runup from009v2prefix12621 before jump.
- Tails010v0 reaches upperleftstair but is hit by a projectile, then lands3792/1456 at3720,alive. Keep3721;011 uses another rightjump/flight from that raised step. v1directrightflight cannotclearwall.

- Sonic011v0 20frame runup+jump succeeds and reaches next launcher11136/940 at13015,2rings. Keep13016.012 takes600neutral to avoid steering the scripted arc.
- Tails011 reaches4021/1328,0rings at4085 after anotherstair flight. Keep4086;012 tries jump orjump/flight onto rightroof.

- Sonic012 neutral preserves launcher chain,ends11959/731 at13615,2rings,alive.013 continues600neutral then600Right.
- Tails012v0 ordinaryjump clears rightroof and reaches5561/1424 at4710,2rings,alive. v1also reaches5524/1424. Preservev0prefix4711 for next continuation; focus Sonic completion first.

- Sonic013 reaches Act1boss14312/812 with7rings,0deaths. Fight author begins fromprefix14350.
- Temporary direct boss controller fight001 dies14751 after2hits. Correcting its missing logicalJump bit in fight002 produces the same death; do not accept001. Ring-chasing variant003 dies14730. No engine changes.
- Bounded forecast author adapted from the earlier KnucklesLRZ tool:15 alternatives,90-step horizon,commit20, full-registry immediate-restore checks, all actual inputs recorded. Search001 remains healthy but nohits through16430; intentionally terminated its confirmed live JVM because the original5000 hurt penalty rejected all useful tradeoffs. Search002 lowers controller scoring's hurt penalty5000→700 and ringlossweight30→5; death penalty remains1,000,000. These are search preferences, not gameplay constants or state writes.
- Tails013 flies too briefly and drops into lowerbumperdeadend6645/1488.014 retains prefix4937 then continues flapping before the drop.

- Search002 lands4first-phasehits but dies15380 after forcing everyzero-ring candidate toward the same lost ring. Search003 resumes acceptedprefix15050 (3hits,1ring), expands horizon90→180 and leaves four candidate targets free while onlycentre policy seeks rings. This changes search options only.
- Tails014 continuing flight reaches upper spring/platform region8245/756 at5856,10rings.015 climbs upperstairs/platform to9589/706 at6682,13rings.016 tries the lower return by backingLeft from015prefix6501 thenrunningRight.

- Search003 succeeds: first phase ends20541, final hit21974, real Act2 load22332, no death. Compressed22333inputprefix +1200neutral independently replays to released320/940. Allprefixrows match12fields; TestDezSoloColdRouteCapture passes61 immediate restore/45replay windows,1pass0skip. No runtime changes.
- Tails016/017 leave too early and remain on upper ledge.018v0 waits30 then210Left, reaches lower return; immediate jump sends back up.019v1 holds100neutral from018prefix6741 thenRight: reaches lower passage, dies7330 atspikes.020 retains7101 before spike and tries jump/flight vsjump.

- Certified Sonic DEZ1 milestone committed9fd5f2e16; summary6dfdbc5a4. Canonical23533input route reaches released Act2;61replaywindows pass. No runtime changes.
- Sonic014 appends originalteam15240..19809 after23533 but dies25120 onlowerconveyor.015 retains24883 and30/45/60extraLeft then84Right+400neutral; all reach1483/2004.016 uses015v0prefix25397 +team16970..19809; progresses staircase andgravitytube but fallsbelowenergybridges. Keep27301 at3064/2476.017 jumpingRight and018wait60/120/180thenjump both fallbelowbridges.019 tries native route's stop/verticalclimb, not runningthrough.
- Tails020jumpRight hits easternwall anddies;019v1prefix7221+Left gives021lowercorridor, needsjumpat9464/1456.022v0prefix7461,30Left+A then320flapframes and450Left crosses but eventuallyrunswestoffroute; retain8041 at8148/1534.023neutral/right fails inhazards.024v1wait30thenRightjump/flight reaches turbine.025from024v1prefix9062 with60/45updown doesn'tclearallpanels.026from025v0prefix12362,20cycles90Up/90Down+900Right succeeds to11445/1712 with38rings;30cyclevariantfails.027from026v0prefix16862 Left110/250thenneutral followslaunchertorisingstair10442/1136 buteventualtorpedodeath17623.028retains17483andtriesRightjump/flightbeforesecondhit.

- Sonic019 reproduced the team's stop/climb pattern too late: platform phase absent at3172, falls before reaching3253.020 insteadbrakes12Left immediately from016prefix27301, waits60/120 thenverticaljumpsequence; pending.
- Tails028 passes stairbutfliesover11136/940launcher, hitsrightdeadendanddies.029retains028v0prefix17721 (near11094/892) andbrakes15/25Leftthen700neutral tolandonlauncher; pending.
- Current committed taskHEAD6dfdbc5a4, clean. Live continuation tool sessions at handoff: Sonic020=23648, Tails029=2412. Logs target/dez-sonic-branch020.log and target/dez-tails-branch029.log. Do not treat these scratch attempts as certified.

- Sonic020jumpsequence starts too farleft/stalls thenfalls;021sixwaitvariants putSonicbelowmovingplatform at3249/2668. The actual first intermediate platform is $4A at3264/2624 withmonitor3264/2592;022 retains021v3prefix27660 and attempts neutral vertical jumps to catch movingplatform, beforeproceedingright.
- Tails029brakinglandsadjacentto11136/944launcher;v1ends11112/944.030from029v1prefix18446,20Right+900neutral catcheslauncher and reachesupperapproach12233/640.031from030v1prefix19366 immediate600Right reachesboss14312/816,6rings,0deaths. Forecast fight search001 uses031v1prefix19740, copied Soniccontroller withactualTails roster. Live29323, logtarget/dez-tails-fight-search001.log; no statewrites, samefullregistryrestorevalidation. Sonic022live83182. CurrentHEAD6dfdbc5a4 clean.

- Sonic022 verticaljumps strikeplatformunderside at2659; no physics defect indicated. Prefixobjectlist establishes3264/2624 subtype0 stationary platform, not moving here (corrects earlier shorthand).023v0 moves30Leftthen30Rightjump, reaches3224/2573 at27720, thenbrakes prematurelyandfalls.024 retains023v0prefix27721, continuesRight20/30then12Left+100neutral tocompleteplatformlanding. Live28562, logtarget/dez-sonic-branch024.log. Tailsfight001stilllive29323, last6rings→ringrecovery,4firstphasehits by20620.

- Sonic024v0 completeslanding onstaticplatform:27852 at3290/2588,3rings,alive.025from024v0prefix27853 attempts10/15Leftjump+neutral towardmonitor/nextenergybridge; live64401. The longer024Right30variant falls offright, reject.

- Sonic025v0/1 jumpsfromplatformonto firstenergybridge at3260/2476 (v0). Retain27899.026jumpfrom3260 hitslowterrainceiling atx3264/y2432; rejectsinput, notenginebug.027uses30Right beforejump, clearsbridgeclimb to3893/2316 with3rings,zero deaths;retainv0prefix28359.028triesrightjump(s)fromnextledge, live80765, logtarget/dez-sonic-branch028.log.

- Sonic028jumpat3893doesnotclearrightwall. Actualroute requiresgravitypad3632/2264 beforethiswall;027ranoffpad beforelanding.029retains027v0prefix28060 at3556/2189,brakes30/40Leftthen160neutral+600Right tolandonpad. Live64719, logtarget/dez-sonic-branch029.log.
- Tails freshapproachcapture19740frames matches031v1 onall12playerfields,zero deaths/followers.21.666667s60fpsclip,full decode+stills19000/19739checked. This is not yet fullrewind/fightcertification. Fight001live29323, sixhits by25880; sourceplayerinputs only.

- Sonic029brakesbeforepad butlandsbesideit at3605/2252; pad3632/2264 blocksrightside.030retains029v1prefix28850andtries10/15Rightjump,20/25A,12Left,200neutral,600Right tolandonpad, live61810 logtarget/dez-sonic-branch030.log.
- Tailsfight001clearedfirstphasearound27000, secondphase6remaining at27600. Stilllive29323 andboundedat28740; ifboundaryarrivesbeforeload, preservebestinput andcontinue normally. Current taskHEAD6dfdbc5a4 clean. No newvalidationclaim beyond freshTailsapproachcapture thisturn; originalgoalremainsactive.

- Tails fight001 completesall16hits, Act2load28320. Prefix28321+1200neutral canonical29521inputs independentlymatchesallprefix12fields,0deaths/followers,released320/944. TestDezSoloColdRouteCapture2tests0fail/error/skip77.77s test1:43Maven:75Tails+61Sonic immediatefullregistryrestore/45replaywindows. Verified52.016667sdefeat/arrivalvideo. Localmilestonecc07626d9; scope/deliverygapsinmatrix/audit. No runtimechanges.
- Sonic030v0 15Rightjumpfrompadside succeeds togravityceiling3981/1875,10rings.031v0 immediate30Rightjump+700Right reaches5129/2259,19rings, inopposing-springtrap.032Rightonly/jumpfromleftwardvelocityfails.033retains032v0prefix30432justafterleftspringlaunchesRight;immediate/2delayRightjumpclearsopposingspring, bothtransporters, reachesuppercorridor6417/1363(v0)or6555/1363(v1),20rings.034from033v1prefix31664triesRightjump+900Rightvs900Right,live15822,logtarget/dez-sonic-branch034.log.
- Tails032coldcanonical29521prefix plus Sonic033v1inputs23533..end startsAct2soloauthoring;live43653,logtarget/dez-tails-branch032.log. Thisis exploratory only; noAct2certificationyet. CurrentHEADcc07626d9 clean, broadcampaignverification/integration/pushstillopen.

- Sonic034cannotclear6588spring;035uses034v1prefix31745at6496/1363,rightward632 andjumpsclearbutSpikebonkermacehitsat31775, consumeslightningshield (rings20unchanged).036retains035v0prefix31811afterhurtlandingat6529/1363, retriesjumpwhileordinaryinvulnerabilityisactive;live24406,logtarget/dez-sonic-branch036.log.
- Tails032reusingSonicinputsdivergesearlybuttakesvalidupperpath,to4789/1263,invertedceiling,1ring.033flightversionhitbySpikebonkerthenlaterdies;ordinaryjumpversionstallswith3rings.034retains033v0prefix37723afterfirsthurtlanding4675/1263, retriesRightjump/flightwith0/20delay;live31662,logtarget/dez-tails-branch034.log. Actualinputonly; theseareunverifiedcontinuations, currentHEADcc07626d9clean.

- Sonic036v0 succeeds pastspring/mace to6709/1395,20rings.037from036v0prefix32441 +team19810..23199 crossesgravitypad/tubeanduppercarriersection butends6958/556at35830. Earlieralignmentwithteamisnotexact; upperledge needsnewjump.038retains037v0prefix35831 andtriesRightjump/secondjump,live48880.
- Tails034v0 flightafterhurtsucceedsupperpassageto5685/1136,0rings,alive.035sameRightjump/flight reaches6005/1167 at39824; ordinaryjumpvariant5899/1167.036from035v0prefix39825 repeatsflightorordinaryjump,live80265, logtarget/dez-tails-branch036.log. No newcertifiedmilestoneyet, taskHEADcc07626d9clean.

- Sonic038v0 Rightjumpclearsupperledge andlauncherchain,reaches8316/553 with0rings at36560;039continuationdies36669at8730/646inconveyordescent.040retains039v0prefix36611, triesimmediate/15delayedRightjumponpad beforehazard,live14543.
- Tails036can'tpass6005/1167: uppermonitorroomhaswallandfloor;flightstopsat1264. Rejectupperdetourtail.037returns032v0prefix33301at3095/1456justaftertube andtakesLeft400/500/600then400neutral. v0ends1483/2000,0rings;v1dies33921;v2ends1729/2000,14rings,aliveat34300.038retains037v2prefix34301,triesRightjump/flightorordinaryjump, live37059, logtarget/dez-tails-branch038.log. TaskHEADcc07626d9stillclean; continuedinputsnotcertified.

- Sonic040v1 delayedjump15Right then30Right+A clearsdescentandlands8757/1132 at37355,zero rings/alive;v0immediatejumpdies36811.041retains040v1prefix37356andappendscanonicalteam23200..25262 forinvertedshaft/bridge continuation;live13053.
- Tails038v0flightclearsstaircase/tube andreaches3381/2480with5rings at35351,alive.039retains038v0prefix35352,triesflightRightorleft-then-rightclimb. Logtarget/dez-tails-branch039.log; see current tool handle. Ordinary038v1jumpstays1937/1999. CurrentHEADcc07626d9clean.

- Sonic041 appendedteamtail failsat38201, backat8757/1294 afterovershootingwestandreturning. Actualpositions:37566=8133/1088,37636=7713/1077,37706=7507/1199,37986=8657/1037.042retains041v0prefix37551nearshaft;triesneutral/brake+jumpRight orLeftjumpandneutral tosettle,live44981,logtarget/dez-sonic-branch042.log. Olderteamcapture20260924predatesinputrepairs; navigationreferenceonly, notstateoracle.
- Tails039v0flightRight successfullyclimbsenergybridges/triggersgravitypad andreachesopposingsprings5119/2255with8rings at36402,alive.039v1leftdetourdies.040retains039v0prefix36389immediatelyafterleftspringlaunchedright, triesRightjumpwith0/2delay+1200Right,live41582,logtarget/dez-tails-branch040.log.

- Tails040jumpclearsopposingspringsandtransporters to6577/1359,8rings.041v0retains040v0prefix37594afterrightwardsbuild-up at6494:jump/flighttakesmacehitbutcontinuesflightandclearsgravitypad to7205/1712,0ringsaliveat38464.042from041v0prefix38465triesflightRightorspindashRightaroundnextcurve,live68102.
- Sonic042v1ends7568/1043,3ringsafterjump/neutral. Owningmatrixspring-shaft notes say spindashisrequiredforcurve;043chargedLeftspindash succeeds reachingfirst/secondspringaround7502/1642,v1prefix38685.044steersRightfromspringarcwith/withoutjump,livecurrenttoolhandle,logtarget/dez-sonic-branch044.log. No runtimechanges;noneofthesecontinuationscertifiedyet.

- Sonic044steeringRightfromlatearc38685 istoo late;getsx7605wallwhileYreturnsup. Secondinvertedretractingspringis7504/1408,first7600/1216;043v1maxY1662at38607.045retains043v1prefix38551andstartsRightimmediate/20delayedearlierinlaunch, logtarget/dez-sonic-branch045.log.
- Tails042v0flightfromcurvepasses to7349/1680,0rings;spindashfromstationarywallfails.043from042v0prefix39416triesflightRightorLeftthenneutral,live62716,logtarget/dez-tails-branch043.log. No enginechanges.

- Sonic045v1 earlierRight clearssecond-springexitbutreturn-facingspring7864/1616sendsbackLeft. Retain38652 at7721/1619,vx1029,grounded.046triesRightjumpwith0/10delay+900Right toclearspring,live87448.
- Tails043Rightflightstays7349/1680;Leftflightends7114/1712. It appears flightpassedovergravitypad7232/1720;044returns042v0prefix39416at7349/1680, movesLeft40/50 thenRight12+200neutral+600Right tolandonpad,live72530. Bothcontinuationspending, taskHEADcc07626d9clean.

- Sonic046v1 (10Rightthenjump) clearsreturn-facingspringandfirstceilingstep, ends8211/1683with5rings at39591.047retains046v1prefix39592andappendscanonicalteam23893..25262 throughlowerpad/bridge; logtarget/dez-sonic-branch047.log, currenttoolhandle.
- Tails044v1(50Leftthenbrake) landsongravitypad andactuallyinverts,risesuppersectionto7322/667,4ringsat40277. v0missespad.045retains044v1prefix40278,triesLeft300/450thenRight600 throughupperbowl/launchroute,live55520. CurrentHEADcc07626d9clean.

- Sonic047lowerpad/bridge tail succeeds to9606/2061,9rings at40961,alive.048retains047v0prefix40962 andappendscanonicalteam25263..28412 throughuppertransportchains/easthub,live76989.
- Tails045walkingLeftalonefailscurvedbowl;ends7313/662(v0)or7342/702(v1).046retains045v0prefix41178andchargesspindashLeft, thenLeft200/350+Right600,live79307. Thisfollowsdocumentedcurved-wallmomentumrequirement. Pendinginput-onlywork,HEADcc07626d9clean.

- Sonic048 reachesnexttransport/curvebowl butstalls, ends10115/1642 with23ringsat44111. Retain42061at9734/1587,onfloor,vx2342:049triesrollDownwith/withoutRight100frames thenRight900 toretaincurvemomentum,live72988.
- Tails046v1chargedLeft350thenRight600 succeedsupperbowl/spring to6696/508,15rings at42141.047v0Rightalonefails, v1jumpRightreaches6965/560;retainfirstgroundarrivalprefix42265.048triesordinaryRightjumporflight intoupperlaunchchain,logtarget/dez-tails-branch048.log. CurrentHEADcc07626d9clean;routecontinuationsnotcertified.

- Sonic049rollingalonefailsheightat10156curve.050retains049v1prefix43061at9971/1638,vx319,grounded;triesbrake+chargedRightspindashor20neutral+charge,8taps,live97941.
- Tails048v0ordinaryRightjumpfrom6965clearslaunchchainanddescends to8757/849at43294,0ringsalive. Flightvariantdies43273at8730/650.049retains048v0prefix43295andcontinuesRightwith/withoutjump, logtarget/dez-tails-branch049.log. Input-onlycontinuation,HEADcc07626d9clean.

- Sonic050v1 (20neutralthen8tapspindash) clearscurve andarrives10357/1388at43325,2rings. v0brakeapproachfails.051retains050v1prefix43326andtriesRightjump/secondjump+continuation,live54191.
- Tails049v0continuesdescentto8757/1136,0ringsaliveat43994;v1ends8725/1136.050retains049v0prefix43995andgoesLeft300/400+300neutral towardinvertedshaft,live40543. CurrentHEADcc07626d9clean; no newruntimechanges/tests.

- Sonic051reaches10769/1420 at43553 with1ring,blockedbyuprightspikes.052retains051v0prefix43554,Rightjumpclearsandtraversestransportto12992/1600,2rings,aliveat44483.053retains052v0prefix44484,pressesDownthenneutral240or180neutral+Left600 throughhubdescent/return,live85530.
- Tails050v0ends7767/1064;051v0chargedLeftspindashreaches7504springoscillation,ends7498/1654with3rings at45112.052retains051v0prefix44974at7498/1472launchingdown,steersRightimmediateor20delayed+700Right, currenttoolhandle/logtarget/dez-tails-branch052.log. HEADcc07626d9clean,no newruntimechanges.

- Sonic053v0Downreaches12992/2112with2rings,aliveat44724. v1Leftcontinuationreaches11640/2328with6rings.054usesv0prefix44725+canonicalteam28413..31951 forreturntransports/lateapproach,live25783.
- Tails052v0earlierRightclearssecondspringbutreturn-facingspringflingsback. Retain45055at7724/1615;053triesRightjumpwith0/10delay+900Right. 052v1lateRightfailswall. Logtarget/dez-tails-branch053.log,currenttoolhandle. CurrentHEADcc07626d9clean,broadercampaignstillopen.


## Continued solo work (2026-09-25)

Sonic column-controller attempt `sonic-act2-column-001` clears all eight gravity
boss hits and requests the final stage at input53721. The candidate canonical
route is53842 inputs including120 neutral arrival inputs. Fresh capture agrees
on all53722 authored rows (12 fields), has no deaths/follower, and its5592-frame
60fps video passes full decode. Rewind initially failed at28910: attracted-ring
slot reservations were lost because the ring adapter ran before the re-registered
object adapter. Simply removing future-slot releases then exposed the ordering
fault as missing rings. Fix both ordering and stale releases. The subsequent
route reached the boss retirement and exposed a retained Robotnik parent identity;
validation of that repair is in progress. Do not call this route rewind-certified
until the final focused run passes.

Tails056 releases flight after46480 and activates the underside gravity pad;
both variants reach8373/2255 with6 rings. Attempts057/058 are invalid tool runs
(class loading during recompilation; malformed `RA` button token respectively).
059 ordinary jumps cannot clear the next obstacle;060 repeated flight loses rings
and dies at47465 at8501/2354. No new engine defect established there.

`sonic-final-001` uses the complete solo Act1/2 prefix without state seeds. It
clears the fingers and lands one core hit, then dies at59598 with1 ring. The
carried act timer may be the constraint; verify before choosing a route repair.
Final-stage completion remains open.


Validated checkpoint: `b7d7ee91f` fixes both rewind issues and records the
Sonic Act2 route. Final1-test run passes103 windows, all8 hits and actual-load
history isolation (0 failures/errors/skips). The preceding137 ring/registration/
loading checks and15 boss checks passed. The original test incorrectly compared
71 pre-load history frames with120 post-load frames plus replay windows; the
reset assertion now runs at the load itself, with a final destination-only seek.
Combined2920-class+guards campaign validation and integration remain pending.

Fresh final001 death still is in `campaign-20260925-sonic-final-death-check`:
HUD9:59 at59598,1 ring. Timer exhaustion is the route constraint. The Act2 movie
contains at least5491 removable-looking stationary inputs, but transport waits
must be distinguished from optional authoring pauses before trimming/replaying.

Tails061 variant0 prefix47044 reaches8647/2480,9rings. Correct lower pad
activation used prefix46582 from056v0,12Right,12Left,160neutral thenRight.
Continuing straight eventually drops below the lower bridge;062 branches from
47044 to try jumping/flying that section. Read its CSV before continuing.


## Pending-contact correction and new candidates

Tails061 was NOT a valid route: comparing its saved-state branch with fresh062
showed first divergence46582, Y2144 vs2136. Pad restore cleared an occupied
contact latch, rearmed a zero timer and allowed an extra toggle. Capture both
press and occupancy latches. The two short tests fail before repair;73 focused
checks,60 route/loading checks and5 rewind guards now pass with0skips.
Tails064v0 actually jumps off and returns to the pad (`30 A;180 -;700 R`). Its
first47140 inputs are canonical `dez2-tails-solo-lower-gravity-pad-320`;12 full
registry windows pass, and fresh capture matches all47140 rows. Video/stills and
README are in `campaign-20260925-tails-lower-pad-fixed-320`. Frontier is the lower
bridge, not Act2 completion. Tails065 jumps at47066 but first gets hurt and later
falls; `tails-hop001` uses live-grounded jumping and retains9rings at8885/2480,
49066 inputs. Branch066 tries flight over the higher wall from that candidate.

Sonictrim001 shortened early waits but missed the energy bridges; rejected.
Trim002 shortened later waits but its spring-shaft inputs were mistimed and died
36732. Trim003 splices trim002prefix36251 (7566/1043) to original38211..48264;
it reaches the gravity boss in46304 inputs (1960 saved). Trim004 removes
trim003 inputs36933..37700 (768 stationary frames at8211/1683); it independently
reaches the boss in45536 inputs,12rings,0deaths. The column controller then clears
all hits and loads final stage at50993 (`sonic-act2-column002`),2728 earlier than
certified original. `sonic-final-002` explores its incoming final fight next.
Do not replace the certified fixture before fresh replay and adjusted rewind
windows pass.

`sonic-final-respawn001` continues after original final001 time-over: death59598,
normal reload60187 at96/112,0rings,camera0/32; later authored attacks die62145 and
64231, with second reload62295. End is TITLE_SCREEN after game over. The author
was not safe with zero rings; this is not a completed ending route, nor evidence
of a restart bug. Replay/lifecycle certification is still open.


Checkpoint `41d7cb05f` commits the pad repair, short regression cases and the
47140-input Tails frontier with12 replay windows. Task tree clean afterwards.
Sonic column002 completes the optimized Act2 load at50993. Final002 still times
out with core health3 at59598 (five hits); final003's aggressive exposed-core
jumping dies56459 with0rings, so do not use it. Final004 limits the extra core
attack to one hit per beam cycle; its author is running in the next continuation
(`target/dez-sonic-final004.log`, source `DezSoloFinalCoreOnceProbe.java`).

Tails hop001 ends49066 at8885/2480,9rings, but starting flight that late cannot
clear the higher wall before tiring. Branch066 is rejected. Branch067 instead
starts at hop001prefix47156 (8885/2380, jump apex): v0 `1 R;repeat100{1 R+A;1 R};600 R`
clears the wall and reaches9525/2160,9rings. Keep prefix47470 to avoid extra idle.
Branch068 from067v0prefix47470: v0 ordinary jump returns to9525/2160; v1 flight
passes the ledge but dies at9773/2031,47669. Branch069 now branches from068v1prefix47601,
braking and releasing flap before the far hazard, then waiting/Down/Right.
Its current log is `target/dez-tails-branch069.log`; inspect actual terminal state
before restarting anything. No Tails completion beyond the lower-pad fixture is
certified yet. Preserve these as authoring evidence, not claimed route passes.

Continuation after `c03dc4170`: final004 dies56459 like003; final005 prefers
collidable fingers but still times out59598 (core5), so both are rejected.
Final006 attacks an exposed core only in the first100 beam frames; all8 core
hits complete58574, before time-over, but the old post-hit movement heads back
left and falls at58605. Final007 retains early attacks and runs/jumps toward
the surviving right floor after core defeat. It is still an input-authoring
trial, not a certified completion.

Tails070v0 starts at067v0prefix47438 (before the raised ledge), then30R+A;400R.
It clears the ledge and vertical tube, ending47868 at10325/847 with12rings,
no death. Flight variant1 reaches the same tube with only3rings; preferv0.
071/072 rightward continuations stall at10325/847. 073 continues070v0 by
heading left along the upper route toward the hub. Fresh replay and new
rewind windows are still required.

Checkpoint `9bc91e469`: Sonic final007 is now preserved as
`dez-sonic-solo-cold-ending-320.{script,bk2}`,64477 inputs, actual ending64476.
Core defeated58059, ship64190;0 deaths. All68 full-registry replay windows pass,
independent capture matches every row on20 fields. Video in
`campaign-20260925-sonic-solo-cold-ending-320`,9477 frames60fps157.95s, decoded.
The first core006 clear was followed by a fall58605;007 fixes only controller
inputs (run/jump to surviving floor after core), no engine changes.

Tails073v1 clears the upper passage via420L;30L+A;300L and reaches9101/971
at48618. 074v0 then100L;900R follows the tube/hub to10357/1392 (2rings);
useprefix49141 to avoid waiting. 075v0 ordinary jump stalls10769/1424; v1
30R+A;1R;repeat80{1R+A;1R};400R clears the obstruction and reaches11172/1453
at49732 with3rings. 076 from weaker075v0 was exploratory and is not preferred.
077v0 from075v1prefix49732+1500R reaches the12992/1600 gravity hub with no death.
078 from077v0prefix51232 tests a release then fresh R/U/D press, because the hub
requires a press edge. Current process output: target/dez-tails-branch078.log.
These Tails extensions remain uncertified until fresh capture and replay windows.

Checkpoint bac660ab4: the final-floor proximity support opt-in caused false
grounding atY186 and alternating animation. Removed; native supportY205 restored.
Sonic final-floor010 now60920 inputs, core57758,ship60632,ending60919;68 rewind
spots pass. Team floor00249448 inputs/31 spots; cold emerald team59722 through
DDZ, positioned320/80027122/27224 through DDZ, all11 spots each. All five route
cases pass;164 focused domain cases pass. The previous64477/54692/64648 and
30918/31531 input lengths are historical. Full native and800 captures linked
in the commit audit. Local commit only; campaign broad/integration/push owed.

Tails078v2 fresh Down exits12992/1600 to12992/2112; useprefix51450. 079L with
right afterward re-enters the hub, so prefer080v0:500L;500R reaches11567/2372
at52450 with7rings. 081v1 uses60L;30L+A;600L and reaches10509/2416 at53140,
7rings,alive. Current082 starts there and tests ordinary jumps or flight right
along the lower return corridor. Source target/dez_branch.py. All new Tails
extensions after the canonical47140 lower-pad route remain authoring, not
certified cold completion.

Tails082v0/v1 ordinary jumps return to10677/2416 (v0 gains17rings). v2 flight
reaches10848/2241 at53360, then rightward input stalls10933/2256 and dies53723.
Branch083 forks082v2 at53360 to turn left toward the return shaft; all three
variants completed. Inspect their CSV maxima/positions and selected PNGs before
choosing the next branch; do not use082v2's lethal full tail.

Tails084 lands on the upper ledge at10602/2160; staying left never enters the
launcher below.085 fresh flight reaches the ceiling atY1871 and cannot bypass
the wall.086 instead starts084v0prefix53990, walks400L after stepping right off
that ledge, then700R: all variants take the native launcher and upper shaft.
Prefer086v0prefix54860 (11189/688,1ring) before its stall/hurt tail.088v0 then
30R+A;1000R reaches the boss approach13781/816 with11rings at55890, no death.
087's ordinary staircase alternatives returned to the lower passage and are
rejected. Current readonly controller author DezTailsBossColumnProbe uses088v0
prefix55890 and is running as tails-boss-column001; inspect its terminal outcome.
No Tails completion certification beyond47140 yet.

2026-09-25 continuation after33a5b0e21: complete Tails Act2 route now committed,
62588 inputs,56 registry windows and independent59.8s video. Final001 timed out
65528 with one hand hit remaining. Short001 indiscriminately removed5603 stationary
inputs and died35930. Short002 removed3488 late stationary inputs but missed the
first down hub and stalled at12992/1600. Short003 removes only795 hub-wait inputs
and reaches final61672. Short004 removes2476 inputs at six explicitly indexed
waits (see script) and reaches final59990 with no death; final002 continuation
clears hands then four core hits before timeout65528. Short005 removes1651 more
stationary inputs and is currently being replayed by DezTailsBossColumnProbe.
All variants are input-only authoring; no runtime writes or timer changes.
Campaign broad validation started at33a5b0e21, session94461, diagnostics under
worktree target/category-tests/20260925T134954Z-1ed239af; do not restart a live run.

Short005 succeeded: final load58339. Final003 cleared all hands,core andship;
actual ending68265,68266 rows,zero deaths. Independent full capture matches20
fields across allrows. New canonical dez-tails-solo-cold-ending-320 resources and
58-window method added, not yet committed: queued session60263 behind campaign
broad session94461. Final video verified112.766667s/6766frames60fps and full decode.
Do not rerun broad merely because these later test resources were added; run the
queued focused method after broad and report its scope separately.

The queued Tails final test was expanded from58 to84 windows before it started,
adding before/after each of the13 shortened waits. Source/docsuncommitted while
waiting for its observed pass. Broad remains running at33a5b0e21 witholdcompiled
route classes; focused queuedtest validateslaternewmethodafterward.
