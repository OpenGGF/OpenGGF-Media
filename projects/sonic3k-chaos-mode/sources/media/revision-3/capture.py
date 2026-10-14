#!/usr/bin/env python3
"""Chaos gallery revision3, 2026-10-14: varied production gameplay captures.

Inputs: captures.json, ordinary InputLogAuthorTool controller recipes, supplied
locked-on ROM, matching packaged Chaos mod. No trace/gameplay hydration. Java,
compiler, decoder and encoder children inherit shared scheduler OS leases.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, signal, subprocess, sys

ROOT = Path(__file__).resolve().parent
QUEUE = Path(os.environ.get('OPENGGF_QUEUE_ROOT', '/home/farrell/code/projects/OpenGGF'))
sys.path.insert(0, str(QUEUE/'tools/testing'))
from maven_queue import maven_slot, inherited_slot, handle_termination


def run(command, cwd, log, lease, env):
    start = datetime.now(timezone.utc).isoformat()
    with log.open('w') as out:
        child = subprocess.Popen(list(map(str, command)), cwd=cwd, env=env,
                                 stdout=out, stderr=subprocess.STDOUT,
                                 start_new_session=True, **inherited_slot(lease))
        try:
            code = child.wait()
        except BaseException:
            os.killpg(child.pid, signal.SIGTERM)
            try: child.wait(timeout=20)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL); child.wait()
            raise
    result = dict(pid=child.pid, cwd=str(cwd), startedUtc=start,
                  finishedUtc=datetime.now(timezone.utc).isoformat(), exitCode=code,
                  command=list(map(str, command)))
    if code: raise RuntimeError(log.read_text()[-5000:])
    return result


def capture(spec, args):
    folder = ROOT/'captures'/spec['name']
    if (folder/'source.mkv').exists() and (folder/'provenance.json').exists():
        print('Retained complete source', spec['name'], flush=True); return
    wt = args.admission_worktree.resolve()
    cp = str(wt/'target/classes')+os.pathsep+(wt/'target/chaos-classpath.txt').read_text().strip()
    jar = args.mod or wt/'target/sonic3k-chaos-mode/sonic3k-chaos-mode.jar'
    env = os.environ.copy(); env.pop('DISPLAY',None); env.pop('WAYLAND_DISPLAY',None)
    with handle_termination():
        with maven_slot(wt, exclusive=True, estimate=25, kind='chaos-gallery-capture') as lease:
            admitted = datetime.now(timezone.utc).isoformat()
            folder.mkdir(parents=True, exist_ok=True)
            settings = folder/'saves/mods/sonic3k-chaos-mode/settings.txt'
            settings.parent.mkdir(parents=True, exist_ok=True)
            settings.write_text('formatVersion=1\ninterval=5\ndurationQuarters=4\nselected='+spec['effect']+'\nenabled=true\nseed=22\n')
            # Copy the actual controller recipe, never synthesize state from CSV.
            (folder/'input.script').write_text(spec['script']+'\n')
            logs=wt/'target/chaos-gallery'; logs.mkdir(parents=True, exist_ok=True)
            author=['java','-cp',cp,'com.openggf.tools.InputLogAuthorTool',
                    '--script',folder/'input.script','--out',folder/'input.txt']
            author_run=run(author,wt,logs/(spec['name']+'-author.log'),lease,env)
            flags=['--game','s3k','--rom',args.rom,'--zone',spec['zone'],
                   '--act',spec['act'],'--width','400','--main','sonic','--sidekick','none',
                   '--mod',jar,'--input',folder/'input.txt','--frames',spec.get('frames',1200),
                   '--every','1','--interactive-pacing','--audio','--no-video',
                   '--out-dir',folder/'output']
            if 'x' in spec: flags+=['--x',spec['x'],'--y',spec['y']]
            if spec.get('checkpoint'): flags+=['--star-post']
            if 'rings' in spec: flags+=['--rings',spec['rings']]
            command=['java','--enable-native-access=ALL-UNNAMED','-Xmx2g',
                     '-XX:ActiveProcessorCount=4','-Dopenggf.headless.gl=surfaceless-egl',
                     '-Dopenggf.saveRoot='+str(folder/'saves'),'-cp',cp,
                     'com.openggf.tools.GameplayCaptureTool',*flags]
            print('Capturing',spec['name'],spec['zone'],spec['act'],flush=True)
            gameplay=run(command,wt,logs/(spec['name']+'-capture.log'),lease,env)
            encode=run(['ffmpeg','-nostdin','-loglevel','error','-y','-framerate','60',
                        '-i',folder/'output/frames/%05d.png','-i',folder/'output/audio.wav',
                        '-c:v','libx264rgb','-crf','0','-preset','fast','-pix_fmt','rgb24',
                        '-threads','2','-c:a','pcm_s16le',folder/'source.mkv'],
                       wt,logs/(spec['name']+'-encode.log'),lease,env)
            meta=dict(spec,sourceCommit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=wt,text=True).strip(),
                      frames=len(list((folder/'output/frames').glob('*.png'))),
                      game='s3k',character='sonic',sidekick='none',donor='off',width=400,
                      cadence='60Hz outer presentation; interactive pacing; every=1; native PCM',
                      selectedPool='singleton',seed=22,
                      rom=str(args.rom),romSha1=hashlib.sha1(args.rom.read_bytes()).hexdigest(),
                      modSha256=hashlib.sha256(Path(jar).read_bytes()).hexdigest(),
                      admission=dict(admittedUtc=admitted,exclusive=True,author=author_run,
                                     gameplay=gameplay,encode=encode))
            (folder/'provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
            print('Completed',spec['name'],meta['frames'],'frames',flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--admission-worktree',type=Path,required=True)
    p.add_argument('--rom',type=Path,required=True)
    p.add_argument('--mod',type=Path)
    p.add_argument('names',nargs='*')
    args=p.parse_args()
    specs=json.loads((ROOT/'captures.json').read_text())
    names=args.names or [s['name'] for s in specs]
    by_name={s['name']:s for s in specs}
    for name in names: capture(by_name[name],args)

if __name__=='__main__': main()
