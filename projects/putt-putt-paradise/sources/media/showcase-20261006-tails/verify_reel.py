"""Check continuous normal-speed cadence and create the cut review contact sheet."""
from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent
reel=root/'putt-putt-paradise-highlights.mp4';edit=json.loads((root/'edit-list.json').read_text())
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(reel)],text=True))
pts=[float(f['best_effort_timestamp_time']) for f in probe['frames']]
deltas=[b-a for a,b in zip(pts,pts[1:])]
assert len(pts)==edit['total_frames'] and all(abs(d-1/30)<1e-5 for d in deltas)
(root/'cadence.json').write_text(json.dumps(dict(frames=len(pts),first_pts=pts[0],last_pts=pts[-1],minimum_delta=min(deltas),maximum_delta=max(deltas),continuous_30_fps=True),indent=2)+'\n')
qa=root/'qa';qa.mkdir(exist_ok=True)
canvas=Image.new('RGB',(1280,648),'#071425');draw=ImageDraw.Draw(canvas)
for c in edit['clips']:
 t=c['reel_frame_start']/30+min(2,c['frames']/60)
 if c['order']==1:t=6.3
 if c['order']==3:t=14.75
 path=qa/('%02d.png'%c['order'])
 subprocess.run(['ffmpeg','-v','error','-nostdin','-ss',str(t),'-i',str(reel),'-frames:v','1','-y',str(path)],check=True)
 im=Image.open(path).convert('RGB').resize((320,180))
 x=c['order']%4*320;y=c['order']//4*216
 canvas.paste(im,(x,y));draw.text((x+4,y+184),str(c['order']+1)+' | '+str(round(t,2))+'s',fill='#f5e9bb')
canvas.save(root/'cut-contact-sheet.png')
print('Verified cadence and generated 12-cut contact sheet')
