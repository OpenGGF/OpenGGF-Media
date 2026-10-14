#!/usr/bin/env python3
"""Chaos demo captures, 2026-10-14. Production GameplayCaptureTool and authored
BizHawk inputs; singleton selected pools and seed22 curate normal scheduler draws.
No mutator/session bypass. Each row is one real 60Hz presentation, native PCM.
"""
from pathlib import Path
import os, subprocess, sys, json, shutil, hashlib
ROOT=Path(__file__).resolve().parent
P=Path(os.environ.get('CHAOS_MEDIA_ROOT',ROOT))
WT=Path(os.environ.get('OPENGGF_WORKTREE',Path.cwd()))
ROM=Path(os.environ.get('OPENGGF_S3K_ROM','/home/farrell/code/projects/OpenGGF/Sonic and Knuckles & Sonic 3 (W) [!].gen'))
CP=str(WT/'target/classes')+os.pathsep+(WT/'target/chaos-classpath.txt').read_text().strip()
JAR=Path(os.environ.get('CHAOS_MOD_JAR',ROOT/'artifacts/sonic3k-chaos-mode.jar'))
env=os.environ.copy()
env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
def run(cmd,log):
    with log.open('w') as out:
        result=subprocess.run(cmd,cwd=WT,env=env,stdout=out,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(log.read_text()[-5000:])
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
    if (base/'source.mkv').exists(): print('retained',name,flush=True); return
    base.mkdir(parents=True,exist_ok=True)
    if name=='menu':
        script=(ROOT/'captures/menu/input.script').read_text()
        frames=1700; effect=None
    else:
        effect,script=SHOTS[name];frames=1080
        prefs=base/'saves/mods/sonic3k-chaos-mode/settings.txt'
        prefs.parent.mkdir(parents=True,exist_ok=True)
        prefs.write_text(f'formatVersion=1\ninterval=5\ndurationQuarters=4\nselected={effect}\nenabled=true\nseed=22\n')
    (base/'input.script').write_text(script+'\n')
    author=['java','-cp',CP,'com.openggf.tools.InputLogAuthorTool','--script',str(base/'input.script'),'--out',str(base/'input.txt')]
    logdir=WT/'target/chaos-reel';logdir.mkdir(exist_ok=True)
    run(author,logdir/f'{name}-author.log')
    args=['--game','s3k','--rom',str(ROM),'--zone','aiz','--act','1','--width','400','--main','sonic','--sidekick','none','--mod',str(JAR),'--input',str(base/'input.txt'),'--frames',str(frames),'--every','1','--interactive-pacing','--audio','--no-video','--out-dir',str(base/'output')]
    if name=='menu':args+=['--title-screen']
    if name=='overdrive':args+=['--x','8912','--y','877']
    command=['java','--enable-native-access=ALL-UNNAMED','-Xmx2g','-XX:ActiveProcessorCount=4','-Dopenggf.headless.gl=surfaceless-egl','-Dopenggf.saveRoot='+str(base/'saves'),'-cp',CP,'com.openggf.tools.GameplayCaptureTool',*args]
    print('capturing',name,flush=True)
    run(command,logdir/f'{name}-capture.log')
    pngs=list((base/'output/frames').glob('*.png'))
    run(['ffmpeg','-nostdin','-loglevel','error','-y','-framerate','60','-i',str(base/'output/frames/%05d.png'),'-i',str(base/'output/audio.wav'),'-c:v','ffv1','-level','3','-threads','2','-c:a','pcm_s16le',str(base/'source.mkv')],logdir/f'{name}-encode.log')
    setup=('positioned native AIZ1 centre8912,877; bypassed approach, no rings/checkpoints/event state seeded' if name=='overdrive' else 'native AIZ1 direct level; no position/ring/world writes') if effect else 'native title and No Save/Sonic launch'
    meta={'sourceCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=WT,text=True).strip(),'command':command,'author':author,'effect':effect,'selectedPool':'singleton' if effect else 'native menu, fresh default settings','seed':22 if effect else 0,'frames':len(pngs),'cadence':'60Hz presentation, interactive pacing, every=1','setup':setup,'rom':str(ROM),'romSha1':hashlib.sha1(ROM.read_bytes()).hexdigest(),'modSha256':hashlib.sha256(JAR.read_bytes()).hexdigest()}
    (base/'provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
    print('captured',name,len(pngs),flush=True)
if __name__=='__main__':
    for name in sys.argv[1:] or ['dvd','heads','wind','bumper','ghosts','gravity','trails','moon','mirror','negative','scenery','magnet','pong','stack','menu']:
        capture(name)
