-- Observe native Hyper slots without changing gameplay RAM; DDZ entry save.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(emu.framecount()==514214)
movie.stop();client.speedmode(6400);client.invisibleemulation(false)
local f=assert(io.open(out..'/stars.csv','w'))
f:write('pass,slot,code,x,y,frame,timer,angle,kos,player_x,player_y,xacc,yacc\n')
local w=mainmemory.read_u16_be;local b=mainmemory.read_u8
for pass=0,180 do
 for child=0,3 do
  local s=0xCD7C+child*0x4A
  f:write(string.format('%d,%d,%X,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',pass,child,mainmemory.read_u32_be(s),w(s+0x10),w(s+0x14),b(s+0x22),b(s+0x24),b(s+0x26),b(0xFF60),w(0xB010),w(0xB014),w(s+0x30),w(s+0x34)))
 end
 if pass>=0 then client.screenshot(out..string.format('/%03d.png',pass)) end
 emu.frameadvance()
end
f:close();local done=assert(io.open(out..'/done.txt','w'));done:write('ok');done:close();client.exit()
