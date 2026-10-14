from pathlib import Path
import subprocess
root=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-v','error','-i',str(root/'raw-62-lrz3-platform-art/capture.mp4'),'-frames:v','300','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(root/'41-lrz3-checkpoint-platforms.mp4')],check=True)
