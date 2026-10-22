#!/usr/bin/env python3
"""Atomically publish the revision-eight handoff. Inputs: checks, owned assets,
engine checkout and existing ROM. Hash identities only; never copy ROMs or logs.
Origin: approved Stageplay revision eight. Paths are relative to this directory.
"""
import argparse,hashlib,json,os,subprocess,tempfile,zlib
from pathlib import Path
root=Path(__file__).resolve().parent
def sha(path,kind='sha256'):
 h=hashlib.new(kind)
 with path.open('rb') as f:
  for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
 return h.hexdigest()
def git(engine,*args):return subprocess.check_output(['git','-C',str(engine),*args],text=True).strip()
def atomic(path,data):
 fd,tmp=tempfile.mkstemp(prefix='.manifest-',dir=path.parent)
 try:
  with os.fdopen(fd,'w') as f:json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
  os.link(tmp,path)
 finally:os.unlink(tmp)
def main():
 p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);a=p.parse_args()
 checks=json.loads((root/'scene-checks.json').read_text());media=json.loads((root/'media-checks.json').read_text());audio=json.loads((root/'audio-qualification.json').read_text())
 assert checks['totalFrames']==2040 and media['videoMusicStopMatchesEveryDecodedPixel'] and media['sfxPcmMatchesDialogueAndClean']
 jar=root/'engine/OpenGGF-1a5ae4ad.jar';rom=a.rom.resolve();crc=0
 with rom.open('rb') as f:
  for data in iter(lambda:f.read(1024*1024),b''):crc=zlib.crc32(data,crc)
 assert sha(rom,'sha1').upper()=='CFBF98C36C776677290A872547AC47C53D2761D6'
 identity=dict(runtimeSourceCommit='1a5ae4adf487efe224f466f936d7fd8a8eded2e5',sceneCommit=git(a.engine,'rev-parse','HEAD'),sceneBranch=git(a.engine,'branch','--show-current'),engineWorktree=str(a.engine.resolve()),jar=dict(path=str(jar.relative_to(root)),sha256=sha(jar),bytes=jar.stat().st_size),rom=dict(originalPath=str(rom),sha1=sha(rom,'sha1'),sha256=sha(rom),crc32=f'{crc:08X}',bytes=rom.stat().st_size),javaHome='/usr/lib/jvm/java-25-openjdk',build=dict(command='JAVA_HOME=/usr/lib/jvm/java-25-openjdk python3 tools/testing/maven_queue.py -Dmse=off package -DskipTests',result='BUILD SUCCESS',executionSeconds=88,tests='skipped by explicit task scope; no broad/baseline/full suite'),capture=dict(display='DISPLAY and WAYLAND_DISPLAY removed',gl='surfaceless-egl',audio='HeadlessSmpsAudioBackend / NoDeviceAudioSink; offline PCM only',scale=2),priorRevision7='7d35d4a7b')
 identityPath=root/'engine/identity.json'
 if identityPath.exists():assert json.loads(identityPath.read_text())==identity
 else:atomic(identityPath,identity)
 paths=dict(story='take-3/story.mkv',clean='take-3/clean-sfx.mkv',sfx='native-sfx.wav',comparison='take-3/comparison-hold8.mkv',comparisonSfx='comparison-native-sfx.wav',dialogueSfx='take-3/story-sfx.mkv',cleanWithMusic='take-3/clean.mkv',music='continuous-music.wav',musicCapture='take-3/music-bed.mkv',screenplay='take-3/story.screenplay.json',scene='take-3/story.stageplay',nativeState='take-3/story.jsonl',comparisonState='take-3/comparison-hold8.jsonl',standalone='wait-for-me-standalone.mp4')
 for name,path in paths.items():assert (root/path).is_file(),name
 notes=[
  dict(startFrame=0,endFrame=240,title='GIVE THEM A REASON',body='Two friends, one promise: cross together.',command='DEZ2 · LIVE · Sonic + Tails'),
  dict(startFrame=240,endFrame=535,title='LET A MOVE CHANGE THINGS',body='Sonic rushes ahead. Tails calls him back.',command='MOVE_TO .65 · JUMP hold 20'),
  dict(startFrame=535,endFrame=780,title='MAKE THE REPLY VISIBLE',body='A crouch gives the apology a beat. Then Sonic returns.',command='CROUCH 45 · return at 660'),
  dict(startFrame=780,endFrame=1065,title='CHOOSE THE SHARED ARRIVAL',body='Tails can fly. Sonic chooses company over speed.',command='WAIT ON_OBJECT · timeout 180'),
  dict(startFrame=1065,endFrame=1240,title='COUNT INTO THE JUMP',body='The final word meets takeoff.',command='Three! at 1135–1140 · jump 1141'),
  dict(startFrame=1240,endFrame=1560,title='WATCH THE CONSEQUENCE',body='Both board the lift. Native contact carries the last reply.',command='ON_OBJECT 166 · frames 1199/1204')]
 assert notes[0]['startFrame']==0 and notes[-1]['endFrame']==1560
 assert all(x['endFrame']==y['startFrame'] for x,y in zip(notes,notes[1:]))
 comparison=dict(startFrame=180,endFrame=450,variantStartFrame=180,change='Change one value: first jump hold, 20 to 8 frames.',outcome='20.34 px lower arc. Lands 8 frames earlier. Both reach the lift.',labelA='A · HOLD 20',labelB='B · HOLD 8',commandA='JUMP · holdFrames: 20',commandB='JUMP · holdFrames: 8')
 files=[]
 for path in sorted(root.rglob('*')):
  if path.is_file() and '__pycache__' not in path.parts and path.name!='manifest.json' and not path.name.startswith('.manifest-'):
   files.append(dict(path=str(path.relative_to(root)),bytes=path.stat().st_size,sha256=sha(path)))
 manifest=dict(schemaVersion=1,provisional=False,fps=60,native=dict(width=320,height=224),captured=dict(width=640,height=448,scale=2),storyFrames=1560,totalFrames=2040,paths=paths,tutorialNotes=notes,comparison=comparison,endcard=dict(frames=480,samplePath='examples/stageplay-demo/src/main/resources/scenes/wait-for-me.stageplay',url='github.com/OpenGGF/OpenGGF',status='Development preview'),events=dict(initialBoarding=dict(sonic=15,tails=16),firstJump=241,firstApex=271,firstLand=293,sonicReaction=dict(startFrame=535,endFrame=580),returnJump=661,returnLand=728,countThreeStart=1135,countThreeFullyRevealed=1140,sharedJump=dict(sonic=1141,tails=1146),sharedLand=dict(sonic=1199,tails=1204),storyEnd=1560,tailEnd=2040),dialogue=checks['dialogue'],platformChanges=checks['platformChanges'],comparisonMeasurements=checks['comparison'],tail=checks['tail'],provenance=identity,verification=dict(scene='scene-checks.json',media='media-checks.json',audio='audio-qualification.json',geometryMethod=checks['geometryMethod'],noEngineSuite='Scene-data task: package skip-tests, structural validation, native simulations, six full renders and decodes; no baseline/broad/full suite requested or run.',musicQualification=audio['musicFreeQualification'],limits=checks['limits']),audioPolicy=dict(music='continuous-music.wav is the sole tutorial music owner; uninterrupted 96-second ROM track 23',sfx='Use native-sfx.wav and comparison-native-sfx.wav only; includes native world ambience/DC floor. Never mix combined source audio into a second bed.',standalone='Original combined story.mkv is retained for standalone playback.'),assets=files)
 atomic(root/'manifest.json',manifest);print(json.dumps(dict(manifest=str(root/'manifest.json'),sceneCommit=identity['sceneCommit'],assets=len(files),storyFrames=1560,totalFrames=2040,editorialSeconds=75)))
if __name__=='__main__':main()
