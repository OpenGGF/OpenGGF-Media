-- SOZ1 desert presentation corroboration: ordinary jump/right from saved entry.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
movie.stop();assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(mainmemory.read_u16_be(0xFE10)==0x800)
client.invisibleemulation(false);client.speedmode(6400)
local f=assert(io.open(out..'/desert.csv','w'))
f:write('frame,lfc,x,y,bgx,bgy,phase,pal0,pal1,pal2,pal3')
for i=0,223 do f:write(',h'..i) end;f:write('\n')
for frame=0,599 do
 local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
 keys['P1 Right']=true; keys['P1 C']=(frame%80)<20
 joypad.set(keys);emu.frameadvance()
 f:write(string.format('%d,%d,%d,%d,%d,%d,%d',frame,mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xEE80),mainmemory.read_u16_be(0xEE84),mainmemory.read_u16_be(0xEE8C),mainmemory.read_u16_be(0xEE90),mainmemory.read_u8(0xF7F1)))
 for i=0,3 do f:write(','..mainmemory.read_u16_be(0xFC58+i*2)) end
 for i=0,223 do f:write(','..mainmemory.read_u32_be(0xE000+i*4)) end;f:write('\n')
 if frame==0 or frame==150 or frame==300 or frame==599 then client.screenshot(out..'/desert-'..frame..'.png') end
end
f:close();client.exit()
