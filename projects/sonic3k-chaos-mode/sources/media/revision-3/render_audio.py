#!/usr/bin/env python3
"""ROM-native continuous HCZ2 bed and ghost reference cues for gallery v3.

Origin: 2026-10-14 Chaos media revision. Uses maintained FmSfxRenderTool, never
an invented soundtrack. Reference92/8A files are NOT automatically dubbed over
the genuine ghost recording. All Java/media execution shares scheduler leases.
"""
from pathlib import Path
import argparse,hashlib,json,os,sys,subprocess
from datetime import datetime,timezone

P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
from capture import run
sys.path.insert(0,os.environ.get('OPENGGF_QUEUE_ROOT','/home/farrell/code/projects/OpenGGF')+'/tools/testing')
from maven_queue import maven_slot,inherited_slot,handle_termination

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--admission-worktree',type=Path,required=True)
    ap.add_argument('--rom',type=Path,required=True)
    args=ap.parse_args();wt=args.admission_worktree.resolve()
    cp=str(wt/'target/classes')+os.pathsep+(wt/'target/chaos-classpath.txt').read_text().strip()
    env=os.environ.copy();env.pop('DISPLAY',None);env.pop('WAYLAND_DISPLAY',None)
    with handle_termination(),maven_slot(wt,exclusive=True,estimate=30,kind='chaos-gallery-rom-audio') as lease:
        logs=wt/'target/chaos-gallery';logs.mkdir(exist_ok=True)
        runs=[]
        for kind,cue,seconds in [('music','04',270),('sfx','92',4),('sfx','8A',4)]:
            dest=P/'assets'/('hcz2' if kind=='music' else 'ghost-'+cue.lower())
            dest.mkdir(parents=True,exist_ok=True)
            cmd=['java','--enable-native-access=ALL-UNNAMED','-Xmx1g','-XX:ActiveProcessorCount=2',
                 '-cp',cp,'com.openggf.tools.audio.FmSfxRenderTool','--game','s3k','--rom',args.rom,
                 '--'+kind,cue,'--rate','48000','--max-seconds',seconds,'--out',dest]
            runs.append(run(cmd,wt,logs/('audio-'+cue+'.log'),lease,env))
            # Raw chip write logs are one-off diagnostics, not production inputs.
            for f in dest.glob('*-ym-writes.txt'):f.unlink()
            for f in dest.glob('*-fm.wav'):f.unlink()
        bed=P/'assets/hcz2/s3k-music-04-mix.wav'
        (P/'assets/audio-provenance.json').write_text(json.dumps(dict(sourceCommit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=wt,text=True).strip(),
            purpose='Continuous naturally looping ROM HCZ2 bed; standalone92/8A are review references only; finalghost retains native captured mixedPCM.',
            romSha1=hashlib.sha1(args.rom.read_bytes()).hexdigest(),bedSha256=hashlib.sha256(bed.read_bytes()).hexdigest(),
            renderedUtc=datetime.now(timezone.utc).isoformat(),admittedRuns=runs),indent=2)+'\n')
        config=json.loads((P/'audio.json').read_text());config['bed']=str(bed.relative_to(P))
        (P/'audio.json').write_text(json.dumps(config,indent=2)+'\n')
        print('Rendered continuous270s HCZ2 bed and nativeghost referencePCM',flush=True)

if __name__=='__main__':main()
