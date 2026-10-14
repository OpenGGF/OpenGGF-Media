-- Temporary read-only native boulder oracle; no RAM writes or engine state input.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_NATIVE_PLAN')))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(movie.isloaded() and emu.framecount()==plan.state_frame)
client.speedmode(6400);client.invisibleemulation(true)
local log=assert(io.open(out..'/state.csv','w'))
log:write('frame,zone,px,py,pvx,pvy,ctl,rings,timer,camx,camy,flags,bcode,bx,bxs,by,bys,bvx,bvy,captured,angle1,angle2,knuxframe\n')
local shots=0
while emu.framecount()<plan.last do
 emu.frameadvance()
 local f=emu.framecount(); local zone=mainmemory.read_u16_be(0xFE10)
 if f>=plan.first then
  local b=0;local k=0
  for slot=2,129 do
   local a=0xB000+slot*0x4A
   local code=mainmemory.read_u32_be(a)&0xFFFFFF
   local map=mainmemory.read_u32_be(a+0xC)&0xFFFFFF
   if code>=0x63C3E and code<=0x63CAC then b=a end
   if mainmemory.read_u8(a+0x2C)==0x24 and code~=0 then k=a end
  end
  local function w(a) return a~=0 and mainmemory.read_u16_be(a) or 0 end
  local function bw(a) return b~=0 and mainmemory.read_u16_be(b+a) or 0 end
  local function bb(a) return b~=0 and mainmemory.read_u8(b+a) or 0 end
  log:write(string.format('%d,%X,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%X,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',f,zone,w(0xB010),w(0xB014),w(0xB018),w(0xB01A),mainmemory.read_u8(0xB02E),w(0xFE20),mainmemory.read_u32_be(0xFE22),w(0xEE78),w(0xEE7C),mainmemory.read_u8(0xFAB8),b~=0 and mainmemory.read_u32_be(b) or 0,bw(0x10),bw(0x12),bw(0x14),bw(0x16),bw(0x18),bw(0x1A),bb(0x38),bb(0x3C),bb(0x3D),k~=0 and mainmemory.read_u8(k+0x22) or 0))
  if b~=0 and shots<8 and f%40==0 then client.invisibleemulation(false);emu.frameadvance();client.screenshot(out..'/f'..emu.framecount()..'.png');client.invisibleemulation(true);shots=shots+1 end
  if zone==0x1600 then client.invisibleemulation(false);emu.frameadvance();client.screenshot(out..'/arrival.png');break end
 end
end
log:close();local done=assert(io.open(out..'/done.txt','w'));done:write('read-only movie observation completed\n');done:close();client.exit()
