# REHEARSAL GENERATOR ONLY: corrected final .txt inputs are authoritative.
# Do not rerun this file over the retained final inputs.
from pathlib import Path
r=Path('/home/farrell/scratch/sv-promo/final')
r.joinpath('story.txt').write_text('20:jump=card_THE_/_STORY\n230:enter\n310:right\n350:left\n400:enter\n950:enter\n')
lines=['0:jump=new_sonic','1:jump=close','2:jump=night_0','3:jump=people_mail_clear','4:jump=people_hold_moto_110_4','5:jump=orchard_clear','6:jump=time_0700','7:jump=give_spring_tulip_seeds_9','8:jump=give_spin_spud_seeds_9','20:jump=card_GROW_/_AND_HARVEST']
t=150
for d in [22,36,50]:
 lines += [f'{t}:jump=farm_180_{d}',f'{t+6}:hold=x',f'{t+30}:release=x'];t+=60
for slot,d in [(1,22),(2,36),(3,50)]:
 lines += [f'{t}:jump=select_{slot}']
 for x in [184,200,216]:
  lines += [f'{t}:jump=farm_{x}_{d}',f'{t+3}:x'];t+=18
 t+=12
lines += [f'{t}:jump=select_0']
for d in [22,36,50]:
 for x in [184,200,216]:
  lines += [f'{t}:jump=farm_{x}_{d}',f'{t+3}:x'];t+=12
lines += [f'{t}:jump=farm_240_72'];t+=45
for n in range(6):
 lines += [f'{t}:jump=night_1',f'{t+1}:jump=people_mail_clear',f'{t+2}:jump=farm_240_72'];t+=30
lines += [f'{t}:jump=select_6'];t+=30
for d in [22,36,50]:
 for x in [184,200,216]:
  lines += [f'{t}:jump=farm_{x}_{d}',f'{t+3}:x'];t+=12
lines += [f'{t+20}:jump=farm_150_10',f'{t+50}:x']
for n in range(7):lines += [f'{t+90+n*12}:enter']
lines += [f'{t+190}:x',f'{t+230}:jump=sleep']
r.joinpath('grow.txt').write_text('\n'.join(lines)+'\n');print('grow frames',t+530)
lines=['0:jump=new_sonic','1:jump=close','2:jump=people_mail_clear','20:jump=card_NEIGHBOURS','140:jump=time_1100','141:jump=valley_1150','160:jump=people_talk_tails','300:enter','340:jump=close','350:jump=people_talk_pip','500:jump=close','510:jump=people_hearts_tails_2','511:jump=time_1200','520:jump=people_event_tails_2']
lines += [f'{t}:enter' for t in range(640,1020,35)]
r.joinpath('neighbours.txt').write_text('\n'.join(lines)+'\n')
r.joinpath('finale.txt').write_text('0:jump=new_sonic\n1:jump=close\n2:jump=people_mail_clear\n20:jump=card_A_YEAR_/_IN_THE_VALLEY\n145:jump=restore\n150:jump=yearend\n510:enter\n')
for kind,debug in [('hunt','ring_hunt'),('race','valley_race'),('parade','sunflower_parade'),('flickies','flickies'),('snowboard','ice_cap')]:
 lines=['0:jump=new_sonic','1:jump=close','2:jump=people_mail_clear']
 start=145 if kind=='hunt' else 40
 if kind=='hunt':lines+=['20:jump=card_FESTIVALS']
 lines += [f'{start}:jump=festival_start_{debug}']
 if kind=='snowboard':lines += [f'{start+90}:down',f'{start+120}:enter']
 lines += [f'{start+170}:hold=right']+[f'{start+200+i*40}:z' for i in range(4)]+[f'{start+350}:release=right']
 r.joinpath(kind+'.txt').write_text('\n'.join(lines)+'\n')
for band,chamber in [('marble',5),('labyrinth',16),('scrap',28)]:
 lines=['0:jump=new_sonic','1:jump=close','2:jump=people_mail_clear','3:jump=rings_500']
 start=145 if band=='marble' else 40
 if band=='marble':lines+=['20:jump=card_ADVENTURE']
 lines += [f'{start}:jump=ruins_{chamber}',f'{start+120}:hold=right',f'{start+165}:z',f'{start+195}:x',f'{start+240}:release=right']
 r.joinpath(band+'.txt').write_text('\n'.join(lines)+'\n')
r.joinpath('lake.txt').write_text('0:jump=new_sonic\n1:jump=close\n2:jump=people_mail_clear\n3:jump=give_fishing_rod_1\n4:jump=select_2\n40:jump=fish_lake\n180:hold=right\n315:release=right\n390:hold=x\n430:release=x\n')
s=Path('/home/farrell/scratch/sv-promo/adventure.txt').read_text().splitlines();lines=['0:jump=new_sonic','1:jump=close','2:jump=people_mail_clear']
for line in s:
 t,action=line.split(':',1)
 if int(t)>=1170:lines.append(f'{int(t)-1130}:{action}')
r.joinpath('orchard-museum.txt').write_text('\n'.join(lines)+'\n')
