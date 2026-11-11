"""Purpose: confirm tempo/phase/downbeat of the bed against low-band (kick) and snare-band onsets.
Inputs: WAV, bpm. Origin: MICA & TALON production promo 2026-11-11."""
import sys,wave,numpy as np
p,bpm=sys.argv[1],float(sys.argv[2])
w=wave.open(p);sr=w.getframerate();n=w.getnframes()
x=np.frombuffer(w.readframes(n),np.int16).reshape(-1,2).astype(np.float32).mean(1)/32768
hop=96;win=1024
fr=np.lib.stride_tricks.sliding_window_view(np.pad(x,(0,win)),win)[::hop]*np.hanning(win)
S=np.abs(np.fft.rfft(fr,axis=1));f=np.fft.rfftfreq(win,1/sr)
def band(lo,hi):
  e=np.log1p(100*S[:,(f>=lo)&(f<hi)].sum(1));o=np.maximum(0,np.diff(e,prepend=e[0]));return o
kick=band(30,130);snare=band(1500,6000);full=band(30,16000)
fps=sr/hop
# tempo by autocorrelation of full onset
for name,o in [('kick',kick),('snare',snare),('full',full)]:
  o=o-o.mean();ac=np.correlate(o[:int(60*fps)],o[:int(60*fps)],'full')[int(60*fps)-1:]
  lags=np.arange(len(ac))/fps;best=[]
  for b in (86.109,129.16,172.218,114.8,143.5,160,165,170,175):
    l=int(round(60/b*fps));best.append((b,ac[l]/ac[0]))
  print(name,' '.join('%g:%.3f'%t for t in best))
bp=60/bpm
for name,o in [('kick',kick),('snare',snare)]:
  res=[]
  for off in np.arange(0,bp,0.005):
    idx=((off+np.arange(int((n/sr-1)/bp))*bp)*fps).round().astype(int)
    res.append((o[idx].mean(),off))
  res.sort(reverse=True);print(name,'best phases',[('%.3f'%r[1],'%.3f'%r[0]) for r in res[:5]])
# first onsets
th=full.max()*0.2;print('first full onsets (s):',[round(i/fps,3) for i in np.where(full>th)[0][:10]])
np.save('/tmp/mt_kick.npy',kick);np.save('/tmp/mt_snare.npy',snare)
