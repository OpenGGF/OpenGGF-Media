#!/usr/bin/env python3
"""Chaos promo revision2: deterministic beat-snapped native-media composites.

External media tool,2026-10-14. Never launches engine/capture/compiler or changes
the repository. Read-only masters are400x224/60Hz. All source audio is muted;
the continuous HCZ2 bed and explicit ROM editorial cues supply the soundtrack.

python3 assemble.py plan --allow-pending
python3 assemble.py preview --shots8,10,12 --allow-pending
python3 assemble.py snapshot --shot12 --frame105
python3 assemble.py render             # coordinate expensive encode with lead

source-selections.json is the editorial source lock: reviewed in-points and
qualified visible effects. Missing/new/conditional masters are never silently
substituted with an obsolete rain/leak/bumper/ghost capture. The first reel is
preserved. Full final rendering requires all used sources explicitly qualified.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import os
import re
import subprocess
import sys
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
OLD = P.parent
W, H, FPS, SR = 1920, 1080, 60, 48000
NAVY, GOLD = (9,20,49), (255,202,48)
BPM, PHASE = 171.107, .316
CHANGED = {"afterimages", "rain", "leak", "bumper", "ghosts", "ghost-close"}
LEASE = None
INHERITED = None
ALIASES = {"trails":"afterimages", "ghost":"ghosts"}
EFFECTS = {"bobble":"bobble-head", "heads":"pulse-head", "afterimages":"afterimages",
    "rainbow":"rainbow-player", "invisible":"invisible-player", "negative":"negative-world",
    "mirror":"mirror-view", "upsidedown":"upside-down-view", "moon":"moon-gravity",
    "gravity":"gravity-hiccup", "fastforward":"fast-forward", "slowmo":"slow-motion",
    "dvd":"dvd-hud", "hudorbit":"hud-orbit", "hudshuffle":"hud-shuffle", "hudscale":"hud-scale",
    "shield":"shield-surprise", "superstar":"ten-second-superstar", "bumper":"bumper-ahead",
    "wind":"windy-day", "ghosts":"soz-ghost-party", "ghost-close":"soz-ghost-party",
    "rain":"ring-rain", "magnet":"ring-magnet", "ringorbit":"ring-orbit", "leak":"ring-leak",
    "flood":"flash-flood", "blueprint":"blueprint-zone", "scenery":"wrong-zone-scenery",
    "squashy":"squashy-view", "overdrive":"projectile-overdrive", "giant":"giant-badniks",
    "spinning":"spinning-badniks", "tiny":"tiny-badniks", "jelly":"jelly-objects",
    "breakout":"monitor-breakout", "vine":"vine-time", "zoom":"zoom-pulse", "quake":"quake-camera",
    "pong-play":"ring-pong", "stack":"monitor-stack", "snake":"ring-snake", "defence":"badnik-defence",
    "chat":"imaginary-chat", "sonicsays":"sonic-says", "landmark":"landmark-hunt",
    "rampage":"rolling-rampage", "buddy":"rescue-buddy", "bunny":"bunny-hop", "springlegs":"spring-legs"}

# Read old helpers without generating/overwriting first-reel bytecode files.
sys.dont_write_bytecode=True
spec = importlib.util.spec_from_file_location("chaos_cards_v1", OLD / "card_renderer.py")
cards = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cards)


def beat_frame(beat):
    # Round ABSOLUTE boundaries once. Never sum rounded shot durations.
    return 0 if beat == 0 else int(math.floor((PHASE + beat * 60 / BPM) * FPS + .5))


def run(args):
    kwargs = INHERITED(LEASE) if LEASE and INHERITED else {}
    result = subprocess.run(list(map(str,args)), capture_output=True, **kwargs)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace")[-5000:])
    return result


@lru_cache(maxsize=128)
def probe(path):
    return json.loads(run(["ffprobe","-v","error","-show_streams","-show_format",
                           "-of","json",path]).stdout)


@lru_cache(maxsize=128)
def state_rows(folder):
    file = Path(folder)/"output/state.csv"
    return list(csv.DictReader(file.open())) if file.exists() else []


def selections():
    file = P/"source-selections.json"
    return json.loads(file.read_text()) if file.exists() else {"sources":{},"stinger":{}}


def choose(name, source_lock):
    name = ALIASES.get(name,name)
    settings = source_lock.get("sources",{}).get(name,{})
    explicit = settings.get("source")
    paths = ([P/explicit] if explicit else []) + [P/"captures"/name/"source.mkv"]
    if name not in CHANGED:
        paths.append(OLD/"captures"/name/"source.mkv")
    path = next((p.resolve() for p in paths if p.exists()),None)
    if path and name in CHANGED and not path.is_relative_to(P/"captures"):
        raise ValueError(f"Changed effect requires a revision2 master:{name}:{path}")
    return name,path,settings


def source_start(value, settings, name):
    arrival = float(settings.get("arrival",10))
    if isinstance(value,(int,float)):
        return round(float(value)*FPS)
    match = re.fullmatch(r"arrival(?:([+-])(\d+(?:\.\d+)?))?",str(value))
    if not match:
        raise ValueError(f"Bad source in-point:{name}:{value}")
    offset = float(match[2] or 0) * (-1 if match[1]=="-" else 1)
    return round((arrival+offset)*FPS)


def panel_data(panel, offset, frames, lock, overrides=None):
    overrides = overrides or {}
    name = Path(panel["src"]).parent.name if isinstance(panel,dict) else panel
    name,path,settings = choose(name,lock)
    value = overrides.get(name, panel.get("in","arrival") if isinstance(panel,dict) else 14)
    # Explicit reviewed selection has priority for a first-use default only.
    if value=="arrival" and "in" in settings:
        value=settings["in"]
    start = source_start(value,settings,name)
    qualified = bool(settings.get("qualified",False))
    result = dict(name=name,source=str(path) if path else None,
                  source_start_frame=start,offset_frame=offset,
                  source_frames=max(0,frames-offset),effect=EFFECTS.get(name),
                  qualified=qualified,review_note=settings.get("notes","Pending lead source review"))
    if path:
        info=probe(str(path));v=next(s for s in info["streams"] if s["codec_type"]=="video")
        if (v["width"],v["height"],v["r_frame_rate"])!=(400,224,"60/1"):
            raise ValueError(f"Source cadence/size mismatch:{path}:{v}")
        available=round(float(info["format"]["duration"])*FPS)
        if start<0 or start+result["source_frames"]>available:
            raise ValueError(f"Source interval outside EOF:{name}:{start}+{result['source_frames']}/{available}")
        metadata=json.loads((path.parent/"provenance.json").read_text())
        command=metadata.get("command",[])
        def option(flag,default):
            return command[command.index(flag)+1] if flag in command else default
        result.update(source_commit=metadata.get("sourceCommit"),setup=metadata.get("setup"),
                      actual_effect=metadata.get("effect"),native_game=option("--game","s3k"),
                      native_act=option("--zone","aiz").upper()+option("--act","1"),
                      character=option("--main","sonic"),sidekick=option("--sidekick","none"))
        if result["effect"] and metadata.get("effect")!=result["effect"]:
            raise ValueError(f"Effect/source mismatch:{name}:{metadata.get('effect')}")
        rows=state_rows(str(path.parent))
        visible=rows[start:start+result["source_frames"]]
        if name!="ghost-close" and any(r.get("dead")=="1" for r in visible):
            raise ValueError(f"Unexpected death inside chosen source:{name}")
    return result


def normalized_plan(lock=None):
    lock=lock or selections()
    edl=json.loads((P/"edl.json").read_text());out=[]
    # Launch needs19.8->23.3 to show the native fade followed by gameplay.
    # It is10beats instead of4, so every subsequent cut shifts by6beats.
    for original_index,raw in enumerate(edl["shots"]):
        raw=dict(raw);a,b=raw["b"]
        if a>=132:a+=6;b+=6
        elif a==128:b=138
        layout=raw["layout"]
        if " x4 " in layout:
            actual="SLICE-2" if layout.startswith("SLICE") else "FULL"
            for j in range(4):
                entry=dict(raw,b=[a+j*2,a+(j+1)*2],layout=actual,panels=[raw["panels"][j]])
                if actual=="SLICE-2":
                    entry["panels"]=raw["panels"][j].split("|")
                entry["recap"]=True
                out.append((original_index,entry))
        else:out.append((original_index,raw|{"b":[a,b]}))
    resolved=[]
    fallback_crescendo=["rainbow","negative","upsidedown","mirror"]
    recap_starts={"bumper":12.0,"rain":13.0,"afterimages":13.0,"dvd":13.0,
                  "giant":13.0,"moon":14.0,"scenery":14.5,"invisible":11.7}
    for original_index,raw in out:
        a,b=raw["b"];start,end=beat_frame(a),beat_frame(b);duration=end-start
        layout=raw["layout"];ps=raw.get("panels",[]);panels=[]
        if original_index==32:
            j=(a-162)//2;p=ps[0]
            name=Path(p["src"]).parent.name
            if not choose(name,lock)[1] or not choose(name,lock)[2].get("qualified"):
                name="blaster" if j==1 and choose("blaster",lock)[2].get("qualified") else fallback_crescendo[j];ps=[name]
            raw["recap"]=True
        if original_index==33:
            ps=[ALIASES.get(n,n) for n in ps]
            ps=["rainbow" if n=="afterimages" else n for n in ps]
            # Sonic-centred slices would crop out Bloominator at sourcex≈360.
            ps=["superstar" if n=="giant" else n for n in ps]
            # The one-shot bumper's later source may contain only ordinary motion;
            # reserve its first beat-aligned contact for the triple reveal.
            ps=["squashy" if n=="bumper" else n for n in ps]
        if original_index==34:ps=["blueprint","rain","overdrive","ghosts"]
        if original_index==36:ps=["rainbow","leak","negative","overdrive"]
        if original_index==24:
            # Captured Vine labels a rope but misses the grab; never claim its swing.
            spare=lock.get("vineReplacement") or next((n for n in ["bunny","springlegs"] if choose(n,lock)[1] and choose(n,lock)[2].get("qualified")),"hudscale")
            ps=[spare];raw["recap"]=True
        # Missing B slots use the written fallbacks; changed A sources stay pending.
        if original_index==17 and not choose("ringorbit",lock)[1]:layout="FULL";ps=ps[:1]
        if original_index==25 and not any(choose(n,lock)[1] for n in ["zoom","quake"]):
            layout="FULL";ps=["wind"];raw["recap"]=True
        for j,p in enumerate(ps):
            if isinstance(p,str):p={"src":str(P/"captures"/p/"source.mkv"),"in":14}
            name=Path(p["src"]).parent.name
            if j and p.get("tier")=="B" and not choose(name,lock)[1]:continue
            offset=0
            if layout=="PAIR":offset=0 if j==0 else beat_frame(a+(2 if original_index==10 else 1))-start
            elif layout=="TRIPLE":offset=beat_frame(a+j)-start
            elif layout=="QUAD":offset=beat_frame(a+j)-start
            elif layout=="SLICE-4":offset=beat_frame(a+2*j)-start
            elif layout=="FULL->QUAD" and j:offset=beat_frame(a+4+j)-start
            override={}
            if original_index==0:override["bobble"]=10-beat_frame(8)/FPS
            if original_index==4:override["afterimages"]=11.2
            if original_index==33:override.update(recap_starts)
            if original_index==33 and name=="rainbow":override["rainbow"]=14.0
            if original_index==33 and name=="superstar":override["superstar"]=14.0
            if original_index==33 and name=="squashy":override["squashy"]=12.0
            if original_index==32:override[name]={"sonicsays":11.0,"rampage":10.1,"buddy":10.35,"blaster":11.15}.get(name,12.0)
            if original_index==34:override.update({"blueprint":13.9,"rain":14.5,"overdrive":14.3,"ghosts":13.5})
            if original_index==35:override["afterimages"]=13.0
            if original_index==36:override.update({"rainbow":15.0,"leak":14.0,"negative":15.5,"overdrive":16.4})
            if original_index==25 and name=="wind":override["wind"]=11
            if original_index==23:override["breakout"]=10.2
            if original_index==24 and name=="hudscale":override["hudscale"]=12.0
            if original_index==24 and name=="bunny":override["bunny"]=15.5
            if original_index==26:override["ghosts"]=11.0
            if original_index==30:override["chat"]=10.5
            if original_index==15 and name=="bumper":
                contact=lock.get("sources",{}).get("bumper",{}).get("contact_frame")
                if contact is not None:override["bumper"]=(int(contact)-(beat_frame(a+1)-start))/FPS
            panels.append(panel_data(p,offset,duration,lock,override))
        if layout=="PAIR" and len(panels)==1:layout="FULL"
        caption=raw.get("caption","");caption_begin=0;caption_end=duration
        if original_index==0:caption_end=beat_frame(7)-start
        if original_index in (12,22):caption_begin=beat_frame(a+5)-start
        if original_index==18:caption_begin=beat_frame(a+1)-start
        entry=dict(index=len(resolved),original_index=original_index,act=raw["act"],
                   beat_start=a,beat_end=b,output_start_frame=start,output_end_frame=end,
                   frames=duration,layout=layout,panels=panels,caption=caption,
                   caption_begin=caption_begin,caption_end=caption_end,
                   card=raw.get("card"),sfx=raw.get("sfx"),notes=raw.get("note",""),
                   recap=raw.get("recap",False))
        entry["title"]=entry["card"] or " / ".join(p["name"] for p in panels)
        resolved.append(entry)
    # Keep the separate post-credit stinger outside the music bed.
    begin=resolved[-1]["output_end_frame"]
    stinger=lock.get("stinger",{})
    name=stinger.get("source","ghost-close");name,path,settings=choose(name,lock)
    shot=dict(index=len(resolved),original_index="stinger",act="stinger",layout="STINGER",
              output_start_frame=begin,output_end_frame=begin+258,frames=258,
              panels=[],card=None,caption=stinger.get("caption","SANDOPOLIS SENDS ITS REGARDS."),
              caption_begin=30,caption_end=234,title="Post-credit consequence",notes="Silence; editorial death cue only if actual death is reviewed")
    if path:
        pp=panel_data({"src":str(path),"in":stinger.get("in",11)},30,228,lock)
        shot["panels"]=[pp]
        rows=state_rows(str(path.parent));death=next((int(r["frame"]) for r in rows[pp["source_start_frame"]:pp["source_start_frame"]+198] if r.get("dead")=="1"),None)
        shot["death_output_frame"]=30+death-pp["source_start_frame"] if death is not None else None
        if name=="ghost-close" and death is None:
            shot["pending"]="Ghost stinger has no observed death in the chosen interval"
    else:shot["pending"]="New qualified ghost-close/stinger source required"
    resolved.append(shot)
    if any(s["output_end_frame"]!=resolved[i+1]["output_start_frame"] for i,s in enumerate(resolved[:-1])):
        raise ValueError("Noncontiguous absolute frame boundaries")
    # Recaps use disjoint intervals. Overlap cannot be hidden by a different layout.
    by_source={}
    for s in resolved:
        for p in s["panels"]:
            if not p["source"]:continue
            key=p["source"];start=p["source_start_frame"];end=start+p["source_frames"]
            for previous_start,previous_end,previous_shot in by_source.get(key,[]):
                if start<previous_end and previous_start<end:
                    raise ValueError(f"Repeated source interval:{p['name']} shots{previous_shot}/{s['index']}:{start}:{end} overlaps{previous_start}:{previous_end}")
            by_source.setdefault(key,[]).append((start,end,s["index"]))
    return resolved


class Reader:
    """Exact sequential60Hz RGB decode; never freezes to hide an EOF."""
    def __init__(self,panel):
        self.panel=panel;self.age=-1;self.last=None
        self.process=subprocess.Popen(["ffmpeg","-nostdin","-loglevel","error","-threads","1",
            "-ss",f"{panel['source_start_frame']/FPS:.9f}","-i",panel["source"],
            "-map","0:v:0","-an","-pix_fmt","rgb24","-f","rawvideo","pipe:1"],
            stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,**(INHERITED(LEASE) if LEASE and INHERITED else {}))
    def frame(self,age):
        if age<self.age:raise ValueError("Source age moved backwards")
        while self.age<age:
            data=self.process.stdout.read(400*224*3)
            if len(data)!=400*224*3:raise ValueError(f"Unexpected source EOF:{self.panel['name']} at{age}")
            self.last=Image.frombytes("RGB",(400,224),data);self.age+=1
        return self.last
    def close(self):
        self.process.stdout.close()
        self.process.terminate()
        try:self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:self.process.kill();self.process.wait()


class PngReader:
    """Bounded layout scout from the retained exact capture PNGs; no decoder jobs."""
    def __init__(self,panel):self.panel=panel
    def frame(self,age):
        file=Path(self.panel["source"]).parent/"output/frames"/f"{self.panel['source_start_frame']+age:05d}.png"
        return Image.open(file).convert("RGB")
    def close(self):pass


@lru_cache(maxsize=1)
def field():
    base=Image.new("RGB",(W,H),NAVY)
    bg=Image.open(OLD/"assets/aiz-background.png").convert("RGB")
    bg=bg.resize((W,H),Image.Resampling.NEAREST)
    base=Image.blend(base,bg,.075)
    d=ImageDraw.Draw(base)
    for x in range(-H,W+H,90):d.line((x,0,x-H,H),fill=(13,25,59),width=22)
    return base


def fit(image,size):
    # Integer nearest expansion, then area filtering as in Slay's split panels.
    if size==(1600,896):return image.resize(size,Image.Resampling.NEAREST)
    if size==(400,224):return image
    return image.resize((1600,896),Image.Resampling.NEAREST).resize(size,Image.Resampling.BOX)


def plate(image,text,y,scale=4,color=cards.WHITE):
    glyphs=cards.text_image(text,small=True,color=color)
    scale=min(scale,1800/max(1,glyphs.width))
    glyphs=glyphs.resize((round(glyphs.width*scale),round(glyphs.height*scale)),Image.Resampling.NEAREST)
    image.paste(glyphs,((W-glyphs.width)//2,y),glyphs)


def panel_box(canvas,image,box,age=99):
    x,y,w,h=map(round,box);picture=fit(image,(max(1,w),max(1,h)))
    if age<6:
        dy=round(-(h+8)*(1-age/6)**2)
        layer=Image.new("RGB",(w,h),NAVY);layer.paste(picture,(0,dy));picture=layer
    canvas.paste(picture,(x,y))
    ImageDraw.Draw(canvas).rectangle((x-2,y-2,x+w+1,y+h+1),outline=GOLD,width=2)


def player_x(panel,age):
    rows=state_rows(str(Path(panel["source"]).parent));n=panel["source_start_frame"]+age
    x=200
    if 0<=n<len(rows):x=int(rows[n]["x"])-int(rows[n]["cam_x"])
    if panel["name"]=="mirror":x=400-x
    return max(0,min(400,x))


def slices(canvas,panels,pictures,ages,tick,count,sweep=False):
    gutter=12;slope=math.tan(math.radians(12));width=W/count
    moving=(tick/max(1,panels[0].get("shot_frames",1)-1)-.5)*280 if sweep else 0
    for j,(panel,picture,age) in enumerate(zip(panels,pictures,ages)):
        if picture is None:continue
        centre=(j+.5)*width
        layer=field().copy();scaled=fit(picture,(1600,896))
        px=round(centre-player_x(panel,age)*4)
        layer.paste(scaled,(px,92))
        left=j*width+moving;right=(j+1)*width+moving
        if j==0:left=-300
        if j==count-1:right=W+300
        delta=slope*(H/2)
        vertices=[(left-delta+gutter/2,0),(right-delta-gutter/2,0),
                  (right+delta-gutter/2,H),(left+delta+gutter/2,H)]
        mask=Image.new("L",(W,H),0);draw=ImageDraw.Draw(mask);draw.polygon(vertices,fill=255)
        if age<6:
            # Masked drop reveal; pictures themselves retain native speed/geometry.
            cutoff=round(H*(1-age/6)**2);draw.rectangle((0,0,W,cutoff),fill=0)
        canvas.paste(layer,(0,0),mask)
        if j<count-1:
            edge=right;ImageDraw.Draw(canvas).line((edge-delta,0,edge+delta,H),fill=GOLD,width=5)


def editorial(shot,tick):
    base=cards.background(Image.open(OLD/"assets/aiz-background.png").convert("RGBA"),tick)
    card=shot["card"]
    if card=="FICTIONAL CRITICS":
        cards.plate(base,"FICTIONAL CRITICS",18,1.8,cards.GOLD)
        quotes=[("TAILS","ONE SONIC WAS PLENTY."),
                ("KNUCKLES","MY ISLAND. MY PROBLEM."),
                ("ROBOTNIK","FINALLY. FAIR COMPETITION.")]
        for j,(name,quote) in enumerate(quotes):
            y=59+j*49
            cards.plate(base,name,y,1.4,cards.GOLD)
            cards.plate(base,quote,y+17,1.35,cards.WHITE)
        cards.plate(base,"FICTIONAL REVIEWS. REAL CONSEQUENCES.",206,1,cards.PALE)
    elif shot["act"]=="end":
        # ROM title face has no digit3. Use the original plate face for the exact
        # SONIC3K wordmark, at a prominent size, above native CHAOS/MODE lettering.
        cards.plate(base,"SONIC3K",14,2.4,cards.GOLD)
        cards.title(base,["CHAOS","MODE"],tick,y0=42,target=1.35)
        cards.plate(base,"105 EFFECTS. CHOOSE YOUR POOL.",144,1.4,cards.GOLD)
        cards.plate(base,"AN OPENGGF MOD",170,1.2,cards.WHITE)
        cards.plate(base,"REQUIRES YOUR OWN SONIC 3 & KNUCKLES ROM",190,1,cards.PALE)
        cards.plate(base,"INDEPENDENT FAN PROJECT",206,1,cards.PALE)
    else:
        words={"ONE HEDGEHOG":["ONE","HEDGEHOG"],"NO RULES":["NO","RULES"],"CHAOS MODE":["CHAOS","MODE"]}[card]
        cards.title(base,words,tick)
        if card=="CHAOS MODE":cards.plate(base,"SONIC3K",171,2.2,cards.GOLD)
        cards.plate(base,"AN OPENGGF EXAMPLE MOD",206,1,cards.GOLD)
    return base.convert("RGB").resize((2000,1120),Image.Resampling.NEAREST).crop((40,20,1960,1100))


class ShotRenderer:
    def __init__(self,shot,allow_pending=False,prefer_png=False):
        self.shot=shot;self.readers={};self.allow_pending=allow_pending
        for i,p in enumerate(shot["panels"]):
            if p["source"]:self.readers[i]=(PngReader(p) if prefer_png else Reader(p))
    def frame(self,tick):
        s=self.shot
        if s["card"]:
            if s["act"]=="end" and tick<2:return Image.new("RGB",(W,H),(255,255,255))
            return editorial(s,tick)
        canvas=field().copy();pictures=[];ages=[]
        for i,p in enumerate(s["panels"]):
            age=tick-p["offset_frame"];ages.append(age)
            if age<0 or i not in self.readers:pictures.append(None);continue
            if s["layout"]=="STINGER":age=min(age,197)
            pictures.append(self.readers[i].frame(age))
        layout=s["layout"]
        if layout=="STINGER" and (tick<30 or tick>=246):canvas=Image.new("RGB",(W,H),(0,0,0))
        elif layout in ("FULL","STINGER"):
            if pictures and pictures[0]:panel_box(canvas,pictures[0],(160,92,1600,896),99)
        elif layout=="PAIR":
            for j,picture in enumerate(pictures):
                if picture:panel_box(canvas,picture,(8+j*960,276,944,528),ages[j])
        elif layout in ("QUAD","FULL->QUAD"):
            shrink=beat_frame(s["beat_start"]+4)-s["output_start_frame"] if layout=="FULL->QUAD" else -99
            for j,picture in enumerate(pictures):
                if picture is None:continue
                target=(8+(j%2)*960,8+(j//2)*536,944,528)
                if j==0 and layout=="FULL->QUAD" and tick<shrink+6:
                    u=max(0,min(1,(tick-shrink)/5))
                    box=tuple(a+(b-a)*u for a,b in zip((160,92,1600,896),target))
                    panel_box(canvas,picture,box,99)
                else:panel_box(canvas,picture,target,99 if j==0 and layout=="FULL->QUAD" else ages[j])
        elif layout in ("SLICE-2","TRIPLE","SLICE-4"):
            count={"SLICE-2":2,"TRIPLE":3,"SLICE-4":4}[layout]
            for p in s["panels"]:p["shot_frames"]=s["frames"]
            slices(canvas,s["panels"],pictures,ages,tick,count,sweep=s["original_index"] in (8,20))
        if s["caption"] and s["caption_begin"]<=tick<s["caption_end"]:
            d=ImageDraw.Draw(canvas);d.rectangle((0,1031,W,H),fill=NAVY);d.line((80,1032,W-80,1032),fill=GOLD,width=2)
            plate(canvas,s["caption"],1047,3)
        if s["act"]=="end" and tick<2:canvas=Image.new("RGB",(W,H),(255,255,255))
        return canvas
    def close(self):
        for reader in self.readers.values():reader.close()


def write_plan(plan):
    out=P/"out";out.mkdir(exist_ok=True)
    effect_set=sorted({p["effect"] for s in plan for p in s["panels"] if p["qualified"] and p["source"] and p["effect"]})
    pending=sorted({p["name"] for s in plan for p in s["panels"] if not p["source"] or not p["qualified"]})
    pending+=sorted({s["pending"] for s in plan if s.get("pending")})
    for s in plan:
        s["output_start_seconds"]=s["output_start_frame"]/FPS;s["output_end_seconds"]=s["output_end_frame"]/FPS
        for p in s["panels"]:
            p["source_start_seconds"]=p["source_start_frame"]/FPS
            p["source_end_seconds"]=(p["source_start_frame"]+p["source_frames"])/FPS
            p["source_relative"]=os.path.relpath(p["source"],P) if p["source"] else None
    data=dict(bpm=BPM,phase=PHASE,fps=FPS,total_frames=plan[-1]["output_end_frame"],
              qualified_effect_count=len(effect_set),qualified_effects=effect_set,
              pending_sources=pending,shots=plan,audio_policy="source audio muted; continuous native ROM bed and explicit editorial ROM cues")
    (out/"edit-timeline.json").write_text(json.dumps(data,indent=2)+"\n")
    with (out/"chapters.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["act","route_order","title","output_start_seconds","output_end_seconds","source","source_start_seconds","source_end_seconds","qualified"])
        writer.writeheader()
        for s in plan:
            for p in s["panels"] or [{}]:
                writer.writerow(dict(act=s["act"],route_order=s["index"],title=s["title"],
                    output_start_seconds=s["output_start_seconds"]+p.get("offset_frame",0)/FPS,
                    output_end_seconds=s["output_end_seconds"],source=p.get("source_relative","editorial"),
                    source_start_seconds=p.get("source_start_seconds",0),source_end_seconds=p.get("source_end_seconds",0),qualified=p.get("qualified",True)))
    print(f"{len(plan)} shots,{data['total_frames']/FPS:.3f}s,{len(effect_set)} explicitly qualified effects; pending:{','.join(pending)}",flush=True)
    return data


def encode_video(plan,destination,preview=False,max_frames=None):
    destination.parent.mkdir(exist_ok=True)
    scale=["-vf","scale=960:540:flags=area"] if preview else []
    process=subprocess.Popen(["ffmpeg","-nostdin","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24",
        "-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0",*scale,"-an","-c:v","libx264","-preset","fast",
        "-crf","18","-pix_fmt","yuv420p","-threads","2","-movflags","+faststart",str(destination)],stdin=subprocess.PIPE,
        **(INHERITED(LEASE) if LEASE and INHERITED else {}))
    sent=0
    try:
        for shot in plan:
            print(f"render{shot['index']:02d}:{shot['title']}({shot['frames']}frames)",flush=True)
            renderer=ShotRenderer(shot,allow_pending=preview)
            try:
                for tick in range(shot["frames"]):
                    if max_frames is not None and sent>=max_frames:break
                    process.stdin.write(renderer.frame(tick).tobytes());sent+=1
            finally:renderer.close()
            if max_frames is not None and sent>=max_frames:break
        process.stdin.close()
        if process.wait()!=0:raise RuntimeError("Video encoder failed")
    except BaseException:
        process.stdin.close();process.terminate();process.wait();raise
    return sent


def finish_audio(plan,video,destination):
    frames=plan[-1]["output_end_frame"];total=frames/FPS
    bed_end=plan[-2]["output_end_frame"]/FPS;fade_begin=beat_frame(210)/FPS
    cues=[]
    for s in plan:
        if s.get("sfx"):cues.append(dict(time=s["output_start_frame"]/FPS,file=str(OLD/"assets/audio"/f"{s['sfx']}.wav"),gain=.45,reason="Editorial card slam"))
        if s.get("death_output_frame") is not None:
            cues.append(dict(time=(s["output_start_frame"]+s["death_output_frame"])/FPS,file=str(OLD/"assets/audio/death.wav"),gain=.65,reason="Native visible death, ROM cue placed editorially"))
    extra=P/"editorial-cues.json"
    if extra.exists():cues+=json.loads(extra.read_text())
    inputs=["-i",str(video),"-i",str(P/"assets/hcz2-bed.wav")]
    graph=f"[1:a]atrim=duration={bed_end},asetpts=PTS-STARTPTS,volume=0.68,afade=t=out:st={fade_begin}:d={bed_end-fade_begin},apad=whole_dur={total}[bed]"
    labels=["[bed]"]
    for i,c in enumerate(cues):
        inputs += ["-i",c["file"]];delay=round(c["time"]*SR)
        graph+=f";[{i+2}:a]asetpts=PTS-STARTPTS,volume={c['gain']},adelay={delay}S:all=1[cue{i}]";labels.append(f"[cue{i}]")
    graph+=";"+"".join(labels)+f"amix=inputs={len(labels)}:normalize=0,atrim=duration={total},alimiter=limit=0.84:level=false,aresample=48000[a]"
    metadata=P/"work/chapters.ffmeta"
    text=";FFMETADATA1\ntitle=Sonic3K Chaos Mode — revision2\ncomment=Gameplay source audio muted; ROM soundtrack and SFX added editorially.\n"
    for s in plan:
        text+=f"[CHAPTER]\nTIMEBASE=1/60\nSTART={s['output_start_frame']}\nEND={s['output_end_frame']}\ntitle={s['title']}\n"
    metadata.write_text(text)
    inputs += ["-i",metadata]
    run(["ffmpeg","-nostdin","-loglevel","error","-y",*inputs,"-filter_complex_threads","1","-filter_complex",graph,
        "-map","0:v:0","-map","[a]","-map_metadata",str(2+len(cues)),"-map_chapters",str(2+len(cues)),
        "-c:v","copy","-c:a","aac","-b:a","256k","-ar","48000","-ac","2","-t",str(total),"-movflags","+faststart",destination])
    (P/"out/audio-cues.json").write_text(json.dumps(dict(bed=str(P/"assets/hcz2-bed.wav"),bed_end=bed_end,fade_begin=fade_begin,source_audio_used=False,cues=cues),indent=2)+"\n")


@contextmanager
def admitted(worktree):
    global LEASE,INHERITED
    sys.path.insert(0,"/home/farrell/code/projects/OpenGGF/tools/testing")
    from maven_queue import maven_slot,inherited_slot,handle_termination
    INHERITED=inherited_slot
    with handle_termination():
        with maven_slot(Path(worktree),exclusive=True,estimate=180,kind="chaos-reel-encode") as lease:
            LEASE=lease
            try:yield
            finally:LEASE=None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=["plan","preview","snapshot","render"])
    parser.add_argument("--allow-pending",action="store_true")
    parser.add_argument("--shots",default="8,10,12")
    parser.add_argument("--shot",type=int,default=12)
    parser.add_argument("--frame",type=int,default=105)
    parser.add_argument("--max-frames",type=int)
    parser.add_argument("--admission-worktree",type=Path,help="Lead-provided available task worktree; mandatory for encoding")
    args=parser.parse_args()
    if not args.admission_worktree:
        raise SystemExit("Source probes/encoding require --admission-worktree from the lead")
    with admitted(args.admission_worktree):
        execute(args)


def execute(args):
    # The single outer admission covers probes, decoders, encoder and final verification.
    plan=normalized_plan();data=write_plan(plan)
    if args.command=="plan":return
    if args.command=="snapshot":
        shot=plan[args.shot];renderer=ShotRenderer(shot,True,prefer_png=True)
        try:
            image=None
            for tick in range(min(args.frame,shot["frames"]-1)+1):image=renderer.frame(tick)
            folder=P/"previews";folder.mkdir(exist_ok=True)
            image.save(folder/f"shot-{args.shot:02d}-frame-{args.frame:04d}.png")
        finally:renderer.close()
        return
    if args.command=="preview":
        if not args.admission_worktree:raise SystemExit("Encoding requires --admission-worktree from the lead")
        chosen=[plan[int(i)] for i in args.shots.split(",")];dest=P/"previews/layout-preview.mp4"
        encode_video(chosen,dest,preview=True,max_frames=args.max_frames)
        run(["ffmpeg","-v","error","-xerror","-i",dest,"-f","null","-"])
        print(dest);return
    if data["pending_sources"] and not args.allow_pending:
        raise SystemExit("Final render blocked by pending source qualification:"+",".join(data["pending_sources"]))
    if args.allow_pending:raise SystemExit("Pending placeholder clips are preview-only; qualify sources before final render.")
    if not args.admission_worktree:raise SystemExit("Encoding requires --admission-worktree from the lead")
    work=P/"work";work.mkdir(exist_ok=True)
    video=work/"revision-2-video.mp4";destination=P/"out/sonic3k-chaos-mode-demo-v2.mp4"
    encode_video(plan,video);finish_audio(plan,video,destination)
    run(["ffmpeg","-v","error","-xerror","-i",destination,"-f","null","-"])
    info=probe(str(destination));(P/"out/media-info.json").write_text(json.dumps(info,indent=2)+"\n")
    if abs(float(info["format"]["duration"])-data["total_frames"]/FPS)>.04:raise ValueError("Final duration mismatch")
    print("FINAL",destination,flush=True)


if __name__=="__main__":main()
