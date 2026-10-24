from run_a import *
save=TASK/'a4-hub-tour/save'
for w in range(1,4):
 for n in range(1,5 if w<3 else 4):
  room=f'{w}-{n}'
  for kind in ('solution','shardSolution'):
   if f'{kind}.0' not in props(room):continue
   run(f'a4-hub-tour/earned/{room}-{kind}',room,[(180,'-')]+route(room,kind)+[(120,'-')],save=save,extra=' --every 999999')
   text=(save/'mods/sonic-echoes/progress.txt').read_text()
   if room+'=' not in text:raise RuntimeError('Failed to earn '+room+' '+kind)
print((save/'mods/sonic-echoes/progress.txt').read_text())
