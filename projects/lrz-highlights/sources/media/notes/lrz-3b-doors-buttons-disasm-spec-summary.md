# LRZ 3b — $19 door, $1A big door, $1C horizontal button, $1D shooting trigger, $33 button, Level_trigger_array
Secondhand research summary relayed by the lead 2026-09-17 (parent agent exited first). Re-read every cited line before writing a test. Lines = sonic3k.asm @1a454a0e.
No routine tables: code-pointer state machines, init falls through into first state the same frame. None has FixBugs branches.
$19 Obj_LRZDoor (:88015, $4292A; Map $429DA 2 frames): art $43A1 (act 2: frame 1, RAW tile $090 -> $4090, height $20), width $10, height $28, priority $200, rest y saved at $46.
 Waiting: tst.b Level_trigger_array[subtype&$F] — WHOLE BYTE, any bit opens. sfx_DoorOpen. Opening: BYTE counter $2E to $40, y = rest − sin(counter)/4 (up $40 px, 64 frames, word write),
 final frame applied. Solid always (closed too): SolidObjectFull d1 $1B, d2 height, d3 d2+1. Sprite_OnScreen_Test. Never closes; no respawn memory (reload replays animation + sfx).
$1A Obj_LRZBigDoor (:88070, $42A18; Map $42B24 1 frame, 24 pieces): art $43A1, width $30, height $40, priority $280. Respawn entry bit 0 = already opened -> start y+$80 settled.
 Trigger PLAYER 1 ONLY: $40 <= (Py−Dy) < $C0 (unsigned bhs on −$40-biased delta) AND (Px−Dx) >= $50 (signed, no upper bound). Sets Screen_shake_flag −1, sfx_BigRumble, bset respawn bit 0.
 Opening: BYTE counter to $40, y = rest + sin/2 (DOWN $80), re-rumble when (Level_frame_counter+1)&$F==0 (global clock), Draw_Sprite (not deletable while moving); end clears Screen_shake_flag.
 Solid d1 $3B d2 $40 d3 $41 in both moving and settled states.
$1C Obj_LRZButtonHorizontal (:88221, $42CD6; Map $42D7C / act 2 Map2 $42D9E): art $63A1 (act 2 $240D), width/height $10, priority $280.
 SolidObjectFull d1 $10 (NOT $1B), d2 $F, d3 $10. PRESS = SolidObjectFull's d6 OUT high word: swap d6; andi #3 (bit0 P1 side-push, bit1 P2 side-push). Not standing_mask.
 Subtype: bits0-3 array index; bit4 latch (never cleared); bit6 -> use array bit 7 instead of bit 0. sfx_Switch only if whole byte was 0. frame 1 pressed.
 If the engine's SolidObjectFull port does not return the side-push result, this button can never press.
$1D Obj_LRZShootingTrigger (:88279, $42DBE; Map $42F06): art $63A1, 16x16, priority $280, collision_flags $C6 (special, size 6 = $10x$10): Touch_Special loc_103FA ADDs to collision_property
 (P1 +1, P2 +2). Interval $30 = ((subtype&$F0)>>4)*4; WORD countdown $2E, reload BEFORE the on-screen test; fires only if render bit 7; first frame reloads only.
 Shot: AllocateObjectAfterCurrent, code loc_42EE8, art $03A1, priority $300, 4x4, collision $98, shield_reaction bit 3, frame 1, x_vel ±$200 (status bit0), y_vel +$200, MoveSprite2 (no gravity),
 deleted first frame off-screen, sfx_Projectile. sub_42EC0 (:88349): requires anim(a1)==2; negates player x_vel,y_vel; bset bit 0 of array byte (always bit 0); becomes Obj_Explosion routine 2 (no animal).
$33 Obj_Button (:60726, $2C518) in both SK sets: zone 9 branch Map_LRZButton art $63A1 (act 2 ArtTile_LRZ2Misc+$1C pal 1 = $2429); y += 4; subtype bit5 clear -> SolidObjectFull d1 $1B d2 4 d3 5,
 set -> SolidObjectTop d1 $10 d3 6; press = status & standing_mask; bits 0-3 index, 4 latch, 6 -> bit 7.
Level_trigger_array $F7E0 (16 bytes). Cleared at level load by clearRAM Tails_CPU_interact,$100 (:7621). Clear_Switches (:104284) clears $20 BYTES = the array AND Anim_Counters ($F7F0);
 called from every seamless act change incl. LRZ loc_56CAA (:115356) before Load_Level, together with clr LRZ_rocks_routine, Respawn_table_keep, Boss_flag and the −$2C00 rebase.
 Array is shared with non-button code (HCZ water flag, +8 elsewhere).
