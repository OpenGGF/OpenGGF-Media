#!/usr/bin/env python3
"""Mutator Lab pacing/audio correction, 2026-10-10, root-owned after user feedback.

Reuse real PNG/PCM captures at exactly 60fps; no engine, display, device or retiming.
The preserved layout recipe supplies fonts and integer-nearest game panels.
This edit replaces short inserts with continuous native runs and longer comparisons.
Dependencies: Python3, NumPy, ffmpeg. Run: python recipe/build_film.py [--plan|--audio-only].
"""
from pathlib import Path
import importlib.util
import json
import math
import os
import subprocess
import sys
import time
import wave
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("layout", ROOT / "recipe/reference_layout.py")
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)
original_captures = Path("/home/farrell/scratch/agent-tmp/claude/mutator-complete-showcase-20261010/captures")
for key, (take, game) in list(layout.TAKES.items()):
    if take.is_relative_to(ROOT / "captures"):
        layout.TAKES[key] = (original_captures / take.relative_to(ROOT / "captures"), game)
layout.ROOT = ROOT
layout.WORK = ROOT / "work/video"
layout.OUT = ROOT / "out"
layout.S = []
S = layout.S
full, multi = layout.full, layout.multi
RATE, SPF = 48000, 800
REG = Path.home() / ".local/state/temporary-agents/mutator-audio-revision-20261010/manifest.json"
FINAL = ROOT / "out/mutator-lab-complete-showcase-revised.mp4"

# Each shot is a continuous native source interval. Configuration -> resumed play
# stays in one shot where possible, including the live native double-speed sound.
full("open-ringstorm", "hero", 708, 850, [(0.15, 2.3, "173 rings. One hit.")])
full("title", "allon", 540, 690, title=True)
full("hero-config", "hero", 84, 208, [(0.15, 1.9, "Drop the whole inventory")])
full("hero-run", "hero", 470, 1000,
     [(0.3, 2.65, "Bank 173 rings"), (3.8, 5.3, "One hit: every ring comes out"),
      (5.4, 8.7, "Grab them back — the head regrows")], layout.HERO)
multi("hero-compare", [("ghznat", 518), ("hero", 702)], 122,
      ("NATIVE: 32 DROP", "FULL INVENTORY: 173 DROP"), 1,
      [(0.15, 1.95, "Same hit, same input")], note="Both: positioned start, 140 rings carried in")
full("chain-config", "chain", 84, 250, [(0.15, 2.65, "300% rebound · choose a speed cap")])
full("chain-run", "chain", 290, 1030,
     [(0.3, 3.1, "Badniks become launch pads"), (3.75, 5.6, "×2"), (6.3, 8.0, "×3"),
      (8.65, 10.4, "×4"), (11.2, 12.3, "×5 — 2,800 points")], layout.CHAIN)
full("grav-normal", "live", 50, 160, [(0.15, 1.7, "Normal gravity")], layout.GRAV_OFF)
full("grav-on", "live", 186, 540,
     [(0.15, 2.65, "Slide gravity down to 25%"), (2.85, 5.8, "Moon jump — no restart")])
full("grav-off", "live", 606, 820,
     [(0.15, 1.65, "Toggle it off"), (1.8, 3.45, "Back to normal")])
full("speed-normal", "spdlive", 110, 240, [(0.15, 2.05, "Game Speed: 100%")], layout.SPD_OFF)
full("speed-on", "spdlive", 352, 760,
     [(0.15, 3.85, "Choose 200% — and audio follows"),
      (4.55, 6.7, "Two native ticks per frame — music too")])
multi("speed-compare", [("spd50", 20), ("spd100", 20), ("spd200", 20)], 280,
      ("50%", "100%", "200%"), 1, [(0.15, 4.5, "Same input. Same time on screen.")],
      note="Act start · audio at normal rate in all three")
