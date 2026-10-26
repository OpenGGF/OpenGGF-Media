#!/usr/bin/env python3
"""Report measured integer position/camera changes, never inferred fight phases.

Origin: spaced Typing route demo, 2026-10-25. Reads GameplayCaptureTool state.csv.
No image selection/rendering, media process, JVM, Maven or engine is launched.
Changed-edge groups are search aids; pauses/subpixel plateaus are not phase labels.
"""
import argparse
import json
import sys
from pathlib import Path

from demo_common import json_new, read_state, sha256


def analyze(rows, merge_gap=0, jump_threshold=256):
    keys = ('x', 'y', 'cam_x', 'cam_y')
    points = [{k: int(row[k]) for k in keys} for row in rows]
    edges = []
    for frame in range(1, len(rows)):
        delta = {k: points[frame][k] - points[frame-1][k] for k in keys}
        if any(delta.values()):
            edges.append({'frame': frame, 'delta': delta,
                          'large_delta_candidate': any(abs(v) >= jump_threshold for v in delta.values())})
    groups = []
    for edge in edges:
        if not groups or edge['frame'] - groups[-1][-1]['frame'] > merge_gap + 1:
            groups.append([])
        groups[-1].append(edge)
    spans = []
    for group in groups:
        first, last = group[0]['frame'], group[-1]['frame']
        previous = first - 1
        spans.append({'measurement_start_frame': previous, 'first_changed_frame': first,
                      'last_changed_frame': last, 'end_frame_exclusive': last+1,
                      'csv_data_rows_inclusive': [previous+1, last+1],
                      'start': points[previous], 'end': points[last],
                      'net_delta': {k: points[last][k]-points[previous][k] for k in keys},
                      'sum_absolute_integer_changes': {k: sum(abs(e['delta'][k]) for e in group) for k in keys},
                      'changed_edges': len(group),
                      'large_delta_candidate_frames': [e['frame'] for e in group if e['large_delta_candidate']]})
    return {'rows': len(rows), 'frames_inclusive': [0, len(rows)-1], 'csv_schema': list(rows[0]),
            'merge_gap_rows': merge_gap, 'large_delta_threshold_pixels': jump_threshold,
            'velocity_columns_all_zero': all(float(row[k]) == 0 for row in rows for k in ('xvel', 'yvel', 'gspeed')),
            'death_frames': [int(r['frame']) for r in rows if r['dead'] == '1'],
            'limits': ['No fight/wave/word/GO fields; inspect matching frames to annotate phases.',
                       'Coordinates are unsigned integer centres; subpixel movement is absent.',
                       'Entry relocation, resets, wrap and excursions can change coordinates without route progression.',
                       'Large-delta flags are a configurable heuristic, not an automatic exclusion or teleport claim.',
                       'Summed integer changes are not path length or native velocity; net delta is only endpoint displacement.',
                       'Frame numbers are zero-based; data row = frame+1; physical CSV line = frame+2.',
                       'State is sampled after stepping and before the matching frame render.'],
            'candidate_changed_edge_spans': spans, 'fight_phases': 'PENDING independent frame review'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv', type=Path, required=True)
    p.add_argument('--frames', type=int, help='Require exactly this many consecutive rows')
    p.add_argument('--merge-gap', type=int, default=0, help='Bridge this many unchanged edges for search grouping only')
    p.add_argument('--jump-threshold', type=int, default=256, help='Flag raw coordinate/camera deltas at least this large')
    p.add_argument('--out', type=Path, help='NEW JSON file; default stdout')
    a = p.parse_args()
    if a.merge_gap < 0 or a.jump_threshold < 1:
        p.error('merge-gap must be nonnegative and jump-threshold positive')
    rows = read_state(a.csv, a.frames)
    report = analyze(rows, a.merge_gap, a.jump_threshold)
    report.update(csv=str(a.csv.resolve()), csv_sha256=sha256(a.csv))
    if a.out:
        json_new(a.out, report)
        print(f'Wrote {len(report["candidate_changed_edge_spans"])} candidate motion groups: {a.out}')
    else:
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))
