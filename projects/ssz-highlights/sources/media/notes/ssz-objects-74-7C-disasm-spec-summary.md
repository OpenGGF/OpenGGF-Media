# SSZ objects $74/$75/$76/$7A/$7B/$7C — disassembly spec summary (secondhand; re-read each cited line before coding)
Source: research subagent of the slice-2 implementer, relayed by the lead 2026-09-17. asm line numbers = sonic3k.asm @1a454a0e.
Pointer set: SSZ zone $0A -> Sprite_ListingK (SK Set 2), loader loc_1B6A8 (:37411). Code-pointer state machines; routine(a0) is only a parent kill flag.
Labels/ROM: $74 Obj_SSZRetractingSpring $46426 (:92306); $75 Obj_SSZSwingingCarrier $460D8 (:92023); $76 Obj_SSZRotatingPlatform $45DAE (:91729);
$7A Obj_SSZElevatorBar $4536C (:90793); $7B Obj_SSZCollapsingBridgeDiagonal $44D60 (:90222); $7C Obj_SSZCollapsingBridge $44C44 (:90120).
All children via AllocateObjectAfterCurrent (same-frame) + CreateNewSprite4. None write collision_flags. ArtTile_SSZMisc=$02D4.
SUBTYPES: $7C and $7B: only bit 7 (set = never collapses). $75: bit 7 (clear = pendulum Gradual_SwingOffset(#$20000,#$821)+$41, width $30 frame 1;
 set = continuous rotation ±1/frame by status bit0, width 8 frame 4, forces player facing on grab, SonicOnObjHitFloor release at x_vel ±$800 sfx_Dash);
 bits 0-1 = chain length 6+(subtype&3). $76: only bit 0, read in the invisible carrier child (width $60 vs $A0; solid half-width $6B/$AB). $74, $7A: no subtype read.
HELPERS: $74 sub_1DD0E (sloped fully solid, byte_468DC, half-width $23, acts on d6 side bit; frames 0/1 not solid -> x parked $7FFF);
 $75 rider bar SolidObjectFull d1 $23 d2 8 d3 8, side/head contact -> sub_24280 -> HurtCharacter, standing -> grab (object_control 1, roll, sfx_Roll), ABC release y_vel -$680;
 $76 pole SolidObjectTop d1 $10 d2/d3 $21, grab object_control 3, angle +=2/frame; carrier child y+$30, invisible, SolidObjectTop d1=$B+width d2/d3 $11,
 radius ramps to $14, only X orbits, writes PLAYER priority ($180/$200 back half, $100/$80 front), restores $100; pose table byte_468C4 (12 records) via loc_460A6;
 $7A no solid call: grab when |dx|<$28 and 0<=dy<$18, object_control 3, y = bar y + $14 ($11 Knuckles-alone and P2), frames $E5/$E9, swing Gradual_SwingOffset(#$18000,#$480),
 release ABC: x_vel ∓$200 by left/right (left sets bar priority $80), y_vel = (bar speed>>8) − $400 (0 extra if down), cooldown 30 (60 on death);
 $7B SolidObjectTopSloped2 d1 $40 byte_46658 (1 byte per 2 px), 8 debris frames 5/4 delays 6..48, slope ptr +4 and half-width −8 every 6 frames, y −/+2, re-grounds non-jumping standing player;
 $7C SolidObjectTop d1 $20 d2 $10 d3 9, 4 debris at x±{$18,8,−8,−$18} frames 2/1 delays 6/12/18/24, half-width −8 every 6 frames, edge nearest player retreats, park $7FFF.
 Debris loc_45052 (:90491): hangs for delay then MoveSprite (gravity $38), deletes when Draw_Sprite clears render bit 7. Shared with $7B/$7C.
$74 spring: proximity scan only on odd Level_frame_counter+1 bit 0 (the ONLY ROM clock in this set); box y[y−$50,y+$10], x[x−$60,x] (mirrored by status bit0);
 frames extend 0->1->2 (sfx_SpringLatch on 0->1), launch ±$C00 x_vel=ground_vel, states 1..3 with 8-frame hold, frames 4/3/5/3.
Maps: Map_SSZCollapsingBridge 14 frames; Map_SSZElevatorBar 5; Map_SSZRotatingPlatform 3 (Ani: dur 7, frames 0,1,2 loop); Map_SSZRetractingSpring 6.
Art tiles: $7B/$7C/debris $C2F4; $7A and $75 hub $4348; $75 arc/rider $6348; $76 $437E; $74 $03A2. Unknown: object status bit 7 set by $7B/$7C/$77 has no reader found.
