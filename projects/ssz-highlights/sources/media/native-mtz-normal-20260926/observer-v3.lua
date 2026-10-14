-- Positioned SSZ MTZ reference, 2026-09-26. Declared checkpoint/reload setup only.
-- No boss phase/health writes. Output is comparison-only; never hydrate the engine.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_NATIVE_PLAN')))
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(emu.framecount()==448920 and mainmemory.read_u16_be(0xFE10)==0xA00)
movie.stop();client.speedmode(6400);client.invisibleemulation(true)
local b=mainmemory.read_u8;local w=mainmemory.read_u16_be;local l=mainmemory.read_u32_be
local writes=assert(io.open(out..'/setup.csv','w'));writes:write('address,size,value\n')
local function put(a,n,v) writes:write(string.format('%X,%d,%X\n',a,n,v));if n==1 then mainmemory.write_u8(a,v) elseif n==2 then mainmemory.write_u16_be(a,v) else mainmemory.write_u32_be(a,v) end end
-- Save_Level_Data/Load_Starpost_Settings bank, verified constants in sonic3k.lst.
put(0xFE2A,1,3);put(0xFE2B,1,3);put(0xFE2C,2,0xA00);put(0xFF9A,2,0xA00)
put(0xFE2E,2,0x1700);put(0xFE30,2,0x420);put(0xFE32,2,0);put(0xFE34,4,0x100)
put(0xFE38,2,0x680);put(0xFE3A,2,0xC0D);put(0xFE3C,2,0x1660);put(0xFE3E,2,0x380)
put(0xFE40,2,0x1000);put(0xFE42,1,0);put(0xFE43,1,0);put(0xFE44,2,0x1000)
put(0xFE46,1,0);put(0xFE47,1,0);put(0xFE48,1,0);put(0xFF0A,2,1);put(0xFE02,2,1)
local function input(left,right,jump)
 joypad.set({['P1 Up']=false,['P1 Down']=false,['P1 Left']=left,['P1 Right']=right,['P1 A']=jump,['P1 B']=false,['P1 C']=false,['P1 Start']=false})
end
local ready=false
for i=1,1200 do
 input(false,false,false);emu.frameadvance()
 if i>60 and w(0xFE02)==0 and w(0xB010)==0x1700 and b(0xB005)==2 and w(0xFE04)<300 then ready=true;break end
end
assert(ready,'native checkpoint reload did not settle')
assert(b(0xFE19)==0,'reload must clear transformation');assert(w(0xFF08)==1,'Sonic alone selection')
-- Declared one-time survival supply, below the transformation threshold.
put(0xFE20,2,40);put(0xFE1D,1,1);writes:close()
savestate.save(out..'/normal-entry.State')
local f=assert(io.open(out..'/observations.csv','w'))
f:write('step,frame,px,py,proutine,status,rings,super,camx,camy,boss,phase,hits,orbs,bx,by,mapping,left,right,jump\n')
for i=0,plan.frames-1 do
 local boss=0
 for slot=2,129 do local a=0xB000+slot*0x4A;if l(a)==0x7A71A then boss=a;break end end
 local px=w(0xB010);local bx=boss~=0 and w(boss+0x10) or px
 local left=boss~=0 and px>bx+12;local right=boss~=0 and px<bx-12
 local jump=boss~=0 and i%40<16
 if i<240 then left=false;right=false;jump=false end
 if boss~=0 and b(boss+0x29)<=1 then
  local target=bx<0x1700 and 0x1790 or 0x1670
  left=px>target+8;right=px<target-8;jump=false
 end
 input(left,right,jump)
 if i%4==0 then client.invisibleemulation(false) end
 emu.frameadvance()
 f:write(table.concat({i,emu.framecount(),w(0xB010),w(0xB014),b(0xB005),b(0xB02A),w(0xFE20),b(0xFE19),w(0xEE78),w(0xEE7C),boss,boss~=0 and b(boss+0x26) or -1,boss~=0 and b(boss+0x29) or -1,boss~=0 and b(boss+0x3C) or -1,bx,boss~=0 and w(boss+0x14) or -1,boss~=0 and b(boss+0x22) or -1,left and 1 or 0,right and 1 or 0,jump and 1 or 0},',')..'\n')
 if i%4==0 then client.screenshot(out..'/f'..string.format('%05d',i)..'.png');client.invisibleemulation(true) end
 if b(0xB005)>=6 then break end
end
f:close();local d=assert(io.open(out..'/done.txt','w'));d:write('complete\n');d:close();client.exit()
