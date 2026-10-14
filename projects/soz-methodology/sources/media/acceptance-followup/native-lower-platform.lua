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
 mainmemory.write_u32_be(0xB010,0x48080000);mainmemory.write_u32_be(0xB014,0x5AD0000)
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
mainmemory.write_u16_be(0xFE20,99) -- local setup only
-- Declared positioned pair: put the live P2 at the same switch approach.
for _,offset in ipairs({0x10,0x14,0x18,0x1C}) do
 mainmemory.write_u32_be(0xB04A+offset,mainmemory.read_u32_be(0xB000+offset))
end
mainmemory.write_u8(0xB04F,2);mainmemory.write_u8(0xB074,2);mainmemory.write_u8(0xB078,0)
local log=assert(io.open(out..'/mechanisms.csv','w'))
log:write('frame,lfc,x,y,status,charge,switch_x,door_y,rock_slot,rock_x,rock_y,rock_routine\n')
local controls=assert(io.open(out..'/controls.csv','w'));controls:write('frame,phase,x,y,vx,vy,ground,charge,right,left,jump\n')
local jumpFrames=0
local phase=0;local start=0
for frame=0,1199 do
 if frame<10 then
 local d=assert(io.open(out..'/debug-'..frame..'.txt','w'))
 for _,a in ipairs({0xF602,0xF604,0xF7CA,0xB000,0xB004,0xB018,0xB01A,0xB02E,0xB032,0xEE00,0xEE04,0xEE14,0xEE16}) do d:write(string.format('%04X=%04X\n',a,mainmemory.read_u16_be(a))) end
 d:close()
end
local charge=mainmemory.read_u8(0xF7EB)
 -- Control may legitimately lock at a later event; observe passage first.
 local x=mainmemory.read_u16_be(0xB010)
 local ground=(mainmemory.read_u8(0xB02A) & 2)==0
 local speed=mainmemory.read_s16_be(0xB01C)
 for k,v in pairs(keys) do keys[k]=false end
 if phase==0 and charge==128 then phase=1;start=frame end
 if phase==1 and frame-start>25 and ground then phase=2;start=frame end
 keys['P2 Right']=true
 keys['P1 Right']=true
 if phase==1 then
  local desired=math.max(-256,math.min(256,(0x4850-x)*32))
  local vx=mainmemory.read_s16_be(0xB018)
  keys['P1 Right']=vx<desired;keys['P1 Left']=vx>desired
 end
 keys['P1 C']=(phase==1 and frame-start<20) or (phase==2 and frame-start>=1 and frame-start<25) or (phase==2 and x>=0x48F0 and x<0x4A40 and (frame-start)%45<20)
 controls:write(string.format('%d,%d,%d,%d,%d,%d,%s,%d,%s,%s,%s\n',frame,phase,x,mainmemory.read_u16_be(0xB014),mainmemory.read_s16_be(0xB018),mainmemory.read_s16_be(0xB01A),tostring(ground),charge,tostring(keys['P1 Right']),tostring(keys['P1 Left']),tostring(keys['P1 C'])))
 joypad.set(keys);emu.frameadvance()
 local sx,dy=-1,-1
 for slot=0,109 do
  local a=0xB000+slot*0x4A;local mapping=mainmemory.read_u32_be(a+0xC)
  if mapping==0x41B56 and mainmemory.read_u16_be(a+0x44)==0x4830 then sx=mainmemory.read_u16_be(a+0x10) end
  if mapping==0x41C72 and mainmemory.read_u16_be(a+0x44)==0x4A10 then dy=mainmemory.read_u16_be(a+0x14) end
 end
 local rock=mainmemory.read_u16_be(0xF7C4)
 log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xB010),mainmemory.read_u16_be(0xB014),mainmemory.read_u8(0xB02A),mainmemory.read_u8(0xF7EB),sx,dy,rock,mainmemory.read_u16_be(rock+0x10),mainmemory.read_u16_be(rock+0x14),mainmemory.read_u32_be(rock)))
 if frame%60==0 then client.screenshot(out..'/mechanisms-'..frame..'.png') end
end
controls:close();log:close();local done=assert(io.open(out..'/complete.txt','w'));done:write('1200 observations complete\n');done:close();client.exit()
