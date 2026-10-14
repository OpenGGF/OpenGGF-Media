# Compare GameplayCaptureTool state.csv (every frame or strided) against a V5 trace physics.csv.gz
# (comparison only). Usage: compare_trace.py <state.csv> <physics.csv.gz> [max_report] [row_to_frame_offset]
# zone0c: trace row r is the state after engine capture frame r + 1 (offset 1).
import csv, gzip, sys
eng = {int(r['frame']): r for r in csv.DictReader(open(sys.argv[1]))}
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
offset = int(sys.argv[4]) if len(sys.argv) > 4 else 1
shown = 0
first = None
for r in csv.DictReader(gzip.open(sys.argv[2], 'rt')):
    f = int(r['frame'], 16) + offset
    e = eng.get(f)
    if e is None:
        continue
    pairs = [('cam_x', 'camera_x'), ('cam_y', 'camera_y'), ('x', 'player_x'), ('y', 'player_y'), ('rings', 'rings')]
    diffs = [(a, int(e[a]) & 0xFFFF, int(r[b], 16)) for a, b in pairs if (int(e[a]) & 0xFFFF) != int(r[b], 16)]
    big = [d for d in diffs if abs(d[1] - d[2]) > 1]
    if big:
        if first is None:
            first = f
        if shown < limit:
            print(f, big)
            shown += 1
print('first >1px divergence frame:', first)
