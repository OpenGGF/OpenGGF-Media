#!/usr/bin/env python3
"""Renders S3K music and sound effects to 48 kHz WAV through OpenGGF's SMPS driver.

Generates a throwaway scene mod (outside the repo) that plays one music track at tick 0 and/or a
schedule of sound effects, and records it with ExampleModCapture --audio.

  render_audio.py music 0x04 100 out.wav          # 100 s of a music ID
  render_audio.py sfx 0xAB,0xB6,0x33 out.wav       # each SFX 3 s apart (slice at k*3 s)
"""
import shutil, subprocess, sys, tempfile
from pathlib import Path

WT = Path("/home/farrell/code/projects/OpenGGF/.worktrees/ai-slay-the-robotnik")
CP = f"{WT}/target/test-classes:{WT}/target/classes:" + (WT / "target/slay-test-classpath.txt").read_text().strip()
SFX_GAP_TICKS = 180

MANIFEST = """formatVersion: 1
id: promo-audio
name: Promo Audio
version: 0.1.0
authors:
  - promo
description: Plays a music track or a schedule of sound effects for offline rendering.
engineApiRange: ">=0.7.0 <0.8.0"
type: patch
baseGame: s3k
entrypoint: promoaudio.AudioMod
dependencies: []
audioOverrides: {}
artOverrides: {}
"""
MOD = """package promoaudio;
import com.openggf.mods.code.GgfMod;
import com.openggf.mods.code.ModContext;
public final class AudioMod implements GgfMod {
    @Override public void register(ModContext context) { context.registerStartupScene(AudioScene::new); }
}
"""
SCENE = """package promoaudio;
import com.openggf.mods.scene.ModScene;
import com.openggf.mods.scene.SceneCanvas;
import com.openggf.mods.scene.SceneContext;
public final class AudioScene implements ModScene {
    private final int music = %MUSIC%;
    private final int[] sfx = {%SFX%};
    private final int gap = %GAP%;
    private int ticks;
    @Override public void enter(SceneContext ctx) { if (music >= 0) ctx.audio().playMusic(music); else ctx.audio().stopMusic(); }
    @Override public void update(SceneContext ctx) {
        if (ticks %% gap == 0 && ticks / gap < sfx.length) ctx.audio().playSfx(sfx[ticks / gap]);
        ticks++;
    }
    @Override public void draw(SceneContext ctx, SceneCanvas canvas) { }
}
"""

def render(music, sfx, ticks, out):
    work = Path(tempfile.mkdtemp(prefix="promo-audio-"))
    src = work / "mod/src/main/java/promoaudio"
    src.mkdir(parents=True)
    res = work / "mod/src/main/resources/META-INF"
    res.mkdir(parents=True)
    (res / "openggf-mod.yaml").write_text(MANIFEST)
    (src / "AudioMod.java").write_text(MOD)
    (src / "AudioScene.java").write_text(SCENE.replace("%MUSIC%", str(music)).replace(
        "%SFX%", ",".join(str(s) for s in sfx)).replace("%GAP%", str(SFX_GAP_TICKS)).replace("%%", "%"))
    log = work / "log.txt"
    with open(log, "w") as f:
        r = subprocess.run(["java", "-cp", CP, "com.openggf.mods.code.ExampleModCapture",
                            "--rom", str(WT / "s3k.gen"), "--mod", str(work / "mod"), "--out", str(work / "out"),
                            "--every", "0", "--ticks", str(ticks), "--audio", str(Path(out).resolve())],
                           cwd=WT, stdout=f, stderr=subprocess.STDOUT)
    if r.returncode != 0 or not Path(out).resolve().exists():
        print(log.read_text()[-3000:])
        sys.exit(1)
    shutil.rmtree(work)

if __name__ == "__main__":
    kind = sys.argv[1]
    if kind == "music":
        render(int(sys.argv[2], 0), [], int(float(sys.argv[3]) * 60), sys.argv[4])
    else:
        ids = [int(x, 0) for x in sys.argv[2].split(",")]
        render(-1, ids, len(ids) * SFX_GAP_TICKS + 60, sys.argv[3])
