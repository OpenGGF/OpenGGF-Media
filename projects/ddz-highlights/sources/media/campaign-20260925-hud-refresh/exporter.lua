-- Native DDZ entry HUD observation: no RAM writes; post-frame Ring_count/redraw.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(emu.framecount()==514214)
movie.stop();client.speedmode(6400);client.invisibleemulation(false)
local f=assert(io.open(out..'/rings.csv','w'))
f:write('pass,rings,redraw\n')
for pass=0,120 do
 f:write(string.format('%d,%d,%d\n',pass,mainmemory.read_u16_be(0xFE20),mainmemory.read_u8(0xFE1D)))
 client.screenshot(out..string.format('/%03d.png',pass))
 emu.frameadvance()
end
f:close();local done=assert(io.open(out..'/done.txt','w'));done:write('ok');done:close();client.exit()
