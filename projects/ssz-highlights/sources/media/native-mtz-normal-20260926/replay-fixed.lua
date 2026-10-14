-- Positioned SSZ MTZ reference, 2026-09-26. Declared checkpoint/reload setup only.
-- No boss phase/health writes. Output is comparison-only; never hydrate the engine.
local out=assert(os.getenv('OGGF_NATIVE_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_NATIVE_PLAN')))
movie.stop()
assert(savestate.load(assert(os.getenv('OGGF_NATIVE_FIXTURE_STATE'))))
assert(not movie.isloaded() and emu.framecount()==449086)
client.speedmode(6400);client.invisibleemulation(true)
local b=mainmemory.read_u8;local w=mainmemory.read_u16_be;local l=mainmemory.read_u32_be
local function input(left,right,jump)
 joypad.set({['P1 Up']=false,['P1 Down']=false,['P1 Left']=left,['P1 Right']=right,['P1 A']=jump,['P1 B']=false,['P1 C']=false,['P1 Start']=false})
end
local f=assert(io.open(out..'/observations.csv','w'))
f:write('step,frame,px,py,proutine,status,rings,super,camx,camy,boss,phase,hits,orbs,bx,by,mapping,left,right,jump\n')
for i=0,plan.frames-1 do
 local boss=0
 for slot=2,129 do local a=0xB000+slot*0x4A;if l(a)==0x7A71A then boss=a;break end end
 local px=w(0xB010);local bx=boss~=0 and w(boss+0x10) or px
 local row=assert(plan.inputs[i+1]);local left=row[1]==1;local right=row[2]==1;local jump=row[3]==1
 input(left,right,jump)
 if i>=plan.first_capture and i<=plan.last_capture then client.invisibleemulation(false) end
 emu.frameadvance()
 f:write(table.concat({i,emu.framecount(),w(0xB010),w(0xB014),b(0xB005),b(0xB02A),w(0xFE20),b(0xFE19),w(0xEE78),w(0xEE7C),boss,boss~=0 and b(boss+0x26) or -1,boss~=0 and b(boss+0x29) or -1,boss~=0 and b(boss+0x3C) or -1,bx,boss~=0 and w(boss+0x14) or -1,boss~=0 and b(boss+0x22) or -1,left and 1 or 0,right and 1 or 0,jump and 1 or 0},',')..'\n')
 if i>=plan.first_capture and i<=plan.last_capture then client.screenshot(out..'/f'..string.format('%05d',i)..'.png');client.invisibleemulation(true) end
 if b(0xB005)>=6 then break end
end
f:close();local d=assert(io.open(out..'/done.txt','w'));d:write('complete\n');d:close();client.exit()
