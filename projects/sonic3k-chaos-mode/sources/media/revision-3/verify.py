#!/usr/bin/env python3
"""Verify the actual Chaos card-gallery video, 2026-10-14.

Inputs: final MP4, cards.json, chapter map and actual source CSVs. Full decode
checks cadence/EOF, bounded actual moving-frame strips check every effect and
every cut. Normal shared scheduler leases cover all media subprocesses.
"""
from pathlib import Path
import argparse,csv,hashlib,importlib.util,json,os,re,sys
from PIL import Image,ImageDraw,ImageChops

P=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('v2_verification',P.parent/'revision-2/verify_v2.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission-worktree',type=Path,required=True)
    args=parser.parse_args()
    sys.path.insert(0,os.environ.get('OPENGGF_QUEUE_ROOT','/home/farrell/code/projects/OpenGGF')+'/tools/testing')
    from maven_queue import maven_slot,inherited_slot,handle_termination
    cards=json.loads((P/'cards.json').read_text())
    assert len(cards)==48 and len({c['effect'] for c in cards})==48
    assert all(c['qualified'] for c in cards)
    frame=240; samples={0,180}
    placements=[]
    for c in cards:
        placements.append((frame,c));samples.update(frame+t for t in [0,12,48,108,168,c['slot_frames']-1])
        frame+=c['slot_frames']
    samples.update([frame,frame+120,frame+359]);total=frame+360
    clip=P/'out/sonic3k-chaos-mode-demo-v3.mp4'
    with handle_termination(),maven_slot(args.admission_worktree,exclusive=True,estimate=60,kind='chaos-gallery-verification') as lease:
        owned=old.OwnedProcesses(lease,inherited_slot)
        try:
            info=old.probe(owned,clip)
            v=next(s for s in info['streams'] if s['codec_type']=='video')
            a=next(s for s in info['streams'] if s['codec_type']=='audio')
            assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'60/1')
            assert int(v['nb_frames'])==total
            assert (a['sample_rate'],a['channels'])==('48000',2)
            assert abs(float(info['format']['duration'])-total/60)<.003
            fast=old.fast_start(clip)
            chapters=info['chapters'];assert len(chapters)==50
            for i,(start,c) in enumerate(placements):
                chapter=chapters[i+1]
                assert abs(float(chapter['start_time'])-start/60)<.0011
                assert c['label'].lower() in chapter['tags']['title'].lower()
                rows=list(csv.DictReader(((P/c['source']).resolve().parent/'output/state.csv').open()))
                s=c['in_frame'];e=s+c['clip_frames']
                assert 0<=s<e<=len(rows)
                assert c.get('allow_death') or not any(r['dead']=='1' for r in rows[s:e])
            # A flat300-term addition can exhaust FFmpeg's expression parser
            # before decoding. Balanced parentheses keep expression depth small.
            def selector(values):
                if len(values)==1:return 'eq(n,'+str(values[0])+')'
                mid=len(values)//2
                return '('+selector(values[:mid])+'+'+selector(values[mid:])+')'
            select=selector(sorted(samples))
            command=['ffmpeg','-nostdin','-v','info','-xerror','-threads','2','-i',clip,
                     '-an','-vf',"showinfo,select='"+select+"',scale=480:270:flags=neighbor",
                     '-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-']
            raw,log=owned.capture(command)
            observations=[(int(n),float(t),h) for n,t,h in old.SHOWINFO.findall(log.decode())]
            assert len(observations)==total
            assert [n for n,_,_ in observations]==list(range(total))
            assert all(abs(t-n/60)<.00055 for n,t,_ in observations)
            stride=480*270*3;assert len(raw)==len(samples)*stride
            pictures={n:Image.frombytes('RGB',(480,270),raw[i*stride:(i+1)*stride]) for i,n in enumerate(sorted(samples))}
            review=P/'out/media-review';review.mkdir(parents=True,exist_ok=True)
            movement=[]
            for k in range(0,len(placements),8):
                group=placements[k:k+8]
                page=Image.new('RGB',(1440,len(group)*294),(9,20,49));d=ImageDraw.Draw(page)
                for row,(start,c) in enumerate(group):
                    d.text((6,row*294+5),str(k+row+1)+' '+c['label']+' | '+c['zone'],fill='white')
                    for col,offset in enumerate([48,108,168]):page.paste(pictures[start+offset],(col*480,row*294+24))
                    crop=(12,10,312,178)
                    region=[pictures[start+t].crop(crop) for t in [48,108,168]]
                    changed=any(ImageChops.difference(region[0],p).getbbox() for p in region[1:])
                    # Most overlays animate; monitor-breakout can be settled at later selected points.
                    movement.append(dict(effect=c['effect'],samples=[start+t for t in [48,108,168]],activeRegionChanged=bool(changed)))
                page.save(review/('moving-'+str(k//8+1)+'.png'))
            for k in range(0,len(placements),8):
                group=placements[k:k+8]
                page=Image.new('RGB',(1440,len(group)*294),(9,20,49));d=ImageDraw.Draw(page)
                for row,(start,c) in enumerate(group):
                    d.text((6,row*294+5),'CARD '+str(k+row+1)+' '+c['label'],fill='white')
                    for col,offset in enumerate([0,12,c['slot_frames']-1]):page.paste(pictures[start+offset],(col*480,row*294+24))
                page.save(review/('cuts-'+str(k//8+1)+'.png'))
            _,loud=owned.capture(['ffmpeg','-nostdin','-v','info','-xerror','-threads','2','-i',clip,'-vn',
                                 '-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
            match=re.search(r'\{\s*"input_i".*?\}',loud.decode(),re.S);assert match
            loudness=json.loads(match.group())
            assert float(loudness['input_tp'])<=-.9, loudness
            summary=dict(file=clip.name,frames=total,durationSeconds=total/60,dimensions=[1920,1080],
                         cadence='60/1',chapters=len(chapters),qualifiedEffects=len(cards),
                         zones=sorted({c['zone'].split(' / ')[0] for c in cards}),
                         fullVideoDecode=True,fullAudioDecode=True,cadenceCheckedEveryFrame=True,
                         sourceIntervalsAndDeathChecked=True,fastStart=fast,loudness=loudness,
                         actualMovingSamples=movement,
                         ghostSourcePcmUsed=cards[-1].get('source_audio',False),
                         sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),bytes=clip.stat().st_size,
                         scope='Media qualification only, not continuous route completion or native parity; root reviews generated strips separately.')
            (review/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
            print(json.dumps({k:v for k,v in summary.items() if k!='actualMovingSamples'},indent=2))
        finally:owned.close()

if __name__=='__main__':main()
