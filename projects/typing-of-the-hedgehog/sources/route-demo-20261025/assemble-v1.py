#!/usr/bin/env python3
"""Compose the 2026-10-25 route demo from real planner/capture outputs at 1x speed.
Requires Python/Pillow, DejaVu Sans and FFmpeg. No fabricated gameplay or editor UI.
The small route overview is drawn from the verified planner's observed path;
coordinates/status are actual native simulation samples. Final film is silent.
"""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--out',default='route-demo.mp4');a=p.parse_args();root=a.root
W,H,FPS=1280,720,60
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
fonts={n:ImageFont.truetype(FONT,n) for n in (14,16,18,20,24,30,38)}
bold={n:ImageFont.truetype(BOLD,n) for n in (18,24,30,38)}
BG='#101820';WHITE='#f1f5fa';MUTED='#a9bbcb';GOLD='#ffd45a';CYAN='#55dce7';GREEN='#93edaa'

def text(d,xy,s,size=20,color=WHITE,strong=False):d.text(xy,s,font=(bold if strong else fonts)[size],fill=color)
def canvas():return Image.new('RGB',(W,H),BG)
def video(path,count):
    proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-an','-frames:v',str(count),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
    try:
        for _ in range(count):
            data=proc.stdout.read(640*280*3)
            assert len(data)==640*280*3,'Missing decoded frame'
            yield Image.frombytes('RGB',(640,280),data)
        assert proc.wait()==0
    finally:
        proc.stdout.close()
        if proc.poll() is None:proc.terminate();proc.wait()

def load(name):
    plan=json.loads((root/(name+'-plan.json')).read_text())['result']
    samples=[]
    for line in (root/(name+'-native.jsonl')).open():
        s=json.loads(line)['sample'];samples.append(dict(frame=s['frame'],actor=s['actors'][0],puppet=s['puppets'][0],world=s['world']['actors'][0]))
    assert plan['nativeVerified'] and plan['status']=='VERIFIED'
    assert all(not s['world']['hurt'] and not s['world']['dead'] for s in samples)
    return plan,samples

def overview(d,plan,sample):
    pts=plan['path'];goal=(plan['request']['targetX'],plan['request']['targetY'])
    xs=[p['x'] for p in pts]+[goal[0]];ys=[p['y'] for p in pts]+[goal[1]]
    scale=min(300/max(1,max(xs)-min(xs)),58/max(1,max(ys)-min(ys)))
    ox=950+(300-(max(xs)-min(xs))*scale)/2;oy=20+(58-(max(ys)-min(ys))*scale)/2
    def pt(x,y):return ox+(x-min(xs))*scale,oy+(y-min(ys))*scale
    d.line([pt(p['x'],p['y']) for p in pts],fill='#4d727f',width=2)
    gx,gy=pt(*goal);d.ellipse((gx-5,gy-5,gx+5,gy+5),outline=GOLD,width=2)
    x,y=pt(sample['actor']['x'],sample['actor']['y']);d.ellipse((x-4,y-4,x+4,y+4),fill=CYAN)
    text(d,(950,82),'OBSERVED ROUTE / TARGET',14,MUTED)

def route_frame(frame,plan,sample,title,detail):
    im=canvas();im.paste(frame.resize((1280,560),Image.Resampling.NEAREST),(0,112));d=ImageDraw.Draw(im)
    text(d,(22,10),title,24,strong=True);text(d,(22,46),detail,20,GOLD)
    text(d,(22,78),f"VERIFIED  |  {plan['expandedNodes']} nodes  |  {plan['simulatedTicks']:,} native simulation ticks",16,GREEN)
    overview(d,plan,sample)
    actor=sample['actor'];puppet=sample['puppet'];req=plan['request']
    settled=(abs(actor['x']-req['targetX'])<=6 and abs(actor['y']-req['targetY'])<=12 and not puppet['airborne'] and abs(puppet['groundSpeed'])<=.25)
    status='SETTLED AT TARGET' if settled else ('AIRBORNE' if puppet['airborne'] else 'FOLLOWING NATIVE TERRAIN')
    text(d,(22,685),f"X {actor['x']:.1f}   Y {actor['y']:.1f}   SPEED {puppet['groundSpeed']:.2f}",18)
    text(d,(750,685),status,18,GREEN if settled else CYAN,strong=True)
    return im

