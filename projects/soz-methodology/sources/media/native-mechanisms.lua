-- Positioned SOZ2 switch/door corroboration, 2026-09-15; not a cold route.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
movie.stop();assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(mainmemory.read_u16_be(0xFE10)==0x801)
client.invisibleemulation(false);client.speedmode(6400)
local function position()
 mainmemory.write_u32_be(0xB010,0x26000000);mainmemory.write_u32_be(0xB014,0x1A40000)
 mainmemory.write_u16_be(0xB018,0);mainmemory.write_u16_be(0xB01A,0);mainmemory.write_u16_be(0xB01C,0)
 mainmemory.write_u8(0xB02A,2);mainmemory.write_u8(0xB02E,0);mainmemory.write_u8(0xB020,0)
end
local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
-- Let camera/object placement streaming catch up while holding the declared entry.
local ready=false
for i=1,1200 do
 position();joypad.set(keys);emu.frameadvance()
 for slot=0,109 do
  local a=0xB000+slot*0x4A
  if mainmemory.read_u32_be(a+0xC)==0x41C72 and mainmemory.read_u16_be(a+0x44)==0x268C then ready=true end
 end
 if ready then break end
end
assert(ready,'camera streaming must load target door before observation')
position()
local log=assert(io.open(out..'/mechanisms.csv','w'))
log:write('frame,lfc,x,y,status,charge,switch_x,door_y\n')
local jumpFrames=0
for frame=0,599 do
 local charge=mainmemory.read_u8(0xF7E8)
 keys['P1 Right']=true
 keys['P1 C']=charge>=120 or (jumpFrames>0 and jumpFrames<20)
 if keys['P1 C'] then jumpFrames=jumpFrames+1 end
 joypad.set(keys);emu.frameadvance()
 local sx,dy=-1,-1
 for slot=0,109 do
  local a=0xB000+slot*0x4A;local mapping=mainmemory.read_u32_be(a+0xC)
  if mapping==0x41B56 and mainmemory.read_u16_be(a+0x44)==0x2630 then sx=mainmemory.read_u16_be(a+0x10) end
  if mapping==0x41C72 and mainmemory.read_u16_be(a+0x44)==0x268C then dy=mainmemory.read_u16_be(a+0x14) end
 end
 log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d\n',frame,mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xB010),mainmemory.read_u16_be(0xB014),mainmemory.read_u8(0xB02A),mainmemory.read_u8(0xF7E8),sx,dy))
 if frame==0 or frame==150 or frame==300 or frame==599 then client.screenshot(out..'/mechanisms-'..frame..'.png') end
end
log:close();client.exit()
