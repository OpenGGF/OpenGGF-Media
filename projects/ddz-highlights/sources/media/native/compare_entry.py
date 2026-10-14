# Compare engine GameplayCaptureTool state.csv against native DDZ exporter observations.
# Usage: compare_entry.py <engine state.csv> <native observations.csv> <movie base frame> [label]
import csv, sys
eng = {int(r['frame']): r for r in csv.DictReader(open(sys.argv[1]))}
B = int(sys.argv[3]); label = sys.argv[4] if len(sys.argv) > 4 else None
fields = [('x','p1_x'),('y','p1_y'),('cam_x','cam_x'),('cam_y','cam_y'),('rings','rings')]
bad = 0
for r in csv.DictReader(open(sys.argv[2])):
    if label and r['label'] != label: continue
    f = int(r['movie_frame']) - B
    e = eng.get(f)
    if e is None: continue
    diffs = [(a, e[a], r[b]) for a, b in fields if int(e[a]) & 0xFFFF != int(r[b]) & 0xFFFF]
    if diffs:
        bad += 1
        if bad <= 25: print(f, diffs)
print('mismatching frames:', bad)
