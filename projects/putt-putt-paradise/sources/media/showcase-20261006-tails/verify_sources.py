"""Verify native route/state cadence and the production VHS rendering evidence."""
from pathlib import Path
import csv,json,subprocess,hashlib
from PIL import Image,ImageChops,ImageStat
root=Path(__file__).resolve().parent
checks=[]
for p in sorted(root.glob('*-final-v5')):
 rows=list(csv.DictReader((p/'state.csv').open()))
 assert [int(r['frame']) for r in rows]==list(range(len(rows)))
 assert all(r['width']=='320' and r['dead']=='false' for r in rows)
 assert len({r['character'] for r in rows})== (2 if p.name.startswith('local') else 1)
 assert rows[-1]['status']==('PLAYING' if p.name.startswith('local') else 'COMPLETE')
 video_frames=(len(rows)+1)//2
 for name,expected in [('gameplay',video_frames),('title',120)]:
  source=p/(name+'.mkv')
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(source)],text=True))
  s=probe['streams'][0]
  assert (s['width'],s['height'],s['r_frame_rate'],int(s['nb_read_frames']))==(320,224,'30/1',expected)
  subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(source),'-f','null','-'],check=True)
 checks.append(dict(capture=p.name,native_rows=len(rows),video_frames=video_frames,final_status=rows[-1]['status'],final_owner=rows[-1]['owner'],final_turn=rows[-1]['turn'],final_score=rows[-1]['score'],dead_rows=0,full_lossless_decode='passed'))
(root/'capture-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
p=root/'ehz1-sonic-rewind-final-v5';rows=list(csv.DictReader((p/'state.csv').open()))
effects=[r for r in rows if float(r['rewind_intensity'])>0]
assert effects and all(r['stage']=='WATCH' for r in effects)
assert float(rows[int(effects[-1]['frame'])+1]['rewind_intensity'])==0
assert all(float(r['rewind_intensity'])==0 for r in rows[int(effects[-1]['frame'])+1:])
a=Image.open(p/'rewind-raw.png').convert('RGB');b=Image.open(p/'rewind-vhs.png').convert('RGB');d=ImageChops.difference(a,b)
different=sum(pixel!=(0,0,0) for pixel in d.get_flattened_data())
assert a.size==b.size==(320,224) and different>1000
check=dict(effect='production RewindVhsEffectPass',first_native_frame=int(effects[0]['frame']),last_native_frame=int(effects[-1]['frame']),native_frames=len(effects),intensity_range=[min(float(r['rewind_intensity']) for r in effects),max(float(r['rewind_intensity']) for r in effects)],speed_range=[min(float(r['rewind_speed']) for r in effects),max(float(r['rewind_speed']) for r in effects)],different_pixels_same_native_frame=different,mean_absolute_rgb_difference=sum(ImageStat.Stat(d).mean)/3,raw_image='ehz1-sonic-rewind-final-v5/rewind-raw.png',effect_image='ehz1-sonic-rewind-final-v5/rewind-vhs.png',effect_clears_after_restore=True)
(root/'effect-checks.json').write_text(json.dumps(check,indent=2)+'\n')
print(json.dumps(checks));print(json.dumps(check))
