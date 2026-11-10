from extra import *
# Explore close ROM-placed enemy clusters. Every candidate has a roundtripped log.
spots=[('s3k',2,1,7600,1136),('s3k',2,1,8840,2290),('s3k',1,0,11760,1480),('s2',0,1,9040,480),('s2',1,0,2920,380),('s3k',0,1,7000,900)]
for j,(g,z,act,x,y) in enumerate(spots):
 for k,(gap,wait) in enumerate([(10,15),(16,10),(22,20),(30,0)]):
  name=f'probe-{j}-{k}';d=P/'captures/phase2'/name;d.mkdir(parents=True,exist_ok=True)
  script=f'{wait+1} -; 1 R+A; 12 R; repeat 25 {{ 1 R+A; {gap} R }}; 60 R'
  (d/'input.script').write_text(script)
  subprocess.run(['java','-cp',cp,'com.openggf.tools.InputLogAuthorTool','--script',str(d/'input.script'),'--out',str(d/'input.txt')],cwd=R,stdout=subprocess.DEVNULL,check=True)
  try:
   java('probe',name,g,z,act,x,y,d/'input.txt')
   rows=list(csv.DictReader((d/'state.csv').open()));events=[(r['frame'],r['score'],r['x'],r['y'])for i,r in enumerate(rows)if i and r['score']!=rows[i-1]['score']]
   print(name,events,'hurt',sum(r['hurt']=='1'for r in rows),flush=True)
  except Exception as e: print(name,type(e).__name__,flush=True)