full("stealth-before", "stealth", 30, 100, [(0.1, 1.1, "Big Head: fixed 200%")], layout.ST_OFF)
full("stealth-on", "stealth", 146, 600,
     [(0.15, 1.9, "Stealth on"), (2.3, 4.8, "Invisible — still playing"),
      (5.0, 6.4, "Still collecting rings…"), (6.45, 7.5, "…still defeating Mashers")])
full("stealth-off", "stealth", 742, 935,
     [(0.15, 1.9, "Stealth off"), (2.15, 3.1, "Back — head and all")])
full("np-before", "np", 165, 440,
     [(0.1, 1.25, "Ten-ring monitor"), (3.45, 4.5, "Invincibility monitor")], layout.NP_OFF)
full("np-config", "np", 776, 852, [(0.05, 1.2, "Remove only Invincibility")], layout.NP_PEND)
multi("np-compare", [("np", 165), ("np", 1222)], 290,
      ("BEFORE", "AFTER FULL RESTART"), 1,
      [(0.15, 2.6, "Ten-ring monitor stays"), (3.1, 4.7, "Invincibility monitor is gone")],
      note="Same take · selective removal applies on a full restart")
full("norings-before", "norings", 250, 370, [(0.15, 1.85, "Rings on the hill…")], layout.NR_CHIP)
full("norings-config", "norings", 410, 560, [(0.15, 2.35, "No Rings — restart the act")])
full("norings-after", "norings", 1150, 1440,
     [(0.15, 2.75, "…gone"), (3.15, 4.7, "No rings. One hit is fatal.")], [("NO RINGS", "on")])
multi("nc-hit", [("nc", 74), ("nc", 554)], 146,
      ("WITH CHECKPOINT", "NO CHECKPOINTS ON LOAD"), 1,
      [(0.1, 2.3, "Same fatal hit")],
      note="Two deaths in one take · setting applies on the next load")
multi("nc-result", [("nc", 553), ("nc", 812)], 90,
      ("RESPAWN AT POST", "RESPAWN AT ACT START"), 1,
      [(0.05, 1.4, "Post respawn vs act start")],
      note="Two actual respawns · loading and settings cut")
multi("ss-touch", [("ssyes", 240), ("ssno", 424)], 140,
      ("STOCK", "NO SPECIAL STAGES"), 0, [(0.15, 2.2, "Same jump into the giant ring")],
      note="Both: positioned near the goal, 50 rings carried in")
multi("ss-outcome", [("ssyes", 1386), ("ssno", 1712)], 150,
      ("SPECIAL STAGE", "STRAIGHT INTO ACT 2"), 0,
      [(0.15, 2.35, "After the native act transition")],
      note="Both: positioned near the goal, 50 rings carried in · loading cut")
multi("bon-compare", [("bonyes", 112), ("bonno", 296)], 332,
      ("STOCK: BONUS STARS", "NO BONUS STAGES"), 0,
      [(0.15, 3.0, "Enter a bonus stage…"), (3.45, 5.4, "…or keep the run moving")],
      note="Sonic 3 & Knuckles only · positioned at starpost, 25 rings carried in")
full("finale-run", "allon", 470, 1034,
     [(0.15, 3.4, "Stack them: low gravity, giant head"), (3.65, 4.9, "211 rings in the bank…"),
      (5.0, 6.55, "…one Rhinobot later"), (6.75, 9.3, "Grab them back. Do it again.")], layout.ALL)
full("outro", "hero", 960, 1140, outro=True)

GROUPS = [("Cold open", "open-"), ("Title", "title"), ("Ringfall + Big Head", "hero-"),
          ("Violent Explosions", "chain-"), ("Gravity", "grav-"), ("Game Speed", "speed-"),
          ("Stealth", "stealth-"), ("No Powerups", "np-"), ("No Rings", "norings-"),
          ("No Checkpoints", "nc-"), ("No Special Stages", "ss-"), ("No Bonus Stages", "bon-"),
          ("Stack everything", "finale-"), ("Outro", "outro")]
