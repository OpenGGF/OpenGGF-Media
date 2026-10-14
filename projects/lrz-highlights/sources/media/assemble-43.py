from pathlib import Path
import subprocess
root=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-v','error','-ss',str(1450/60),'-i',str(root/'raw-65-lrz3-boss-lifetime/capture.mp4'),'-frames:v','1200','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(root/'43-lrz3-boss-first-cycle.mp4')],check=True)
