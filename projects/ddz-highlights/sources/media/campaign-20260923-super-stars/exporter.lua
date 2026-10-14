-- DDZ Super-star oracle from native entry; declare no Super Emeralds so loc_8167C
-- selects loc_8242A instead of Hyper effects. All other movie state is retained.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(emu.framecount()==514214)
mainmemory.write_u8(0xFFB1,0)
movie.stop();client.speedmode(6400);client.invisibleemulation(false)
local f=assert(io.open(out..'/stars.csv','w'))
f:write('pass,code,x,y,frame,timer,player_x,player_y,art,priority\n')
local w=mainmemory.read_u16_be;local b=mainmemory.read_u8
for pass=0,100 do
 local s=0xCBC0
 f:write(string.format('%d,%X,%d,%d,%d,%d,%d,%d,%X,%X\n',pass,mainmemory.read_u32_be(s),w(s+0x10),w(s+0x14),b(s+0x22),b(s+0x24),w(0xB010),w(0xB014),w(s+0xA),w(s+8)))
 if pass>=50 and pass<=70 then client.screenshot(out..string.format('/%03d.png',pass)) end
 emu.frameadvance()
end
f:close();local done=assert(io.open(out..'/done.txt','w'));done:write('ok');done:close();client.exit()
