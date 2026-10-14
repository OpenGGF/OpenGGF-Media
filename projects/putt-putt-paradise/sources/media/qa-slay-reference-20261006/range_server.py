"""Task-owned local video QA server; byte-range seeking for native browser playback."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kw): super().__init__(*args,directory=str(ROOT),**kw)
 def translate_path(self,path):
  if path.split('?')[0]=='/slay.mp4': return '/home/farrell/Videos/OGGF/slay-the-robotnik-promo/promo.mp4'
  return super().translate_path(path)
 def end_headers(self):
  self.send_header('Accept-Ranges','bytes'); super().end_headers()
 def send_head(self):
  self.remaining=None
  path=Path(self.translate_path(self.path)); header=self.headers.get('Range')
  match=re.fullmatch(r'bytes=(\d+)-(\d*)',header or '')
  if not match or not path.is_file(): return super().send_head()
  size=path.stat().st_size; start=int(match[1]); end=min(int(match[2]) if match[2] else size-1,size-1)
  if start>end:
   self.send_response(416); self.send_header('Content-Range',f'bytes */{size}'); self.end_headers(); return None
  f=path.open('rb'); f.seek(start); self.remaining=end-start+1
  self.send_response(206); self.send_header('Content-type',self.guess_type(str(path)))
  self.send_header('Content-Range',f'bytes {start}-{end}/{size}'); self.send_header('Content-Length',str(self.remaining))
  self.end_headers(); return f
 def copyfile(self,source,output):
  if self.remaining is None: return super().copyfile(source,output)
  while self.remaining:
   block=source.read(min(self.remaining,65536))
   if not block: break
   output.write(block); self.remaining-=len(block)
ThreadingHTTPServer(('127.0.0.1',8880),Handler).serve_forever()
