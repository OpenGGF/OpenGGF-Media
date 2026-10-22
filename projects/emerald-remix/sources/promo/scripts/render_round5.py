#!/usr/bin/env python3
"""Render Emerald Remix round5 review exports. Inputs: edit.py, retained native takes, ROM audio.
Output 1080p60; native speed; no mastering beyond the compositor's existing rough mix.
"""
import json,sys,subprocess
from pathlib import Path
from multiprocessing import Pool
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
import promo_kit as pk
if __name__=='__main__':
 e=pk.load_edit(P/'edit.py');b=e.bf
 ranges={'comparison':(b(4)-12,b(16)+12),'type-and-strip':(b(16)-18,b(28)+18),
 'triple-payoff':(b(28)-18,b(36)+18),'drawn-by-code':(b(36)-24,b(44)+40),
 'clover-spring-rings':(b(44)-24,b(52)+30),'clover-jump-goal':(b(52)-24,b(62)+30),
 'end-card':(b(62)-24,e.end())}
 (P/'previews/ranges.json').write_text(json.dumps({k:{'in':a,'out':z,'fps':60,'size':[1920,1080]} for k,(a,z) in ranges.items()},indent=2)+'\n')
 audio=e.mix()
 todo=[('rough',(0,e.end()))] if sys.argv[1:]==['rough'] else list(ranges.items())
 if sys.argv[1:] and sys.argv[1:]!=['rough']:todo=[x for x in todo if x[0] in sys.argv[1:]]
 for name,(a,z) in todo:
  path=P/'out/emerald-remix-rough.mp4' if name=='rough' else P/f'previews/{name}.mp4'
  wav=P/f'build/r5-{name}.wav';pk.write_wav(wav,audio[a*800:z*800])
  enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','60','-i','-',
   '-i',str(wav),'-c:v','libx264','-threads','4','-preset','fast','-crf','16','-tune','animation','-pix_fmt','yuv420p',
   '-c:a','aac','-b:a','256k','-movflags','+faststart','-shortest',str(path)],stdin=subprocess.PIPE)
  with Pool(4,initializer=pk._init_worker,initargs=(str(P/'edit.py'),)) as pool:
   for i,pixels in enumerate(pool.imap(pk._frame_bytes,range(a,z),chunksize=4)):
    enc.stdin.write(pixels)
    if i%600==0:print(name,i,z-a,flush=True)
  enc.stdin.close()
  if enc.wait():raise RuntimeError(str(path))
  wav.unlink();print('rendered',path,z-a,'frames',flush=True)
