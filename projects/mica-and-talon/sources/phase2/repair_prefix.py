"""Render the final 198-frame wide opening; patch an in-flight earlier render after it completes.
A fresh render_all.py uses this same final edit and does not require this repair.
"""
import os,sys,subprocess
from pathlib import Path
P=Path(__file__).parent;R=Path('/mnt/LinuxData/T3/worktrees/OpenGGF/t3-66af4c18');os.environ.update(MT_CHECKOUT=str(R),MT_TAKE='phase2',MT_VERTICAL='0',PROMO_FONT_DIRS=str(P/'fonts'));sys.path.insert(0,str(R/'tools/media'))
import promo_kit as kit
if sys.argv[1]=='prefix':
 e=kit.load_edit(P/'edit/edit.py');out=P/'out/prefix-final.mp4';enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','60','-i','-','-an','-c:v','libx264','-preset','fast','-crf','14','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 for f in range(198):enc.stdin.write(e.render_frame(f).tobytes())
 enc.stdin.close();assert enc.wait()==0
 kit.write_wav(P/'out/final-mix.wav',e.mix())
else:
 out=P/'out/master-16x9.mp4';old=P/'out/pre-prefix-master-16x9.mp4';out.replace(old)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'out/prefix-final.mp4'),'-i',str(old),'-i',str(P/'out/final-mix.wav'),'-filter_complex','[1:v]trim=start_frame=198,setpts=PTS-STARTPTS[tail];[0:v][tail]concat=n=2:v=1:a=0[v];[2:a]volume=-5dB[a]','-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','14','-c:a','aac','-b:a','192k','-pix_fmt','yuv420p','-movflags','+faststart','-shortest',str(out)],check=True)
