-- Read-only SSZ2 crane observations, from the saved BK2 entry. No RAM writes.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_NATIVE_PLAN')))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(movie.isloaded() and emu.framecount()==plan.state_frame)
client.speedmode(6400); client.invisibleemulation(false)
local roots={[0x7CA16]=true,[0x7CA3A]=true,[0x7CAAA]=true,[0x7CAD2]=true,[0x7CAE6]=true,[0x7CAF8]=true,[0x7CB28]=true,[0x7CB64]=true,[0x7CBA4]=true,[0x7CBCE]=true,[0x7CC26]=true}
local claws={[0x7CCFE]=true,[0x7CD22]=true,[0x7CD36]=true,[0x7CD42]=true,[0x7CD76]=true,[0x7CD82]=true,[0x7CE1E]=true,[0x7CE42]=true}
local w=mainmemory.read_u16_be;local b=mainmemory.read_u8;local l=mainmemory.read_u32_be
local file=assert(io.open(out..'/crane-events.csv','w'))
file:write('frame,zone,root_slot,root_code,root_x_fixed,root_y_fixed,root_xvel,root_yvel,claw_slot,claw_code,claw_y,claw_height,flags,mecha_slot,camx,camy,playerx,playery,control\n')
local previous=''
while emu.framecount()<plan.last_frame do
 emu.frameadvance()
 local root,claw=0,0
 for slot=3,92 do
  local a=0xB000+slot*0x4A;local code=l(a)
  if roots[code] then root=a end
  if claws[code] then claw=a end
 end
 local key=string.format('%X:%X:%X:%X',l(root),l(claw),b(0xFAB8),w(0xFAA4))
 if key~=previous then
  previous=key
  local f=emu.framecount()
  file:write(string.format('%d,%X,%X,%X,%u,%u,%d,%d,%X,%X,%d,%d,%X,%X,%d,%d,%d,%d,%d\n',f,w(0xFE10),root,l(root),l(root+0x10),l(root+0x14),w(root+0x18),w(root+0x1A),claw,l(claw),w(claw+0x14),b(claw+0x1A),b(0xFAB8),w(0xFAA4),w(0xEE78),w(0xEE7C),w(0xB010),w(0xB014),b(0xB02E)))
  client.screenshot(out..'/f'..f..'.png')
 end
end
file:close();local d=assert(io.open(out..'/done.txt','w'));d:write('ok\n');d:close();client.exit()
