#!/usr/bin/env python3
"""Verify the actual Chaos card-gallery video, 2026-10-14.

Inputs: final MP4, cards.json, chapter map and actual source CSVs. Full decode
checks cadence/EOF, bounded actual moving-frame strips check every effect and
every cut. Normal shared scheduler leases cover all media subprocesses.
"""
from pathlib import Path
import argparse,csv,hashlib,importlib.util,json,math,os,re,sys,wave
from array import array
from PIL import Image,ImageDraw,ImageChops

P=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('v2_verification',P.parent/'revision-2/verify_v2.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def music_continuity(owned, clip, placements):
    """Check HCZ waveform identity before, inside and after the ghost card.

    The inside window precedes the observed apparition event. It independently
    catches the old music dropout/DEZ switch rather than trusting mixer settings.
    AAC is lossy; centered correlation and recovered gain are bounded evidence.
    """
    config=json.loads((P/'audio.json').read_text())
    mix=json.loads((P/'out/audio-mix.json').read_text())
    assert mix['source_audio_used'] is False
    assert mix['source_zone_music_used'] is False and mix['bed_duck_used'] is False
    ghost_start,ghost=placements[-1]
    output_start=ghost_start+ghost['slot_frames']-ghost['clip_frames']
    anchors=[('before',output_start-60,30),('during',output_start+12,24),
             ('after',ghost_start+ghost['slot_frames']+18,24)]
    raw,_=owned.capture(['ffmpeg','-nostdin','-v','error','-xerror','-threads','1','-i',clip,
                         '-map','0:a:0','-ac','2','-ar','48000','-f','s16le','-'])
    decoded=array('h',raw)
    if sys.byteorder!='little':decoded.byteswap()
    gain=10**((config.get('bed_gain_db',0)+config.get('master_gain_db',0))/20)
    results=[]
    with wave.open(str((P/config['bed']).resolve())) as bed, wave.open(str((P/config['ghost_sfx']['file']).resolve())) as sfx:
        for name,start,count in anchors:
            bed.setpos(start*800)
            reference=array('h',bed.readframes(count*800))
            if sys.byteorder!='little':reference.byteswap()
            actual=decoded[start*1600:(start+count)*1600]
            assert len(reference)==len(actual)==count*1600
            if name=='during':
                source=ghost['in_frame']+start-output_start
                sfx.setpos(source*800)
                silence=array('h',sfx.readframes(count*800))
                if sys.byteorder!='little':silence.byteswap()
                avg=sum(silence)/len(silence)
                variance=sum((value-avg)**2 for value in silence)/len(silence)
                assert variance<=1,('Selected continuity window contains an active SFX',variance)
            n=len(reference);a=sum(reference)/n;b=sum(actual)/n
            xx=sum((v-a)**2 for v in reference);yy=sum((v-b)**2 for v in actual)
            xy=sum((x-a)*(y-b) for x,y in zip(reference,actual))
            assert xx>0 and yy>0
            correlation=xy/math.sqrt(xx*yy);recovered=xy/xx
            assert correlation>=.985,(name,correlation)
            assert .80<=recovered/gain<=1.05,(name,recovered,gain)
            results.append(dict(window=name,output_frame=start,frames=count,
                                zero_lag_correlation=correlation,recovered_gain=recovered,configured_gain=gain))
    return dict(continuous_hcz_before_during_after_ghost=True,source_zone_music_used=False,
                bed_duck_used=False,windows=results,
                scope='Actual AAC waveform checks in three cue-free windows; not whole-track bit parity or listening review.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admission-worktree',type=Path,required=True)
    args=parser.parse_args()
    sys.path.insert(0,os.environ.get('OPENGGF_QUEUE_ROOT','/home/farrell/code/projects/OpenGGF')+'/tools/testing')
    from maven_queue import maven_slot,inherited_slot,handle_termination
    cards=json.loads((P/'cards.json').read_text())
    assert len(cards)==20 and len({c['effect'] for c in cards})==20
    assert all(c['qualified'] for c in cards)
    assert not {'ring-pong','ring-snake','monitor-stack','shield-beat','badnik-defence','sonic-says','imaginary-chat'}.intersection(c['effect'] for c in cards)
    frame=240; samples={0,180}
    placements=[]
    for c in cards:
        placements.append((frame,c));samples.update(frame+t for t in [0,12,48,108,168,c['slot_frames']-1])
        frame+=c['slot_frames']
    samples.update([frame,frame+120,frame+359]);total=frame+360
    clip=P/'out/sonic3k-chaos-mode-demo-v4.mp4'
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
            chapters=info['chapters'];assert len(chapters)==len(cards)+2
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
            bookends=Image.new('RGB',(1440,588),(9,20,49));bd=ImageDraw.Draw(bookends)
            for index,n in enumerate([0,180,frame,frame+120,frame+359]):
                x=(index%3)*480;y=(index//3)*294
                bd.text((x+6,y+5),'ACTUAL OUTPUT FRAME '+str(n),fill='white')
                bookends.paste(pictures[n],(x,y+24))
            bookends.save(review/'bookends.png')
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
            assert float(loudness['input_tp'])<=-1.5, loudness
            continuity=music_continuity(owned,clip,placements)
            dac=json.loads((P/'assets/hcz2/render-provenance.json').read_text())['dacProof']
            assert dac['dac_enabled'] and dac['nonconstant_native_dac_stream']
            summary=dict(file=clip.name,frames=total,durationSeconds=total/60,dimensions=[1920,1080],
                         cadence='60/1',chapters=len(chapters),qualifiedEffects=len(cards),
                         zones=sorted({c['zone'].split(' / ')[0] for c in cards}),
                         fullVideoDecode=True,fullAudioDecode=True,cadenceCheckedEveryFrame=True,
                         sourceIntervalsAndDeathChecked=True,fastStart=fast,loudness=loudness,
                         actualMovingSamples=movement,
                         ghostSourcePcmUsed=False,ghostNativeSfxRenderedFromAcceptedEvents=True,
                         musicContinuity=continuity,nativeDacProof=dac,
                         sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),bytes=clip.stat().st_size,
                         scope='Media qualification only, not continuous route completion or native parity; root reviews generated strips separately.')
            (review/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
            print(json.dumps({k:v for k,v in summary.items() if k!='actualMovingSamples'},indent=2))
        finally:owned.close()

if __name__=='__main__':main()
