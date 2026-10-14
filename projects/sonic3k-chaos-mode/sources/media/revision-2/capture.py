#!/usr/bin/env python3
"""Chaos demo captures, 2026-10-14. Production GameplayCaptureTool and authored
BizHawk inputs; singleton selected pools and seed22 curate normal scheduler draws.
No mutator/session bypass. Each row is one real 60Hz presentation, native PCM.
"""
from pathlib import Path
import os, subprocess, sys, json, shutil, hashlib, signal
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
P=Path(os.environ.get('CHAOS_MEDIA_ROOT',ROOT))
WT=Path(os.environ.get('OPENGGF_WORKTREE',Path.cwd()))
ROM=Path(os.environ.get('OPENGGF_S3K_ROM','/home/farrell/code/projects/OpenGGF/Sonic and Knuckles & Sonic 3 (W) [!].gen'))
CP=str(WT/'target/classes')+os.pathsep+(WT/'target/chaos-classpath.txt').read_text().strip()
JAR=Path(os.environ.get('CHAOS_MOD_JAR',WT/'target/sonic3k-chaos-mode/sonic3k-chaos-mode.jar'))
# Use the shared scheduler even though gameplay classes are already built.
QUEUE_ROOT=Path(os.environ.get('OPENGGF_QUEUE_ROOT','/home/farrell/code/projects/OpenGGF'))
sys.path.insert(0,str(QUEUE_ROOT/'tools/testing'))
from maven_queue import maven_slot, inherited_slot, handle_termination
env=os.environ.copy()
env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
def run(cmd,log,lease,cwd=WT):
    started=datetime.now(timezone.utc).isoformat()
    with log.open('w') as out:
        child=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=out,stderr=subprocess.STDOUT,start_new_session=True,**inherited_slot(lease))
        try:
            status=child.wait()
        except BaseException:
            os.killpg(child.pid,signal.SIGTERM)
            try: child.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGKILL);child.wait()
            raise
    interval={'cwd':str(cwd),'pid':child.pid,'startedUtc':started,'finishedUtc':datetime.now(timezone.utc).isoformat(),'exitCode':status}
    if status:
        raise RuntimeError(log.read_text()[-5000:])
    return interval
MOVING='600 -; repeat 6 { 1 R+A; 59 R }; 120 -'
SHOTS={
 'dvd':('dvd-hud',MOVING), 'heads':('pulse-head',MOVING),
 'trails':('afterimages',MOVING),'moon':('moon-gravity',MOVING),
 'gravity':('gravity-hiccup',MOVING),'mirror':('mirror-view',MOVING),
 'negative':('negative-world',MOVING),'scenery':('wrong-zone-scenery',MOVING),
 'wind':('windy-day','720 -; 240 R; 120 -'),
 'bumper':('bumper-ahead','570 -; 60 R; 1 R+A; 209 R; 240 -'),
 'ghosts':('soz-ghost-party',MOVING),'magnet':('ring-magnet',MOVING),
 'pong':('ring-pong','600 -; repeat 4 {60 L; 60 R}'),
 'stack':('monitor-stack','600 -; repeat 8 {20 R; 1 A; 1 -; 20 L; 1 A; 17 -}'),
 'flood':('flash-flood',MOVING),
 'bobble':('bobble-head','600 -; 80 R; 200 -; 200 R'),
 'invisible':('invisible-player',MOVING),
 'overdrive':('projectile-overdrive','1080 -'),
 'ghost-close':('soz-ghost-party','650 -; 1 A; 149 -; 280 R'),
 'pong-play':('ring-pong','600 -; repeat 6 {30 U; 30 D; 20 -}'),
 'rain':('ring-rain','780 -; 1 A; 119 -; 180 R'),
}
def capture(name):
    base=P/'captures'/name
    if (base/'source.mkv').exists() and (base/'provenance.json').exists():
        print('retained',name,flush=True);return
    with handle_termination():
        with maven_slot(WT,exclusive=True,estimate=30,kind='chaos-gameplay-capture') as lease:
            capture_admitted(name,lease)

