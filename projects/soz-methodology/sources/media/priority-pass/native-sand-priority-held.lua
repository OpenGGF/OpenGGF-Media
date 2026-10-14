-- SOZ rising-sand sprite layering probe, 2026-09-16 priority pass.
-- Positioned setup at 20C0/056C, then repeated P1 holds at 22A0/0340 from frame500.
-- Isolated presentation probe; NOT ordinary gameplay or trajectory parity.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_NATIVE_PLAN')))
movie.stop();assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(mainmemory.read_u16_be(0xFE10)==0x801)
client.invisibleemulation(false);client.speedmode(6400)
local function position()
 mainmemory.write_u32_be(0xB010,0x20C00000);mainmemory.write_u32_be(0xB014,0x056C0000)
 mainmemory.write_u16_be(0xB018,0);mainmemory.write_u16_be(0xB01A,0);mainmemory.write_u16_be(0xB01C,0)
 mainmemory.write_u8(0xB02A,2);mainmemory.write_u8(0xB02E,0);mainmemory.write_u8(0xB020,0)
end
local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
local ready=false
for i=1,1200 do
 position();joypad.set(keys);emu.frameadvance()
 if mainmemory.read_u16_be(0xEE78)>=0x2000 and mainmemory.read_u16_be(0xEEC2)==0x10 then ready=true;break end
end
assert(ready,'camera and background admission not ready')
position();mainmemory.write_u16_be(0xFE20,99)
local log=assert(io.open(out..'/observations.csv','w'))
log:write('frame,lfc,x,y,cam_x,cam_y,bg,sand,pillar_x,pillar_y,pillar_tile,pillar_bucket\n')
for frame=0,#plan.inputs-1 do
 if frame>=500 then
  mainmemory.write_u32_be(0xB010,0x22A00000);mainmemory.write_u32_be(0xB014,0x03400000)
  mainmemory.write_u16_be(0xB018,0);mainmemory.write_u16_be(0xB01A,0);mainmemory.write_u16_be(0xB01C,0)
  mainmemory.write_u8(0xB02A,2);mainmemory.write_u8(0xB02E,0);mainmemory.write_u8(0xB020,0)
 end
 local mask=frame>=500 and 0 or plan.inputs[frame+1]
 keys['P1 Left']=(mask & 4)~=0;keys['P1 Right']=(mask & 8)~=0;keys['P1 C']=(mask & 16)~=0
 joypad.set(keys);emu.frameadvance()
 local px,py,tile,bucket=-1,-1,-1,-1
 for slot=0,109 do
  local a=0xB000+slot*0x4A
  -- Obj_SOZFloatingPillar uses Map_SOZFloatingPillar; find via plan-verified mapping below.
  if mainmemory.read_u32_be(a+0xC)==0x412E0 and mainmemory.read_u8(a+0x2C)==0x22 then px=mainmemory.read_u16_be(a+0x10);py=mainmemory.read_u16_be(a+0x14);tile=mainmemory.read_u16_be(a+0xA);bucket=mainmemory.read_u16_be(a+8) end
 end
 log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xB010),mainmemory.read_u16_be(0xB014),mainmemory.read_u16_be(0xEE78),mainmemory.read_u16_be(0xEE7C),mainmemory.read_u16_be(0xEEC2),mainmemory.read_u16_be(0xEE9C),px,py,tile,bucket))
 if frame%60==0 then client.screenshot(out..'/sand-'..frame..'.png') end
end
log:close();local done=assert(io.open(out..'/complete.txt','w'));done:write('complete\n');done:close();client.exit()
