-- One-off source corroboration: positioned SOZ2 loop fall-through, 2026-09-15.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
movie.stop(); assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(mainmemory.read_u16_be(0xFE10)==0x801,'SOZ2 required')
client.invisibleemulation(false); client.speedmode(6400)
local function position()
 mainmemory.write_u32_be(0xB010,0xB500000);mainmemory.write_u32_be(0xB014,0x1000000)
 mainmemory.write_u16_be(0xB018,0);mainmemory.write_u16_be(0xB01A,0)
 mainmemory.write_u16_be(0xB01C,0);mainmemory.write_u8(0xB02A,2)
 mainmemory.write_u8(0xB02E,0);mainmemory.write_u8(0xB020,0)
end
position()
local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
for i=1,300 do position();joypad.set(keys);emu.frameadvance() end
position()
mainmemory.write_u32_be(0xB014,0x1300000);mainmemory.write_u16_be(0xB01A,0x800)
local log=assert(io.open(out..'/loop.csv','w'));log:write('frame,lfc,x,y,vy,control,status,owner\n')
local acquired,released=false,false
for frame=0,79 do
 joypad.set(keys);emu.frameadvance()
 local owner=0
 for slot=0,109 do
  local a=0xB000+slot*0x4A
  if mainmemory.read_u32_be(a)==0x4045E and mainmemory.read_u16_be(a+0x10)==0xB50 then owner=a end
 end
 local control=mainmemory.read_u8(0xB02E)
 if control==0x81 then acquired=true end
 if acquired and control==0 then released=true end
 log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d\n',frame,mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xB010),mainmemory.read_u16_be(0xB014),mainmemory.read_s16_be(0xB01A),control,mainmemory.read_u8(0xB02A),owner))
 if frame==0 or frame==10 or (released and frame<40) then client.screenshot(out..'/loop-'..frame..'.png') end
 if released then break end
end
log:close()
if released then local f=assert(io.open(out..'/released.json','w'));f:write('{"released":true}\n');f:close() end
client.exit()
