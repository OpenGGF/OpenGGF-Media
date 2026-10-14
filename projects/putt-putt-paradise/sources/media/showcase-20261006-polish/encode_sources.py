"""Encode the retained final PNG sequences losslessly at their authored 30fps cadence."""
from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parent
edit=json.loads((root/'edit-list.json').read_text())
for name in sorted({c['scenario'] for c in edit['clips']}):
 p=root/name
 for source,folder in [('gameplay','frames'),('title','title-frames')]:
  out=p/(source+'.mkv')
  subprocess.run(['ffmpeg','-v','error','-nostdin','-framerate','30','-i',str(p/folder/'%06d.png'),'-c:v','ffv1','-level','3','-pix_fmt','bgr0','-threads','2',str(out)],check=True)
 print('Encoded '+name,flush=True)
