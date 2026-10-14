-- Diagnostic: native final-fight support and collapsing columns, 2026-09-25.
-- Read-only complete-run movie; no RAM writes or gameplay seeds.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_NATIVE_PLAN')))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(movie.isloaded() and emu.framecount()==509032)
assert(mainmemory.read_u16_be(0xFE10)==0x1700)
local w=mainmemory.read_u16_be; local b=mainmemory.read_u8; local l=mainmemory.read_u32_be
local f=assert(io.open(out..'/floor.csv','w'))
f:write('frame,camx,copyx,coarseback,camy,px,py,pstatus,window,bossx,bossy,redraw,request,frontier,slot,code,x,y,yvel,flags,previousCamera\n')
client.speedmode(6400)
while emu.framecount()<514200 do
 local next=emu.framecount()+1
 client.invisibleemulation(next < (plan.first or 509033) or next % (plan.every or 15) ~= 0)
 emu.frameadvance()
 local frame=emu.framecount()
 for slot=0,109 do
  local a=0xB000+slot*0x4A; local code=l(a)&0xFFFFFF
  if code==0x5A7EC or code==0x5A8B2 or code==0x5A904 then
   f:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%X,%d,%d,%d,%d,%d\n',frame,w(0xEE78),w(0xEE80),w(0xF7DA),w(0xEE7C),w(0xB010),w(0xB014),b(0xB02A),w(0xEED2),w(0xEED4),w(0xEED6),w(0xEED8),w(0xEEDA),w(0xEEE8),slot,code,w(a+0x10),w(a+0x14),w(a+0x1A),b(a+4),w(a+0x2E)))
  end
 end
 if frame >= (plan.first or 509033) and frame % (plan.every or 15) == 0 then client.screenshot(out..'/f'..frame..'.png') end
end
f:close()
local d=assert(io.open(out..'/done.txt','w'));d:write('ok\n');d:close();client.exit()
