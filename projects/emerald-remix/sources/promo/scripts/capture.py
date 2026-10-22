#!/usr/bin/env python3
"""Emerald Remix promo capture driver, 2026-10-22; InputLogAuthorTool/GameplayCaptureTool only.
Inputs: authored script, supplied REV01 ROM, packaged example. No state seeding or desktop access.
Run from the assigned checkout; all generated durable products stay in the production folder.
"""
import hashlib, json, os, shlex, subprocess, sys
from pathlib import Path
ROOT=Path('/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach')
PROD=Path('/home/farrell/Videos/OGGF/emerald-remix-promo')
JAVA='/usr/lib/jvm/java-25-openjdk/bin/java'
CP=str(ROOT/'target/classes')+':'+(ROOT/'target/examples-classpath.txt').read_text().strip()
BASE=[JAVA,'--enable-native-access=ALL-UNNAMED','-Xmx2g','-Djava.awt.headless=true','-Duser.dir='+str(ROOT/'target/promo-capture-prefs'),'-Dopenggf.headless.gl=surfaceless-egl','-cp',CP]
ENV=os.environ.copy()
for key in ['DISPLAY','WAYLAND_DISPLAY']: ENV.pop(key,None)
ENV['JAVA_HOME']='/usr/lib/jvm/java-25-openjdk'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(cmd, label):
    record={'label':label,'cwd':str(ROOT),'env':{'unset':['DISPLAY','WAYLAND_DISPLAY'],'JAVA_HOME':ENV['JAVA_HOME']},'argv':cmd}
    with (PROD/'scripts/commands.jsonl').open('a') as f: f.write(json.dumps(record)+'\n')
    log=ROOT/'target'/f'promo-{label}.log'
    with log.open('w') as f:
        p=subprocess.run(cmd,cwd=ROOT,env=ENV,stdout=f,stderr=subprocess.STDOUT)
    lines=log.read_text(errors='replace').splitlines()
    print('\n'.join(lines[-18:]),flush=True)
    if p.returncode: raise SystemExit(f'FAILED {label}: {p.returncode}; {log}')
    return lines
if __name__=='__main__':
    prefs=ROOT/'target/promo-capture-prefs'
    prefs.mkdir(exist_ok=True)
    (prefs/'config.yaml').write_text((PROD/'scripts/capture-config.yaml').read_text())
    mode=sys.argv[1]
    if mode=='author':
        name=sys.argv[2]; src=PROD/'inputs'/f'{name}.script'; out=src.with_suffix('.bk2')
        run(BASE+['com.openggf.tools.InputLogAuthorTool','--script',str(src),'--out',str(out),'--game','s2'],f'author-{name}')
    elif mode=='capture':
        name,script,zone,frames,every=sys.argv[2:7]; flags=sys.argv[7:]
        out=PROD/'captures'/name
        width='400'
        if '--width' in flags:
            i=flags.index('--width'); width=flags[i+1]; del flags[i:i+2]
        video='--video' in flags
        if video: flags.remove('--video')
        if out.exists(): raise SystemExit(f'Preserving existing capture {out}')
        args=['--game','s2','--rom',str(ROOT/'s2.gen'),'--zone',zone,'--act','1','--width',width,'--main','sonic','--sidekick','none','--input',str(PROD/'inputs'/f'{script}.bk2'),'--frames',frames,'--every',every,'--fps','60','--no-video','--out-dir',str(out)]
        if '--stock' in flags: flags.remove('--stock')
        else: args+=['--mod',str(ROOT/'target/emerald-remix/emerald-remix.jar')]
        args+=flags
        if video:
            args.remove('--no-video'); args+=['--scale','3']
        lines=run(BASE+['com.openggf.tools.GameplayCaptureTool']+args,name)
        metadata={'source_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_status':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),'rom_sha1':hashlib.sha1((ROOT/'s2.gen').read_bytes()).hexdigest(),'mod_sha256':sha(ROOT/'target/emerald-remix/emerald-remix.jar') if '--mod' in args else None,'input_sha256':sha(PROD/'inputs'/f'{script}.bk2'),'capture_preferences':(ROOT/'target/promo-capture-prefs/config.yaml').read_text(),'source_kind':'normal gameplay with scripted BK2 input','entry':('positioned direct act load; start centre '+args[args.index('--x')+1]+','+args[args.index('--y')+1]+'; no ring, velocity, clock or immunity seeds' if '--x' in args else 'cold direct act load; no position, rings, velocity, clock or immunity writes'),'audio':'silent; no --audio','width':int(width),'fps':60,'stride':int(every),'argv':BASE+['com.openggf.tools.GameplayCaptureTool']+args,'boot_evidence':[line for line in lines if any(s in line.lower() for s in ['clover','remix','emerald hill','zonekey','zone 11','loaded level','nullaudio','surfaceless'])],'report':lines[-7:]}
        (out/'provenance.json').write_text(json.dumps(metadata,indent=2)+'\n')
