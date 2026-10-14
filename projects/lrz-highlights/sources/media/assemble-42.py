from pathlib import Path
import subprocess
root=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-v','error','-i',str(root/'raw-63-lrz3-platform-mask/capture.mp4'),'-frames:v','900','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(root/'42-lrz3-platform-emergence.mp4')],check=True)
