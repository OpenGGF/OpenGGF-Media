-- 2026-09-15 common host refactor: read-only SOZ save-state capture smoke check.
local out=assert(os.getenv('OGGF_FBZ_VISUAL_OUTPUT'))
local plan=dofile(assert(os.getenv('OGGF_FBZ_VISUAL_PLAN')))
movie.stop()
assert(savestate.load(assert(os.getenv('OGGF_FBZ_FIXTURE_STATE'))),'native state load failed')
assert(mainmemory.read_u16_be(0xFE10)==0x0800+plan.fresh_entry_act-1,'unexpected zone')
local log=assert(io.open(out..'/observations.csv','w'))
log:write('frame,zone,lfc,control_lock\n')
for i=1,3 do
 emu.frameadvance()
 log:write(string.format('%d,%d,%d,%d\n',i,mainmemory.read_u16_be(0xFE10),mainmemory.read_u16_be(0xFE04),mainmemory.read_u8(0xF7CA)))
end
log:close()
client.screenshot(out..'/native.png')
client.exit()
