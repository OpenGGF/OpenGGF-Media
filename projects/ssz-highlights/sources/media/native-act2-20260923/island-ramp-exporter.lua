-- Isolated loc_58F52/loc_5906A arithmetic oracle, declared SSZ2 stage18.
-- No engine gameplay state is imported from this native diagnostic.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(emu.framecount()==419846)
local boss=mainmemory.read_u16_be(0xFAA4);assert(mainmemory.read_u32_be(boss)==0x7BCFC)
mainmemory.write_u32_be(boss,0x852A0)
mainmemory.write_u8(0xEE0A,0xFF);mainmemory.write_u16_be(0xEECC,0)
movie.stop();client.speedmode(6400);client.invisibleemulation(true)
local log=assert(io.open(out..'/samples.csv','w'));log:write('sample,seed,camera,new_drift,bgx\n')
local samples={{0x208000,0x880},{0xFFFF8000,0x885},{0x80008000,0x880},{0x208000,0x720}}
for i,s in ipairs(samples) do
 mainmemory.write_u16_be(0xEEC0,0x18);mainmemory.write_u16_be(0xEEC2,0)
 mainmemory.write_u16_be(0xEE7C,s[2]);mainmemory.write_u16_be(0xEE84,s[2]);mainmemory.write_u16_be(0xEE8C,0x5E)
 for x=0,0x1FF do mainmemory.write_u8(0xA800+x,0) end
 mainmemory.write_u32_be(0xA800,s[1]);mainmemory.write_u16_be(0xA804,0x1234);mainmemory.write_u16_be(0xA914,77)
 emu.frameadvance()
 local f=assert(io.open(out..'/sample'..i..'.bin','wb'))
 for x=4,0x197 do f:write(string.char(mainmemory.read_u8(0xA800+x))) end
 for x=0,0x37F do f:write(string.char(mainmemory.read_u8(0xE000+x))) end
 f:close()
 log:write(string.format('%d,%u,%d,%u,%d\n',i,s[1],mainmemory.read_u16_be(0xEE84),mainmemory.read_u32_be(0xA800),mainmemory.read_u16_be(0xEE8C)))
end
log:close();local f=assert(io.open(out..'/done.txt','w'));f:write('ok');f:close();client.exit()