def capture_admitted(name,lease):
    base=P/'captures'/name
    admitted=datetime.now(timezone.utc).isoformat()
    base.mkdir(parents=True,exist_ok=True)
    if name=='menu':
        script=(ROOT.parent/'captures/menu/input.script').read_text()
        frames=1700; effect=None
    else:
        effect,script=SHOTS[name];frames=1080
        prefs=base/'saves/mods/sonic3k-chaos-mode/settings.txt'
        prefs.parent.mkdir(parents=True,exist_ok=True)
        prefs.write_text(f'formatVersion=1\ninterval=5\ndurationQuarters=4\nselected={effect}\nenabled=true\nseed=22\n')
    (base/'input.script').write_text(script+'\n')
    author=['java','-cp',CP,'com.openggf.tools.InputLogAuthorTool','--script',str(base/'input.script'),'--out',str(base/'input.txt')]
    logdir=WT/'target/chaos-reel';logdir.mkdir(exist_ok=True)
    author_interval=run(author,logdir/f'{name}-author.log',lease)
    args=['--game','s3k','--rom',str(ROM),'--zone','aiz','--act','1','--width','400','--main','sonic','--sidekick','none','--mod',str(JAR),'--input',str(base/'input.txt'),'--frames',str(frames),'--every','1','--interactive-pacing','--audio','--no-video','--out-dir',str(base/'output')]
    if name=='menu':args+=['--title-screen']
    if name in {'overdrive','giant','spinning','tiny','jelly'}:args+=['--x','8912','--y','877']
    if name=='leak':args+=['--rings','32']
    command=['java','--enable-native-access=ALL-UNNAMED','-Xmx2g','-XX:ActiveProcessorCount=4','-Dopenggf.headless.gl=surfaceless-egl','-Dopenggf.saveRoot='+str(base/'saves'),'-cp',CP,'com.openggf.tools.GameplayCaptureTool',*args]
    print('capturing',name,flush=True)
    capture_cwd=WT
    if name=='defence':
        # Bind all three ordinary actions in an owned cwd; never edit shared config.yaml.
        (base/'config.yaml').write_text('configFormat: 2\ninput:\n  player1:\n    a: SPACE\n    b: X\n    c: C\ndiscord:\n  enabled: false\n')
        capture_cwd=base
    capture_interval=run(command,logdir/f'{name}-capture.log',lease,cwd=capture_cwd)
    pngs=list((base/'output/frames').glob('*.png'))
    run(['ffmpeg','-nostdin','-loglevel','error','-y','-framerate','60','-i',str(base/'output/frames/%05d.png'),'-i',str(base/'output/audio.wav'),'-c:v','libx264rgb','-crf','0','-preset','medium','-pix_fmt','rgb24','-threads','2','-c:a','pcm_s16le',str(base/'source.mkv')],logdir/f'{name}-encode.log',lease)
    setup=('positioned native AIZ1 centre8912,877; bypassed approach, no rings/checkpoints/event state seeded' if name in {'overdrive','giant','spinning','tiny','jelly'} else 'native AIZ1 direct level; no position/ring/world writes') if effect else 'native title and No Save/Sonic launch'
    if name=='defence':setup+='; owned normal config binds A=Space B=X C=C, shared config unchanged'
    if name=='leak':setup+='; declared carried inventory32rings to demonstrate loss (not earned in the shot)'
    meta={'admission':{'scheduler':str(QUEUE_ROOT/'tools/testing/maven_queue.py'),'kind':'chaos-gameplay-capture','exclusive':True,'admittedUtc':admitted,'author':author_interval,'gameplay':capture_interval},'sourceCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=WT,text=True).strip(),'command':command,'author':author,'effect':effect,'selectedPool':'singleton' if effect else 'native menu, fresh default settings','seed':22 if effect else 0,'frames':len(pngs),'cadence':'60Hz presentation, interactive pacing, every=1','setup':setup,'rom':str(ROM),'romSha1':hashlib.sha1(ROM.read_bytes()).hexdigest(),'modSha256':hashlib.sha256(JAR.read_bytes()).hexdigest()}
    (base/'provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
    print('captured',name,len(pngs),flush=True)
SHOTS.update({
 'afterimages':('afterimages',MOVING), 'rainbow':('rainbow-player',MOVING),
 'upsidedown':('upside-down-view',MOVING),'fastforward':('fast-forward',MOVING),
 'slowmo':('slow-motion',MOVING),'hudorbit':('hud-orbit',MOVING),
 'hudshuffle':('hud-shuffle',MOVING),'hudscale':('hud-scale',MOVING),
 'shield':('shield-surprise',MOVING),'superstar':('ten-second-superstar',MOVING),
 'blueprint':('blueprint-zone',MOVING),'squashy':('squashy-view',MOVING),
 'giant':('giant-badniks','1080 -'),'spinning':('spinning-badniks','1080 -'),
 'tiny':('tiny-badniks','1080 -'),'jelly':('jelly-objects','1080 -'),
 'breakout':('monitor-breakout','620 -; 1 D; repeat 6 {1 D+A; 1 D}; 1 -; 246 R; 200 -'),
 'vine':('vine-time','600 -; 160 R; 1 A; 319 R'),
 'snake':('ring-snake','600 -; repeat 3 {24 R;24 D;24 L;24 U;64 -}'),
 'chat':('imaginary-chat',MOVING),'ringorbit':('ring-orbit',MOVING),
 'zoom':('zoom-pulse',MOVING),'quake':('quake-camera',MOVING),
 'defence':('badnik-defence','620 -; repeat 10 {1 A;14 -;1 B;14 -;1 C;14 -};10 -'),
 'sonicsays':('sonic-says',MOVING),'landmark':('landmark-hunt',MOVING),
 'rampage':('rolling-rampage','550 -; 200 R; 1 D; 209 R; 120 -'),
 'buddy':('rescue-buddy',MOVING),'springlegs':('spring-legs',MOVING),
 'bunny':('bunny-hop','600 -;480 R'),
 'leak':('ring-leak','570 -;150 R;180 L;180 R'),
 'blaster':('eggman-blaster',MOVING),
})
if __name__=='__main__':
    for name in sys.argv[1:] or ['dvd','heads','wind','bumper','ghosts','gravity','trails','moon','mirror','negative','scenery','magnet','pong','stack','menu']:
        capture(name)
