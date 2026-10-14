-- SOZ native entry observation. Read-only saved-state continuation; no position writes.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
movie.stop();assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
client.speedmode(6400)
local log=assert(io.open(out..'/entry.csv','w'))
log:write('frame,lfc,x,y,vx,vy,status,control,lock,debug,mode\n')
for frame=0,1799 do
 local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
 joypad.set(keys);emu.frameadvance()
 if frame%30==0 then
  log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xB010),mainmemory.read_u16_be(0xB014),mainmemory.read_s16_be(0xB018),mainmemory.read_s16_be(0xB01A),mainmemory.read_u8(0xB02A),mainmemory.read_u8(0xB02E),mainmemory.read_u8(0xF7CA),mainmemory.read_u16_be(0xFE08),mainmemory.read_u8(0xF600)))
 end
 if mainmemory.read_u8(0xF7CA)==0 then savestate.save(out..'/ready.State');break end
end
log:close();client.screenshot(out..'/last.png');client.exit()
