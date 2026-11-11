"""Purpose: build the promo bed from the owner-supplied track with one bar-line splice.
Edit: source bars 8-35 (11.327-50.347 s) then bars 76-end (106.090 s to file end), first bar at 0.178 s,
172.218 BPM. Join: 12 ms equal-power crossfade on the bar line (well under one beat); 4 ms head fade
to avoid a click; the track's own ending and decay are kept untouched.
Inputs: WAV path, output path. Origin: MICA & TALON production promo 2026-11-11."""
import sys,wave,numpy as np
src,dst=sys.argv[1],sys.argv[2]
w=wave.open(src);sr=w.getframerate();x=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float32)/32768
BAR=4*60/172.218;FIRST=0.178
def t(b):return FIRST+b*BAR
a0,a1,b0=int(round(t(8)*sr)),int(round(t(36)*sr)),int(round(t(76)*sr))
xf=int(0.012*sr);head=int(0.004*sr)
A=x[a0:a1+xf//2].copy();B=x[b0-xf//2:].copy()
A[:head]*=np.linspace(0,1,head)[:,None]
th=np.linspace(0,np.pi/2,xf)[:,None]
mid=A[-xf:]*np.cos(th)+B[:xf]*np.sin(th)
out=np.concatenate([A[:-xf],mid,B[xf:]])
# trim trailing digital silence after the decay (keep 0.3 s of it)
env=np.abs(out).max(1);last=np.where(env>1e-4)[0][-1];out=out[:min(len(out),last+int(0.3*sr))]
o=wave.open(dst,'wb');o.setnchannels(2);o.setsampwidth(2);o.setframerate(sr);o.writeframes((np.clip(out,-1,1)*32767).astype(np.int16).tobytes());o.close()
print('bed',len(out)/sr,'s; join at',(a1-a0)/sr,'s; final hit (bar 115) at',(a1-a0)/sr+(t(115)-t(76)),'s')
