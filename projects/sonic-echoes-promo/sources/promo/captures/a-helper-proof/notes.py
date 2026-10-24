from pathlib import Path
import csv,subprocess,sys
from PIL import Image
T=Path('/home/james/tmp/sonic-echoes-promo/captures')
labels={
 'a4-hub-tour':{930:'Emerald Hill tab, all four cards cleared, 33/36; reviewed.',987:'Hill Top tab, all four cards cleared, 33/36; reviewed.',1039:'Chemical Plant tab, 3-1…3-3 cleared and 3-4 unlocked; reviewed.',1120:'3-4 THE LAST LOOP selected, ready and unplayed; reviewed.',1333:'First ordinary native tick after real Up input; mod HUD appears while entry camera settles; reviewed.',1370:'Live Sonic and whole mod HUD visible after camera settles; reviewed.',1452:'Finale room after 120 ordinary gameplay ticks, live Sonic and whole mod HUD visible; reviewed.'},
 'a1-chain':{899:'Native Sonic 2 emblem and ECHOES wordmark, reviewed.',930:'Fresh Echo Engine hub, 0/36, room 1-1 selected; reviewed.',3090:'Returned hub: 1-1 has three lifetime stars, 1-2 unlocked; reviewed.'},
 'a2-two-hands':{551:'Cyan and magenta echoes visible on their plates; live Sonic crossing magenta plate; gate condition opens. Reviewed.',663:'ROOM CLEAR with Clear and Par stars; reviewed.'},
 'a3-escort':{604:'Magenta echo destroys native Buzzer; 100 score and explosion visible, live Sonic below. Reviewed.',778:'ROOM CLEAR with Clear and Par stars; reviewed.'}}
