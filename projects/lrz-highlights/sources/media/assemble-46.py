from pathlib import Path
import subprocess
r=Path(__file__).resolve().parent
segments=[(60,700),(1700,2030),(2270,2720),(4660,5110),(8820,9520),(12200,12820)]
filters=[]
for i,(start,end) in enumerate(segments):
    filters.append(f"[0:v]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS[v{i}]")
filters.append(''.join(f'[v{i}]' for i in range(len(segments)))+f'concat=n={len(segments)}:v=1:a=0,scale=960:672:flags=neighbor[out]')
subprocess.run(['ffmpeg','-v','error','-i',str(r/'raw-69-lrz3-cold-completion/capture.mp4'),'-filter_complex',';'.join(filters),'-map','[out]','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(r/'46-lrz3-cold-route-through-hpz.mp4')],check=True)
