-- SOZ pushable-rock diagnostic, 2026-09-15. Seeded position, not cold-route evidence.
-- Loads the prior native SOZ1 LFC35 state, normalizes P1 position/motion/control,
-- then uses ordinary neutral/right input only. ROM rules: Obj_SOZPushableRock $40546.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
movie.stop() -- Saved after movie playback ended; detach before loading.
local loaded=savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE')))
local zone=mainmemory.read_u16_be(0xFE10)
console.log(string.format('SOZ probe load=%s zone=%04X',tostring(loaded),zone))
assert(zone==0x0800,'SOZ1 native state required')
client.invisibleemulation(false);client.speedmode(6400)
-- Obj_LevelIntro_PlayerFallIntoGround: loc_420A6 waits for a fresh jump;
-- loc_4213C releases control after the player emerges. Finish with ordinary input.
local intro=assert(io.open(out..'/intro.csv','w'))
intro:write('frame,y,lock,jump\n')
for frame=0,299 do
 local jump=false
 for slot=0,109 do
  if mainmemory.read_u32_be(0xB000+slot*0x4A)==0x420A6 then jump=true end
 end
 local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
 keys['P1 C']=jump;joypad.set(keys);emu.frameadvance()
 intro:write(string.format('%d,%d,%d,%d\n',frame,mainmemory.read_u16_be(0xB014),mainmemory.read_u8(0xF7CA),jump and 1 or 0))
 if mainmemory.read_u8(0xF7CA)==0 then break end
end
intro:close()
assert(mainmemory.read_u8(0xF7CA)==0,'native intro jump must release control before positioned setup')
mainmemory.write_u32_be(0xB010,0x3B00000)
mainmemory.write_u32_be(0xB014,0x5EC0000)
mainmemory.write_u16_be(0xB018,0);mainmemory.write_u16_be(0xB01A,0)
mainmemory.write_u16_be(0xB01C,0);mainmemory.write_u8(0xB02A,0)
mainmemory.write_u8(0xB02E,0);mainmemory.write_u8(0xB020,0)
local log=assert(io.open(out..'/pushable.csv','w'))
log:write('frame,lfc,px,py,rock,x,y,vx,vy,phase,timer,target,cursor,status\n')
local falling=false
for frame=0,799 do
 local keys={};for _,k in ipairs({'Up','Down','Left','Right','A','B','C','Start'}) do keys['P1 '..k]=false end
 keys['P1 Right']=frame>=30 and not falling
 joypad.set(keys);emu.frameadvance()
 if frame==60 then
  local d=assert(io.open(out..'/controls.txt','w'))
  for k,v in pairs(joypad.get()) do d:write(tostring(k)..'='..tostring(v)..'\n') end
  for _,a in ipairs({0xF602,0xF604,0xF7CA,0xB000,0xB002,0xB004,0xB02E,0xB032}) do d:write(string.format('%04X=%04X\n',a,mainmemory.read_u16_be(a))) end
  d:close()
 end
 for slot=0,109 do
  local a=0xB000+slot*0x4A
  if mainmemory.read_u32_be(a+0xC)==0x40776 and mainmemory.read_u8(a+0x2C)%32==9 then
   if mainmemory.read_u32_be(a)==0x405D8 then falling=true end
   log:write(string.format('%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,
    mainmemory.read_u16_be(0xFE04),mainmemory.read_u16_be(0xB010),mainmemory.read_u16_be(0xB014),a,
    mainmemory.read_u16_be(a+0x10),mainmemory.read_u16_be(a+0x14),mainmemory.read_s16_be(a+0x18),mainmemory.read_s16_be(a+0x1A),
    mainmemory.read_u32_be(a),mainmemory.read_s16_be(a+0x32),mainmemory.read_u16_be(a+0x3A),mainmemory.read_u32_be(a+0x36),mainmemory.read_u8(a+0x2A)))
  end
 end
 if frame==30 or frame==300 or frame==500 or frame==700 then client.screenshot(out..'/pushable-'..frame..'.png') end
end
log:close();client.exit()
