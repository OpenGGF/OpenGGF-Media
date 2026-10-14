# Connected cold SOZ2 route attempt

Native 320-pixel Sonic + Tails, donor off; cold Act 2. Production omitted-title lifecycle and initial ProcessSprites setup consumed before recorded inputs. No position, plane, checkpoint, or other gameplay state writes after boot. Exact full controller sequence is `Input Log.txt`; `tail.script` records the latest authored tail (older prefix comments may be stale; full input log is authoritative). CSV records every frame and PNGs every 30 frames plus chunk boundaries.

Initial 1500 inputs originate at zero-based index 365809 of the original complete-emeralds BK2; all later inputs are authored. The original native route started seamlessly, so these are an adapted cold-route attempt, not native movie replay certification. Native comparison rows were consulted only for route direction, never hydration. Runtime used current compiled bfce36a2c branch (root306d7fe0f plus final-swing fix).

Recorded rows: 8097. Last CSV row:

```csv
frame,x,y,xvel,yvel,gspeed,air,rolling,spindash,hurt,dead,rings,mapping_frame,cam_x,cam_y,mode,input,checkpoint,ghosts
8096,3339,940,-24,0,-24,0,0,0,0,0,25,183,3195,844,LEVEL,|..L.....|........|,1,2
```

This is bounded traversal evidence, not Act 2 completion. Rock-ride-3 ends in a late-jump door crush; rock-ride-5 crosses that door and reaches the tall chamber but misses the upper wire. Wire-approach variants are input-timing experiments for boarding the swinging platform/handle.
