-- Lava Reef act 2 background after the seamless act change.
-- s3k-sonic-tails-complete-emeralds/lrz: bk2_frame_offset 389982, pre_trace_osc_frames 1,
-- so trace row r is movie frame 389983 + r. The act word flips at row 25558 (camera_x
-- 0x2C00 -> 0x0000, player 0x2C9E -> 0x009E, camera_y 0x0710 throughout).
return {
  frames = {415532, 415541, 415543, 415549, 415586, 415641, 416433},
  save_state_frame = 415400,
  save_state_path = os.getenv('OGGF_NATIVE_OUTPUT') .. '/lrz-act-change.State',
}