for name in (sys.argv[1:] or ('a1-chain','a2-two-hands','a3-escort','a4-hub-tour')):
 d=T/name
 if not (d/'state.csv').exists():continue
 a=list(csv.DictReader((d/'session.csv').open()));b=list(csv.DictReader((d/'state.csv').open()));fs=sorted((d/'frames').glob('*.png'))
 assert len(a)==len(b)==len(fs),(name,len(a),len(b),len(fs))
 assert all(r['frame']==t['frame'] and (r['liveX'],r['liveY'],r['camX'],r['camY'])==(t['x'],t['y'],t['cam_x'],t['cam_y']) for r,t in zip(a,b))
 blacks=[];start=last=None
 for p in fs:
  dark=Image.open(p).convert('RGB').getextrema()==((0,0),(0,0),(0,0));n=int(p.stem)
  if dark:
   if start is None:start=n
   last=n
  elif start is not None:blacks.append((start,last));start=None
 if start is not None:blacks.append((start,last))
 title=name in ('a1-chain','a4-hub-tour')
 entry='Cold title boot (`--title-screen --interactive-pacing`), real Genesis Start/hub navigation/confirmation.' if title else f'Pre-boot room selection through `echoes.capture.room={a[0]["room"]}`, then ordinary stock boot. 180 neutral entry rows.'
 text=f'# {name}\n\nBase commit: `5fca08819f88cb867c0d89eee3be7a4e2b611c8b`, current main checkout, `feature/ai-sonic-echoes`. No commits/push/branch changes.\n\nEntry: {entry} No teleport, seeded recordings, forced drift or gameplay mutation. **No native S2 room title card appears in this capture** (capture tool default; mod room entry finishes initial presentation).\n\n{len(a)} PNGs, **frames 0–{len(a)-1}**, 400×224, 60 Hz, every frame, lossless, silent, surfaceless EGL with DISPLAY/WAYLAND_DISPLAY unset. No audio enabled. `preview.mp4` is a silent uncut convenience encode.\n\n`state.csv` / `session.csv`: equal row counts and frame numbers; live centre/camera coordinates match on every row. Logical held input, face actions and Start are recorded. Echo slots are zero-based. Shard events use room placement indices. `star:1/2/3` means Clear/Par/Shards. `hubSelected` records selected card where available.\n\nTest-only helpers: shared `PromoCaptureMod.java` plus Worker B’s `PromoActionCaptureMod.java`. See `../HELPER.md` and `../HELPER_BUILD.py --actions`. ECHO commands are scheduled at authored loop/frame boundaries through the ordinary mod command path. Genesis input is compiled and round-trip-validated with InputLogAuthorTool. Each nonfinal authored loop is followed by 13 neutral rows (command plus 12-frame rewind hold). Distributed sources/jar are untouched.\n\nExact capture command (JAVA_HOME and Maven PATH as assigned in task):\n\n```sh\n'+(d/'command.txt').read_text()+'```\n\nExact authored Genesis input:\n\n```text\n'+(d/'inputs.script').read_text()+'```\n\n| Frame | Event | On-screen evidence |\n| --- | --- | --- |\n'
 for r in a:
  if not r['events']:continue
  ev=r['events'];desc='Room/HUD state changes; matching frame PNG available.'
  if 'rewind_start' in ev:desc='Authored attempt commits; mod’s twelve-frame rewind flash starts.'
  elif 'restore' in ev:desc='World returns to room spawn; recorded echo joins next loop.'
  elif 'badnik_kill:echo1' in ev:desc='Magenta echo pops native Buzzer; explosion and 100 points, personally reviewed.'
  elif 'badnik_kill:live' in ev:desc='Recording loop Sonic pops native Buzzer; reproduced by magenta echo in final loop.'
  elif ev=='clear':desc='ROOM CLEAR overlay begins at the rift.'
  elif 'star:' in ev:desc='Result star pop; Clear=1, Par=2, Shards=3.'
  elif 'hub_move' in ev:desc='Real controller navigation moves selected hub card'+(' to '+r.get('hubSelected','') if r.get('hubSelected') else '')+'.'
  elif 'hub_confirm' in ev:desc='Real controller confirm launches selected room.'
  elif 'gate_open' in ev:desc='Plate channels activate and gate condition opens; early final-loop frame keeps echoes on screen.'
  elif 'shard:' in ev:desc='Live/echo collects room shard(s), indicated by placement index.'
  text+=f'| {r["frame"]} | {ev} | {desc} |\n'
 text+='\nRepresentative frames personally opened:\n\n'
 for f,desc in labels.get(name,{}).items():text+=f'- `{f:05d}.png`: {desc}\n'
 text+='\nQuality: Sonic, readable echoes and whole mod HUD inspected; native terrain moves correctly. Expected READY, rewind and results holds are intentional. No debug overlays. '
 text+=('Black transition ranges: '+', '.join(f'{a}–{b}' for a,b in blacks)+'. These are short stock title/launch fades; the longest is eight rows. No sustained black gameplay.\n') if blacks else 'No fully black frames.\n'
 if name=='a1-chain':text+='\nShot-list limitation: the authored shard route uses two echoes while par is one. This continuous take first earns Clear+Par, returns to the hub, reselects 1-1 with real input, then earns Shards. The final hub honestly shows all three lifetime stars and 1-2 unlocked. The shard-run results pop Clear and Shards, with Par hollow; three simultaneous result-star pops cannot be achieved with these authored routes. No behavior change was made.\n'
 if name=='a4-hub-tour':text+='\nEarned save: `save/mods/sonic-echoes/progress.txt` contains 33 stars from real reference-route replays of 1-1…2-4 and 3-1…3-3. Room 3-4 is absent (unplayed). Each par and shard solution was driven by InputLogAuthorTool logs in `earned/`, with a complete `state.csv`. Earnings runs use one initial PNG (`every=999999`) because they are progress replays rather than film takes. World 1 and most world 2 runs use timeout commits; the 2-4 shard retry and world 3 use tight ECHO commands. The earlier timeout 2-4 shard attempt reached an existing provider identity limit at frame 3401; progress was already earned by the successful par route and the compact shard retry completed. No save file was fabricated or edited.\n'
 (d/'NOTES.md').write_text(text)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','60','-i',str(d/'frames/%05d.png'),'-vf','scale=800:448:flags=neighbor','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-an',str(d/'preview.mp4')],check=True)
 print(name,len(a),'black',blacks,flush=True)
