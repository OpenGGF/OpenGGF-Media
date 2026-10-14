-- SSZ2 native boss state/presentation observations only. No RAM writes.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_NATIVE_PLAN')))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(movie.isloaded() and emu.framecount()==plan.state_frame)
client.speedmode(6400);client.invisibleemulation(false)
local w=mainmemory.read_u16_be;local b=mainmemory.read_u8;local l=mainmemory.read_u32_be
local file=assert(io.open(out..'/boss-events.csv','w'))
file:write('frame,slot,code,routine,x,y,xvel,yvel,hits,mapping,timer,flags,camx,camy,playerx,playery,control,fg_signal\n')
local previous='';local pictures={};local stopped=false
while emu.framecount()<plan.last_frame do
 emu.frameadvance()
 local slot=w(0xFAA4)
 if slot>=0xB0DE and slot<0xCAE2 then
  local code=l(slot);local routine=b(slot+5);local hits=b(slot+0x29)
  local key=string.format('%X:%X:%X',code,routine,hits)
  if key~=previous then
   previous=key;local f=emu.framecount()
   file:write(string.format('%d,%X,%X,%d,%d,%d,%d,%d,%d,%d,%d,%X,%d,%d,%d,%d,%d,%X\n',f,slot,code,routine,w(slot+0x10),w(slot+0x14),w(slot+0x18),w(slot+0x1A),hits,b(slot+0x22),w(slot+0x2E),b(slot+0x38),w(0xEE78),w(0xEE7C),w(0xB010),w(0xB014),b(0xB02E),w(0xEEC8)))
   local presentation=string.format('%X-%X',code,routine)
   if not pictures[presentation] then
    pictures[presentation]=true;client.screenshot(out..'/f'..f..'-'..presentation..'.png')
   end
  end
  if code==0x7BD4C and not stopped then
   savestate.save(out..'/super-phase.State');stopped=true
  end
  -- loc_7BCFC's last pre-ending frame: next decrement would enter the excluded ending.
  if code==0x7BCFC and w(slot+0x2E)==0 then
   client.screenshot(out..'/cold-stop.png');savestate.save(out..'/cold-stop.State')
   break
  end
 end
end
file:close();local d=assert(io.open(out..'/done.txt','w'));d:write(tostring(emu.framecount())..'\n');d:close();client.exit()
