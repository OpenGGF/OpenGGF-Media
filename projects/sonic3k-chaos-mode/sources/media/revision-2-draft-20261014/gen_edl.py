import json,sys
P=60/171.107; B0=0.316
bt=lambda b: B0+b*P if b>0 else 0.0
R='/home/farrell/scratch/sonic3k-chaos-demo-20261014/captures/'
N='/home/farrell/scratch/sonic3k-chaos-demo-20261014/revision-2/captures/'
def src(name,at,new=False,tier='reuse',cond=None,fallback=None):
    d={'src':(N if new else R)+name+'/source.mkv','in':at,'tier':'A-new' if new and tier=='reuse' else tier}
    if cond:d['condition']=cond
    if fallback:d['fallback']=fallback
    return d
ARR='arrival'  # = first frame the Chaos panel names the effect; root reads it from the source
S=[
# act 0 cold open
dict(b=(0,12),act='0 cold open',layout='FULL',effects=['bobble-head'],panels=[src('bobble','arrival-2.805')],caption='ANGEL ISLAND, 10:00 AM. NOTHING TO REPORT.',note='Native idle + diegetic CHAOS countdown; head pops exactly on b8 (arrival frame placed at bt(8)). Caption b0-b7 only.'),
dict(b=(12,14),act='0',layout='CARD',card='ONE HEDGEHOG',sfx='boom'),
dict(b=(14,16),act='0',layout='CARD',card='NO RULES',sfx='skid'),
dict(b=(16,20),act='0',layout='CARD',card='CHAOS MODE',sub='SONIC 3 & KNUCKLES  (plate font)',sfx='dash'),
# act 1 one hedgehog, many problems
dict(b=(20,24),act='1 player',layout='FULL',effects=['afterimages'],panels=[src('afterimages',ARR,True,cond='re-capture after the stronger Too Many Sonics change')]),
dict(b=(24,26),act='1',layout='FULL',effects=['rainbow-player'],panels=[src('rainbow',ARR,True)]),
dict(b=(26,28),act='1',layout='FULL',effects=['pulse-head'],panels=[src('heads',15.0)]),
dict(b=(28,30),act='1',layout='FULL',effects=['invisible-player'],panels=[src('invisible',10.0)]),
dict(b=(30,32),act='1',layout='SLICE-2',effects=['negative-world','mirror-view'],panels=[src('negative',10.0),src('mirror',10.0)],note='diagonal 12deg slice sweeps L->R across the 2 beats'),
dict(b=(32,36),act='1',layout='FULL',effects=['upside-down-view'],panels=[src('upsidedown',ARR,True)]),
dict(b=(36,44),act='1',layout='PAIR',effects=['moon-gravity','gravity-hiccup'],panels=[src('moon',10.0),src('gravity',9.75)],note='payoff 2.8s; right panel lands on b38'),
dict(b=(44,48),act='1',layout='PAIR',effects=['fast-forward','slow-motion'],panels=[src('fastforward',ARR,True),src('slowmo',ARR,True)]),
dict(b=(48,56),act='1',layout='FULL->QUAD',effects=['dvd-hud','hud-orbit','hud-shuffle','hud-scale|shy-hud (B)'],panels=[src('dvd',9.75),src('hudorbit',ARR,True),src('hudshuffle',ARR,True),src('hudscale',ARR,True,'B',fallback='drop to 3 panels; keep TR empty navy with caption')],caption='THE HUD HAS UNIONISED.',note='dvd plays FULL b48-52 then shrinks into TL on b52; TR/BL/BR drop in on b53/b54/b55. Caption from b53.'),
# act 2 power-ups and economy
dict(b=(56,58),act='2 economy',layout='FULL',effects=['shield-surprise'],panels=[src('shield',ARR,True)],note='instant: shield appearance frame on b56'),
dict(b=(58,60),act='2',layout='FULL',effects=['ten-second-superstar'],panels=[src('superstar',ARR,True)]),
dict(b=(60,64),act='2',layout='TRIPLE',effects=['bumper-ahead','windy-day','soz-ghost-party'],panels=[src('bumper',9.75,cond='donor colour verdict'),src('wind',9.75),src('ghosts','arrival',cond='donor colour verdict')],note='bumper contact frame on b61; slices drop in b60/b61/b62',fallback='if donor colours wrong and not fixed: replace bumper+ghosts with spring-legs (B) / moon later in-point, or PAIR wind|flood'),
dict(b=(64,72),act='2',layout='FULL',effects=['ring-rain'],panels=[src('rain',ARR,True,cond='re-capture after full-viewport diagonal rain change')],caption='THE ECONOMY IS DOING GREAT.',note='payoff 2.8s; idle under the rain then run through it'),
dict(b=(72,76),act='2',layout='PAIR',effects=['ring-magnet','ring-orbit (B)'],panels=[src('magnet',12.0),src('ringorbit',ARR,True,'B')],fallback='FULL magnet 12.0'),
dict(b=(76,84),act='2',layout='FULL',effects=['ring-leak'],panels=[src('leak',ARR,True,cond='real lost rings left behind; rings counter falls')],caption='...PLEASE MIND YOUR BELONGINGS.',note='hard cut from rain = the joke; caption from b77'),
dict(b=(84,88),act='2',layout='FULL',effects=['flash-flood'],panels=[src('flood',9.85)]),
# act 3 world and badniks
dict(b=(88,92),act='3 world',layout='SLICE-2',effects=['blueprint-zone','wrong-zone-scenery'],panels=[src('blueprint',ARR,True),src('scenery',12.8)],note='slice line travels across 4 beats, revealing scenery under blueprint'),
dict(b=(92,96),act='3',layout='FULL',effects=['squashy-view'],panels=[src('squashy',ARR,True)]),
dict(b=(96,108),act='3',layout='FULL->QUAD',effects=['projectile-overdrive','giant-badniks','spinning-badniks','tiny-badniks|jelly-objects (B)'],panels=[src('overdrive',10.0),src('giant',ARR,True),src('spinning',ARR,True),src('tiny',ARR,True,'B',fallback='3 panels')],caption='THE BADNIKS ARE GOING THROUGH SOMETHING.',note='overdrive FULL b96-100, shrinks TL on b100; others drop b101/b102/b103; caption from b101'),
dict(b=(108,112),act='3',layout='FULL',effects=['monitor-breakout'],panels=[src('breakout',ARR,True)],note='cage appears ~b108, spindash escape before b112'),
dict(b=(112,116),act='3',layout='FULL',effects=['vine-time'],panels=[src('vine',ARR,True)]),
dict(b=(116,120),act='3',layout='PAIR',effects=['zoom-pulse (B)','quake-camera (B)'],panels=[src('zoom',ARR,True,'B'),src('quake',ARR,True,'B')],fallback='FULL wind 11.0 (Windy Day already counted) or blink-step (B)'),
dict(b=(120,124),act='3',layout='FULL',effects=['soz-ghost-party'],panels=[src('ghosts','arrival+0.5',cond='donor colour verdict')],fallback='bunny-hop (B) or rainbow later in-point'),
dict(b=(124,128),act='3 breather',layout='FULL',effects=[],panels=[src('menu',11.1)],caption='CHOOSE YOUR PROBLEMS.'),
dict(b=(128,132),act='3',layout='FULL',effects=[],panels=[src('menu',19.8)],caption='THEN PLAY THE ACTUAL GAME.'),
# act 4 sidegames, chat, critics
dict(b=(132,140),act='4 sidegames',layout='QUAD',effects=['ring-pong','monitor-stack','ring-snake','badnik-defence|shield-beat (B)'],panels=[src('pong-play',10.0),src('stack',10.0),src('snake',ARR,True),src('defence',ARR,True,'B',fallback='3 panels')],caption='WE INTERRUPT THIS PLATFORMER.',note='panels drop b132/133/134/135'),
dict(b=(140,148),act='4',layout='FULL',effects=['imaginary-chat'],panels=[src('chat',ARR,True)],note='no editorial caption; its own simulated-chat text is the joke'),
dict(b=(148,156),act='4',layout='CARD',card='FICTIONAL CRITICS',reviews=True,note='3 reviews slam on b148/b150/b152, hold to b156'),
# act 5 crescendo
dict(b=(156,164),act='5 crescendo',layout='FULL x4 (2 beats each)',effects=['sonic-says (B)','landmark-hunt (B)','rolling-rampage (B)','rescue-buddy (B)'],panels=[src(n,ARR,True,'B') for n in ('sonicsays','landmark','rampage','buddy')],fallback='any uncaptured slot uses a recap: rainbow 12.0, negative 11.0, upside-down later, mirror 11.0'),
dict(b=(164,172),act='5',layout='SLICE-2 x4 (2 beats each)',effects=['recaps'],panels=['bumper|rain','afterimages|dvd','giant|moon','scenery|invisible'],note='later in-points than first use; never repeat an identical source interval'),
dict(b=(172,180),act='5',layout='QUAD',effects=['recaps'],panels=['afterimages','rain','overdrive','ghosts (or leak)'],note='panels drop b172/173/174/175; no caption'),
dict(b=(180,188),act='5',layout='FULL',effects=['afterimages'],panels=[src('afterimages','arrival+3.0',True)],note='HERO payoff 2.8s: the crowded bright echo run, ideally mid-jump across b184'),
dict(b=(188,196),act='5',layout='SLICE-4',effects=['recaps'],panels=['rain','leak','trails','ghost/overdrive'],note='four diagonal strips, one added per 2 beats; white 2-frame flash at b196'),
dict(b=(196,212),act='end',layout='CARD',card='CHAOS MODE',sub=['105 EFFECTS. CHOOSE YOUR POOL.','AN OPENGGF MOD. YOUR OWN SONIC 3 & KNUCKLES ROM.'],note='HCZ2 bed fades over b204-b212'),
]
t=bt(212)
stinger=dict(t=(round(t,3),round(t+4.3,3)),act='stinger',layout='FULL',effects=['soz-ghost-party'],segments=['0.5s black, silence','ghost-close 11.0->14.3 (death at source frame 840 = 14.00s)','hold 0.3s after death on last frame, then black'],caption='SANDOPOLIS SENDS ITS REGARDS.',sfx='death.wav at death frame',cond='donor colour verdict',fallback='leak: lone ring drops, ringloss.wav, caption "WE DID WARN YOU." or first-reel bumper stinger')
for s in S:
    a,b=s['b'];s['t']=(round(bt(a),3),round(bt(b),3));s['dur']=round(bt(b)-bt(a),3)
out=dict(meta=dict(bpm=171.107,beat_s=round(P,6),first_beat_s=B0,beat_time='t(b)=0.316+b*0.350664 (b=0 -> 0.0)',total_s=round(t+4.3,2),bed='/home/farrell/Videos/OGGF/slay-the-robotnik-promo/audio/m-hcz2.wav'),shots=S,stinger=stinger)
json.dump(out,open(sys.argv[1],'w'),indent=1)
eff=set()
for s in S+[stinger]:
    for e in s.get('effects',[]):
        if e!='recaps':eff.add(e)
a=[e for e in eff if '(B)' not in e]; print(len(a),'A/reuse effects;',len(eff),'incl B slots; total',round(t+4.3,2))
for s in S: print(f"b{s['b'][0]:>3}-{s['b'][1]:<3} {s['t'][0]:6.2f}-{s['t'][1]:6.2f} {s['layout']}")