# Local frame intervals actually showing Lab configuration. Lower/muffle the same
# continuous soundtrack, then release it before the production Resume cue.
DUCKS = {
    "hero-config": [(0, 118)], "chain-config": [(0, 156)],
    "grav-on": [(0, 156)], "grav-off": [(0, 80)],
    "speed-on": [(0, 258)], "stealth-on": [(0, 117)],
    "stealth-off": [(0, 114)], "np-config": [(0, 76)],
    "norings-config": [(0, 150)],
}


def run(cmd, timeout=600):
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    start = Path(f"/proc/{proc.pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    if REG.exists():
        registry = json.loads(REG.read_text())
        registry.setdefault("processes", []).append({"pid": proc.pid, "start_ticks": start,
            "argv": cmd, "cwd": str(ROOT), "owner": "root-paced-remix", "state": "running"})
        REG.write_text(json.dumps(registry, indent=2) + "\n")
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except BaseException:
        proc.terminate()
        try: proc.communicate(timeout=10)
        except subprocess.TimeoutExpired: proc.kill(); proc.communicate(timeout=10)
        raise
    finally:
        if REG.exists():
            registry = json.loads(REG.read_text())
            for item in registry["processes"]:
                if item.get("pid") == proc.pid and item.get("start_ticks") == start:
                    item.update(state="reaped", exit_code=proc.returncode)
            REG.write_text(json.dumps(registry, indent=2) + "\n")
    if proc.returncode:
        raise RuntimeError(stderr[-4000:])
    return stdout, stderr


def render_run(cmd):
    # Bound the existing layout recipe's FFmpeg worker/filter/encoder threads.
    cmd = cmd[:1] + ["-nostdin", "-threads", "4", "-filter_complex_threads", "2"] + cmd[1:]
    idx = cmd.index("-preset")
    cmd[idx:idx] = ["-threads", "4"]
    run(cmd)


def plan():
    shots, pos = [], 0
    for s in S:
        sources = []
        w, h, xy = layout.GEOM[s["kind"]]
        for j, (key, frame) in enumerate(s["panels"]):
            take = layout.TAKES[key][0]
            endpoint = take / "capture/frames" / f"{frame + s['n'] - 1:05d}.png"
            assert endpoint.is_file(), endpoint
            sources.append({"take": str(take), "frames": [frame, frame+s["n"]],
                "crop": [*xy[j], w, h], "audio": j == s["audio"]})
        shots.append({"id": s["id"], "kind": s["kind"], "frames": s["n"],
            "output_frames": [pos, pos+s["n"]], "start_s": pos/60,
            "end_s": (pos+s["n"])/60, "sources": sources,
            "captions": s["caps"], "labels": s.get("labels", []), "note": s.get("note"),
            "configuration_local_frames": DUCKS.get(s["id"], [])})
        pos += s["n"]
    chapters = []
    for title, prefix in GROUPS:
        matches = [s for s in shots if s["id"].startswith(prefix)]
        chapters.append({"title": title, "start_s": matches[0]["start_s"],
                         "end_s": matches[-1]["end_s"]})
    return {"frames": pos, "duration_s": pos/60, "shots": len(shots),
            "segments": shots, "chapters": chapters, "speed": "native source frames1:1, no editorial retiming"}


def pcm(take):
    with wave.open(str(Path(take) / "capture/audio.wav")) as f:
        assert (f.getframerate(), f.getnchannels(), f.getsampwidth()) == (48000, 2, 2)
        return np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").reshape(-1, 2).astype(np.float64)/32768


def soundtrack(p):
    n = p["frames"]*SPF
    dry, wet = {}, {}
    trims = json.loads((ROOT / "recipe/trims.json").read_text())
    mix = np.zeros((n, 2))
    manifest = []
    segments = p["segments"]
    previous_lag = 0
    for i, seg in enumerate(segments):
        src = next(x for x in seg["sources"] if x["audio"])
        take, frame = src["take"], src["frames"][0]
        if take not in dry:
            dry[take] = pcm(take)
        # The outro is intentionally silent, as in the Hardened reference reel.
        if seg["id"] == "outro":
            manifest.append({"segment": seg["id"], "silent": True}); continue
        a, b = seg["output_frames"]
        lead = 6 if i else 0
        lag = 6 if i < len(segments)-2 else 0
        # The complete native 200% demonstration is protected through its last
        # sample. Its handoff begins after the picture switches to the trio.
        if i and segments[i-1]["id"] == "speed-on":
            lead = 0
        if seg["id"] == "speed-on":
            lag = 12
        lag = min(lag, len(dry[take])//SPF-frame-seg["frames"])
        assert lag >= 0
        # Keep the opening ring spill intact; its first sound is3frames in.
        aa, bb = a-lead, b+lag
        sa, sb = (frame-lead)*SPF, (frame+seg["frames"]+lag)*SPF
        raw = dry[take][sa:sb].copy()
        assert raw.shape == ((bb-aa)*SPF, 2), (seg["id"], raw.shape)
        gain = np.ones(len(raw))
        if i:
            k = (lead + previous_lag)*SPF
            gain[:k] = np.sin((np.arange(k)+.5)/k*np.pi/2)
        if lag:
            k = (lag + (0 if seg["id"] == "speed-on" else 6))*SPF
            gain[-k:] = np.cos((np.arange(k)+.5)/k*np.pi/2)
        if not i:
            k=2*SPF; gain[:k] *= np.sin((np.arange(k)+.5)/k*np.pi/2)
        muffle = np.zeros(len(raw))
        for da, db in seg["configuration_local_frames"]:
            lo, hi = (da+lead)*SPF, (db+lead)*SPF
            muffle[lo:hi] = 1
            k=min(6*SPF, hi-lo)
            if da: muffle[lo:lo+k] = (1-np.cos((np.arange(k)+.5)/k*np.pi))/2
            muffle[hi-k:hi] = (1+np.cos((np.arange(k)+.5)/k*np.pi))/2
        if np.any(muffle):
            if take not in wet:
                target = ROOT / "work" / (Path(take).name + "-lowpass.f32")
                if not target.exists():
                    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-threads", "2", "-i",
                         str(Path(take)/"capture/audio.wav"), "-af", "lowpass=f=1600:p=2",
                         "-acodec", "pcm_f32le", "-f", "f32le", str(target)])
                wet[take]=np.fromfile(target,dtype="<f4").reshape(-1,2).astype(np.float64)
            raw=raw*(1-muffle[:,None])+wet[take][sa:sb]*muffle[:,None]
            gain *= 10**(-7*muffle/20)
        trim = trims.get(Path(take).name,0)
        gain *= 10**(trim/20)
        if i == len(segments)-2:
            # Fade down in the final second of moving gameplay, then silence.
            k=60*SPF; gain[-k:] *= np.cos((np.arange(k)+.5)/k*np.pi/2)
        mix[aa*SPF:bb*SPF] += raw*gain[:,None]
        manifest.append({"segment": seg["id"], "take": take,
            "source_samples": [sa,sb], "output_samples": [aa*SPF,bb*SPF],
            "nominal_output_frames": [a,b], "trim_db": trim,
            "handoff_s": (lead+previous_lag)/60 if i else 0,
            "fade_in_output_samples": [aa*SPF,(a+previous_lag)*SPF] if i else [0,2*SPF],
            "fade_out_output_samples": [(b-(0 if seg['id']=='speed-on' else 6))*SPF,(b+lag)*SPF] if lag else [(b-60)*SPF,b*SPF],
            "configuration_local_frames": seg['configuration_local_frames'],
            "configuration_ramp_frames": 6, "configuration_duck_db": -7,
            "lowpass_hz": 1600 if np.any(muffle) else None,
            "synchronous": True, "audio_owner": "selected panel only; brief equal-power handoffs"})
        previous_lag = lag
    prenorm=ROOT/"work/mix-prenorm.f32";mix.astype("<f4").tofile(prenorm)
    _,stderr=run(["ffmpeg","-nostdin","-hide_banner","-v","info","-threads","2",
        "-f","f32le","-ar","48000","-ac","2","-i",str(prenorm),"-af",
        "loudnorm=I=-16:TP=-2.5:LRA=11:print_format=json","-f","null","-"])
    stats=json.loads(stderr[stderr.rfind('{'):stderr.rfind('}')+1])
    # Static normalization: no pumping or limiting. Leave AAC reconstruction headroom.
    gain_db=min(-16-float(stats["input_i"]),-2.5-float(stats["input_tp"]))
    mix*=10**(gain_db/20)
    q=np.rint(mix*32767).astype("<i2")
    assert np.max(np.abs(mix))<1
    assert not np.any(np.abs(q.astype(np.int32))>=32767)
    wav=ROOT/"out/soundtrack.wav"
    with wave.open(str(wav),"wb") as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(48000);f.writeframes(q.tobytes())
    (ROOT/"out/audio-manifest.json").write_text(json.dumps({
        "status":"Editorial mix from native music+SFX captures, not isolated stems or raw audio evidence",
        "samples":n,"rate":48000,"channels":2,"static_gain_db":gain_db,
        "measured_prenorm":stats,"pcm_clipped_samples":0,"pieces":manifest,
        "speed_proof":"speed-on source616–760 plays its actual native double-speed PCM, aligned to picture",
        "limits":"Equal-power joins alter only clip boundaries; configuration audio is ducked/low-passed. No devices observed."},indent=2)+'\n')
    return wav


