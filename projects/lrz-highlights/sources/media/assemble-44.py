from pathlib import Path
import subprocess
root=Path(__file__).resolve().parent
# Opening encounter, then final hit through results and the Hidden Palace load.
subprocess.run(['ffmpeg','-v','error','-i',str(root/'raw-67-lrz3-boss-completion/capture.mp4'),'-filter_complex','[0:v]trim=start_frame=1450:end_frame=2100,setpts=PTS-STARTPTS[a];[0:v]trim=start_frame=5700:end_frame=7300,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(root/'44-lrz3-boss-clear-and-hpz.mp4')],check=True)
