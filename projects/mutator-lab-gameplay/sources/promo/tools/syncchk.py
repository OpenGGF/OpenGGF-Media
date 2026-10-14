import csv,gzip,sys
tr=list(csv.DictReader(gzip.open(sys.argv[1],"rt"))); ob=list(csv.DictReader(open(sys.argv[2]))); off=int(sys.argv[3])
tx=[(int(r['player_x'],16),int(r['player_y'],16)) for r in tr]; ox=[(int(r['x']),int(r['y'])) for r in ob]
div=None
for f in range(off,len(ox)):
    if f-off>=len(tx): break
    if tx[f-off]!=ox[f]: div=f; break
print('first divergence capture frame',div,'trace row',None if div is None else div-off)
if div: 
    for g in range(div-3,div+3): print(' ',g, tx[g-off], ox[g], tr[g-off]['player_y_speed'], ob[g]['yvel'], 'rings', int(tr[g-off]['rings'],16), ob[g]['rings'])
print('rings cap/trace at end', ob[-1]['rings'], int(tr[min(len(tr)-1,len(ox)-1-off)]['rings'],16))
