from pathlib import Path
import csv,json,hashlib,subprocess
P=Path(__file__).parent;C=P/'captures/phase2';rows=[]
for f in sorted(C.glob('*/provenance.json')):
 d=json.loads(f.read_text());st=f.parent/'state.csv';rs=list(csv.DictReader(st.open()))if st.exists()else[]
 row={k:d.get(k,'')for k in ['id','source_kind','game','zone','act','x','y','rings','timer','emeralds','main','sidekick','commit','jar_sha256']};row.update(path=str(f.parent.relative_to(P)),frames=len(rs),modes=','.join(sorted({r.get('mode','')for r in rs})),outcome='captured'if rs else 'scout or failed; see capture.log');rows.append(row)
with (P/'shot-list.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
f=C/'halfpipe-cleared-post/provenance.json';d=json.loads(f.read_text());d.update(source_kind='debug positioned ROM-starpost component entry; real ring collision admission',setup='After 120 revealed ticks, reposition MICA to (3568,150), declare 70 rings, clear previously activated checkpoint, instantiate the original ROM Obj79 spawn at (3568,170). No direct enterSpecialStage call. Jump at input150; SPECIAL_STAGE observed at165. MICA leads/TALON follows.');f.write_text(json.dumps(d,indent=2))
f=C/'ending-full/provenance.json';d=json.loads(f.read_text());d['setup']='S2 DEZ1 positioned boot; bind production Engine, requestCreditsTransition debug entry, ordinary ending provider steps/draws. Edit uses 2700 onward, TALON piloting Tornado; stock photos at0–2000 excluded. state.csv mode is retained GameplayCaptureSession loop (LEVEL), not Engine ending loop; do not interpret as gameplay route evidence.';f.write_text(json.dumps(d,indent=2))
# Keep native observations separate from authored setup.
r=list(csv.DictReader((C/'hero-mgz2/state.csv').open()));events=[dict(frame=int(v['frame']),score=int(v['score']),air=int(v['air']),x=int(v['x']),y=int(v['y']))for i,v in enumerate(r)if i and v['score']!=r[i-1]['score']];(P/'homing-events.json').write_text(json.dumps(dict(events=events,first_hurt=183,used_cold_frames=[15,169],used_homing_frames=[0,176],proof='First three score deltas 100,200,500; consecutive ROM Mantis kills, airborne, corroborated PNG65/82/104/110. No trace input.'),indent=2))
