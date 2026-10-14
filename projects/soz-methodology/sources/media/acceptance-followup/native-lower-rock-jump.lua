-- Positioned SOZ2 switch/door corroboration, 2026-09-15; not a cold route.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
movie.stop();assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(mainmemory.read_u16_be(0xFE10)==0x801)
client.invisibleemulation(false);client.speedmode(6400)
-- Let the title/entry owner release controls before any positioned setup.
for i=1,600 do
 if mainmemory.read_u8(0xF7CA)==0 then break end
 joypad.set({});emu.frameadvance()
end
assert(mainmemory.read_u8(0xF7CA)==0,'title must release controls')
local function position()
 mainmemory.write_u32_be(0xB010,0x47540000);mainmemory.write_u32_be(0xB014,0x5AD0000)
 mainmemory.write_u16_be(0xB018,0);mainmemory.write_u16_be(0xB01A,0);mainmemory.write_u16_be(0xB01C,0)
 mainmemory.write_u8(0xB02A,2);mainmemory.write_u8(0xB02E,0);mainmemory.write_u8(0xB020,0)
 mainmemory.write_u8(0xB005,2)
end
local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
-- Let camera/object placement streaming catch up while holding the declared entry.
local ready=false
for i=1,1200 do
 position();joypad.set(keys);emu.frameadvance()
 for slot=0,109 do
  local a=0xB000+slot*0x4A
  if mainmemory.read_u32_be(a+0xC)==0x41B56 and mainmemory.read_u16_be(a+0x44)==0x4830 then ready=true end
 end
 if ready then break end
end
assert(ready,'camera streaming must load target door before observation')
position()
mainmemory.write_u8(0xB005,2)
mainmemory.write_u16_be(0xFE20,99) -- declared local hazard-survival setup
local log=assert(io.open(out..'/mechanisms.csv','w'))
log:write('frame,lfc,x,y,status,charge,switch_x,door_y,rock_slot,rock_x,rock_y,rock_routine\n')
local jumpFrames=0
for frame=0,1199 do
 local charge=mainmemory.read_u8(0xF7EB)
 assert(mainmemory.read_u8(0xF7CA)==0,'input lock returned')
 keys['P1 Right']=true
 keys['P1 C']=frame<30
 if keys['P1 C'] then jumpFrames=jumpFrames+1 end
 joypad.set(keys);emu.frameadvance()
 local sx,dy=-1,-1
 for slot=0,109 do
  local a=0xB000+slot*0x4A;local mapping=mainmemory.read_u32_be(a+0xC)
  if mapping==0x41B56 and mainmemory.read_u16_be(a+0x44)==0x4830 then sx=mainmemory.read_u16_be(a+0x10) end
  if mapping==0x41C72 and mainmemory.read_u16_be(a+0x44)==0x4A10 then dy=mainmemory.read_u16_be(a+0x14) end
 end
 local rock=mainmemory.read_u16_be(0xF7C4)
 log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xB010),mainmemory.read_u16_be(0xB014),mainmemory.read_u8(0xB02A),mainmemory.read_u8(0xF7EB),sx,dy,rock,mainmemory.read_u16_be(rock+0x10),mainmemory.read_u16_be(rock+0x14),mainmemory.read_u32_be(rock)))
 if frame==0 or frame==150 or frame==300 or frame==1199 then client.screenshot(out..'/mechanisms-'..frame..'.png') end
end
log:close();client.exit()
