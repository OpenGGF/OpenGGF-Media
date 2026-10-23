"""Maps the capture frame numbers the edit was written against onto a re-captured take.

Film A's constants (GO, take-offs, the death, the vote...) are frame numbers in the captures the
edit was cut from. A re-capture of the same scripted run (2026-10-23, new race HUD) differs by a
few frames per chapter (load timing), so each capture directory keeps the chapters the edit was
written against in edit-chapters.csv beside the new take's chapters.csv: frame f in edit
chapter k is frame f + (new_k - old_k) in the take. Directories without edit-chapters.csv map 1:1.
"""
import csv
from functools import lru_cache
from pathlib import Path


def _chapters(path):
    with open(path, encoding="utf-8") as fh:
        return [(int(row[0]), " ".join(row[1].split())) for row in csv.reader(fh) if row]


@lru_cache(maxsize=None)
def segments(cap_dir):
    """[(edit_start, delta)] in edit numbering, sorted; empty when the take is the edit's own."""
    cap_dir = Path(cap_dir)
    old_path = cap_dir / "edit-chapters.csv"
    if not old_path.exists():
        return ()
    old, new = _chapters(old_path), _chapters(cap_dir / "chapters.csv")
    if [n for _, n in old] != [n for _, n in new]:
        raise ValueError(f"{cap_dir}: chapters differ: {[n for _, n in old]} vs {[n for _, n in new]}")
    return tuple((o, n - o) for (o, _), (n, _) in zip(old, new))


def to_take(cap_dir, frame):
    """The take's frame for edit frame `frame`."""
    delta = 0
    for start, d in segments(cap_dir):
        if frame >= start:
            delta = d
    return frame + delta


def to_edit(cap_dir, frame):
    """The edit frame for the take's frame `frame` (inverse of to_take)."""
    delta = 0
    for start, d in segments(cap_dir):
        if frame >= start + d:
            delta = d
    return frame - delta
