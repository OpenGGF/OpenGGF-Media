"""Verify final native source ranges after two menu holds; task e0603654 r2.
Inputs: existing film/chapters/source PNGs and PCM; no engine/display/device.
One bounded decode supplies all sampled frames; observations are comparison only.
"""
from pathlib import Path
import hashlib, json, subprocess, wave
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FILM = ROOT/'out/mutator-lab-complete-showcase.mp4'
chap = json.loads((ROOT/'out/chapters.json').read_text())
checks = {}; position = 0
for segment in chap['segments']:
    if segment['id'] not in ('title', 'outro'):
        for offset in (segment['frames']//4, segment['frames']//2, 3*segment['frames']//4):
            checks.setdefault(position+offset, []).extend((segment['id'], source, offset) for source in segment['sources'])
    position += segment['frames']
def combine(terms):
    if len(terms) == 1: return terms[0]
    half = len(terms)//2
    return '('+combine(terms[:half])+')+('+combine(terms[half:])+')'
selection = combine(['eq(n\\,%d)'%f for f in sorted(checks)])
cmd = ['ffmpeg','-v','error','-xerror','-threads','4','-filter_threads','2','-i',str(FILM),'-vf','select='+selection,
       '-fps_mode','vfr','-threads','2','-f','rawvideo','-pix_fmt','rgb24','-']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
results = []
try:
    for output_frame in sorted(checks):
        data = bytearray()
        while len(data) < 1920*1080*3:
            piece = proc.stdout.read(1920*1080*3-len(data))
            if not piece: raise RuntimeError('missing decoded sample %d: %s'%(output_frame,proc.stderr.read().decode(errors='replace')))
            data.extend(piece)
        image = Image.frombytes('RGB',(1920,1080),bytes(data))
        for identifier, source, offset in checks[output_frame]:
            x,y,w,h = source['crop']
            sample = np.asarray(image.crop((x,y,x+w,y+h)).resize((320,224),Image.Resampling.NEAREST)).reshape(-1)[::5].astype(np.int16)
            frame = source['frames'][0]+offset
            distances = {}
            for delta in (-2,-1,0,1,2):
                path = Path(source['take'])/'capture/frames'/('%05d.png'%(frame+delta))
                if path.is_file():
                    with Image.open(path) as original:
                        native = np.asarray(original.convert('RGB')).reshape(-1)[::5].astype(np.int16)
                    distances[delta] = round(float(np.abs(sample-native).mean()),3)
            best = min(distances,key=distances.get)
            results.append({'segment':identifier,'output_frame':output_frame,'source_frame':frame,
                            'best_offset':best,'distances':distances,
                            'mismatch':best!=0 and distances[best]<distances[0]-.5})
    remainder = proc.stdout.read()
    if remainder: raise RuntimeError('unexpected extra decoded samples')
    stderr = proc.stderr.read().decode(errors='replace')
    exit_code = proc.wait(timeout=120)
finally:
    if proc.poll() is None:
        proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill();proc.wait(timeout=10)
assert exit_code == 0, stderr

def wav(path):
    with wave.open(str(path)) as audio:
        assert (audio.getframerate(),audio.getnchannels(),audio.getsampwidth())==(48000,2,2)
        return audio.readframes(audio.getnframes())
edited = wav(ROOT/'work/edit/audio.wav'); cache={}; position=0; audio_errors=[]; compared=0
for segment in chap['segments']:
    source = next(x for x in segment['sources'] if x['audio'])
    start,end = source['audio_samples'];n=end-start
    if source['take'] not in cache: cache[source['take']]=wav(Path(source['take'])/'capture/audio.wav')
    native = cache[source['take']][start*4:end*4]
    current = edited[position*4:(position+n)*4]
    if len(native)!=n*4 or current[481*4:(n-481)*4]!=native[481*4:(n-481)*4]: audio_errors.append(segment['id'])
    compared += max(0,n-962);position+=n
assert position==chap['frames']*800==len(edited)//4

def mono(path):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a','-ac','1','-ar','8000','-f','f32le','-'])
    return np.frombuffer(raw,dtype='<f4').astype(np.float64)
actual,reference=mono(FILM),mono(ROOT/'work/edit/audio.wav');av=[]
for i in range(12):
    time=2+i*(chap['duration_s']-6)/11;start=int(time*8000);n=4000
    ref=reference[start:start+n];ref_norm=np.linalg.norm(ref);scores=[]
    for lag in range(-240,241,2):
        window=actual[start+lag:start+lag+n]
        norm=np.linalg.norm(window)*ref_norm
        scores.append((float(np.dot(window,ref)/norm) if norm else 0,lag))
    corr,lag=max(scores)
    av.append({'time_s':round(time,3),'lag_ms':lag/8,'correlation':round(corr,5)})
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(FILM)]))
pts_raw=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=pts','-of','csv=p=0',str(FILM)],text=True)
pts=[int(x) for x in pts_raw.replace(',',' ').split()]
report={'film':str(FILM),'sha256':hashlib.sha256(FILM.read_bytes()).hexdigest(),'decode_exit':exit_code,
        'frames':len(pts),'pts_deltas':sorted(set(b-a for a,b in zip(pts,pts[1:]))),
        'video_checks':len(results),'video_mismatches':[x for x in results if x['mismatch']],
        'pcm_segment_errors':audio_errors,'pcm_frames':len(edited)//4,'pcm_frames_compared':compared,
        'av':av,'probe':probe,'video_details':results}
(ROOT/'out/verify.json').write_text(json.dumps(report,indent=2)+'\n')
assert len(pts)==chap['frames'] and report['pts_deltas']==[256]
assert not report['video_mismatches'] and not audio_errors
assert max(abs(x['lag_ms']) for x in av)==0
print(json.dumps({k:report[k] for k in ['sha256','decode_exit','frames','video_checks','video_mismatches','pcm_segment_errors','pcm_frames']}))
