"""pathmap.py layoutdir observe.csv x0 x1 — rings/objects vs the observed path (y at that x), marks collected."""
import csv, sys
L, obs, x0, x1 = sys.argv[1], sys.argv[2], int(sys.argv[3], 0), int(sys.argv[4], 0)
ob = list(csv.DictReader(open(obs)))
path = {}
for r in ob:
    x = int(r['x']); path.setdefault(x // 8, []).append((int(r['y']), int(r['frame'])))
def near(x, y):
    best = None
    for k in (x // 8 - 1, x // 8, x // 8 + 1):
        for py, f in path.get(k, []):
            d = abs(py - y)
            if best is None or d < best[0]: best = (d, py, f)
    return best
R = sorted((int(r['x']), int(r['y'])) for r in csv.DictReader(open(L + "/rings.csv")))
Ob = sorted((int(o['x']), int(o['y']), o['name'], o['subtype']) for o in csv.DictReader(open(L + "/objects.csv")))
skip = ('Scenery', 'LayerSwitcher', 'EHZWaterfall', 'AIZForegroundPlant', 'PathSwap', 'EdgeWalls')
items = [(x, y, 'o', '') for x, y in R if x0 <= x <= x1] + [(x, y, n, s) for x, y, n, s in Ob if x0 <= x <= x1 and n not in skip]
for x, y, n, s in sorted(items):
    b = near(x, y)
    tag = "-" if b is None else ("HIT" if b[0] <= 20 else f"dy{y-b[1]:+d}@f{b[2]}")
    print(f"{'ring' if n=='o' else n+'['+s+']':16s} {x:5d} {y:5d}  {tag}")
