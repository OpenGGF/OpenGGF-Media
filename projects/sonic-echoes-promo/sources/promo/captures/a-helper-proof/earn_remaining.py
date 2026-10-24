from run_a import *
def tight(room,kind):
 p=props(room);i=0;segs=[];actions=[]
 while f'{kind}.{i}' in p:
  loop=[(int(a.split(':')[0]),'+'.join(a.split(':')[1].replace('J','A'))) for a in p[f'{kind}.{i}'].split(',')];segs+=loop
  if f'{kind}.{i+1}' in p:segs.append((13,'-'));actions.append(f'{i}:{sum(n for n,b in loop)}:ECHO')
  i+=1
 return segs,actions
for room,kind in [('2-4','shardSolution')]+[(f'3-{n}',k) for n in range(1,4) for k in ('solution','shardSolution')]:
 segs,actions=tight(room,kind)
 run(f'a4-hub-tour/earned/{room}-{kind}-tight',room,[(180,'-')]+segs+[(120,'-')],save=TASK/'a4-hub-tour/save',extra=' --every 999999',actions=','.join(actions))
print((TASK/'a4-hub-tour/save/mods/sonic-echoes/progress.txt').read_text())
