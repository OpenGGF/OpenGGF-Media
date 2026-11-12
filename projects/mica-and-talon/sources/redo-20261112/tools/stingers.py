#!/usr/bin/env python3
"""Purpose: stinger report for the edit: each ROM sound's output frame/time, level against the music under it
(loudest 100 ms of the stinger x its gain, vs the bed x its gain and fade at that moment) and left/right balance.
Same measure as promo_kit's sound_balance, printed as a table instead of warnings.
Inputs: edit/edit.py (imports it). Output: JSON on stdout. Origin: MICA & TALON promo redo 2026-11-12."""
import importlib.util, json, os, sys
from pathlib import Path
import numpy as np
T = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get('MT_CHECKOUT', '/mnt/LinuxData/T3/worktrees/OpenGGF/t3-841b918f'))
sys.path.insert(0, str(ROOT / 'tools/media'))
import promo_kit
spec = importlib.util.spec_from_file_location('mt_edit', T / 'edit/edit.py'); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
e = promo_kit.Edit(**mod.EDIT); mod.build(e)
SR = promo_kit.SR; spf = SR // e.fps; win = SR // 10
bed_wav, b_at, b_gain = e.beds[0][0], e.beds[0][1], e.beds[0][2]
bed = promo_kit.read_wav(bed_wav)
lvl = lambda a: 20 * np.log10(max(float(np.sqrt((a ** 2).mean())) if len(a) else 0.0, 1e-9))
rows = []
for f, wav, gain, length in sorted(e.sfx, key=lambda x: x[0]):
    a = promo_kit.read_wav(wav)
    power = (a ** 2).mean(axis=1); n = min(win, len(a))
    i = int(np.argmax(np.convolve(power, np.ones(n) / n, mode='valid')))
    loud = a[i:i + n] * gain
    under = bed[f * spf + i:f * spf + i + n] * b_gain
    rows.append(dict(frame=f, t=round(f / e.fps, 3), sfx=Path(wav).name.replace('-paced.wav', ''), gain=gain,
                     stinger_db=round(lvl(loud), 1), bed_db=round(lvl(under), 1), under_bed_db=round(lvl(under) - lvl(loud), 1),
                     l_minus_r_db=round(lvl(loud[:, 0]) - lvl(loud[:, 1]), 1)))
json.dump(rows, sys.stdout, indent=1)
