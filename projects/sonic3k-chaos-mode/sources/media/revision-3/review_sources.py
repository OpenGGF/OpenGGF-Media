#!/usr/bin/env python3
"""Bounded source review/compaction for the 2026-10-14 Chaos gallery.

Reads actual CSV first. Independent pixel/PCM equality before deleting ONLY
new, redundant PNG/WAV media. Retains lossless masters, recipes and provenance.
Every decoder/probe holds ordinary shared scheduler admission.
"""
from pathlib import Path
import argparse,csv,hashlib,importlib.util,json,os,re,signal,subprocess,sys
from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('old_archive',P.parent/'revision-2/archive_sources.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--admission-worktree',type=Path,required=True)
    ap.add_argument('--compact',action='store_true')
    ap.add_argument('--effects',default='',help='Only changed effect IDs; retain earlier review artifacts')
    args=ap.parse_args()
    sys.path.insert(0,os.environ.get('OPENGGF_QUEUE_ROOT','/home/farrell/code/projects/OpenGGF')+'/tools/testing')
    from maven_queue import maven_slot,inherited_slot,handle_termination
    old.INHERITED=inherited_slot
    with handle_termination(),maven_slot(args.admission_worktree,exclusive=True,estimate=90,kind='chaos-source-review') as lease:
        old.LEASE=lease
        out=P/'review';out.mkdir(exist_ok=True)
        cards=json.loads((P/'cards.json').read_text())
        selected={x for x in args.effects.split(',') if x}
        if selected:cards=[c for c in cards if c['effect'] in selected]
        selected_folders={(P/c['source']).resolve().parent for c in cards}
        checksfile=P/'lossless-source-checks.json'
        checks=json.loads(checksfile.read_text()) if checksfile.exists() else {}
        # Equality check all completed new takes, including later rejected takes.
        for folder in sorted((P/'captures').iterdir()):
            if selected and folder.resolve() not in selected_folders:continue
            master=folder/'source.mkv'
            if not master.exists():continue
            digest=hashlib.sha256(master.read_bytes()).hexdigest()
            if folder.name not in checks:
                checks[folder.name]=old.verify_master(folder)
                checksfile.write_text(json.dumps(checks,indent=2)+'\n')
            assert checks[folder.name]['masterSha256']==digest
            if args.compact:
                import shutil
                images=folder/'output/frames'
                if images.exists():shutil.rmtree(images)
                (folder/'output/audio.wav').unlink(missing_ok=True)
            print('LOSSLESS',folder.name,checks[folder.name]['frames'],flush=True)
        summary=[]
        audio=json.loads((P/'audio.json').read_text())
        audio_measurements={}
        audio_files=[] if selected else [('bed',P/audio['bed']),('ghost',(P/cards[-1]['source']).resolve())]
        for key,file in audio_files:
            prefix=[] if key=='bed' else ['-ss',str(cards[-1]['in_frame']/60),'-t',str(cards[-1]['clip_frames']/60)]
            child=subprocess.Popen(['ffmpeg','-nostdin','-v','info',*prefix,'-i',str(file),'-vn','-af',
                                    'loudnorm=I=-17:TP=-1.5:LRA=11:print_format=json','-f','null','-'],
                                   stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                                   start_new_session=True,**inherited_slot(lease))
            try:_,measurement=child.communicate()
            except BaseException:
                os.killpg(child.pid,signal.SIGTERM)
                try:child.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid,signal.SIGKILL);child.communicate()
                raise
            assert child.returncode==0
            match=re.search(r'\{\s*"input_i".*?\}',measurement.decode(),re.S);assert match
            audio_measurements[key]=json.loads(match.group())
        if audio_measurements:(out/'audio-source-loudness.json').write_text(json.dumps(audio_measurements,indent=2)+'\n')
        for begin in range(0,len(cards),8):
            group=cards[begin:begin+8]
            page=Image.new('RGB',(1200,len(group)*254),(9,20,49));d=ImageDraw.Draw(page)
            for row,c in enumerate(group):
                source=(P/c['source']).resolve();folder=source.parent
                rows=list(csv.DictReader((folder/'output/state.csv').open()))
                start=c['in_frame'];end=start+c['clip_frames']
                assert 0<=start<end<=len(rows),(c['effect'],end,len(rows))
                interval=rows[start:end]
                deaths=[int(r['frame']) for r in interval if r['dead']=='1']
                frames=[start+12,start+c['clip_frames']//2,end-13]
                d.text((5,row*254+8),str(begin+row+1)+' '+c['effect']+' | '+c['zone']+' | '+str(frames),fill='white')
                for col,n in enumerate(frames):
                    raw=old.run(['ffmpeg','-nostdin','-v','error','-threads','1','-ss',str(n/60),'-i',source,'-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'])
                    assert len(raw)==400*224*3
                    picture=Image.frombytes('RGB',(400,224),raw)
                    page.paste(picture,(col*400,row*254+30))
                    # Individual actual representative images support root QA.
                    picture.save(out/(c['effect']+'-'+str(n)+'.png'))
                summary.append(dict(effect=c['effect'],zone=c['zone'],source=c['source'],
                                    in_frame=start,out_frame=end,source_frames=len(rows),
                                    death_frames=deaths[:1],sample_frames=frames,
                                    x_range=[min(int(r['x']) for r in interval),max(int(r['x']) for r in interval)],
                                    rings_range=[min(int(r['rings']) for r in interval),max(int(r['rings']) for r in interval)]))
            stem='sources-'+('-'.join(sorted(selected))+'-' if selected else '')+str(begin//8+1)
            page.save(out/(stem+'.png'))
        summary_name='source-review'+('-'+'-'.join(sorted(selected)) if selected else '')+'.json'
        (out/summary_name).write_text(json.dumps(summary,indent=2)+'\n')
        print('SOURCE REVIEW',len(summary),'cards',flush=True)

if __name__=='__main__':main()
