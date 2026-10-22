#!/usr/bin/env python3
"""Render all changed-section rough-cut reviews through promo_kit at full 1920x1080 / 60Hz.
Inputs: edit.py, captures and ROM-derived audio; no retiming. Origin: Emerald Remix promo 2026-10-22.
Ranges are output frames [in,out); audio is the same edit mix at those sample positions.
"""
import json,sys,subprocess
from pathlib import Path
from multiprocessing import Pool
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
import promo_kit as pk
RANGES={'cold-open':(0,180),'comparison':(125,543),'title-drop':(525,831),
        'remix-build-run':(795,1236),'clover-entrance':(1200,1370),'clover-pixels':(1200,1500),
        'clover-high-road':(1480,1790),'clover-finish':(1770,2215),'end-card':(2175,2602)}
if __name__=='__main__':
 e=pk.load_edit(ROOT/'edit.py');out=ROOT/'previews';out.mkdir(exist_ok=True)
 audio=e.mix()
 for name,(a,b) in RANGES.items():
  if len(sys.argv)>1 and name not in sys.argv[1:]:continue
  wav=out/(name+'.wav');pk.write_wav(wav,audio[a*800:b*800])
  cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','60','-i','-',
       '-i',str(wav),'-c:v','libx264','-threads','4','-preset','fast','-crf','18','-tune','animation','-pix_fmt','yuv420p',
       '-c:a','aac','-b:a','256k','-movflags','+faststart','-shortest',str(out/(name+'.mp4'))]
  enc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
  with Pool(4,initializer=pk._init_worker,initargs=(str(ROOT/'edit.py'),)) as pool:
   for pixels in pool.imap(pk._frame_bytes,range(a,b),chunksize=4):enc.stdin.write(pixels)
  enc.stdin.close()
  if enc.wait():raise RuntimeError(name+' encode failed')
  wav.unlink();print(name,a,b,(b-a)/60,flush=True)
 (out/'ranges.json').write_text(json.dumps({k:{'in':v[0],'out':v[1],'fps':60,'size':[1920,1080]} for k,v in RANGES.items()},indent=2)+'\n')
