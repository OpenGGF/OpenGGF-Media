"""Purpose: map the owner-supplied bed into bars (RMS, band energy, onset strength) to plan phrase-boundary edits.
Inputs: WAV path, bpm, first-beat seconds. Origin: MICA & TALON production promo 2026-11-11."""
import sys,wave,numpy as np
p,bpm,first=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
w=wave.open(p);sr=w.getframerate();n=w.getnframes();ch=w.getnchannels();sw=w.getsampwidth()
raw=w.readframes(n);dt={2:np.int16,4:np.int32}[sw]
x=np.frombuffer(raw,dt).reshape(-1,ch).astype(np.float32)/(2**(8*sw-1));m=x.mean(1)
print('sr',sr,'ch',ch,'sw',sw,'dur',n/sr)
# onset envelope
hop=480;win=2048
frames=np.lib.stride_tricks.sliding_window_view(np.pad(m,(0,win)),win)[::hop]*np.hanning(win)
S=np.abs(np.fft.rfft(frames,axis=1));freqs=np.fft.rfftfreq(win,1/sr)
flux=np.maximum(0,np.diff(np.log1p(S*10),axis=0)).sum(1);flux=np.r_[0,flux]
low=S[:,freqs<150].sum(1);hi=S[:,freqs>4000].sum(1)
t=np.arange(len(flux))*hop/sr
bp=60/bpm;bar=4*bp
# beat phase check: mean flux at beat positions offsets
for off in np.linspace(0,bp,8,endpoint=False):
  idx=((first+off+np.arange(0,int((n/sr-first)/bp))*bp)*sr/hop).astype(int);idx=idx[idx<len(flux)]
  print('phase+%.3f flux %.2f'%(off,flux[idx].mean()))
# downbeat: which beat in bar has most low energy
beats=((first+np.arange(int((n/sr-first)/bp))*bp)*sr/hop).astype(int);beats=beats[beats<len(flux)]
for k in range(4):print('beat-in-bar',k,'low %.1f flux %.2f'%(low[beats[k::4]].mean(),flux[beats[k::4]].mean()))
nb=int((n/sr-first)/bar)
for b in range(nb+1):
  a=int((first+b*bar)*sr);z=int(min(n,(first+(b+1)*bar)*sr))
  if z<=a:break
  seg=m[a:z];fa,fz=int(a/hop),int(z/hop)
  print('bar %3d t=%7.3f rms %5.3f low %6.0f hi %6.0f flux %5.1f'%(b,first+b*bar,np.sqrt((seg**2).mean()),low[fa:fz].mean(),hi[fa:fz].mean(),flux[fa:fz].mean()))
