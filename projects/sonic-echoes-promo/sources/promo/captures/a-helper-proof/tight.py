from run_a import *
import shutil

def tight(room,kind='solution'):
 p=props(room);i=0;segs=[];actions=[]
 while f'{kind}.{i}' in p:
  loop=[(int(a.split(':')[0]),'+'.join(a.split(':')[1].replace('J','A'))) for a in p[f'{kind}.{i}'].split(',')]
  segs+=loop
  if f'{kind}.{i+1}' in p:segs.append((13,'-'));actions.append(f'{i}:{sum(n for n,b in loop)}:ECHO')
  i+=1
 return segs,actions
for name,room in [('a2-two-hands','1-2'),('a3-escort','1-4'),('a1-chain',None)]:
 d=TASK/name
 shutil.rmtree(d/'frames');shutil.rmtree(d/'save')
 if room:
  segs,actions=tight(room);segs=[(180,'-')]+segs+[(120,'-')]
 else:
  par,a=tight('1-1');shard,b=tight('1-1','shardSolution');actions=a+b
  segs=[(900,'-'),(1,'S'),(60,'-'),(1,'S'),(200,'-')]+par+[(120,'-'),(1,'A'),(240,'-'),(1,'L'),(25,'-'),(1,'A'),(200,'-')]+shard+[(120,'-'),(1,'A'),(240,'-')]
 run(name,room,segs,title=room is None,actions=','.join(actions))
