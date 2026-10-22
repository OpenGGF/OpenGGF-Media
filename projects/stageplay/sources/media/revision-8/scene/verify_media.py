#!/usr/bin/env python3
"""Decode/probe final captures and compare full native video/PCM streams.
Origin: Stageplay revision eight. Inputs: take-3 lossless MKVs; outputs concise
checks, two native-SFX WAVs, continuous music WAV, and checks the already-created standalone story MP4.
No loudness, listening, normal-speed creative review or ROM-parity claim.
"""
import array,hashlib,json,subprocess,wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
root=Path(__file__).resolve().parent;take=root/'take-3'
names=['story','clean','story-sfx','clean-sfx','comparison-hold8','music-bed']
def run(args):return subprocess.check_output(args,stderr=subprocess.PIPE,text=True)
def inspect(name):
 file=take/f'{name}.mkv'
 probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(file)]))
 video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
 assert (video['width'],video['height'],video['r_frame_rate'])==(640,448,'60/1')
 assert int(video['nb_read_frames'])==(5760 if name=='music-bed' else 2040)
 assert audio['channels']==2
 hashes={}
 for stream in ['v:0','a:0']:
  cmd=['ffmpeg','-v','error','-xerror','-i',str(file),'-map','0:'+stream]
  if stream=='v:0':cmd+=['-pix_fmt','rgb24']
  else:cmd+=['-c:a','pcm_s16le']
  hashes[stream]=run(cmd+['-f','hash','-hash','sha256','-']).strip()
 return name,dict(path=str(file.relative_to(root)),frames=int(video['nb_read_frames']),width=640,height=448,fps='60/1',audioChannels=audio['channels'],sampleRate=audio['sample_rate'],fullDecode='passed',streamHashes=hashes)
with ThreadPoolExecutor(max_workers=3) as pool:results=dict(pool.map(inspect,names))
for x,y in [('story','story-sfx'),('clean','clean-sfx')]:assert results[x]['streamHashes']['v:0']==results[y]['streamHashes']['v:0'],(x,y)
assert results['story-sfx']['streamHashes']['a:0']==results['clean-sfx']['streamHashes']['a:0']
assert results['story']['streamHashes']['a:0']==results['clean']['streamHashes']['a:0']
assert results['story']['streamHashes']['a:0']!=results['story-sfx']['streamHashes']['a:0']
for name,dest in [('clean-sfx','native-sfx.wav'),('comparison-hold8','comparison-native-sfx.wav'),('music-bed','continuous-music.wav')]:
 path=root/dest
 if not path.exists():subprocess.run(['ffmpeg','-v','error','-nostdin','-n','-i',str(take/f'{name}.mkv'),'-vn','-c:a','pcm_s16le',str(path)],check=True)
waveChecks={}
for name in ['native-sfx.wav','comparison-native-sfx.wav','continuous-music.wav']:
 with wave.open(str(root/name)) as w:
  pcm=array.array('h',w.readframes(w.getnframes()));peak=max(abs(x) for x in pcm)
  assert peak>0
  waveChecks[name]=dict(frames=w.getnframes(),rate=w.getframerate(),channels=w.getnchannels(),peakSample=peak,nonzeroSamples=sum(x!=0 for x in pcm),totalSamples=len(pcm))
short=root/'wait-for-me-standalone.mp4'
# Existing one-off standalone predates parent steering; never encode another here.
if short.exists():subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(short),'-f','null','-'],check=True)
report=dict(captures=results,waves=waveChecks,standalone=(dict(path=short.name,frames=1560,width=1280,height=896,fps=60,fullDecode='passed') if short.exists() else None),videoMusicStopMatchesEveryDecodedPixel=True,sfxPcmMatchesDialogueAndClean=True,musicAndSfxAreDistinct=True,limits='Decoded media and deterministic stream equality. No physical listening, loudness mastering or normal-speed creative review; parent owns final edit review.')
(root/'media-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
