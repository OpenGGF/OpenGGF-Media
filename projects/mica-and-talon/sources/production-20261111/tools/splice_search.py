"""Purpose: find seamless bar-line splice points in the bed (bar X jumps to bar Y where the surrounding bars repeat).
Inputs: WAV, bpm, first beat. Origin: MICA & TALON production promo 2026-11-11."""
import sys,wave,numpy as np
p,bpm,first=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
w=wave.open(p);sr=w.getframerate();x=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float32).mean(1)/32768
bar=4*60/bpm;nb=int((len(x)/sr-first)/bar)
F=[]
for b in range(nb):
  seg=x[int((first+b*bar)*sr):int((first+(b+1)*bar)*sr)]
  # 8 sub-beat slices x log-spectrum 64 bands
  sl=np.array_split(seg,16);v=[]
  for s in sl:
    sp=np.abs(np.fft.rfft(s*np.hanning(len(s)),8192))[:2048];bands=np.add.reduceat(sp,np.geomspace(1,2048,49).astype(int)[:-1]);v.append(np.log1p(bands))
  v=np.concatenate(v);v=(v-v.mean())/v.std();F.append(v)
F=np.array(F);C=F@F.T/F.shape[1]
np.save('/tmp/mt_ssm.npy',C)
res=[]
for X in range(9,nb):
  for Y in range(X+8,nb):
    # play bars ..X-1 then Y..; match context X-2,X-1 vs Y-2,Y-1 and X,X+1 vs Y,Y+1
    if Y+1>=nb or X+1>=nb:continue
    sc=(C[X-1,Y-1]+C[X-2,Y-2]+C[X,Y]+C[X+1,Y+1])/4
    res.append((sc,X,Y))
res.sort(reverse=True)
for sc,X,Y in res[:40]:print('%.3f  bar %3d (%.2fs) -> bar %3d (%.2fs) saves %d bars'%(sc,X,first+X*bar,Y,first+Y*bar,Y-X))
