#!/usr/bin/env python3
"""Per-row audio health of the r5 Putt Putt Paradise captures (Opus final round, 2026-10-06).

Purpose: catch the faults that sank the r4 draft (constant DC with the music missing, weak
zone music, dropouts) before any footage is edited. Each 60 Hz row owns exactly one 800-frame
stereo packet, so every statistic is reported per row and joined to the request log.

For every WAV it reports: rows, the AC level (standard deviation, dBFS) and DC (mean) over the
whole file and over gameplay after the first zone-music request, every run of >= 8 consecutive
"flat" rows (AC < -70 dBFS: silence or constant DC), the largest |DC| of any row, and every
sample-to-sample jump > 0.5 FS (a click/discontinuity at a packet boundary). Flat runs are
attributed: before the first music request (expected ROM entry silence) or after (a fault unless
a music request, pause or rewind explains it).

Usage: audio_qc.py CAPTURE_DIR [CAPTURE_DIR ...]   (writes audio-qc.json in each directory)
"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

SPF = 800
FLAT_DB = -70.0
MIN_RUN = 8


def load(path):
    with wave.open(str(path)) as w:
        assert w.getframerate() == 48000 and w.getnchannels() == 2 and w.getsampwidth() == 2, path
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float64) / 32768


def db(x):
    return round(float(20 * np.log10(max(x, 1e-9))), 2)


def requests(cap):
    out = []
    path = cap / "audio-requests.csv"
    for line in path.read_text().splitlines()[1:]:
        phase, row, kind, ident = line.split(",")
        out.append((phase, int(row), kind, ident))
    return out


def analyse(wav, phase, reqs):
    data = load(wav)
    rows = len(data) // SPF
    per = data[:rows * SPF].reshape(rows, SPF, 2)
    ac = per.std(axis=1).max(axis=1)
    dc = per.mean(axis=1)
    music = [r for p, r, k, i in reqs if p == phase and k == "MUSIC"]
    first = music[0] if music else rows
    flat = ac < 10 ** (FLAT_DB / 20)
    runs, start = [], None
    for r in range(rows + 1):
        if r < rows and flat[r]:
            start = r if start is None else start
        elif start is not None:
            if r - start >= MIN_RUN:
                runs.append({"from": start, "to": r - 1, "rows": r - start,
                             "dc": round(float(np.abs(dc[start:r]).max()), 5),
                             "before_first_music": r - 1 < first})
            start = None
    jumps = np.abs(np.diff(data, axis=0)).max(axis=1)
    big = np.nonzero(jumps > 0.5)[0]
    body = per[first:] if first < rows else per[:0]
    flat_after = [x for x in runs if not x["before_first_music"]]
    return {
        "wav": wav.name, "rows": rows, "first_music_row": first if music else None,
        "music_requests": [(r, i) for p, r, k, i in reqs if p == phase and k == "MUSIC"],
        "ac_dbfs_all": db(data.std()), "dc_all": round(float(np.abs(data.mean(axis=0)).max()), 6),
        "ac_dbfs_after_music": db(body.reshape(-1, 2).std()) if len(body) else None,
        "max_row_abs_dc": round(float(np.abs(dc).max()), 5),
        "rows_with_abs_dc_over_0p02": int((np.abs(dc).max(axis=1) > 0.02).sum()),
        "flat_runs": runs, "flat_rows_after_first_music": int(sum(x["rows"] for x in flat_after)),
        "jumps_over_half_fs": [{"sample": int(s), "row": int(s // SPF)} for s in big[:20]],
        "peak_dbfs": db(np.abs(data).max()),
    }


def main():
    for arg in sys.argv[1:]:
        cap = Path(arg)
        reqs = requests(cap)
        report = {"capture": cap.name}
        for wav, phase in (("title.wav", "title"), ("gameplay.wav", "gameplay")):
            if (cap / wav).exists():
                report[phase] = analyse(cap / wav, phase, reqs)
        (cap / "audio-qc.json").write_text(json.dumps(report, indent=1) + "\n")
        g = report.get("gameplay", {})
        print(f"{cap.name}: rows={g.get('rows')} firstMusic={g.get('first_music_row')} "
              f"AC={g.get('ac_dbfs_after_music')}dBFS maxRowDC={g.get('max_row_abs_dc')} "
              f"dcRows={g.get('rows_with_abs_dc_over_0p02')} flatAfterMusic={g.get('flat_rows_after_first_music')} "
              f"runs={[(x['from'], x['to']) for x in g.get('flat_runs', [])]} jumps={len(g.get('jumps_over_half_fs', []))} "
              f"| title AC={report.get('title', {}).get('ac_dbfs_all')} runs={[(x['from'], x['to']) for x in report.get('title', {}).get('flat_runs', [])]}")


if __name__ == "__main__":
    main()
