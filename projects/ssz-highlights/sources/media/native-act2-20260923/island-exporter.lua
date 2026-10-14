-- Declared SSZ2 presentation seed at the native pre-ending stop.
-- Retire only the defeated boss so it cannot allocate the excluded ending owner;
-- write that owner's documented negative Events_fg_4 signal. No engine state input.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(emu.framecount()==419846)
local w=mainmemory.read_u16_be;local l=mainmemory.read_u32_be
local boss=w(0xFAA4);assert(l(boss)==0x7BCFC)
mainmemory.write_u32_be(boss,0x852A0) -- Go_Delete_Sprite
mainmemory.write_u16_be(0xEEC4,0xFF00)
mainmemory.write_u8(0xEE0A,0xFF) -- loc_5E70E Scroll_lock, required with omitted owner
mainmemory.write_u16_be(0xEECC,0) -- loc_5E70E clears Screen_shake_flag
-- The omitted loc_85EE6 worker restores the saved palette after the white fade.
-- Seed its completed palette, preserving the saved native colors rather than inventing RGB.
for offset=0,127 do mainmemory.write_u8(0xFC00+offset,mainmemory.read_u8(0xFC80+offset)) end
movie.stop();client.speedmode(6400);client.invisibleemulation(false)
local f=assert(io.open(out..'/island.csv','w'))
f:write('pass,stage,camera_y,cloud,signal,remaining\n')
for pass=0,5000 do
 local stage=w(0xEEC0);local remain=w(0xEECA)
 f:write(string.format('%d,%d,%d,%d,%d,%d\n',pass,stage,w(0xEE7C),l(0xEE9C),w(0xEEC4),remain))
 if pass%60==0 or stage==12 then client.screenshot(out..string.format('/%05d.png',pass)) end
 -- Next ScreenEvent finishes the redraw and falls into excluded sub_5B18E.
 if stage==12 and remain==1 then break end
 emu.frameadvance()
end
assert(w(0xEEC0)==12 and w(0xEECA)==1,'did not reach pre-ending redraw boundary')
f:close();local done=assert(io.open(out..'/done.txt','w'));done:write(tostring(emu.framecount()));done:close();client.exit()
