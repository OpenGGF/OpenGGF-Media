#!/usr/bin/env python3
"""Bounded media review for Sonic3K Chaos Mode revision2,2026-10-14.

Mandatory normal exclusive admission for ALL ffprobe/ffmpeg subprocesses:
  python3 verify_v2.py --admission-worktree /lead/owned/worktree

The final H264 video is decoded once. Full-resolution showinfo checksums/PTS
describe the actual decoded frames; only selected480x270 review thumbnails are
retained. Every cut gets boundary and changing-frame strips, plus midpoint
contact pages. Audio is decoded independently once for measured loudness/peak.
No completeRGB sequence, source recapture, Java job or raw log archive is made.
The output under out/media-review is review evidence, never a pass cache.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import signal
import struct
import subprocess
import sys
import threading
from collections import deque
from fractions import Fraction
from pathlib import Path

from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent
EXPECTED_FRAMES=4864
EXPECTED_CHAPTERS=45
FPS=60
THUMB=(480,270)
THUMB_BYTES=THUMB[0]*THUMB[1]*3
NAVY=(9,20,49)
GOLD=(255,202,48)
NEW_REQUIRED={"afterimages","ring-rain","ring-leak","bumper-ahead","soz-ghost-party"}
SHOWINFO=re.compile(r"\bn:\s*(\d+).*?\bpts_time:([-\d.e+]+).*?\bchecksum:([0-9A-F]+)")


def require(condition,message):
    if not condition:raise ValueError(message)


def sha256(path):
    digest=hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda:file.read(1024*1024),b""):digest.update(block)
    return digest.hexdigest()


class OwnedProcesses:
    """Exact owned process groups, always reaped before the admission context exits."""
    def __init__(self,lease,inherited):
        self.lease=lease;self.inherited=inherited;self.children=[]
    def start(self,args,**kwargs):
        require("pass_fds" not in kwargs,"Caller must not override admission descriptors")
        child=subprocess.Popen(list(map(str,args)),start_new_session=(os.name=="posix"),
                               **kwargs,**self.inherited(self.lease))
        self.children.append(child)
        return child
    def forget(self,child):
        require(child.poll() is not None,"Cannot forget an unreaped media process")
        if child in self.children:self.children.remove(child)
    def capture(self,args):
        child=self.start(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            stdout,stderr=child.communicate()
            require(child.returncode==0,f"Media subprocess failed:{Path(str(args[0])).name}:\n{stderr.decode(errors='replace')[-5000:]}")
            return stdout,stderr
        finally:
            if child.poll() is not None:self.forget(child)
    def stop(self,child):
        if child.poll() is None:
            try:
                if os.name=="posix":os.killpg(child.pid,signal.SIGTERM)
                else:child.terminate()
            except ProcessLookupError:pass
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    if os.name=="posix":os.killpg(child.pid,signal.SIGKILL)
                    else:child.kill()
                except ProcessLookupError:pass
                child.wait()
        else:child.wait()
        for file in (child.stdin,child.stdout,child.stderr):
            if file is not None:
                try:file.close()
                except OSError:pass
        self.forget(child)
    def close(self):
        # A decoder/encoder may retain the leaseFDs, so cleanup precedes unlock.
        for child in list(reversed(self.children)):self.stop(child)


def probe(owned,path):
    stdout,_=owned.capture(["ffprobe","-v","error","-show_format","-show_streams",
                            "-show_chapters","-of","json",path])
    return json.loads(stdout)


def fast_start(path):
    size=path.stat().st_size;boxes=[]
    with path.open("rb") as file:
        while file.tell()<size:
            start=file.tell();header=file.read(8)
            require(len(header)==8,"Truncated top-level MP4 atom")
            atom_size,kind=struct.unpack(">I4s",header);header_size=8
            if atom_size==1:
                extra=file.read(8);require(len(extra)==8,"Truncated extended MP4 atom")
                atom_size=struct.unpack(">Q",extra)[0];header_size=16
            elif atom_size==0:atom_size=size-start
            require(atom_size>=header_size and start+atom_size<=size,"Invalid MP4 atom bounds")
            boxes.append((kind.decode("ascii",errors="replace"),start,atom_size))
            file.seek(start+atom_size)
    moov=next((at for kind,at,_ in boxes if kind=="moov"),None)
    mdat=next((at for kind,at,_ in boxes if kind=="mdat"),None)
    require(moov is not None and mdat is not None and moov<mdat,"MP4 is not fast-start (moov before mdat)")
    return {"moov_offset":moov,"mdat_offset":mdat,"passed":True}


def reconcile_timeline(data,owned):
    shots=data["shots"]
    require(len(shots)==EXPECTED_CHAPTERS,f"Expected45shots,got{len(shots)}")
    require(data.get("total_frames")==EXPECTED_FRAMES,"Timeline expected-frame contract changed")
    require(not data.get("pending_sources"),"Timeline still contains pending source qualification")
    formats={};used={};effects=set();sources=[]
    for i,shot in enumerate(shots):
        start,end=shot["output_start_frame"],shot["output_end_frame"]
        require(shot.get("index")==i,f"Shot index/order mismatch:{i}")
        require(start==(0 if i==0 else shots[i-1]["output_end_frame"]),f"Noncontiguous shot:{i}")
        require(end>start and shot.get("frames")==end-start,f"Shot duration mismatch:{i}")
        for key,value in [("output_start_seconds",start/FPS),("output_end_seconds",end/FPS)]:
            require(abs(float(shot.get(key,value))-value)<1e-6,f"Shot seconds/frames disagree:{i}:{key}")
        require(not shot.get("pending"),f"Pending shot:{i}:{shot.get('pending')}")
        for panel in shot.get("panels",[]):
            require(panel.get("qualified") is True,f"Unqualified source:{i}:{panel.get('name')}")
            source=Path(panel["source"]).resolve()
            require(source.is_file(),f"Missing source:{source}")
            relative=panel.get("source_relative")
            if relative is not None:require((P/relative).resolve()==source,f"Relative source disagrees:{i}")
            if source not in formats:
                info=probe(owned,source);videos=[s for s in info["streams"] if s["codec_type"]=="video"]
                require(len(videos)==1,f"Expected one source video:{source}")
                video=videos[0]
                require((video["width"],video["height"])==(400,224),f"Unexpected source dimensions:{source}")
                require(Fraction(video["avg_frame_rate"])==FPS,f"Unexpected source cadence:{source}")
                duration=float(info["format"]["duration"])
                formats[source]={"frames":round(duration*FPS),"duration_seconds":duration}
                provenance=source.parent/"provenance.json"
                require(provenance.is_file(),f"Source lacks provenance:{source}")
                declared=json.loads(provenance.read_text())
                require(declared.get("sourceCommit")==panel.get("source_commit"),f"Source commit mismatch:{source}")
                formats[source]["provenance_effect"]=declared.get("effect")
            first=panel["source_start_frame"];count=panel["source_frames"];offset=panel["offset_frame"]
            require(all(isinstance(x,int) for x in [first,count,offset]),f"Noninteger source interval:{i}")
            require(first>=0 and count>0 and offset>=0,f"Invalid source interval:{i}")
            require(first+count<=formats[source]["frames"],f"Source interval past EOF:{i}:{source}")
            require(count<=shot["frames"]-offset,f"Source interval exceeds output slot:{i}")
            for key,value in [("source_start_seconds",first/FPS),("source_end_seconds",(first+count)/FPS)]:
                require(abs(float(panel.get(key,value))-value)<1e-6,f"Source seconds/frames disagree:{i}:{key}")
            for old_start,old_end,old_shot in used.get(source,[]):
                require(first>=old_end or old_start>=first+count,f"Repeated source frames in shots{old_shot}/{i}:{source}")
            used.setdefault(source,[]).append((first,first+count,i))
            effect=panel.get("effect")
            if effect:
                require(effect==panel.get("actual_effect")==formats[source]["provenance_effect"],f"Effect/source mismatch:{i}:{source}")
                if effect in NEW_REQUIRED:
                    require(source.is_relative_to(P/"captures"),f"Changed effect reused obsolete master:{effect}:{source}")
                effects.add(effect)
            sources.append({"shot":i,"name":panel.get("name"),"source":os.path.relpath(source,P),
                            "source_start_frame":first,"source_end_frame":first+count,
                            "output_offset_frame":offset,"effect":effect,"qualified":True,
                            "setup":panel.get("setup"),"source_commit":panel.get("source_commit")})
    require(shots[-1]["output_end_frame"]==EXPECTED_FRAMES,"Timeline does not end at4864")
    require(effects==set(data.get("qualified_effects",[])),"Qualified-effect list disagrees with actual used panels")
    require(len(effects)==data.get("qualified_effect_count"),"Qualified-effect count disagrees with actual used panels")
    return shots,{"unique_sources":len(formats),"qualified_effect_count":len(effects),
                  "qualified_effects":sorted(effects),"source_intervals":sources,
                  "limits":"Qualified flags are root's visible-footage approval; this reconciles metadata, not all-act gameplay or pixel parity."}


def inspect_format(info,shots):
    videos=[s for s in info["streams"] if s["codec_type"]=="video"]
    audios=[s for s in info["streams"] if s["codec_type"]=="audio"]
    require(len(videos)==len(audios)==1,"Final must have one video and one audio stream")
    v,a=videos[0],audios[0]
    require((v["codec_name"],v["width"],v["height"])==("h264",1920,1080),"Final video codec/dimensions mismatch")
    require(Fraction(v["avg_frame_rate"])==Fraction(v["r_frame_rate"])==FPS,"Final cadence must be60fps")
    require((a["codec_name"],a["sample_rate"],a["channels"])==("aac","48000",2),"Final audio must be AAC48kHz stereo")
    expected=EXPECTED_FRAMES/FPS
    require(abs(float(info["format"]["duration"])-expected)<=.002,"Final duration differs from4864/60")
    if v.get("duration") is not None:require(abs(float(v["duration"])-expected)<.0002,"Video stream duration mismatch")
    if v.get("nb_frames") is not None:require(int(v["nb_frames"])==EXPECTED_FRAMES,"Declared video frame count mismatch")
    chapters=info.get("chapters",[]);require(len(chapters)==EXPECTED_CHAPTERS,"Expected45chapters")
    for i,(chapter,shot) in enumerate(zip(chapters,shots)):
        require(abs(float(chapter["start_time"])-shot["output_start_frame"]/FPS)<=.002,f"Chapter start mismatch:{i}")
        require(abs(float(chapter["end_time"])-shot["output_end_frame"]/FPS)<=.002,f"Chapter end mismatch:{i}")
        require(chapter.get("tags",{}).get("title")==shot["title"],f"Chapter title mismatch:{i}")
    return {"dimensions":[1920,1080],"fps":FPS,"declared_frames":v.get("nb_frames"),
            "duration_seconds":float(info["format"]["duration"]),"video_codec":"h264",
            "audio_codec":"aac","sample_rate":48000,"channels":2,"chapters":len(chapters)}


def samples_for(shots):
    result={};wanted=set()
    for shot in shots:
        start,end=shot["output_start_frame"],shot["output_end_frame"]
        boundary=sorted({max(0,start-2),max(0,start-1),start,min(end-1,start+1),min(end-1,start+2)})
        movement=sorted({min(end-1,start+round((end-start-1)*f)) for f in [0,.18,.36,.5,.72,1]})
        result[shot["index"]]={"boundary":boundary,"movement":movement,"midpoint":start+(end-start)//2}
        wanted.update(boundary+movement+[result[shot["index"]]["midpoint"]])
    require(len(wanted)<=600,"Review sampling exceeded bounded thumbnail budget")
    return result,wanted


class StderrDrain:
    """Bounded log tail plus numeric frame evidence; no raw log files."""
    def __init__(self,pipe,shots):
        self.pipe=pipe;self.shots=shots;self.tail=deque(maxlen=96);self.errors=[]
        self.count=0;self.last_pts=None;self.min_delta=None;self.max_delta=None
        self.unique=[set() for _ in shots];self.frames=[0 for _ in shots];self.shot_index=0
        self.thread=threading.Thread(target=self.read,daemon=True)
    def read(self):
        try:
            for raw in iter(self.pipe.readline,b""):
                line=raw.decode(errors="replace");self.tail.append(line[-2000:])
                match=SHOWINFO.search(line)
                if not match:continue
                number=int(match[1]);pts=float(match[2]);checksum=match[3]
                if number!=self.count:self.errors.append(f"Decoded frame index discontinuity:{number}/{self.count}")
                if self.last_pts is None:
                    if abs(pts)>.00002:self.errors.append(f"First frame PTS is not0:{pts}")
                else:
                    delta=pts-self.last_pts
                    self.min_delta=delta if self.min_delta is None else min(self.min_delta,delta)
                    self.max_delta=delta if self.max_delta is None else max(self.max_delta,delta)
                    if abs(delta-1/FPS)>.000025 and len(self.errors)<10:self.errors.append(f"Non60Hz PTS at{number}:{delta}")
                self.last_pts=pts;self.count+=1
                while self.shot_index<len(self.shots)-1 and number>=self.shots[self.shot_index]["output_end_frame"]:self.shot_index+=1
                self.unique[self.shot_index].add(checksum);self.frames[self.shot_index]+=1
        except BaseException as error:self.errors.append(f"Stderr evidence reader:{error}")
    def start(self):self.thread.start()
    def join(self):self.thread.join(timeout=10);require(not self.thread.is_alive(),"Decoder log drain did not exit")


def decode_selected(owned,path,shots,wanted):
    child=owned.start(["ffmpeg","-nostdin","-hide_banner","-loglevel","info","-xerror","-threads","2",
        "-i",path,"-map","0:v:0","-an","-sn","-dn","-vf","showinfo,scale=480:270:flags=area,format=rgb24",
        "-fps_mode","passthrough","-pix_fmt","rgb24","-f","rawvideo","pipe:1"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    drain=StderrDrain(child.stderr,shots);drain.start();images={};count=0
    try:
        while True:
            pixels=child.stdout.read(THUMB_BYTES)
            if not pixels:break
            require(len(pixels)==THUMB_BYTES,"Partial final decoded frame")
            if count in wanted:images[count]=Image.frombytes("RGB",THUMB,pixels)
            count+=1
            require(count<=EXPECTED_FRAMES,"Export contains more than4864decoded frames")
        child.stdout.close();status=child.wait();drain.join()
        require(status==0,"Final video decode failed:\n"+"".join(drain.tail)[-5000:])
        child.stderr.close()
        owned.forget(child)
        require(count==drain.count==EXPECTED_FRAMES,f"Decoded frame count mismatch:{count}/{drain.count}/{EXPECTED_FRAMES}")
        require(not drain.errors,"Frame cadence errors:"+"; ".join(drain.errors))
        require(set(images)==wanted,"Selected export frames missing")
        return images,{"decoded_frames":count,"full_video_decode":"PASS","no_interpolation":"fps_mode passthrough",
                       "first_pts":0,"last_pts":drain.last_pts,"min_pts_delta":drain.min_delta,
                       "max_pts_delta":drain.max_delta,
                       "shots":[{"shot":s["index"],"decoded_frames":drain.frames[i],
                                 "distinct_fullframe_checksums":len(drain.unique[i])} for i,s in enumerate(shots)]}
    finally:
        if child in owned.children:owned.stop(child)
        drain.thread.join(timeout=10)


def review_images(output,shots,samples,images,decode):
    review=[];pages=[];measure={s["shot"]:s for s in decode["shots"]}
    for shot in shots:
        index=shot["index"];chosen=samples[index]
        # First row includes actual frames from both sides of the cut. Second
        # row samples actual motion throughout the new shot, never interpolated.
        strip=Image.new("RGB",(6*THUMB[0],2*(THUMB[1]+34)),NAVY);d=ImageDraw.Draw(strip)
        for row,key in enumerate(["boundary","movement"]):
            for col,frame in enumerate(chosen[key]):
                x=col*THUMB[0];y=row*(THUMB[1]+34)
                strip.paste(images[frame],(x,y))
                relation="PREVIOUS" if frame<shot["output_start_frame"] else f"+{frame-shot['output_start_frame']}f"
                d.text((x+8,y+THUMB[1]+7),f"{key.upper()}  export{frame} /{frame/FPS:.3f}s /{relation}",fill=GOLD)
        name=f"cut-{index:02d}.png";strip.save(output/name)
        actual=[hashlib.sha256(images[f].tobytes()).hexdigest() for f in chosen["movement"]]
        full_count=measure[index]["distinct_fullframe_checksums"]
        review.append({"shot":index,"title":shot["title"],"layout":shot["layout"],"strip":name,
                       "boundary_export_frames":chosen["boundary"],"movement_export_frames":chosen["movement"],
                       "distinct_sample_thumbnails":len(set(actual)),"distinct_fullframe_checksums":full_count,
                       "observed_changing_pixels":full_count>1,
                       "review_status":"Manual moving/cut interpretation required; changing pixels alone do not prove actor motion."})
    for page_start in range(0,len(shots),9):
        group=shots[page_start:page_start+9];page=Image.new("RGB",(3*THUMB[0],3*(THUMB[1]+34)),NAVY);d=ImageDraw.Draw(page)
        for local,shot in enumerate(group):
            x=local%3*THUMB[0];y=local//3*(THUMB[1]+34)
            frame=samples[shot["index"]]["midpoint"]
            page.paste(images[frame],(x,y))
            d.text((x+8,y+THUMB[1]+6),f"{shot['index']:02d} {frame/FPS:.2f}s {shot['title'][:60]}",fill=GOLD)
        name=f"midpoints-{page_start//9+1:02d}.png";page.save(output/name);pages.append(name)
    return {"cut_strips":review,"midpoint_contact_pages":pages,
            "sampling":"Actual decoded export frames;480x270 whole-frame thumbnails; no animation/speed interpolation."}


def measure_audio(owned,path):
    # Target values configure the measuring filter; input_i/input_tp report the
    # ACTUAL existing mix. No target-value assertion or normalization is applied.
    _,stderr=owned.capture(["ffmpeg","-nostdin","-hide_banner","-loglevel","info","-xerror",
        "-i",path,"-map","0:a:0","-vn","-sn","-dn","-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"])
    text=stderr.decode(errors="replace");start=text.rfind("{");end=text.rfind("}")
    require(start>=0 and end>start,"Missing measured loudness statistics")
    stats=json.loads(text[start:end+1]);integrated=float(stats["input_i"]);peak=float(stats["input_tp"])
    require(math.isfinite(integrated) and math.isfinite(peak),"Final audio is silent/nonfinite")
    return {"full_audio_decode":"PASS","integrated_lufs":integrated,"true_peak_dbtp":peak,
            "loudness_range_lu":float(stats["input_lra"]),"threshold_lufs":float(stats["input_thresh"]),
            "measurement":"Decoded final AAC via loudnorm input statistics; no exact LUFS target assumed.",
            "listening_review":"Not performed by this verifier.","peak_below_digital_full_scale":peak<0}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--admission-worktree",type=Path,required=True)
    parser.add_argument("--input",type=Path,default=P/"out/sonic3k-chaos-mode-demo-v2.mp4")
    parser.add_argument("--timeline",type=Path,default=P/"out/edit-timeline.json")
    parser.add_argument("--audio-only",action="store_true",help="Remeasure an audio-only remux; require exact video packets/timestamps and unchanged reviewed timeline")
    args=parser.parse_args()
    require(args.input.is_file(),f"Final export is not present:{args.input}")
    require(args.timeline.is_file(),f"Final timeline is not present:{args.timeline}")
    require(args.admission_worktree.is_dir(),"Lead-owned admission worktree is not present")
    data=json.loads(args.timeline.read_text());output=P/"out/media-review"
    # No media subprocess is started before acquisition. The process owner's
    # finally clause is INSIDE the lease context, including cancellation paths.
    sys.path.insert(0,"/home/farrell/code/projects/OpenGGF/tools/testing")
    from maven_queue import maven_slot,inherited_slot,handle_termination
    with handle_termination():
        with maven_slot(args.admission_worktree.resolve(),exclusive=True,estimate=180,kind="chaos-reel-media-review") as lease:
            owned=OwnedProcesses(lease,inherited_slot)
            try:
                initial_export=sha256(args.input);initial_timeline=sha256(args.timeline)
                if args.audio_only:
                    report=json.loads((output/"summary.json").read_text())
                    require(report["timeline_sha256"]==initial_timeline,"Audio-only remux changed the reviewed timeline")
                    previous_export=report["sha256"]
                    shots=data["shots"]
                    media=inspect_format(probe(owned,args.input),shots)
                    media["fast_start"]=fast_start(args.input)
                    # Container bytes change when AAC changes. Compare the actual
                    # H264 packets and their PTS/DTS/durations with the retained
                    # video encode, rather than repeating unchanged frame strips.
                    video_master=P/"work/revision-2-video.mp4"
                    hashes=[];timings=[]
                    for path in [video_master,args.input]:
                        stdout,_=owned.capture(["ffmpeg","-nostdin","-v","error","-i",path,"-map","0:v:0","-c:v","copy","-f","hash","-hash","sha256","-"])
                        hashes.append(stdout.decode().strip())
                        stdout,_=owned.capture(["ffprobe","-v","error","-select_streams","v:0","-show_entries","packet=pts_time,dts_time,duration_time,size","-of","json",path])
                        timings.append(json.loads(stdout)["packets"])
                    require(hashes[0]==hashes[1],"Audio remux changed H264 packet bytes")
                    require(timings[0]==timings[1] and len(timings[1])==EXPECTED_FRAMES,"Audio remux changed video frame timestamps/count")
                    audio=measure_audio(owned,args.input)
                    require(-16<=audio["integrated_lufs"]<=-12,"Adjusted promo mix is outside the reviewed loudness range")
                    require(audio["true_peak_dbtp"]<-.9,"Adjusted promo mix has inadequate peak headroom")
                    require(initial_export==sha256(args.input),"Audio export changed during review")
                    require(initial_timeline==sha256(args.timeline),"Timeline changed during audio review")
                    report.update(sha256=initial_export,media=media,audio=audio)
                    report["audio_remux"]={"previous_export_sha256":previous_export,"h264_packet_hash":hashes[0],"video_packets_and_timestamps_unchanged":True,"reviewed_frames":EXPECTED_FRAMES}
                    (output/"summary.json").write_text(json.dumps(report,indent=2)+"\n")
                    print(f"Audio remux:4864video packets/timestamps unchanged; measured{audio['integrated_lufs']:.2f}LUFS/{audio['true_peak_dbtp']:.2f}dBTP.",flush=True)
                    return
                shots,source_review=reconcile_timeline(data,owned)
                info=probe(owned,args.input);media=inspect_format(info,shots);media["fast_start"]=fast_start(args.input)
                samples,wanted=samples_for(shots)
                print(f"Reviewing45cuts; retaining{len(wanted)}actual export thumbnails during one full decode.",flush=True)
                images,decode=decode_selected(owned,args.input,shots,wanted)
                output.mkdir(parents=True,exist_ok=True)
                strips=review_images(output,shots,samples,images,decode);images.clear()
                audio=measure_audio(owned,args.input)
                require(initial_export==sha256(args.input),"Final export changed during review")
                require(initial_timeline==sha256(args.timeline),"Final timeline changed during review")
                report={"tested_export":str(args.input.resolve()),"sha256":initial_export,
                        "timeline_sha256":initial_timeline,"media":media,"decode":decode,
                        "source_review":source_review,"frame_review":strips,"audio":audio,
                        "outcome":"Format,frames,cadence,chapters,source intervals and complete decode checked; manual picture/listening review remains root-owned.",
                        "limits":"Curated engine captures and editorial ROM soundtrack. No all-effect/all-act parity, source-SFX isolation, listening review or independent compositor pixel-parity claim."}
                (output/"summary.json").write_text(json.dumps(report,indent=2)+"\n")
                print(f"Decoded4864frames/{EXPECTED_FRAMES/FPS:.3f}s;45chapters;{source_review['qualified_effect_count']}qualified effects; measured{audio['integrated_lufs']:.2f}LUFS/{audio['true_peak_dbtp']:.2f}dBTP.",flush=True)
            finally:owned.close()


if __name__=="__main__":main()
