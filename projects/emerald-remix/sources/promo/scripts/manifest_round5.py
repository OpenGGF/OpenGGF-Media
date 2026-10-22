#!/usr/bin/env python3
"""Chapter/source map for Emerald Remix r5; captures retain their own complete provenance.
Editorial cuts and art assembly do not establish an uninterrupted completion or ROM parity.
"""
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,'/home/farrell/code/projects/OpenGGF/.worktrees/promo-coach/tools/media')
import promo_kit as pk
import csv
if __name__=='__main__':
 e=pk.load_edit(P/'edit.py');b=e.bf
 entries=[(0,b(4),'cold hero','remix-tumble-hero-final',103,103+b(4)),
 (b(4),b(12),'stock / remix counted split',['stock-tumble-wide-exit02-final','remix-tumble-wide-final'],50,50+b(12)-b(4)),
 (b(12),b(16),'new route split',['stock-opening-final','remix-opening-final'],195,195+b(16)-b(12)),
 (b(16),b(24),'blue-band title','remix-opening-final',0,b(24)-b(16)),
 (b(24),b(28),'double plus single assembly',None,None,None),
 (b(28),b(36),'triple payoff','remix-tumble-hero-final',65,65+b(36)-b(28)),
 (b(36),b(44),'original pixel-function landscape',None,None,None),
 (b(44),b(52),'spring and 22 pickups','clover-shipping-route-final',410,410+b(52)-b(44)),
 (b(52),b(56),'last complete jump','clover-shipping-route-final',710,710+b(56)-b(52)),
 (b(56),b(62),'goal; held crop','clover-shipping-route-final',850,850+b(62)-b(56)),
 (b(62),b(74),'blue-band invitation','clover-tail-final',30,30+b(74)-b(62))]
 data=[]
 for a,z,title,src,sa,sz in entries:
  data.append(dict(output_frames=[a,z],output_seconds=[a/60,z/60],chapter=title,source=src,source_frames=None if src is None else [sa,sz],kind='editorial art diagram' if src is None else 'native-speed gameplay excerpts with editorial composition'))
 (P/'chapters-round5.json').write_text(json.dumps(data,indent=2)+'\n')
 print('source map:',len(data),'shots',e.end(),'output frames')