edit=[
 dict(title='Destination and verified route',kind='editorial title over real source still',source='ghz-loop.mkv',source_start_frame=0,source_end_frame=1,output_frames=180),
 dict(title='Green Hill: Run + Hard Stop',kind='authored native-world rehearsal',source='ghz-loop.mkv',source_start_frame=0,source_end_frame=330,output_frames=330),
 dict(title='Emerald Hill: Walk + Gentle Stop',kind='authored native-world rehearsal',source='ehz-gentle.mkv',source_start_frame=0,source_end_frame=305,output_frames=305),
 dict(title='Typing: run, fight, run',kind='actual selected-section attract demo; No-Fail',source='typing-hilltop-current/frames',source_start_frame=234,source_end_frame=1800,output_frames=1566),
 dict(title='Shared steering, separate planners',kind='editorial end card',source='',source_start_frame=0,source_end_frame=0,output_frames=120),
]
at=0
for e in edit:
    e.update(output_start_frame=at,output_start_seconds=at/FPS);at+=e['output_frames'];e.update(output_end_frame=at,output_end_seconds=at/FPS)
(root/'edit-list.json').write_text(json.dumps(dict(fps=FPS,width=W,height=H,audio='silent',source_speed=1,segments=edit),indent=2)+'\n')
meta=[';FFMETADATA1','title=Route planning in action']
for e in edit:
    meta+=['[CHAPTER]','TIMEBASE=1/60',f"START={e['output_start_frame']}",f"END={e['output_end_frame']}",'title='+e['title']]
(root/'chapters.ffmeta').write_text('\n'.join(meta)+'\n')
out=root/a.out
assert not out.exists(),'Use a new output name for another edit'
proc=subprocess.Popen(['ffmpeg','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1280x720','-framerate','60','-i','pipe:0','-f','ffmetadata','-i',str(root/'chapters.ffmeta'),'-map','0:v:0','-map_metadata','1','-map_chapters','1','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
count=0

def emit(im):
    global count
    proc.stdin.write(im.tobytes());count+=1
    if count in (1,180,510,815,2381,2501):im.save(root/f'review-{count:04}.png')
try:
    ghz,gs=load('ghz-loop');ehz,es=load('ehz-gentle')
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(root/'ghz-loop.mkv'),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
    initial=Image.frombytes('RGB',(640,280),raw)
    intro=route_frame(initial,ghz,gs[0],'ROUTE PLANNING IN ACTION','Destination  (5860, 621)  /  Run + Hard Stop')
    d=ImageDraw.Draw(intro);d.rectangle((130,265,1149,470),fill=BG,outline=GOLD,width=2)
    text(d,(170,292),'Pick a target. Generate native inputs.',30,strong=True)
    text(d,(170,344),'Then replay from a fresh world and verify the stop.',24)
    text(d,(170,395),'Real planner output and ROM terrain. No keyed movement.',20,CYAN)
    for _ in range(180):emit(intro)
    for i,frame in enumerate(video(root/'ghz-loop.mkv',330)):emit(route_frame(frame,ghz,gs[i],'1  /  GREEN HILL: THROUGH THE LOOP','RUN  +  HARD STOP     Target (5860, 621)'))
    for i,frame in enumerate(video(root/'ehz-gentle.mkv',305)):emit(route_frame(frame,ehz,es[i],'2  /  EMERALD HILL: SETTLE ON THE SLOPE','WALK  +  GENTLE STOP     Target (400, 624)'))
    files=sorted((root/'typing-hilltop-current/frames').glob('*.png'));assert len(files)==1800
    for index in range(234,1800):
        im=canvas();im.paste(Image.open(files[index]).convert('RGB').resize((1200,672),Image.Resampling.NEAREST),(40,48));d=ImageDraw.Draw(im)
        text(d,(22,8),'3  /  TYPING: RUN > FIGHT > RUN',24,strong=True)
        text(d,(800,15),'ATTRACT TYPING / NO-FAIL / 1x SPEED',16,GOLD)
        emit(im)
    end=canvas();d=ImageDraw.Draw(end)
    text(d,(80,190),'Shared steering. Separate rehearsal systems.',38,strong=True)
    text(d,(80,276),'Stageplay: route search + fresh native-world verification.',24,CYAN)
    text(d,(80,326),'Typing: bounded native corridor rehearsal between fights.',24,CYAN)
    text(d,(80,404),'Both use the same native-input direction / braking kernel.',24)
    text(d,(80,515),'Captured from develop 0df2ac129  |  60 fps  |  silent technical demo',18,MUTED)
    for _ in range(120):emit(end)
finally:
    proc.stdin.close();code=proc.wait()
assert code==0 and count==at,(code,count,at)
print(json.dumps(dict(movie=str(out),frames=count,seconds=count/FPS,chapters=len(edit))))