def main():
    for d in [ROOT/"work",layout.WORK,ROOT/"out"]:d.mkdir(parents=True,exist_ok=True)
    p=plan();(ROOT/"out/chapters.json").write_text(json.dumps(p,indent=2)+'\n')
    if "--plan" in sys.argv:
        print(json.dumps({k:p[k] for k in ["frames","duration_s","shots","chapters"]},indent=2));return
    if "--audio-only" not in sys.argv:
        layout.run=render_run
        for i,s in enumerate(S):
            out=layout.WORK/f"seg{i:03d}-{s['id']}.mkv"
            existing=list(layout.WORK.glob("seg*-"+s['id']+".mkv"))
            if not out.exists() and existing:
                # Reuse only an unchanged shot's already-rendered source range.
                os.rename(existing[0],out)
            if not out.exists():layout.render(s,i)
            print(f"{i+1}/{len(S)} {s['id']} {s['n']/60:.2f}s",flush=True)
        video_list=ROOT/"work/concat.txt"
        paths = [layout.WORK / ("seg%03d-%s.mkv" % (i, s["id"])) for i,s in enumerate(S)]
        video_list.write_text(''.join("file '%s'\n" % path for path in paths))
        run(["ffmpeg","-nostdin","-v","error","-y","-threads","4","-filter_threads","2",
             "-f","concat","-safe","0","-i",str(video_list),"-map","0:v:0","-an",
             "-vf","setpts=N/(60*TB)","-r","60","-fps_mode","cfr","-c:v","libx264",
             "-threads","4","-preset","medium","-crf","16","-profile:v","high","-pix_fmt","yuv420p",
             str(ROOT/"work/picture.mp4")])
    wav=soundtrack(p)
    meta=ROOT/"work/chapters.ffmeta"
    lines=[';FFMETADATA1','title=Mutator Lab — complete showcase, revised pacing and sound',
           'comment=Native gameplay at recorded speed. Editorially mixed native music and SFX; see audio-manifest.json.']
    for c in p['chapters']:
        lines+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(c['start_s']*1000)}",f"END={round(c['end_s']*1000)}",f"title={c['title']}"]
    meta.write_text('\n'.join(lines)+'\n')
    run(["ffmpeg","-nostdin","-v","error","-y","-threads","4","-i",str(ROOT/"work/picture.mp4"),
        "-i",str(wav),"-i",str(meta),"-map","0:v:0","-map","1:a:0","-map_metadata","2",
        "-map_chapters","2","-c:v","copy","-c:a","aac","-b:a","256k","-ar","48000",
        "-ac","2","-movflags","+faststart",str(FINAL)])
    print(FINAL,flush=True)


if __name__ == '__main__':main()
