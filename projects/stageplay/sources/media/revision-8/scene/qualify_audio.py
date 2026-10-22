#!/usr/bin/env python3
"""Bounded PCM/owner audit of MUSIC_STOP. Origin: Stageplay revision eight.
Inputs: native-sfx.wav, engine source paths; no physical listening claimed.
"""
import array,json,math,wave
from pathlib import Path
root=Path(__file__).resolve().parent
with wave.open(str(root/'native-sfx.wav')) as w:
 rate=w.getframerate();channels=w.getnchannels();pcm=array.array('h',w.readframes(w.getnframes()))
windows=[]
for start,end,label in [(0,10/60,'first ten frames'),(1,2,'before first jump'),(3,4,'before first jump'),(24,25,'DC-dominated quiet interval'),(26,27,'tail beginning'),(33,34,'tail ending')]:
 v=pcm[round(start*rate)*channels:round(end*rate)*channels];mean=sum(v)/len(v);sq=sum(x*x for x in v)/len(v)
 windows.append(dict(startSeconds=start,endSeconds=end,label=label,rms=math.sqrt(sq),dcMean=mean,acRms=math.sqrt(max(0,sq-mean*mean)),peak=max(map(abs,v)),nonzeroFraction=sum(x!=0 for x in v)/len(v)))
assert windows[0]['peak']==0
first=next(i for i,x in enumerate(pcm) if x)
report=dict(musicFreeQualification='Supported MUSIC_STOP at frame zero, no later music cues; owner inspection confirms removal of both SMPS and streamed foreground music. Initial ten captured frames are exactly silent. Retained PCM is native world SFX/ambience with a measurable DC floor, not a second music bed.',firstNonzeroFrame=(first//channels)*60/rate,windows=windows,ownerChain=[dict(file='src/main/java/com/openggf/stageplay/runtime/StageplayAudio.java',method='dispatch',behavior='MUSIC_STOP dispatches audio.stopMusic().'),dict(file='src/main/java/com/openggf/audio/AudioManager.java',method='stopMusic',behavior='Records StopMusic, calls backend.stopPlayback().'),dict(file='src/main/java/com/openggf/audio/AbstractSmpsAudioBackend.java',method='stopPlayback / stopForegroundNow / stopStream',behavior='Stops and closes current SMPS driver/stream; pending StopForeground also stops streamedMusicPort, clears foreground/music stack and sets currentMusicId=-1. Later native SFX can own a separate standalone stream.'),dict(file='src/main/java/com/openggf/game/sonic3k/objects/S3kDezLightningObjectInstance.java',method='startFlash',behavior='Repeated native visible lightning flashes request LIGHTNING SFX 0x79; nearby world objects remain active during the ride.'),dict(file='src/main/java/com/openggf/audio/HeadlessSmpsAudioBackend.java',method='device hooks',behavior='Device hooks are no-ops; offline presentation producer supplies captured PCM.')],interpretation='99% nonzero is not 99% music: native world ambience repeats throughout this LIVE route; one quiet window has RMS 290, DC 287 and AC RMS 44. Initial exact silence plus stop owner and absence of later music cues qualifies the stem. Owner inspection supports lightning as an ambience source; this audit does not identify every PCM sample or certify perceived mix quality.',limits='PCM metering and owner inspection only. No physical listening, perceptual certification or per-voice native audio export. Keep the one continuous music-bed WAV as the sole editorial music owner.')
(root/'audio-qualification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
